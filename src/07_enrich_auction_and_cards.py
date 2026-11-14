import json
import pandas as pd

def enrich_player_profiles():
    print("=== Enriching Player Profiles with Auction Availability & Plain English Insights ===")

    bat_df = pd.read_csv('outputs/batting_rankings.csv')
    bowl_df = pd.read_csv('outputs/bowling_rankings.csv')

    # Detailed auction research mappings
    bat_auction_meta = {
        'Suryakumar Yadav': {
            'auction_status': 'Retained Core Pillar (Mumbai Indians)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Mumbai Indians',
            'plain_english_role': 'World #1 360° Death-Overs Finisher',
            'clutch_score': 99,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/174.png',
            'country': 'India',
            'flag': '🇮🇳',
            'scouting_verdict': 'Unattainable in auction. Mumbai Indians top retention and captaincy figurehead. Keep as benchmark for ideal 360° pressure metrics.',
            'non_technical_summary': 'Scores at an astonishing 173 runs per 100 balls in tight games. Hits boundaries to all 360 degrees of the ground regardless of bowler pace or field placements.',
            'rr_fit': 'Benchmark standard; impossible to acquire.'
        },
        'Jos Buttler': {
            'auction_status': 'Prime RR Target / Marquee Wicketkeeper-Opener',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / Ex-RR / Gujarat Titans',
            'plain_english_role': 'Explosive Match-Winning Opener & Anchor',
            'clutch_score': 95,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/182.png',
            'country': 'England',
            'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
            'scouting_verdict': 'Top priority re-acquisition for RR. Proven match-winner at SMS Stadium Jaipur, commands highest pressure stability in 200+ chases.',
            'non_technical_summary': 'The consummate big-match player. In high-pressure games, his strike rate actually climbs to 168.7 with an elite boundary-hitting consistency.',
            'rr_fit': 'Seamless fit at opening slot; leadership synergy with Sanju Samson.'
        },
        'Reeza Hendricks': {
            'auction_status': 'High Availability Auction Sleeper',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'International / Free Agent',
            'plain_english_role': 'Top-Order Stabilizer & Chase Accelerator',
            'clutch_score': 94,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/320000/320077.png',
            'country': 'South Africa',
            'flag': '🇿🇦',
            'scouting_verdict': 'High-value, cost-effective overseas anchor. Extremely high uplift (+0.375 CAVA) in high-stakes international tournament matches.',
            'non_technical_summary': 'A technically sound top-order batter who elevates his scoring rate when wickets fall early, preventing collapses while keeping the scoreboard moving.',
            'rr_fit': 'Budget-friendly overseas top-order backup/starter.'
        },
        'Heinrich Klaasen': {
            'auction_status': 'Retained Core Pillar (Sunrisers Hyderabad)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Sunrisers Hyderabad (INR 23 Cr)',
            'plain_english_role': 'Premier Middle-Overs Spin Destroyer',
            'clutch_score': 93,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/202.png',
            'country': 'South Africa',
            'flag': '🇿🇦',
            'scouting_verdict': 'Retained by SRH for INR 23 Cr. Completely unattainable in auction. Benchmark for handling defensive spin chokes.',
            'non_technical_summary': 'The most destructive batter in T20 cricket against spinners in overs 7–15. Turns high required run rates into routine chases by hitting length balls for sixes.',
            'rr_fit': 'Retained by SRH; impossible to acquire.'
        },
        'Phil Salt': {
            'auction_status': 'Marquee Auction Target (Explosive Wicketkeeper)',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / Ex-KKR',
            'plain_english_role': 'Hyper-Aggressive Powerplay Demolisher',
            'clutch_score': 92,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/1183.png',
            'country': 'England',
            'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
            'scouting_verdict': 'Premier explosive opening target. Strikes at 170+ under pressure, obliterating opposition bowling before death overs begin.',
            'non_technical_summary': 'Attacks from ball one without fear. In high-stakes chases, he forces bowlers off their lengths and gives the team an immediate 15-20 run head start.',
            'rr_fit': 'Ideal opening partner for Yashasvi Jaiswal, relieving pressure on middle order.'
        },
        'Ryan Rickelton': {
            'auction_status': 'Prime Emerging Auction Target (Wicketkeeper-Batter)',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / MI Cape Town',
            'plain_english_role': 'Dynamic Left-Handed Top-Order Enforcer',
            'clutch_score': 90,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/321800/321876.png',
            'country': 'South Africa',
            'flag': '🇿🇦',
            'scouting_verdict': 'High-upside South African keeper-batter. Enormous pressure uplift (+0.204 CAVA), excellent against pace on hard surfaces.',
            'non_technical_summary': 'An aggressive, fearless left-hander who thrives under pressure. Has demonstrated remarkable consistency across franchise leagues and international T20s.',
            'rr_fit': 'High-value value pick for top 3 with wicketkeeping flexibility.'
        },
        'Abhishek Sharma': {
            'auction_status': 'Retained Core Pillar (Sunrisers Hyderabad)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Sunrisers Hyderabad',
            'plain_english_role': 'Elite Powerplay Strike-Rate Booster',
            'clutch_score': 88,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/212.png',
            'country': 'India',
            'flag': '🇮🇳',
            'scouting_verdict': 'Retained by SRH. Unattainable. Benchmark for rapid powerplay boundary hitting.',
            'non_technical_summary': 'Hits boundaries with 173+ strike rate in the first 6 overs. Puts bowling attacks under immediate psychological duress.',
            'rr_fit': 'Retained by SRH; unattainable.'
        },
        'Andre Russell': {
            'auction_status': 'Retained Core Pillar (Kolkata Knight Riders)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Kolkata Knight Riders',
            'plain_english_role': 'Legendary Death-Overs Power Match-Winner',
            'clutch_score': 87,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/141.png',
            'country': 'West Indies',
            'flag': '🌴',
            'scouting_verdict': 'KKR franchise cornerstone. Retained. The standard for brute force boundary clearing under 12+ RRR.',
            'non_technical_summary': 'Possesses unmatched raw bat speed. Can win games requiring 20 runs in the final over purely through physical power and boundary clearance.',
            'rr_fit': 'Retained by KKR; unattainable.'
        },
        'Tristan Stubbs': {
            'auction_status': 'Top Priority Auction / Retention Target',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Delhi Capitals / Auction Pool',
            'plain_english_role': 'Elite Death-Overs Finisher & 360° Striker',
            'clutch_score': 86,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/1017.png',
            'country': 'South Africa',
            'flag': '🇿🇦',
            'scouting_verdict': 'MUST-TARGET for Rajasthan Royals. Proven ability to hit both 145+ km/h pace and mystery spin at the death (+0.194 CAVA uplift). Solves RR finishing void.',
            'non_technical_summary': 'An extraordinarily versatile young finisher. Can scoop 145 km/h yorkers over fine leg and hit spinners straight down the ground under intense pressure.',
            'rr_fit': 'Perfect No. 5/6 finisher to pair with Shimron Hetmyer.'
        },
        'Sikandar Raza': {
            'auction_status': 'High Availability Auction Target (All-Rounder)',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / Ex-PBKS',
            'plain_english_role': 'Veteran Pressure Absorber & Middle-Order Anchor',
            'clutch_score': 84,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/320000/320013.png',
            'country': 'Zimbabwe',
            'flag': '🇿🇼',
            'scouting_verdict': 'Smart, tactical budget pick. 365 pressure balls with +0.219 CAVA uplift. Excellent composure in close, low-scoring thrillers.',
            'non_technical_summary': 'A hardened veteran who thrives when the team is in trouble. Reads match situations astutely and picks low-risk boundary options to steer chases home.',
            'rr_fit': 'Cost-effective squad balance all-rounder.'
        }
    }

    bowl_auction_meta = {
        'Sunil Narine': {
            'auction_status': 'Retained Core Pillar (Kolkata Knight Riders)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Kolkata Knight Riders',
            'plain_english_role': 'The Ultimate High-Pressure Mystery Choke Spinner',
            'clutch_score': 99,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/156.png',
            'country': 'West Indies',
            'flag': '🌴',
            'scouting_verdict': 'KKR lifetime retention. Unattainable. Benchmark for death-over run containment (6.37 economy in pressure situations).',
            'non_technical_summary': 'Virtually impossible to score boundaries against even in the 19th and 20th overs. Bowls with a mystery grip that batters cannot read under pressure.',
            'rr_fit': 'Retained by KKR; unattainable.'
        },
        'Jasprit Bumrah': {
            'auction_status': 'Retained Core Pillar (Mumbai Indians)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Mumbai Indians',
            'plain_english_role': 'Greatest All-Format T20 Death Bowler in History',
            'clutch_score': 98,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/9.png',
            'country': 'India',
            'flag': '🇮🇳',
            'scouting_verdict': 'Mumbai Indians cornerstone. Unattainable. 575 pressure deliveries with 6.93 economy and 34 clutch wickets.',
            'non_technical_summary': 'Unrivaled pinpoint yorker accuracy and deceptive slower balls. Consistently defends 7-8 runs in the final over against elite batters.',
            'rr_fit': 'Retained by MI; unattainable.'
        },
        'Kuldeep Yadav': {
            'auction_status': 'Retained Core Pillar (Delhi Capitals)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Delhi Capitals',
            'plain_english_role': 'Elite Attacking Middle-Overs Wicket Hunter',
            'clutch_score': 95,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/14.png',
            'country': 'India',
            'flag': '🇮🇳',
            'scouting_verdict': 'Delhi Capitals top retention. 40 pressure wickets at 6.95 economy. The premier wrist-spinner in high-demand middle overs.',
            'non_technical_summary': 'Breaks big partnerships when opponents are cruising. Uses sharp turn both ways to deceive batters looking to accelerate.',
            'rr_fit': 'Retained by DC; unattainable.'
        },
        'Krunal Pandya': {
            'auction_status': 'High Availability Auction / Trade Target',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / Ex-LSG / RCB',
            'plain_english_role': 'Defensive Powerplay & Middle Choke Specialist',
            'clutch_score': 92,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/17.png',
            'country': 'India',
            'flag': '🇮🇳',
            'scouting_verdict': 'HIGH-PRIORITY INDIAN TARGET for RR. Phenomenal 6.03 economy under pressure with +0.461 CAVA uplift. Solves domestic all-rounder balance.',
            'non_technical_summary': 'Fires flat, rapid darts into the pitch that batters cannot get under. Creates massive dot-ball pressure that forces mistakes.',
            'rr_fit': 'Crucial Indian spin-bowling all-rounder for RR XI.'
        },
        'Sufiyan Muqeem': {
            'auction_status': 'BCCI Policy Ineligible (Pakistan National)',
            'is_auction_available': False,
            'availability_tier': 'Tier 2: BCCI Restricted',
            'current_franchise': 'Pakistan / International Only',
            'plain_english_role': 'Emerging Left-Arm Wrist-Spin Mystery Bowler',
            'clutch_score': 91,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/372000/372091.png',
            'country': 'Pakistan',
            'flag': '🇵🇰',
            'scouting_verdict': 'BCCI regulations prohibit Pakistani players from entering the IPL auction. Kept in model for pure statistical integrity.',
            'non_technical_summary': 'Extraordinary 4.60 economy rate in pressure matches with sharp deceptive wrong-uns. Statistically brilliant but administratively unavailable.',
            'rr_fit': 'Ineligible due to BCCI policy.'
        },
        'Shaheen Afridi': {
            'auction_status': 'BCCI Policy Ineligible (Pakistan National)',
            'is_auction_available': False,
            'availability_tier': 'Tier 2: BCCI Restricted',
            'current_franchise': 'Pakistan / International Only',
            'plain_english_role': 'Lethal Opening-Over Swing & Yorker Speadhead',
            'clutch_score': 89,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/320000/320050.png',
            'country': 'Pakistan',
            'flag': '🇵🇰',
            'scouting_verdict': 'BCCI policy ineligible. Included for objective benchmarking.',
            'non_technical_summary': 'Unrivaled powerplay wicket-taker who strikes in the 1st over of high-stakes matches with 145 km/h inswingers.',
            'rr_fit': 'Ineligible due to BCCI policy.'
        },
        'Josh Hazlewood': {
            'auction_status': 'Marquee Auction Target (Pace Spearhead)',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Auction Pool / Ex-RCB / CSK',
            'plain_english_role': 'Elite Relentless Line & Length Lockdown Bowler',
            'clutch_score': 88,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/830.png',
            'country': 'Australia',
            'flag': '🇦🇺',
            'scouting_verdict': 'TOP OVERSEAS PACER TARGET FOR RR. 45 pressure wickets across 549 balls. Incredible hit-the-deck discipline in powerplay and death.',
            'non_technical_summary': 'Operates like a robotic bowling machine. Repeatedly lands deliveries on the top of off-stump at high pace, conceding almost zero free hits under pressure.',
            'rr_fit': 'Commands new-ball and death overs; would form elite pace attack with Sandeep Sharma.'
        },
        'Matheesha Pathirana': {
            'auction_status': 'CSK Core Retention / High-Bid Auction Target',
            'is_auction_available': True,
            'availability_tier': 'Tier 3: Prime RR Target',
            'current_franchise': 'Chennai Super Kings / Auction Pool',
            'plain_english_role': 'Unorthodox 148 km/h Sling-Action Death Destroyer',
            'clutch_score': 87,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/1014.png',
            'country': 'Sri Lanka',
            'flag': '🇱🇰',
            'scouting_verdict': 'If CSK does not retain or in auction, GO ALL OUT. 38 pressure wickets at 7.70 economy. The closest modern successor to Lasith Malinga.',
            'non_technical_summary': 'Releases the ball from an impossibly low angle at 148 km/h. Batters cannot spot the ball at the death, leading to clean-bowled dismissals and missed swings.',
            'rr_fit': 'Completely solves RR death bowling for the next 5 years.'
        },
        'Rashid Khan': {
            'auction_status': 'Retained Core Pillar (Gujarat Titans)',
            'is_auction_available': False,
            'availability_tier': 'Tier 1: Retained Pillar',
            'current_franchise': 'Gujarat Titans',
            'plain_english_role': 'World Premier T20 Match-Winning Leg-Spinner',
            'clutch_score': 86,
            'image_url': 'https://documents.iplt20.com/ipl/IPLHeadshot2024/218.png',
            'country': 'Afghanistan',
            'flag': '🇦🇫',
            'scouting_verdict': 'Gujarat Titans top retention. 57 pressure wickets across 801 balls (highest volume in dataset). Unattainable.',
            'non_technical_summary': 'Bowls 95–100 km/h quick leg-spin with a rapid arm speed that denies batters reaction time. A guaranteed choke point in any chase.',
            'rr_fit': 'Retained by GT; unattainable.'
        },
        'Abrar Ahmed': {
            'auction_status': 'BCCI Policy Ineligible (Pakistan National)',
            'is_auction_available': False,
            'availability_tier': 'Tier 2: BCCI Restricted',
            'current_franchise': 'Pakistan / International Only',
            'plain_english_role': 'High-Accuracy Mystery Leg-Spinner',
            'clutch_score': 85,
            'image_url': 'https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci/db/PICTURES/CMS/369400/369431.png',
            'country': 'Pakistan',
            'flag': '🇵🇰',
            'scouting_verdict': 'BCCI policy ineligible. Included for objective statistical completeness.',
            'non_technical_summary': 'Bowls with high precision (5.37 economy rate in pressure games). Highly effective carrom ball.',
            'rr_fit': 'Ineligible due to BCCI policy.'
        }
    }

    # Save to enriched JSON
    enriched_data = {
        'batters': bat_auction_meta,
        'bowlers': bowl_auction_meta
    }
    with open('outputs/enriched_player_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_data, f, indent=2, ensure_ascii=False)

    print("Saved outputs/enriched_player_profiles.json successfully!")

if __name__ == '__main__':
    enrich_player_profiles()
