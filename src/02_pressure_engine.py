import os
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

def run_pressure_engine():
    print("=== Step 2: Starting Pressure Engine & Leverage Modeling ===")
    os.environ['LOKY_MAX_CPU_COUNT'] = '4'
    
    # 1. Load delivery preball data
    df = pd.read_parquet('data_processed/fact_delivery_preball.parquet')
    matches = pd.read_csv('Data Pack/matches.csv')

    # Merge win_team_id
    df = df.merge(matches[['match_id', 'win_team_id']], on='match_id', how='left')
    df['batting_team_won'] = (df['batting_team_id'] == df['win_team_id']).astype(int)

    # 2. Train Win Probability Model strictly on historical training data (year <= 2024)
    # to maintain strict chronological separation and prevent data leakage
    inn2_mask = df['innings'] == 2
    train_mask = inn2_mask & (df['year'] <= 2024)

    wp_features = ['legal_balls_remaining', 'runs_required', 'wickets_in_hand', 'venue_par_score']
    X_train = df.loc[train_mask, wp_features].fillna(0)
    y_train = df.loc[train_mask, 'batting_team_won']

    wp_model = LogisticRegression(max_iter=1000, random_state=42)
    wp_model.fit(X_train, y_train)
    print("Trained Logistic Win Probability model on 2022-2024 training split.")
    print("Coefficients:", dict(zip(wp_features, wp_model.coef_[0].round(4))))

    # 3. Compute Win Probability and Leverage for Innings 2 deliveries
    print("Evaluating pre-ball win probability and leverage swings...")
    
    # Pre-ball state
    X_inn2 = df.loc[inn2_mask, wp_features].fillna(0)
    wp_current = wp_model.predict_proba(X_inn2)[:, 1]

    # Counterfactual state 1: Boundary (+4 runs, -1 ball)
    X_boundary = X_inn2.copy()
    X_boundary['legal_balls_remaining'] = np.maximum(0, X_boundary['legal_balls_remaining'] - 1)
    X_boundary['runs_required'] = np.maximum(0, X_boundary['runs_required'] - 4)
    wp_boundary = wp_model.predict_proba(X_boundary)[:, 1]

    # Counterfactual state 2: Wicket (0 runs, -1 wicket, -1 ball)
    X_wkt = X_inn2.copy()
    X_wkt['legal_balls_remaining'] = np.maximum(0, X_wkt['legal_balls_remaining'] - 1)
    X_wkt['wickets_in_hand'] = np.maximum(0, X_wkt['wickets_in_hand'] - 1)
    wp_wkt = wp_model.predict_proba(X_wkt)[:, 1]

    # Leverage Index = Potential outcome swing normalized
    swing = np.abs(wp_boundary - wp_wkt)
    # Normalize swing: 0.20 swing represents very high leverage
    leverage_inn2 = np.clip(swing / 0.20, 0.0, 1.0)

    # 4. Demand Index for Innings 2 (Chase Demand & Resource Scarcity)
    rrr = df.loc[inn2_mask, 'required_run_rate'].clip(0, 36)
    wickets_down = 10 - df.loc[inn2_mask, 'wickets_in_hand']
    shocks = df.loc[inn2_mask, 'recent_wickets_last12'].clip(0, 4)
    is_death = (df.loc[inn2_mask, 'phase'] == 'Death').astype(float)

    # Required rate difficulty above standard 7.5 rpo baseline
    rate_demand = np.clip((rrr - 6.5) / 7.5, 0.0, 1.0)
    resource_scarcity = wickets_down / 9.0
    shock_scarcity = np.clip(shocks / 2.0, 0.0, 1.0)

    demand_inn2 = np.clip(
        0.40 * rate_demand +
        0.35 * resource_scarcity +
        0.15 * shock_scarcity +
        0.10 * is_death,
        0.0, 1.0
    )

    # Composite MPI for Innings 2
    mpi_inn2 = 0.50 * demand_inn2 + 0.50 * leverage_inn2

    # 5. Demand & Leverage for Innings 1 (Trajectory Expectations, Par Deficit, and Acceleration)
    inn1_mask = df['innings'] == 1
    
    # Expected par progress curve at delivery t without look-ahead
    # Fraction of 20 overs bowled: b / 120
    b_used = df.loc[inn1_mask, 'pre_legal_balls'].clip(0, 120)
    b_frac = b_used / 120.0
    par = df.loc[inn1_mask, 'venue_par_score']
    # Par expected runs at this ball
    expected_par_at_t = par * (1.0 - np.power(1.0 - b_frac, 1.25))
    par_deficit = expected_par_at_t - df.loc[inn1_mask, 'pre_runs']
    par_demand = np.clip(par_deficit / 25.0, 0.0, 1.0)

    w_down_inn1 = 10 - df.loc[inn1_mask, 'wickets_in_hand']
    shocks_inn1 = df.loc[inn1_mask, 'recent_wickets_last12'].clip(0, 4)
    death_inn1 = (df.loc[inn1_mask, 'phase'] == 'Death').astype(float)

    demand_inn1 = np.clip(
        0.35 * par_demand +
        0.35 * (w_down_inn1 / 9.0) +
        0.15 * np.clip(shocks_inn1 / 2.0, 0.0, 1.0) +
        0.15 * death_inn1,
        0.0, 1.0
    )

    # Leverage in Innings 1: Higher in death overs and when wickets are scarce
    leverage_inn1 = np.clip(
        0.40 * death_inn1 +
        0.40 * (w_down_inn1 / 9.0) +
        0.20 * np.clip(par_demand, 0.0, 1.0),
        0.0, 1.0
    )

    mpi_inn1 = 0.55 * demand_inn1 + 0.45 * leverage_inn1

    # 6. Assign back to main dataframe
    df['demand_index'] = 0.0
    df['leverage_index'] = 0.0
    df['match_pressure_index'] = 0.0
    df['win_probability'] = np.nan

    df.loc[inn2_mask, 'win_probability'] = wp_current
    df.loc[inn2_mask, 'demand_index'] = demand_inn2
    df.loc[inn2_mask, 'leverage_index'] = leverage_inn2
    df.loc[inn2_mask, 'match_pressure_index'] = mpi_inn2

    df.loc[inn1_mask, 'demand_index'] = demand_inn1
    df.loc[inn1_mask, 'leverage_index'] = leverage_inn1
    df.loc[inn1_mask, 'match_pressure_index'] = mpi_inn1

    # Super Overs (innings 3 & 4): Maximum pressure
    super_over_mask = df['innings'] >= 3
    df.loc[super_over_mask, 'demand_index'] = 1.0
    df.loc[super_over_mask, 'leverage_index'] = 1.0
    df.loc[super_over_mask, 'match_pressure_index'] = 1.0

    # Knockout Multiplier (Amplifies stakes in playoff/knockout matches)
    ko_mask = df['knock_out'] == 1
    df.loc[ko_mask, 'match_pressure_index'] = np.clip(df.loc[ko_mask, 'match_pressure_index'] * 1.15, 0.0, 1.0)

    # 7. Threshold Calibration on Training Set (2022-2024)
    train_deliveries = df[df['year'] <= 2024]
    p50 = float(train_deliveries['match_pressure_index'].quantile(0.50))
    p70 = float(train_deliveries['match_pressure_index'].quantile(0.70))
    p75 = float(train_deliveries['match_pressure_index'].quantile(0.75))
    p80 = float(train_deliveries['match_pressure_index'].quantile(0.80))
    
    # Frozen high-pressure threshold: 70th percentile (~top 30% most pressured balls)
    frozen_threshold = round(p70, 3)
    df['is_high_pressure'] = df['match_pressure_index'] >= frozen_threshold

    pressure_config = {
        'training_cutoff_year': 2024,
        'model_type': 'Logistic_Calibrated_Swing_Plus_Demand',
        'distribution_quantiles': {
            'p50_median': round(p50, 4),
            'p70': round(p70, 4),
            'p75': round(p75, 4),
            'p80': round(p80, 4)
        },
        'frozen_high_pressure_threshold': frozen_threshold,
        'total_deliveries': len(df),
        'high_pressure_deliveries_count': int(df['is_high_pressure'].sum()),
        'high_pressure_share_pct': round(float(df['is_high_pressure'].mean()) * 100, 2),
        'share_by_phase': df.groupby('phase')['is_high_pressure'].mean().round(4).to_dict(),
        'share_by_innings': df.groupby('innings')['is_high_pressure'].mean().round(4).to_dict(),
        'share_by_comp': df.groupby('comp_category')['is_high_pressure'].mean().round(4).to_dict()
    }

    with open('outputs/pressure_config.json', 'w') as f:
        json.dump(pressure_config, f, indent=2)
    print("Saved outputs/pressure_config.json:")
    print(json.dumps(pressure_config, indent=2))

    # 8. Save updated fact table
    df.to_parquet('data_processed/fact_delivery_pressure.parquet', index=False)
    print(f"Saved fact_delivery_pressure.parquet: {len(df)} rows.")

if __name__ == '__main__':
    run_pressure_engine()
