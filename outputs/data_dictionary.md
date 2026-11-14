# SupeRR Selector Season 2 — Round 1: Data Dictionary

## 1. Primary Dimension & Entity Tables

### `dim_player`
- `player_id` (INTEGER, Primary Key): Unique identifier assigned across all competitions.
- `player_name` (STRING): Canonical full name of the player.
- `batting_type` (STRING): Striker batting hand (`RHB` for Right-Hand Bat, `LHB` for Left-Hand Bat).
- `bowling_type` (STRING): Primary bowling style (e.g., `Right-arm Fast`, `Slow left-arm orthodox`, `Right-arm Leg-Break`, `Left-arm Chinaman`).

### `dim_competition`
- `comp_id` (INTEGER, Primary Key): Unique identifier of the tournament or series.
- `comp_name` (STRING): Full tournament name (e.g., `IPL 2024`, `ICC Men's T20 World Cup 2024`).
- `match_format` (STRING): `T20` or `T20I`.
- `season` (INTEGER): Season year (2022 to 2026).
- `is_ipl` (BOOLEAN): Flag indicating Indian Premier League fixtures.
- `comp_category` (STRING): `IPL`, `T20I`, or `Other_T20`.

### `dim_venue`
- `venue_id` (INTEGER, Primary Key): Unique stadium code.
- `venue_country` (STRING): Host country.
- `venue_par_score` (FLOAT): Empirical average first-innings score at this venue across all matches.

---

## 2. Match Fact Table (`fact_match`)
- `match_id` (INTEGER, Primary Key): Unique match ID.
- `match_date` (DATE): Match date (YYYY-MM-DD). Range: 2022-01-22 to 2026-11-01.
- `home_team_id` / `away_team_id` (INTEGER): Team identifiers.
- `knock_out` (BOOLEAN): 1 for playoffs, qualifiers, eliminators, and finals; 0 for group stage.
- `revised_target` (FLOAT): DLS revised target where applicable (null for standard matches).
- `first_inn_revised_overs` / `second_inn_revised_overs` (FLOAT): Revised innings lengths measured in **legal balls** (e.g., 90.0 balls = 15.0 overs).
- `win_team_id` (INTEGER): Match winner.

---

## 3. Delivery Pre-Ball State (`fact_delivery_preball` / `fact_delivery_cava`)
- `match_id` (INTEGER): Match reference.
- `innings` (INTEGER): 1 (First Innings), 2 (Second Innings Chase), 3 & 4 (Super Overs).
- `overid` (INTEGER): 1-indexed over number (1 to 20).
- `over_ball_num` (INTEGER): Ball sequence number within the over (1 to n).
- `innings_ball_num` (INTEGER): Ball sequence number within the innings.
- `striker_id` / `bowler_id` (INTEGER): Active batter facing and bowler delivering.
- `runs` (INTEGER): Runs scored strictly off the bat (0, 1, 2, 3, 4, 5, 6).
- `extras_type` (STRING): `wide`, `Overstep` (front-foot no-ball), `other` (height/beamer no-ball), `byes`, `legbyes`, `Penalty`, or null.
- `extras1_runs` / `extras_2_runs` (INTEGER): Primary and secondary extra runs.
- `is_legal_ball` (BOOLEAN): True if not a wide or no-ball (`Overstep`/`other`).
- `is_wicket` (BOOLEAN): True if a wicket fell on the delivery.
- `is_bowler_wicket` (BOOLEAN): True for `Caught`, `Bowled`, `LBW`, `Stump`, and `Hit Wicket`. False for `RunOut`, `Retire Out`, and `Obstructing the field`.
- `pre_runs` (INTEGER): Cumulative team runs scored immediately prior to this delivery.
- `pre_wickets` (INTEGER): Cumulative wickets fallen immediately prior to this delivery.
- `pre_legal_balls` (INTEGER): Cumulative legal deliveries bowled immediately prior to this delivery.
- `legal_balls_remaining` (INTEGER): Remaining legal deliveries available in the innings.
- `wickets_in_hand` (INTEGER): $10 - \text{pre\_wickets}$.
- `target` (FLOAT): Runs required to win + 1 (Innings 2 only).
- `runs_required` (FLOAT): $\max(0, \text{target} - \text{pre\_runs})$.
- `required_run_rate` (FLOAT): $(\text{runs\_required} / (\text{legal\_balls\_remaining} / 6))$.
- `current_run_rate` (FLOAT): $(\text{pre\_runs} / (\text{pre\_legal\_balls} / 6))$.
- `recent_wickets_last12` (INTEGER): Wickets fallen in the prior 12 deliveries (shock collapse indicator).
- `phase` (STRING): `Powerplay` (overs 1-6), `Middle` (overs 7-15), `Death` (overs 16-20).

---

## 4. Pressure & Leverage Metrics
- `demand_index` (FLOAT, [0, 1]): Contextual difficulty combining chase rate deficit, resource depletion, recent collapse shocks, and phase.
- `leverage_index` (FLOAT, [0, 1]): Expected swing in win probability between a boundary (+4) and a wicket on the upcoming delivery:
  $$LI_t = \frac{|WP(\text{boundary}) - WP(\text{wicket})|}{0.20}$$
- `match_pressure_index` (FLOAT, [0, 1]): Composite pre-delivery pressure metric:
  $$MPI_t = 0.50 \cdot \text{demand\_index} + 0.50 \cdot \text{leverage\_index} \quad (\times 1.15 \text{ if knockout})$$
- `is_high_pressure` (BOOLEAN): Delivery classified as high pressure if $MPI_t \ge 0.55$ (frozen 70th percentile of training data).

---

## 5. Performance & Ranking Metrics
- `exp_bat_runs` / `exp_bowl_runs` (FLOAT): Expected runs based on pre-ball matchup context and match state.
- `exp_bat_wkt_prob` / `exp_bowl_wkt_prob` (FLOAT): Calibrated probability of dismissal/wicket.
- `wicket_value` (FLOAT): State-dependent run value of preserving a wicket (4.0 to 6.2 runs).
- `cava_bat` (FLOAT): Context-Adjusted Value Added per ball for the batter:
  $$\text{CAVA}_{\text{bat}} = (\text{runs} - \mathbb{E}[\text{runs}]) - V_w \cdot (\mathbb{I}_{\text{out}} - \mathbb{E}[\text{wicket}])$$
- `cava_bowl` (FLOAT): Context-Adjusted Value Added per ball for the bowler:
  $$\text{CAVA}_{\text{bowl}} = (\mathbb{E}[\text{bowler\_runs}] - \text{runs\_conceded}) + V_w \cdot (\mathbb{I}_{\text{bowler\_wkt}} - \mathbb{E}[\text{bowler\_wkt}])$$
- `hp_cava_per_ball` (FLOAT): Average CAVA per ball in high-pressure deliveries.
- `uplift_cava` (FLOAT): Elevation under pressure ($\text{hp\_cava\_per\_ball} - \text{base\_cava\_per\_ball}$).
- `shrunk_cava_per_ball` (FLOAT): Empirical Bayes partial pooling posterior mean.
- `shrunk_se` (FLOAT): Match-clustered posterior standard error.
- `pressure_rank_score` (FLOAT): Primary ranking score using the conservative 20th percentile posterior:
  $$\text{Rank Score} = \hat{\theta}_{\text{shrunk}} - 0.84 \cdot \text{SE}_{\text{shrunk}}$$
