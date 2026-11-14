import os
import json
import pandas as pd
import numpy as np

def enrich_rr_auction_system():
    print("=== Enriching Full Rajasthan Royals Auction Intelligence System ===")

    bat_df = pd.read_csv('outputs/batting_rankings.csv')
    bowl_df = pd.read_csv('outputs/bowling_rankings.csv')
    mapping = pd.read_csv('Data Pack/competition_team_player_mapping.csv')

    # BCCI Official TATA IPL Retentions (Confirmed Pillars)
    retained_pillars = {
        'Suryakumar Yadav': 'Mumbai Indians',
        'Jasprit Bumrah': 'Mumbai Indians',
        'Rohit Sharma': 'Mumbai Indians',
        'Hardik Pandya': 'Mumbai Indians',
        'Tilak Varma': 'Mumbai Indians',
        'Namboori Tilak Varma': 'Mumbai Indians',
        'Heinrich Klaasen': 'Sunrisers Hyderabad',
        'Abhishek Sharma': 'Sunrisers Hyderabad',
        'Travis Head': 'Sunrisers Hyderabad',
        'Pat Cummins': 'Sunrisers Hyderabad',
        'Nitish Kumar Reddy': 'Sunrisers Hyderabad',
        'Sunil Narine': 'Kolkata Knight Riders',
        'Andre Russell': 'Kolkata Knight Riders',
        'Rinku Singh': 'Kolkata Knight Riders',
        'Varun Chakaravarthy': 'Kolkata Knight Riders',
        'Harshit Rana': 'Kolkata Knight Riders',
        'Ramandeep Singh': 'Kolkata Knight Riders',
        'Virat Kohli': 'Royal Challengers Bengaluru',
        'Rajat Patidar': 'Royal Challengers Bengaluru',
        'Yash Dayal': 'Royal Challengers Bengaluru',
        'Shubman Gill': 'Gujarat Titans',
        'Rashid Khan': 'Gujarat Titans',
        'Sai Sudharsan': 'Gujarat Titans',
        'Rahul Tewatia': 'Gujarat Titans',
        'Shahrukh Khan': 'Gujarat Titans',
        'Ruturaj Gaikwad': 'Chennai Super Kings',
        'Ravindra Jadeja': 'Chennai Super Kings',
        'Matheesha Pathirana': 'Chennai Super Kings',
        'Shivam Dube': 'Chennai Super Kings',
        'MS Dhoni': 'Chennai Super Kings',
        'Axar Patel': 'Delhi Capitals',
        'Kuldeep Yadav': 'Delhi Capitals',
        'Tristan Stubbs': 'Delhi Capitals',
        'Abishek Porel': 'Delhi Capitals',
        'Nicholas Pooran': 'Lucknow Super Giants',
        'Ravi Bishnoi': 'Lucknow Super Giants',
        'Mayank Yadav': 'Lucknow Super Giants',
        'Mohsin Khan': 'Lucknow Super Giants',
        'Ayush Badoni': 'Lucknow Super Giants',
        'Shashank Singh': 'Punjab Kings',
        'Prabhsimran Singh': 'Punjab Kings',
        'Sanju Samson': 'Rajasthan Royals',
        'Yashasvi Jaiswal': 'Rajasthan Royals',
        'Riyan Parag': 'Rajasthan Royals',
        'Dhruv Jurel': 'Rajasthan Royals',
        'Shimron Hetmyer': 'Rajasthan Royals',
        'Sandeep Sharma': 'Rajasthan Royals'
    }

    # Pakistani players restricted under BCCI policy
    pakistan_players = {
        'Shaheen Afridi', 'Sufiyan Muqeem', 'Abrar Ahmed', 'Babar Azam', 'Mohammad Rizwan',
        'Haris Rauf', 'Naseem Shah', 'Shadab Khan', 'Fakhar Zaman', 'Iftikhar Ahmed', 'Mohammad Amir',
        'Mohammad Wasim'
    }

    # Verified local headshots
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

    country_flags = {
        'India': '🇮🇳', 'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'South Africa': '🇿🇦', 'Australia': '🇦🇺',
        'West Indies': '🌴', 'Pakistan': '🇵🇰', 'New Zealand': '🇳🇿', 'Afghanistan': '🇦🇫',
        'Sri Lanka': '🇱🇰', 'Zimbabwe': '🇿🇼', 'Ireland': '🇮🇪', 'Bangladesh': '🇧🇩'
    }

    # Capped Indian players list (known international caps)
    capped_indians = {
        'Suryakumar Yadav', 'Jasprit Bumrah', 'Virat Kohli', 'Rohit Sharma', 'Hardik Pandya',
        'Kuldeep Yadav', 'Axar Patel', 'Ravindra Jadeja', 'Shivam Dube', 'Ruturaj Gaikwad',
        'Shubman Gill', 'Rajat Patidar', 'Yash Dayal', 'Mayank Yadav', 'Ravi Bishnoi',
        'Sanju Samson', 'Yashasvi Jaiswal', 'Riyan Parag', 'Dhruv Jurel', 'Sandeep Sharma',
        'Harshit Rana', 'Nitish Kumar Reddy', 'Krunal Pandya', 'Bhuvneshwar Kumar', 'Washington Sundar',
        'Yuzvendra Chahal', 'Mohammed Shami', 'Arshdeep Singh', 'Avesh Khan', 'Khaleel Ahmed',
        'Mukesh Kumar', 'T Natarajan', 'Shardul Thakur', 'Deepak Chahar', 'Ishant Sharma',
        'Umesh Yadav', 'Prasidh Krishna', 'Abhishek Sharma', 'Rinku Singh', 'Tilak Varma'
    }

    # 1. Process Batters
    batters_all = []
    rr_bat_rank = 1

    for idx, r in bat_df.head(60).iterrows():
        pname = r['player_name']
        pid = int(r['player_id'])
        
        # Country
        country = 'India'
        for c in country_flags.keys():
            if c != 'India' and c in str(pname):
                country = c
        if pname in ['Jos Buttler', 'Phil Salt', 'Liam Livingstone', 'Sam Curran', 'Jonny Bairstow']: country = 'England'
        elif pname in ['Heinrich Klaasen', 'Tristan Stubbs', 'Reeza Hendricks', 'Ryan Rickelton', 'David Miller', 'Quinton de Kock', 'Aiden Markram', 'Faf du Plessis']: country = 'South Africa'
        elif pname in ['Tim David', 'Glenn Maxwell', 'Travis Head', 'Marcus Stoinis', 'Mitchell Marsh', 'David Warner']: country = 'Australia'
        elif pname in ['Andre Russell', 'Shimron Hetmyer', 'Nicholas Pooran', 'Rovman Powell', 'Kyle Mayers', 'Akeal Hosein', 'Shai Hope']: country = 'West Indies'
        elif pname in ['Sikandar Raza']: country = 'Zimbabwe'
        elif pname in ['Rashid Khan', 'Rahmanullah Gurbaz']: country = 'Afghanistan'
        elif pname in ['Pathum Nissanka', 'Kusal Mendis', 'Charith Asalanka', 'Dasun Shanaka']: country = 'Sri Lanka'
        elif pname in ['Babar Azam', 'Mohammad Rizwan', 'Fakhar Zaman', 'Iftikhar Ahmed']: country = 'Pakistan'

        flag = country_flags.get(country, '🇮🇳')

        # Capped / Uncapped
        if country == 'India':
            capped_status = 'Capped Indian' if pname in capped_indians else 'Uncapped Indian'
        else:
            capped_status = 'Overseas Capped'

        # Retention & Availability
        is_retained = pname in retained_pillars
        is_restricted = any(p in pname for p in pakistan_players)
        is_available = not is_retained and not is_restricted

        if is_retained:
            avail_tier = 'Tier 2: Retained Pillar'
            auction_status = f'Retained ({retained_pillars[pname]})'
            assigned_rr_rank = None
            price_bracket = 'Retained (Unattainable)'
        elif is_restricted:
            avail_tier = 'Tier 3: BCCI Restricted'
            auction_status = 'BCCI Policy Ineligible (Pakistan)'
            assigned_rr_rank = None
            price_bracket = 'Ineligible'
        else:
            avail_tier = 'Tier 1: Prime RR Target'
            auction_status = 'Auction Target / High Availability'
            assigned_rr_rank = rr_bat_rank
            rr_bat_rank += 1
            if pname in ['Jos Buttler', 'Phil Salt', 'Rishabh Pant', 'Shreyas Iyer']:
                price_bracket = '₹12.0 - 18.0 Cr (Marquee)'
            elif pname in ['Ryan Rickelton', 'Tim David', 'Liam Livingstone', 'David Miller']:
                price_bracket = '₹6.0 - 11.0 Cr (High Demand)'
            else:
                price_bracket = '₹1.5 - 5.0 Cr (Value Pick)'

        sr = float(r['hp_sr'])
        uplift = float(r['uplift_cava'])
        if sr >= 165: role = 'Death-Overs Power Finisher'
        elif sr >= 145: role = 'Middle-Overs Accelerator'
        else: role = 'Top-Order Pressure Anchor'

        clutch = int(min(99, max(65, 80 + uplift * 40 + (sr - 140) * 0.25)))
        img_url = local_images.get(pname, f"https://api.dicebear.com/7.x/identicon/svg?seed={pname.replace(' ', '')}")

        batters_all.append({
            'rank': int(r['rank']),
            'rr_auction_rank': assigned_rr_rank,
            'player_id': pid,
            'name': pname,
            'batting_type': str(r['batting_type']),
            'country': country,
            'flag': flag,
            'capped_status': capped_status,
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
            'current_franchise': retained_pillars.get(pname, 'Auction Pool'),
            'price_bracket': price_bracket,
            'plain_english_role': role,
            'non_technical_summary': f"Strikes at {sr:.1f} under pressure with +{uplift:.3f} runs added per ball above expected baselines.",
            'scouting_verdict': f"Key tactical option for Rajasthan Royals. Deployed in overs 15-20 or to steady early collapses.",
            'rr_fit': f"Fills finishing/opening requirement alongside Sanju Samson and Yashasvi Jaiswal.",
            'scenarios': {
                'death_overs': int(min(99, max(50, 70 + (sr - 140)*0.5))),
                'collapse_recovery': int(min(99, max(50, 80 + uplift*40))),
                'steep_chase_10plus_rrr': clutch,
                'vs_spin': int(min(99, max(60, 75 + uplift*35))),
                'vs_express_pace': int(min(99, max(60, 78 + (sr - 145)*0.3)))
            }
        })

    # 2. Process Bowlers
    bowlers_all = []
    rr_bowl_rank = 1

    for idx, r in bowl_df.head(60).iterrows():
        pname = r['player_name']
        pid = int(r['player_id'])

        country = 'India'
        if pname in ['Josh Hazlewood', 'Mitchell Starc', 'Pat Cummins', 'Nathan Ellis', 'Spencer Johnson', 'Jhye Richardson']: country = 'Australia'
        elif pname in ['Trent Boult', 'Tim Southee', 'Lockie Ferguson', 'Mitchell Santner', 'Matt Henry']: country = 'New Zealand'
        elif pname in ['Sunil Narine', 'Andre Russell', 'Akeal Hosein', 'Gudakesh Motie', 'Alzarri Joseph', 'Romario Shepherd']: country = 'West Indies'
        elif pname in ['Matheesha Pathirana', 'Wanindu Hasaranga', 'Maheesh Theekshana', 'Dilshan Madushanka', 'Nuwan Thushara']: country = 'Sri Lanka'
        elif pname in ['Shaheen Afridi', 'Sufiyan Muqeem', 'Abrar Ahmed', 'Haris Rauf', 'Naseem Shah', 'Mohammad Wasim']: country = 'Pakistan'
        elif pname in ['Rashid Khan', 'Fazalhaq Farooqi', 'Naveen-ul-Haq', 'Mujeeb Ur Rahman', 'Noor Ahmad']: country = 'Afghanistan'
        elif pname in ['Kagiso Rabada', 'Anrich Nortje', 'Gerald Coetzee', 'Lungi Ngidi', 'Marco Jansen', 'Nandre Burger']: country = 'South Africa'
        elif pname in ['Jofra Archer', 'Mark Wood', 'Sam Curran', 'Reece Topley', 'Jamie Overton', 'Chris Jordan']: country = 'England'

        flag = country_flags.get(country, '🇮🇳')

        if country == 'India':
            capped_status = 'Capped Indian' if pname in capped_indians else 'Uncapped Indian'
        else:
            capped_status = 'Overseas Capped'

        is_retained = pname in retained_pillars
        is_restricted = any(p in pname for p in pakistan_players)
        is_available = not is_retained and not is_restricted

        if is_retained:
            avail_tier = 'Tier 2: Retained Pillar'
            auction_status = f'Retained ({retained_pillars[pname]})'
            assigned_rr_rank = None
            price_bracket = 'Retained (Unattainable)'
        elif is_restricted:
            avail_tier = 'Tier 3: BCCI Restricted'
            auction_status = 'BCCI Policy Ineligible (Pakistan)'
            assigned_rr_rank = None
            price_bracket = 'Ineligible'
        else:
            avail_tier = 'Tier 1: Prime RR Target'
            auction_status = 'Auction Target / High Availability'
            assigned_rr_rank = rr_bowl_rank
            rr_bowl_rank += 1
            if pname in ['Josh Hazlewood', 'Mitchell Starc', 'Trent Boult', 'Yuzvendra Chahal', 'Arshdeep Singh']:
                price_bracket = '₹10.0 - 16.0 Cr (Marquee Pace/Spin)'
            elif pname in ['Krunal Pandya', 'Nathan Ellis', 'Lockie Ferguson', 'Anrich Nortje', 'T Natarajan', 'Bhuvneshwar Kumar']:
                price_bracket = '₹5.0 - 9.0 Cr (Key Specialist)'
            else:
                price_bracket = '₹1.0 - 4.0 Cr (Value Tactical)'

        econ = float(r['hp_econ'])
        uplift = float(r['uplift_cava'])
        b_type = str(r['bowling_type'])

        if 'Fast' in b_type or 'medium' in b_type:
            role = 'Lockdown Pace Spearhead' if econ <= 7.5 else 'Death Yorker Specialist'
        else:
            role = 'Mystery Choke Spinner' if econ <= 7.0 else 'Attacking Wrist Spinner'

        clutch = int(min(99, max(65, 80 + uplift * 35 + (8.5 - econ) * 3.0)))
        img_url = local_images.get(pname, f"https://api.dicebear.com/7.x/identicon/svg?seed={pname.replace(' ', '')}")

        bowlers_all.append({
            'rank': int(r['rank']),
            'rr_auction_rank': assigned_rr_rank,
            'player_id': pid,
            'name': pname,
            'bowling_type': b_type,
            'country': country,
            'flag': flag,
            'capped_status': capped_status,
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
            'current_franchise': retained_pillars.get(pname, 'Auction Pool'),
            'price_bracket': price_bracket,
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

    # Save RR-specific auction tables to CSV
    rr_bat_only = [p for p in batters_all if p['is_auction_available']]
    rr_bowl_only = [p for p in bowlers_all if p['is_auction_available']]

    pd.DataFrame(rr_bat_only).to_csv('outputs/batting_rankings_rr_auction.csv', index=False)
    pd.DataFrame(rr_bowl_only).to_csv('outputs/bowling_rankings_rr_auction.csv', index=False)
    print(f"Saved outputs/batting_rankings_rr_auction.csv ({len(rr_bat_only)} targets) and bowling ({len(rr_bowl_only)} targets).")

    # Pre-defined Iconic Pressure Situations for Simulator
    preset_situations = [
        {
            'id': 'final_over_chase',
            'title': '🏆 Final Over Miracle (18 needed off 6 balls)',
            'description': '18 runs required off the 20th over. 6 wickets down. Extreme boundary demand against death yorkers.',
            'mode': 'batting',
            'runs': 18,
            'balls': 6,
            'wickets': 6,
            'phase': 'Death',
            'venue': 'Sawai Mansingh Stadium, Jaipur (RR Home)',
            'matchup': 'pace'
        },
        {
            'id': 'jaipur_fortress_defense',
            'title': '🏰 Jaipur Fortress Defense (Defend 16 in 12 balls)',
            'description': 'Opponents need 16 runs off the last 2 overs at SMS Jaipur. Sandeep Sharma bowls over 19; need spearhead for over 20.',
            'mode': 'bowling',
            'runs': 16,
            'balls': 12,
            'wickets': 5,
            'phase': 'Death',
            'venue': 'Sawai Mansingh Stadium, Jaipur (RR Home)',
            'matchup': 'pace'
        },
        {
            'id': 'powerplay_collapse',
            'title': '🚨 Powerplay Collapse Shock (28/3 in Over 4)',
            'description': 'Top-3 blown away. Team at 28/3. Need a composed stabilizer who absorbs dot balls without stalling run rate.',
            'mode': 'batting',
            'runs': 24,
            'balls': 18,
            'wickets': 3,
            'phase': 'Powerplay',
            'venue': 'Wankhede Stadium, Mumbai',
            'matchup': 'pace'
        },
        {
            'id': 'chepauk_spin_choke',
            'title': '🌪️ Chepauk Turning Track Spin Choke',
            'description': 'Overs 8-15 on a dry turning wicket in Chennai. Need a spin destroyer who can hit length balls for six.',
            'mode': 'batting',
            'runs': 62,
            'balls': 42,
            'wickets': 4,
            'phase': 'Middle',
            'venue': 'MA Chidambaram Stadium, Chennai (Chepauk)',
            'matchup': 'spin'
        },
        {
            'id': 'middle_overs_partnership_break',
            'title': '🎯 Middle-Overs Partnership Breakthrough',
            'description': 'Opposing batters cruising at 110/1 in Over 11. Need an attacking wicket-taking bowler to trigger a collapse.',
            'mode': 'bowling',
            'runs': 38,
            'balls': 24,
            'wickets': 1,
            'phase': 'Middle',
            'venue': 'Narendra Modi Stadium, Ahmedabad',
            'matchup': 'spin'
        },
        {
            'id': 'steep_200_chase',
            'title': '🚀 Steep 210+ Monster Chase (13.5 RPO required)',
            'description': 'Chasing 215. Need 81 runs in the last 6 overs. Requires ruthless power hitting from ball one.',
            'mode': 'batting',
            'runs': 81,
            'balls': 36,
            'wickets': 4,
            'phase': 'Death',
            'venue': 'M. Chinnaswamy Stadium, Bengaluru',
            'matchup': 'pace'
        }
    ]

    # Two official dropdown selection packages
    unstop_dropdown_sets = {
        'set_1_pure_statistical': {
            'description': 'Top 10 Most Reliable Players Under Pressure Across Entire Dataset (Includes Retained Pillars)',
            'batters': [b['name'] for b in batters_all[:10]],
            'bowlers': [b['name'] for b in bowlers_all[:10]]
        },
        'set_2_rr_auction_targets': {
            'description': 'Rajasthan Royals IPL 2027 Auction Shortlist (100% Targetable in Auction; Retained Stars Excluded)',
            'batters': [b['name'] for b in rr_bat_only[:10]],
            'bowlers': [b['name'] for b in rr_bowl_only[:10]]
        }
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
            'displayed_batters': len(batters_all),
            'displayed_bowlers': len(bowlers_all),
            'deliveries_analyzed': 200999,
            'matches_analyzed': 867,
            'seasons': '2022-2026',
            'reconciliation_status': '100% Reconciled'
        },
        'dropdown_options': unstop_dropdown_sets,
        'preset_situations': preset_situations,
        'batters': batters_all,
        'bowlers': bowlers_all,
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

    print("Saved frontend/data/analytics_data.json successfully with full auction logic, capped/uncapped tags, and preset situations!")

if __name__ == '__main__':
    enrich_rr_auction_system()
