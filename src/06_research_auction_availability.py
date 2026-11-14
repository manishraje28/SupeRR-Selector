import pandas as pd
import json

mapping = pd.read_csv('Data Pack/competition_team_player_mapping.csv')
p11 = pd.read_csv('Data Pack/playing_eleven.csv')
matches = pd.read_csv('Data Pack/matches.csv')
teams = pd.read_csv('Data Pack/teams.csv')
bat = pd.read_csv('outputs/batting_rankings.csv')
bowl = pd.read_csv('outputs/bowling_rankings.csv')

top_bat_pids = set(bat.head(25).player_id)
top_bowl_pids = set(bowl.head(25).player_id)
top_pids = top_bat_pids.union(top_bowl_pids)

ipl_comps = mapping[mapping.comp_name.str.startswith('IPL')].comp_name.unique()
ipl_mapping = mapping[mapping.comp_name.str.startswith('IPL') & mapping.player_id.isin(top_pids)]
player_ipl_teams = ipl_mapping.groupby(['player_id', 'player_name'])['team_name'].unique().to_dict()

# Print detailed summary
print("=== TOP BATTERS IPL TEAM HISTORY ===")
for _, r in bat.head(15).iterrows():
    pid = r['player_id']
    t_names = player_ipl_teams.get((pid, r['player_name']), ['No IPL Appearance / International Only'])
    print(f"Rank {int(r['rank'])}: {r['player_name']} (ID {pid}) -> Teams: {list(t_names)}")

print("\n=== TOP BOWLERS IPL TEAM HISTORY ===")
for _, r in bowl.head(15).iterrows():
    pid = r['player_id']
    t_names = player_ipl_teams.get((pid, r['player_name']), ['No IPL Appearance / International Only'])
    print(f"Rank {int(r['rank'])}: {r['player_name']} (ID {pid}) -> Teams: {list(t_names)}")
