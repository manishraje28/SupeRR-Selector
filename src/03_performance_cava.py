import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, log_loss, roc_auc_score, brier_score_loss

def run_performance_engine():
    print("=== Step 3: Starting CAVA Performance Engine & Context Modeling ===")
    os.environ['LOKY_MAX_CPU_COUNT'] = '4'
    
    # 1. Load data
    df = pd.read_parquet('data_processed/fact_delivery_pressure.parquet')
    
    # Feature engineering for context models
    features = [
        'innings', 'overid', 'legal_balls_remaining',
        'pre_runs', 'pre_wickets', 'wickets_in_hand',
        'batting_order', 'bowl_speed', 'venue_par_score',
        'knock_out'
    ]
    
    # Categorical encodings
    cat_cols = ['phase', 'batting_type', 'bowling_type', 'pace_or_spin', 'comp_category']
    for c in cat_cols:
        df[c + '_code'] = df[c].astype('category').cat.codes
        features.append(c + '_code')

    # Fill missing speeds with median
    median_speed = df['bowl_speed'].median()
    df['bowl_speed'] = df['bowl_speed'].fillna(median_speed)

    train_mask = df['year'] <= 2024
    test_mask = df['year'] > 2024

    X_train = df.loc[train_mask, features]
    X_test = df.loc[test_mask, features]
    X_all = df[features]

    # 2. Train Batter Expected Runs Regressor
    print("Training Batter Expected Runs Regressor on 2022-2024 data...")
    y_bat_runs_train = df.loc[train_mask, 'runs']
    bat_runs_model = HistGradientBoostingRegressor(max_iter=100, min_samples_leaf=30, random_state=42)
    bat_runs_model.fit(X_train, y_bat_runs_train)

    # 3. Train Bowler Expected Conceded Runs Regressor
    print("Training Bowler Expected Conceded Runs Regressor on 2022-2024 data...")
    y_bowl_runs_train = df.loc[train_mask, 'bowler_conceded_runs']
    bowl_runs_model = HistGradientBoostingRegressor(max_iter=100, min_samples_leaf=30, random_state=42)
    bowl_runs_model.fit(X_train, y_bowl_runs_train)

    # 4. Train Expected Wicket Classifier (Batter Dismissal Risk)
    print("Training Batter Expected Wicket Classifier...")
    y_bat_wkt_train = df.loc[train_mask, 'is_wicket'].astype(int)
    bat_wkt_model = HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=30, random_state=42)
    bat_wkt_model.fit(X_train, y_bat_wkt_train)

    # 5. Train Bowler Expected Wicket Classifier (Bowler-Credited Wicket Probability)
    print("Training Bowler Expected Wicket Classifier...")
    y_bowl_wkt_train = df.loc[train_mask, 'is_bowler_wicket'].astype(int)
    bowl_wkt_model = HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=30, random_state=42)
    bowl_wkt_model.fit(X_train, y_bowl_wkt_train)

    # 6. Evaluate out-of-time on 2025-2026 test matches
    print("Evaluating out-of-time validation metrics on 2025-2026 data...")
    y_bat_runs_test = df.loc[test_mask, 'runs']
    bat_runs_pred_test = bat_runs_model.predict(X_test)
    rmse_runs = float(np.sqrt(mean_squared_error(y_bat_runs_test, bat_runs_pred_test)))
    mae_runs = float(mean_absolute_error(y_bat_runs_test, bat_runs_pred_test))

    y_bat_wkt_test = df.loc[test_mask, 'is_wicket'].astype(int)
    bat_wkt_prob_test = bat_wkt_model.predict_proba(X_test)[:, 1]
    brier_wkt = float(brier_score_loss(y_bat_wkt_test, bat_wkt_prob_test))
    logloss_wkt = float(log_loss(y_bat_wkt_test, bat_wkt_prob_test))
    auc_wkt = float(roc_auc_score(y_bat_wkt_test, bat_wkt_prob_test))

    y_bowl_wkt_test = df.loc[test_mask, 'is_bowler_wicket'].astype(int)
    bowl_wkt_prob_test = bowl_wkt_model.predict_proba(X_test)[:, 1]
    auc_bowl_wkt = float(roc_auc_score(y_bowl_wkt_test, bowl_wkt_prob_test))

    validation_metrics = {
        'evaluation_strategy': 'Chronological_Rolling_Origin (Train: 2022-2024, Test: 2025-2026)',
        'train_matches': int(df.loc[train_mask, 'match_id'].nunique()),
        'test_matches': int(df.loc[test_mask, 'match_id'].nunique()),
        'train_deliveries': int(train_mask.sum()),
        'test_deliveries': int(test_mask.sum()),
        'expected_runs_metrics': {
            'rmse': round(rmse_runs, 4),
            'mae': round(mae_runs, 4)
        },
        'expected_wicket_metrics': {
            'auc_batter_out': round(auc_wkt, 4),
            'auc_bowler_wkt': round(auc_bowl_wkt, 4),
            'brier_score': round(brier_wkt, 4),
            'log_loss': round(logloss_wkt, 4)
        }
    }
    with open('outputs/validation_metrics.json', 'w') as f:
        json.dump(validation_metrics, f, indent=2)
    print("Saved outputs/validation_metrics.json:")
    print(json.dumps(validation_metrics, indent=2))

    # 7. Predict context expectations for all deliveries
    print("Generating context expectations across all deliveries...")
    df['exp_bat_runs'] = bat_runs_model.predict(X_all)
    df['exp_bowl_runs'] = bowl_runs_model.predict(X_all)
    df['exp_bat_wkt_prob'] = bat_wkt_model.predict_proba(X_all)[:, 1]
    df['exp_bowl_wkt_prob'] = bowl_wkt_model.predict_proba(X_all)[:, 1]

    # 8. State-Dependent Wicket Value (V_w)
    # Estimate resource-dependent run value of a wicket:
    # Top/middle phase (overs 1-15): ~5.5 to 6.5 runs; Death phase (overs 16-20): ~3.5 to 4.5 runs
    phase_wicket_value = {'Powerplay': 6.2, 'Middle': 5.4, 'Death': 4.0}
    df['wicket_value'] = df['phase'].map(phase_wicket_value).fillna(5.0)

    # 9. Compute CAVA (Context-Adjusted Value Added)
    # Batter CAVA: Runs above expectation minus wicket penalty above risk
    df['cava_bat'] = (df['runs'] - df['exp_bat_runs']) - df['wicket_value'] * (df['is_wicket'].astype(float) - df['exp_bat_wkt_prob'])
    
    # Bowler CAVA: Runs saved below expectation plus wicket reward above expected rate
    df['cava_bowl'] = (df['exp_bowl_runs'] - df['bowler_conceded_runs']) + df['wicket_value'] * (df['is_bowler_wicket'].astype(float) - df['exp_bowl_wkt_prob'])

    # Save to fact table
    df.to_parquet('data_processed/fact_delivery_cava.parquet', index=False)
    print(f"Saved fact_delivery_cava.parquet: {len(df)} rows.")

if __name__ == '__main__':
    run_performance_engine()
