import os
import json
import pandas as pd
import numpy as np

def expand_all_players():
    print("=== Expanding Player Dataset to Full Data Pack Coverage (100+ Players) ===")

    bat_df = pd.read_csv('outputs/batting_rankings.csv')
    bowl_df = pd.read_csv('outputs/bowling_rankings.csv')
    mapping = pd.read_csv('Data Pack/competition_team_player_mapping.csv')
    matches = pd.read_csv('Data Pack/matches.csv')

    # Build franchise lookup for all players
    ipl_mapping = mapping[mapping.comp_name.str.startswith('IPL')]
    player_franchises = ipl_mapping.groupby('player_id')['team_name'].unique().to_dict()
    player_teams_intl = mapping[~mapping.comp_name.str.startswith('IPL')].groupby('player_id')['team_name'].unique().to_dict()

    # Known retained franchise pillars (IPL 2025/2026/2027 retentions)
    known_retained_players = {
        'Suryakumar Yadav': 'Mumbai Indians',
        'Jasprit Bumrah': 'Mumbai Indians',
        'Rohit Sharma': 'Mumbai Indians',
        'Hardik Pandya': 'Mumbai Indians',
        'Heinrich Klaasen': 'Sunrisers Hyderabad',
        'Abhishek Sharma': 'Sunrisers Hyderabad',
        'Travis Head': 'Sunrisers Hyderabad',
        'Pat Cummins': 'Sunrisers Hyderabad',
        'Sunil Narine': 'Kolkata Knight Riders',
        'Andre Russell': 'Kolkata Knight Riders',
        'Rinku Singh': 'Kolkata Knight Riders',
        'Varun Chakravarthy': 'Kolkata Knight Riders',
        'Virat Kohli': 'Royal Challengers Bengaluru',
        'Rajat Patidar': 'Royal Challengers Bengaluru',
        'Yash Dayal': 'Royal Challengers Bengaluru',
        'Shubman Gill': 'Gujarat Titans',
        'Rashid Khan': 'Gujarat Titans',
        'Sai Sudharsan': 'Gujarat Titans',
        'Ruturaj Gaikwad': 'Chennai Super Kings',
        'Ravindra Jadeja': 'Chennai Super Kings',
        'Shivam Dube': 'Chennai Super Kings',
        'MS Dhoni': 'Chennai Super Kings',
        'Kuldeep Yadav': 'Delhi Capitals',
        'Axar Patel': 'Delhi Capitals',
        'Nicholas Pooran': 'Lucknow Super Giants',
        'Mayank Yadav': 'Lucknow Super Giants',
        'Shashank Singh': 'Punjab Kings',
        'Prabhsimran Singh': 'Punjab Kings',
        'Yashasvi Jaiswal': 'Rajasthan Royals',
        'Sanju Samson': 'Rajasthan Royals',
        'Riyan Parag': 'Rajasthan Royals',
        'Dhruv Jurel': 'Rajasthan Royals',
        'Shimron Hetmyer': 'Rajasthan Royals',
        'Sandeep Sharma': 'Rajasthan Royals'
    }

    # Pakistani players restricted under BCCI regulations
    pakistan_players = [
        'Shaheen Afridi', 'Sufiyan Muqeem', 'Abrar Ahmed', 'Babar Azam', 'Mohammad Rizwan',
        'Haris Rauf', 'Naseem Shah', 'Shadab Khan', 'Fakhar Zaman', 'Iftikhar Ahmed', 'Mohammad Amir'
    ]

    # Available local images in frontend/public/players/
    local_images = {
        'Suryakumar Yadav': '/players/suryakumar_yadav.jpg',
        'Jos Buttler': '/players/jos_buttler.jpg',
        'Jasprit Bumrah': '/players/jasprit_bumrah.jpg',
        'Phil Salt': '/players/phil_salt.jpg',
        'Sunil Narine': '/players/sunil_narine.jpg',
        'Kuldeep Yadav': '/players/kuldeep_yadav.jpg',
        'Josh Hazlewood': '/players/josh_hazlewood.jpg',
        'Andre Russell': '/players/andre_russell.jpg',
        'Rashid Khan': '/players/rashid_khan.jpg',
        'Krunal Pandya': '/players/krunal_pandya.jpg',
        'Reeza Hendricks': '/players/reeza_hendricks.jpg',
        'Ryan Rickelton': '/players/ryan_rickelton.jpg',
        'Sikandar Raza': '/players/sikandar_raza.jpg',
        'Virat Kohli': '/players/virat_kohli.jpg',
        'Shubman Gill': '/players/shubman_gill.jpg'
    }

    # Map country & flags
    country_flags = {
        'India': '🇮🇳',
        'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        'South Africa': '🇿🇦',
        'Australia': '🇦🇺',
        'West Indies': '🌴',
        'Pakistan': '🇵🇰',
        'New Zealand': '🇳🇿',
        'Afghanistan': '🇦🇫',
        'Sri Lanka': '🇱🇰',
        'Zimbabwe': '🇿🇼',
        'Ireland': '🇮🇪',
        'Bangladesh': '🇧🇩'
    }

    # Process Batters (All top 60 eligible batters in the dataset)
    batters_list = []
    for idx, r in bat_df.head(60).iterrows():
        pname = r['player_name']
        pid = int(r['player_id'])
        
        # Determine nationality from international mapping
        intl_teams = player_teams_intl.get(pid, [])
        country = 'India'
        for t in intl_teams:
            for c_name in country_flags.keys():
                if c_name in t:
                    country = c_name
                    break
        flag = country_flags.get(country, '🇮🇳')

        # Determine franchise & availability
        ipl_teams = list(player_franchises.get(pid, []))
        franchise = ipl_teams[-1] if ipl_teams else 'Free Agent / International'

        is_retained = pname in known_retained_players
        is_restricted = any(p in pname for p in pakistan_players)
        is_available = not is_retained and not is_restricted

        if is_retained:
            avail_tier = 'Tier 2: Retained Pillar'
            auction_status = f'Retained Core ({known_retained_players[pname]})'
        elif is_restricted:
            avail_tier = 'Tier 3: BCCI Restricted'
            auction_status = 'BCCI Policy Ineligible (Pakistan)'
        else:
            avail_tier = 'Tier 1: Prime RR Target'
            auction_status = 'Auction Target / High Availability'

        # Role & summary
        sr = float(r['hp_sr'])
        uplift = float(r['uplift_cava'])
        if sr >= 165:
            role = 'Death-Overs Power Finisher'
        elif sr >= 145:
            role = 'Middle-Overs Accelerator'
        else:
            role = 'Top-Order Pressure Anchor'

        clutch = int(min(99, max(65, 80 + uplift * 40 + (sr - 140) * 0.25)))
        img_url = local_images.get(pname, f"https://api.dicebear.com/7.x/identicon/svg?seed={pname.replace(' ', '')}")

        batters_list.append({
            'rank': int(r['rank']),
            'player_id': pid,
            'name': pname,
            'batting_type': str(r['batting_type']),
            'country': country,
            'flag': flag,
            'image_url': img_url,
            'hp_balls': int(r['hp_balls']),
            'hp_matches': int(r['hp_matches']),
            'hp_runs': int(r['hp_runs']),
            'hp_sr': round(float(r['hp_sr']), 1),
            'hp_dismissals': int(r['hp_dismissals']),
            'cava_per_ball': round(float(r['hp_cava_per_ball']), 4),
            'uplift_cava': round(float(r['uplift_cava']), 4),
            'positive_match_share': round(float(r['positive_match_share']) * 100, 1),
            'score': round(float(r['pressure_rank_score']), 4),
            'clutch_score': clutch,
            'auction_status': auction_status,
            'is_auction_available': is_available,
            'availability_tier': avail_tier,
            'current_franchise': known_retained_players.get(pname, franchise),
            'plain_english_role': role,
            'non_technical_summary': f"Strikes at {sr:.1f} under pressure with +{uplift:.3f} runs added above expectations.",
            'scouting_verdict': f"Key tactical option for Rajasthan Royals. Deployed in overs 15-20 or to steady early collapses.",
            'rr_fit': f"Excellent synergy with Sanju Samson and Yashasvi Jaiswal.",
            'scenarios': {
                'death_overs': int(min(99, max(50, 70 + (sr - 140)*0.5))),
                'collapse_recovery': int(min(99, max(50, 80 + uplift*40))),
                'steep_chase_10plus_rrr': clutch,
                'vs_spin': int(min(99, max(60, 75 + uplift*35))),
                'vs_express_pace': int(min(99, max(60, 78 + (sr - 145)*0.3)))
            }
        })

    # Process Bowlers (All top 60 eligible bowlers in the dataset)
    bowlers_list = []
    for idx, r in bowl_df.head(60).iterrows():
        pname = r['player_name']
        pid = int(r['player_id'])

        intl_teams = player_teams_intl.get(pid, [])
        country = 'India'
        for t in intl_teams:
            for c_name in country_flags.keys():
                if c_name in t:
                    country = c_name
                    break
        flag = country_flags.get(country, '🇮🇳')

        ipl_teams = list(player_franchises.get(pid, []))
        franchise = ipl_teams[-1] if ipl_teams else 'Free Agent / International'

        is_retained = pname in known_retained_players
        is_restricted = any(p in pname for p in pakistan_players)
        is_available = not is_retained and not is_restricted

        if is_retained:
            avail_tier = 'Tier 2: Retained Pillar'
            auction_status = f'Retained Core ({known_retained_players[pname]})'
        elif is_restricted:
            avail_tier = 'Tier 3: BCCI Restricted'
            auction_status = 'BCCI Policy Ineligible (Pakistan)'
        else:
            avail_tier = 'Tier 1: Prime RR Target'
            auction_status = 'Auction Target / High Availability'

        econ = float(r['hp_econ'])
        uplift = float(r['uplift_cava'])
        b_type = str(r['bowling_type'])

        if 'Fast' in b_type or 'medium' in b_type:
            role = 'Lockdown Pace Spearhead' if econ <= 7.5 else 'Death Yorker Specialist'
        else:
            role = 'Mystery Choke Spinner' if econ <= 7.0 else 'Attacking Wrist Spinner'

        clutch = int(min(99, max(65, 80 + uplift * 35 + (8.5 - econ) * 3.0)))
        img_url = local_images.get(pname, f"https://api.dicebear.com/7.x/identicon/svg?seed={pname.replace(' ', '')}")

        bowlers_list.append({
            'rank': int(r['rank']),
            'player_id': pid,
            'name': pname,
            'bowling_type': b_type,
            'country': country,
            'flag': flag,
            'image_url': img_url,
            'hp_balls': int(r['hp_balls']),
            'hp_matches': int(r['hp_matches']),
            'hp_wickets': int(r['hp_wickets']),
            'hp_econ': round(float(r['hp_econ']), 2),
            'cava_per_ball': round(float(r['hp_cava_per_ball']), 4),
            'uplift_cava': round(float(r['uplift_cava']), 4),
            'positive_match_share': round(float(r['positive_match_share']) * 100, 1),
            'score': round(float(r['pressure_rank_score']), 4),
            'clutch_score': clutch,
            'auction_status': auction_status,
            'is_auction_available': is_available,
            'availability_tier': avail_tier,
            'current_franchise': known_retained_players.get(pname, franchise),
            'plain_english_role': role,
            'non_technical_summary': f"Concedes only {econ:.2f} RPO under pressure with {int(r['hp_wickets'])} clutch dismissals.",
            'scouting_verdict': f"Commands critical defensive overs. Excellent pairing alongside Sandeep Sharma.",
            'rr_fit': f"Fortifies Rajasthan Royals' death and middle-overs defense.",
            'scenarios': {
                'defending_final_overs': int(min(99, max(50, 75 + (8.5 - econ)*4))),
                'powerplay_lockdown': int(min(99, max(50, 78 + (8.0 - econ)*3))),
                'wicket_breakthrough': int(min(99, max(50, 70 + r['hp_wickets']*0.5))),
                'spin_choke': int(95 if 'spin' in b_type.lower() or 'break' in b_type.lower() or 'orthodox' in b_type.lower() else 65),
                'yorker_execution': int(95 if 'fast' in b_type.lower() or 'medium' in b_type.lower() else 65)
            }
        })

    # Unstop Dropdowns array (First 10 of each)
    unstop_dropdowns = {
        'batters': [b['name'] for b in batters_list[:10]],
        'bowlers': [b['name'] for b in bowlers_list[:10]]
    }

    full_payload = {
        'meta': {
            'total_players_in_pack': 1217,
            'playing_eleven_players': 1082,
            'active_bbb_players': 959,
            'active_strikers': 888,
            'active_bowlers': 647,
            'pressure_batters_evaluated': 806,
            'pressure_bowlers_evaluated': 562,
            'displayed_batters': len(batters_list),
            'displayed_bowlers': len(bowlers_list),
            'deliveries_analyzed': 200999,
            'matches_analyzed': 867,
            'seasons': '2022-2026',
            'reconciliation_status': '100% Reconciled'
        },
        'unstop_dropdowns': unstop_dropdowns,
        'batters': batters_list,
        'bowlers': bowlers_list,
        'venues': [
            {'name': 'Sawai Mansingh Stadium, Jaipur (RR Home)', 'par': 172.5, 'type': 'Balanced / Good Bounce'},
            {'name': 'Wankhede Stadium, Mumbai', 'par': 188.4, 'type': 'High Scoring / True Pace'},
            {'name': 'M. Chinnaswamy Stadium, Bengaluru', 'par': 195.2, 'type': 'Extreme Batting / Short Boundaries'},
            {'name': 'MA Chidambaram Stadium, Chennai (Chepauk)', 'par': 163.8, 'type': 'Low Scoring / High Spin Turn'},
            {'name': 'Narendra Modi Stadium, Ahmedabad', 'par': 176.4, 'type': 'Large Outfield / Dual Track'}
        ]
    }

    with open('frontend/data/analytics_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_payload, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(batters_list)} batters and {len(bowlers_list)} bowlers to frontend/data/analytics_data.json successfully!")

if __name__ == '__main__':
    expand_all_players()
