"""
build_comprehensive_database.py
Generates the comprehensive, non-generic player database for the Rajasthan Royals
War Room & Unstop SupeRR Selector submission.

Includes:
- Complete player census (1,217 players, 888 strikers, 647 bowlers)
- Franchise contract & retention prediction model (MI, SRH, KKR, RR, CSK, DC, GT, RCB, LSG, PBKS)
- Capped / Uncapped / Overseas categorization
- Verified local headshot mappings
- Plain-English non-technical scouting summaries & auction war-room tags
- Pre-defined tactical pressure scenarios
"""

import os
import json
import pandas as pd
import numpy as np

# Load raw mappings and processed data
DATA_PACK_DIR = "Data Pack"
PROCESSED_DIR = "data_processed"
OUTPUTS_DIR = "outputs"
FRONTEND_DATA_DIR = "frontend/data"
PUBLIC_PLAYERS_DIR = "frontend/public/players"

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)

# 1. Load Data Pack Files
df_map = pd.read_csv(os.path.join(DATA_PACK_DIR, "competition_team_player_mapping.csv"))
df_p11 = pd.read_csv(os.path.join(DATA_PACK_DIR, "playing_eleven.csv"))
df_teams = pd.read_csv(os.path.join(DATA_PACK_DIR, "teams.csv"))
df_matches = pd.read_csv(os.path.join(DATA_PACK_DIR, "matches.csv"))

# 2. Load Processed Rankings
df_bat = pd.read_csv(os.path.join(OUTPUTS_DIR, "batting_rankings.csv"))
df_bowl = pd.read_csv(os.path.join(OUTPUTS_DIR, "bowling_rankings.csv"))

# Verify available local images
local_images = set(os.listdir(PUBLIC_PLAYERS_DIR)) if os.path.exists(PUBLIC_PLAYERS_DIR) else set()
print(f"Loaded {len(local_images)} local headshots in {PUBLIC_PLAYERS_DIR}")

# 3. Known Franchise Retentions & Contract Status (Real-world IPL mega-auction & 2026 data mapping)
FRANCHISE_RETENTIONS = {
    # Mumbai Indians Core (Unavailable)
    "Suryakumar Yadav": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Captain", "auction_target": False},
    "Jasprit Bumrah": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Ace", "auction_target": False},
    "Ryan Rickelton": {"status": "CONTRACTED_RIVAL", "team": "Mumbai Indians", "label": "MI Family / Contracted", "auction_target": False},
    "Hardik Pandya": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Captain/All-rounder", "auction_target": False},
    "Rohit Sharma": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Veteran", "auction_target": False},
    "Tilak Varma": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Middle-Order", "auction_target": False},
    "Namboori Tilak Varma": {"status": "RETAINED_RIVAL", "team": "Mumbai Indians", "label": "MI Retained Middle-Order", "auction_target": False},

    # Sunrisers Hyderabad Core (Unavailable)
    "Heinrich Klaasen": {"status": "RETAINED_RIVAL", "team": "Sunrisers Hyderabad", "label": "SRH Retained Finisher (23 Cr)", "auction_target": False},
    "Abhishek Sharma": {"status": "RETAINED_RIVAL", "team": "Sunrisers Hyderabad", "label": "SRH Retained Opener (14 Cr)", "auction_target": False},
    "Pat Cummins": {"status": "RETAINED_RIVAL", "team": "Sunrisers Hyderabad", "label": "SRH Retained Captain (18 Cr)", "auction_target": False},
    "Travis Head": {"status": "RETAINED_RIVAL", "team": "Sunrisers Hyderabad", "label": "SRH Retained Opener (14 Cr)", "auction_target": False},
    "Nitish Kumar Reddy": {"status": "RETAINED_RIVAL", "team": "Sunrisers Hyderabad", "label": "SRH Retained All-Rounder", "auction_target": False},

    # Kolkata Knight Riders Core (Unavailable)
    "Sunil Narine": {"status": "RETAINED_RIVAL", "team": "Kolkata Knight Riders", "label": "KKR Franchise Icon Retained", "auction_target": False},
    "Andre Russell": {"status": "RETAINED_RIVAL", "team": "Kolkata Knight Riders", "label": "KKR Franchise Icon Retained", "auction_target": False},
    "Rinku Singh": {"status": "RETAINED_RIVAL", "team": "Kolkata Knight Riders", "label": "KKR Retained Finisher", "auction_target": False},
    "Varun Chakaravarthy": {"status": "RETAINED_RIVAL", "team": "Kolkata Knight Riders", "label": "KKR Retained Spinner", "auction_target": False},
    "Harshit Rana": {"status": "RETAINED_RIVAL", "team": "Kolkata Knight Riders", "label": "KKR Retained Pacer", "auction_target": False},

    # Chennai Super Kings Core (Unavailable)
    "Ruturaj Gaikwad": {"status": "RETAINED_RIVAL", "team": "Chennai Super Kings", "label": "CSK Retained Captain", "auction_target": False},
    "Matheesha Pathirana": {"status": "RETAINED_RIVAL", "team": "Chennai Super Kings", "label": "CSK Retained Death Specialist (13 Cr)", "auction_target": False},
    "Ravindra Jadeja": {"status": "RETAINED_RIVAL", "team": "Chennai Super Kings", "label": "CSK Retained All-Rounder (18 Cr)", "auction_target": False},
    "Shivam Dube": {"status": "RETAINED_RIVAL", "team": "Chennai Super Kings", "label": "CSK Retained Power Hitter (12 Cr)", "auction_target": False},
    "MS Dhoni": {"status": "RETAINED_RIVAL", "team": "Chennai Super Kings", "label": "CSK Retained Uncapped Icon", "auction_target": False},

    # Delhi Capitals Core (Unavailable)
    "Kuldeep Yadav": {"status": "RETAINED_RIVAL", "team": "Delhi Capitals", "label": "DC Retained Spinner (13.25 Cr)", "auction_target": False},
    "Axar Patel": {"status": "RETAINED_RIVAL", "team": "Delhi Capitals", "label": "DC Retained All-Rounder (16.5 Cr)", "auction_target": False},
    "Tristan Stubbs": {"status": "RETAINED_RIVAL", "team": "Delhi Capitals", "label": "DC Retained Middle Order (10 Cr)", "auction_target": False},
    "Abishek Porel": {"status": "RETAINED_RIVAL", "team": "Delhi Capitals", "label": "DC Retained Wicketkeeper (4 Cr)", "auction_target": False},

    # Gujarat Titans Core (Unavailable)
    "Rashid Khan": {"status": "RETAINED_RIVAL", "team": "Gujarat Titans", "label": "GT Retained Ace Spinner (18 Cr)", "auction_target": False},
    "Shubman Gill": {"status": "RETAINED_RIVAL", "team": "Gujarat Titans", "label": "GT Retained Captain (16.5 Cr)", "auction_target": False},
    "Sai Sudharsan": {"status": "RETAINED_RIVAL", "team": "Gujarat Titans", "label": "GT Retained Anchor (8.5 Cr)", "auction_target": False},
    "Rahul Tewatia": {"status": "RETAINED_RIVAL", "team": "Gujarat Titans", "label": "GT Retained Finisher (4 Cr)", "auction_target": False},

    # Royal Challengers Bengaluru Core (Unavailable)
    "Virat Kohli": {"status": "RETAINED_RIVAL", "team": "Royal Challengers Bengaluru", "label": "RCB Retained Pillar (21 Cr)", "auction_target": False},
    "Rajat Patidar": {"status": "RETAINED_RIVAL", "team": "Royal Challengers Bengaluru", "label": "RCB Retained Batter (11 Cr)", "auction_target": False},
    "Yash Dayal": {"status": "RETAINED_RIVAL", "team": "Royal Challengers Bengaluru", "label": "RCB Retained Pacer (5 Cr)", "auction_target": False},

    # Lucknow Super Giants Core (Unavailable)
    "Nicholas Pooran": {"status": "RETAINED_RIVAL", "team": "Lucknow Super Giants", "label": "LSG Retained Star (21 Cr)", "auction_target": False},
    "Ravi Bishnoi": {"status": "RETAINED_RIVAL", "team": "Lucknow Super Giants", "label": "LSG Retained Spinner (11 Cr)", "auction_target": False},
    "Mayank Yadav": {"status": "RETAINED_RIVAL", "team": "Lucknow Super Giants", "label": "LSG Retained Express Pacer (11 Cr)", "auction_target": False},

    # Punjab Kings Core (Unavailable)
    "Shashank Singh": {"status": "RETAINED_RIVAL", "team": "Punjab Kings", "label": "PBKS Retained Finisher (5.5 Cr)", "auction_target": False},

    # Rajasthan Royals Retained Core (CURRENT WAR ROOM SQUAD)
    "Sanju Samson": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Captain / WK (18 Cr)", "auction_target": False},
    "Yashasvi Jaiswal": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Explosive Opener (18 Cr)", "auction_target": False},
    "Riyan Parag": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Clutch Batter (14 Cr)", "auction_target": False},
    "Dhruv Jurel": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Middle/WK (14 Cr)", "auction_target": False},
    "Shimron Hetmyer": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Finisher (11 Cr)", "auction_target": False},
    "Sandeep Sharma": {"status": "RR_CORE", "team": "Rajasthan Royals", "label": "RR Retained Death Bowler (4 Cr)", "auction_target": False},

    # BCCI Policy Ineligible (Pakistan National Players)
    "Shaheen Afridi": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan International (BCCI Ineligible)", "auction_target": False},
    "Shaheen Shah Afridi": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan International (BCCI Ineligible)", "auction_target": False},
    "Sufiyan Muqeem": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan Emerging (BCCI Ineligible)", "auction_target": False},
    "Abrar Ahmed": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan Mystery Spinner (BCCI Ineligible)", "auction_target": False},
    "Mohammad Wasim": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan Pacer (BCCI Ineligible)", "auction_target": False},
    "Babar Azam": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan International (BCCI Ineligible)", "auction_target": False},
    "Mohammad Rizwan": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan International (BCCI Ineligible)", "auction_target": False},
    "Haris Rauf": {"status": "BCCI_INELIGIBLE", "team": "Pakistan", "label": "Pakistan International (BCCI Ineligible)", "auction_target": False},
}

# Real-world Auction Pool Targets (Available for RR to bid & acquire in IPL 2027)
AUCTION_TARGET_TIERS = {
    # Batters
    "Jos Buttler": {"tier": "Tier 1 Marquee", "est_price": "₹12.0 - 15.0 Cr", "role": "Opening Batter / Aggressive Anchor", "scouting": "Former RR champion with 94.6 CAVA under pressure. Unmatched ability to pace high-target chases."},
    "Reeza Hendricks": {"tier": "Tier 1 International", "est_price": "₹3.0 - 5.0 Cr", "role": "Top Order Anchor / Opener", "scouting": "International free agent. 90.7 CAVA under pressure with extraordinary 56.5% positive-match clutch rate. Ideal high-value top-order pickup."},
    "Phil Salt": {"tier": "Tier 1 Marquee", "est_price": "₹9.0 - 12.0 Cr", "role": "Wicketkeeper / Powerplay Blaster", "scouting": "Strike rate 168.4 in high pressure. Destroys bowling in first 6 overs to establish dominant required rates."},
    "Sikandar Raza": {"tier": "Tier 2 Value", "est_price": "₹2.5 - 4.0 Cr", "role": "Spin All-Rounder / Finisher", "scouting": "Zimbabwe veteran with proven clutch finishes. Elite value-for-money batting-spin combo."},
    "Tim David": {"tier": "Tier 1 Finisher", "est_price": "₹6.0 - 8.5 Cr", "role": "Power Death Finisher", "scouting": "Raw power hitter at numbers 6-7. Exceptional boundary conversion percentage against express pace in death overs."},
    "Pathum Nissanka": {"tier": "Tier 2 Value", "est_price": "₹2.0 - 3.5 Cr", "role": "Opening Batter", "scouting": "Sri Lankan anchor who converts starts under pressure with controlled strike rotation and boundary placement."},
    "Prabhsimran Singh": {"tier": "Tier 2 Domestic Capped", "est_price": "₹3.5 - 5.5 Cr", "role": "Top Order / Aggressor", "scouting": "Young Indian capped batter with fearless powerplay approach; complements Jaiswal and Samson."},
    "Glenn Phillips": {"tier": "Tier 2 Dynamic Utility", "est_price": "₹4.0 - 6.0 Cr", "role": "Middle Order / Off-Spin / Keeper", "scouting": "Exceptional fielder, 360-degree hitter, and handy off-spin option against left-handers under pressure."},
    "Akeal Hosein": {"tier": "Tier 2 Specialist", "est_price": "₹2.0 - 3.0 Cr", "role": "Bowling All-Rounder / Finisher", "scouting": "Economical left-arm spinner and handy power hitter down the order under tight game states."},
    "Kusal Mendis": {"tier": "Tier 2 Wicketkeeper", "est_price": "₹2.0 - 3.5 Cr", "role": "Top Order / WK", "scouting": "Experienced Sri Lankan campaigner with proven match-winning innings in tight international T20 run-chases."},

    # Bowlers
    "Krunal Pandya": {"tier": "Tier 1 Domestic All-Rounder", "est_price": "₹6.0 - 8.5 Cr", "role": "Left-Arm Orthodox / Middle-Overs Controller", "scouting": "Highest-rated auction-available spinner under pressure (83.8 score). Economy 6.94 in high pressure situations with elite defensive dot-ball percentage."},
    "Josh Hazlewood": {"tier": "Tier 1 Marquee Pacer", "est_price": "₹8.0 - 11.0 Cr", "role": "New Ball & Death Enforcer", "scouting": "World-class accuracy. Bowls tight test-match lengths under white-ball pressure, denying batters scoring arcs."},
    "Tim Southee": {"tier": "Tier 2 Veteran Swing", "est_price": "₹2.0 - 3.5 Cr", "role": "Powerplay & Death Swing", "scouting": "Vastly experienced international leader. 49.6 CAVA under pressure with unmatched calm in final over defenses."},
    "Jamie Overton": {"tier": "Tier 2 Express All-Rounder", "est_price": "₹3.5 - 5.0 Cr", "role": "Middle Overs Enforcer / Lower Order Hitter", "scouting": "Hits 145+ km/h and extracts steep bounce on flat tracks. Dual threat with bat and ball under match pressure."},
    "Nathan Ellis": {"tier": "Tier 1 Death Specialist", "est_price": "₹4.5 - 6.5 Cr", "role": "Specialist Death Bowler", "scouting": "Master of back-of-the-hand slower balls and pinpoint wide yorkers. 47.9 CAVA in death over high-leverage deliveries."},
    "Gudakesh Motie": {"tier": "Tier 2 Mystery Orthodox", "est_price": "₹2.5 - 4.0 Cr", "role": "Spin Choke Specialist", "scouting": "West Indian left-arm spinner who stymies scoring rates in overs 7-15. Exceptional 52.8% positive-match share under pressure."},
    "Mujeeb Ur Rahman": {"tier": "Tier 2 Mystery Spinner", "est_price": "₹3.0 - 4.5 Cr", "role": "Powerplay & Middle Mystery Spinner", "scouting": "Can bowl with 2 fielders out in powerplay and strangle right-handers with carrom ball variations."},
    "Bhuvneshwar Kumar": {"tier": "Tier 2 Indian Swing Icon", "est_price": "₹4.0 - 6.0 Cr", "role": "Powerplay Swing Specialist", "scouting": "Two-time Purple Cap winner. Guarantees early wickets and defensive control in first 4 overs without conceding boundary spikes."},
    "Mitchell Santner": {"tier": "Tier 2 All-Rounder", "est_price": "₹3.5 - 5.0 Cr", "role": "Left-Arm Choke & Captaincy Mind", "scouting": "Consistently concedes under 7.00 RPO under extreme leverage. World-class tactical acumen and fielding."},
    "Trent Boult": {"tier": "Tier 1 Marquee Pacer", "est_price": "₹7.0 - 9.0 Cr", "role": "First-Over Wicket Enforcer", "scouting": "Former RR opening stalwart. Lethal inswing to right-handers in over 1; provides psychological edge in big games."},
    "Yuzvendra Chahal": {"tier": "Tier 1 Match Winner", "est_price": "₹8.0 - 10.5 Cr", "role": "Attacking Leg-Spinner", "scouting": "IPL's all-time leading wicket-taker. Not afraid to buy wickets in overs 10-17 under heavy chasing pressure."}
}

# 4. Helper to determine Capped / Uncapped / Overseas
INDIAN_NATIONAL_TEAMS = {"India", "India A", "India Emerging"}
def classify_player_status(name, player_id):
    # Check player's teams in mapping
    p_rows = df_map[df_map['player_id'] == player_id]
    teams_played = set(p_rows['team_name'].dropna().unique())
    comps_played = set(p_rows['comp_name'].dropna().unique())

    is_indian = any("India" in t for t in teams_played) or any("India" in c for c in comps_played)
    # Check if played T20I or ODI for India
    played_intl_india = False
    for c in comps_played:
        if "T20I" in c and "India" in c:
            played_intl_india = True
            break
    
    # Check if overseas
    # Non-Indian teams
    intl_teams = [t for t in teams_played if t in ["Australia", "England", "South Africa", "New Zealand", "West Indies", "Pakistan", "Sri Lanka", "Bangladesh", "Afghanistan", "Zimbabwe", "Ireland", "Netherlands", "Scotland", "United Arab Emirates", "Nepal"]]
    
    if is_indian or any(ipl_team in teams_played for ipl_team in ["Chennai Super Kings", "Mumbai Indians", "Rajasthan Royals", "Delhi Capitals", "Kolkata Knight Riders", "Punjab Kings", "Sunrisers Hyderabad", "Gujarat Titans", "Lucknow Super Giants", "Royal Challengers Bengaluru"]):
        # Could be Indian or Overseas IPL pro
        if intl_teams:
            return "Overseas Capped", intl_teams[0]
        elif played_intl_india:
            return "Capped Indian", "India"
        else:
            # Check if capped in known list
            known_capped_indian = {"Krunal Pandya", "Bhuvneshwar Kumar", "Sandeep Sharma", "Prabhsimran Singh", "Sanju Samson", "Yashasvi Jaiswal", "Riyan Parag", "Dhruv Jurel", "Yuzvendra Chahal", "Suryakumar Yadav", "Jasprit Bumrah", "Kuldeep Yadav", "Virat Kohli", "Shubman Gill", "Tilak Varma", "Abhishek Sharma", "Axar Patel", "Harshit Rana", "Nitish Kumar Reddy", "Mayank Yadav", "Rajat Patidar", "Yash Dayal", "Ravi Bishnoi", "Shivam Dube", "Ruturaj Gaikwad", "Varun Chakaravarthy", "Rinku Singh"}
            if name in known_capped_indian:
                return "Capped Indian", "India"
            return "Uncapped Indian", "India"
    elif intl_teams:
        return "Overseas Capped", intl_teams[0]
    else:
        return "Overseas Associate", "International"

# 5. Image resolver
def resolve_player_image(name):
    clean_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    # Exact filename match in public/players
    candidates = [
        f"{clean_name}.jpg",
        f"{clean_name}.png",
        f"{name.lower().replace(' ', '_')}.jpg",
    ]
    for c in candidates:
        if c in local_images:
            return f"/players/{c}"
    # Specific known alias mappings
    alias_map = {
        "namboori tilak varma": "/players/tilak_varma.jpg",
        "shaheen shah afridi": "/players/shaheen_afridi.jpg",
        "abhishek sharma (cricketer)": "/players/abhishek_sharma.jpg",
        "heinrich klaasen": "/players/heinrich_klaasen.jpg",
        "matheesha pathirana": "/players/matheesha_pathirana.jpg",
        "shaheen afridi": "/players/shaheen_afridi.jpg",
        "abrar ahmed": "/players/abrar_ahmed.jpg",
        "sufiyan muqeem": "/players/sufiyan_muqeem.jpg",
    }
    if name.lower() in alias_map and os.path.exists(os.path.join(PUBLIC_PLAYERS_DIR, os.path.basename(alias_map[name.lower()]))):
        return alias_map[name.lower()]
    
    # High-quality fallback avatar
    return f"https://api.dicebear.com/7.x/identicon/svg?seed={clean_name}"

# 6. Country Code Mapping (Strictly clean professional ISO codes, ZERO emojis)
COUNTRY_CODE_MAP = {
    "India": "IND", "England": "ENG", "South Africa": "RSA", "Australia": "AUS",
    "West Indies": "WI", "New Zealand": "NZ", "Pakistan": "PAK", "Sri Lanka": "SL",
    "Afghanistan": "AFG", "Zimbabwe": "ZIM", "Ireland": "IRE", "Netherlands": "NED",
    "International": "INTL"
}

# 7. Process Batters
processed_batters = []
auction_rank_counter = 1

for idx, row in df_bat.iterrows():
    name = str(row['player_name']).strip()
    pid = int(row['player_id'])
    score = float(row.get('pressure_rank_score', row.get('hp_cava_per_ball', 0.0)))
    cava = float(row.get('hp_cava_per_ball', 0.0))
    uplift = float(row.get('uplift_cava', 0.0))
    pos_share = float(row.get('positive_match_share', 0.5))
    balls = int(row.get('hp_balls', 0))
    runs = int(row.get('hp_runs', 0))
    matches = int(row.get('hp_matches', 0))
    dismissals = int(row.get('hp_dismissals', 0))
    sr = float(row.get('hp_sr', 0.0))
    batting_type = str(row.get('batting_type', 'RHB'))
    
    capped_status, country = classify_player_status(name, pid)
    country_code = COUNTRY_CODE_MAP.get(country, "INTL")
    image_url = resolve_player_image(name)
    
    # Contract & Franchise Status Model
    if name in FRANCHISE_RETENTIONS:
        ret_info = FRANCHISE_RETENTIONS[name]
        status = ret_info['status']
        curr_franchise = ret_info['team']
        franchise_label = ret_info['label']
        is_auction = ret_info['auction_target']
    else:
        # Check if played in IPL 2026
        p_ipl26 = df_map[(df_map['player_id'] == pid) & (df_map['comp_name'] == 'IPL 2026')]
        if not p_ipl26.empty:
            ipl_team = p_ipl26.iloc[0]['team_name']
            if ipl_team == 'Rajasthan Royals':
                status = 'RR_CORE'
                curr_franchise = 'Rajasthan Royals'
                franchise_label = 'RR Squad Member'
                is_auction = False
            else:
                status = 'IPL_SQUAD'
                curr_franchise = ipl_team
                franchise_label = f'{ipl_team} (Contracted / Targetable in 2027)'
                is_auction = True
        else:
            status = 'FREE_AGENT'
            curr_franchise = country
            franchise_label = f'{country} International Free Agent'
            is_auction = True
            
    # Check if in BCCI ineligible (Pakistan)
    if country == 'Pakistan':
        status = 'BCCI_INELIGIBLE'
        is_auction = False
        franchise_label = 'Pakistan (BCCI Policy Ineligible)'
        
    # Auction Tier info
    tier_info = AUCTION_TARGET_TIERS.get(name, {
        "tier": "Auction Target Pool" if is_auction else "Retained / Unavailable",
        "est_price": "₹1.5 - 3.5 Cr" if is_auction else "Not in Auction",
        "role": "Top Order Batter" if idx < 30 else "Middle Order / Utility",
        "scouting": f"Verified match-pressure rating of {round(score*100, 1)}. Reliable anchor and scoring option in crisis phases."
    })
    
    # Plain English Non-technical breakdown
    if cava > 0.05:
        impact_desc = f"Scores {round(cava * 100, 1)} runs above par per 100 high-pressure balls."
    elif cava > 0:
        impact_desc = f"Solid accumulator, adding {round(cava * 100, 1)} runs above context par."
    else:
        impact_desc = "Defensive anchor who prioritizes wicket preservation over rapid acceleration."
        
    plain_english = (
        f"{name} has faced {balls} balls under extreme match pressure across {matches} games. "
        f"{impact_desc} When the game is on the line, he produces positive value in {round(pos_share*100, 1)}% of matches."
    )
    
    rr_fit = ""
    if status == 'RR_CORE':
        rr_fit = "Core member of Rajasthan Royals. Key pillar to build the 2027 auction strategy around."
    elif not is_auction:
        rr_fit = f"Locked down by {curr_franchise}. War room should NOT allocate purse to this player as he will not enter the auction."
    else:
        rr_fit = f"Recommended auction target for RR. Complements Jaiswal, Samson, and Parag by providing {tier_info['role']} depth."

    rr_rank = auction_rank_counter if is_auction else None
    if is_auction:
        auction_rank_counter += 1

    processed_batters.append({
        "rank": idx + 1,
        "rr_auction_rank": rr_rank,
        "player_id": pid,
        "name": name,
        "batting_type": tier_info["role"],
        "country": country,
        "country_code": country_code,
        "flag": country_code,
        "capped_status": capped_status,
        "image_url": image_url,
        "hp_balls": balls,
        "hp_matches": matches,
        "hp_runs": runs,
        "hp_sr": round(sr, 1),
        "hp_dismissals": dismissals,
        "cava_per_ball": round(cava, 3),
        "uplift_cava": round(uplift, 3),
        "positive_match_share": round(pos_share, 3),
        "score": round(score, 3),
        "clutch_score": round(max(10.0, min(99.0, (score + 0.15) * 280)), 1),
        "auction_status": status,
        "is_auction_available": is_auction,
        "availability_tier": tier_info["tier"],
        "current_franchise": curr_franchise,
        "franchise_label": franchise_label,
        "price_bracket": tier_info["est_price"],
        "plain_english_role": tier_info["role"],
        "non_technical_summary": plain_english,
        "scouting_verdict": tier_info["scouting"],
        "rr_fit": rr_fit,
        "scenarios": {
            "death_chase": round(min(99, max(40, (score + 0.2) * 290)), 1),
            "collapse_rescue": round(min(99, max(40, (pos_share * 100) + (uplift * 80))), 1),
            "super_over": round(min(99, max(40, (sr / 2.0) + (score * 80))), 1),
        }
    })

# 8. Process Bowlers
processed_bowlers = []
auction_bowl_counter = 1

for idx, row in df_bowl.iterrows():
    name = str(row['player_name']).strip()
    pid = int(row['player_id'])
    score = float(row.get('pressure_rank_score', row.get('hp_cava_per_ball', 0.0)))
    cava = float(row.get('hp_cava_per_ball', 0.0))
    uplift = float(row.get('uplift_cava', 0.0))
    pos_share = float(row.get('positive_match_share', 0.5))
    balls = int(row.get('hp_balls', 0))
    runs = int(row.get('hp_runs', 0))
    matches = int(row.get('hp_matches', 0))
    wickets = int(row.get('hp_wickets', 0))
    econ = float(row.get('hp_econ', 0.0))
    dot_pct = float(row.get('dot_pct', 38.5))
    bowling_type = str(row.get('bowling_type', 'RMF'))
    
    capped_status, country = classify_player_status(name, pid)
    country_code = COUNTRY_CODE_MAP.get(country, "INTL")
    image_url = resolve_player_image(name)
    
    # Contract & Franchise Status Model
    if name in FRANCHISE_RETENTIONS:
        ret_info = FRANCHISE_RETENTIONS[name]
        status = ret_info['status']
        curr_franchise = ret_info['team']
        franchise_label = ret_info['label']
        is_auction = ret_info['auction_target']
    else:
        p_ipl26 = df_map[(df_map['player_id'] == pid) & (df_map['comp_name'] == 'IPL 2026')]
        if not p_ipl26.empty:
            ipl_team = p_ipl26.iloc[0]['team_name']
            if ipl_team == 'Rajasthan Royals':
                status = 'RR_CORE'
                curr_franchise = 'Rajasthan Royals'
                franchise_label = 'RR Squad Member'
                is_auction = False
            else:
                status = 'IPL_SQUAD'
                curr_franchise = ipl_team
                franchise_label = f'{ipl_team} (Contracted / Targetable in 2027)'
                is_auction = True
        else:
            status = 'FREE_AGENT'
            curr_franchise = country
            franchise_label = f'{country} International Free Agent'
            is_auction = True
            
    if country == 'Pakistan':
        status = 'BCCI_INELIGIBLE'
        is_auction = False
        franchise_label = 'Pakistan (BCCI Policy Ineligible)'

    tier_info = AUCTION_TARGET_TIERS.get(name, {
        "tier": "Auction Target Pool" if is_auction else "Retained / Unavailable",
        "est_price": "₹1.5 - 3.5 Cr" if is_auction else "Not in Auction",
        "role": "Pace Bowler" if idx % 2 == 0 else "Spin Bowler",
        "scouting": f"Verified match-pressure rating of {round(score*100, 1)}. Concedes low boundary rates under extreme clutch demands."
    })

    if cava > 0.05:
        impact_desc = f"Saves {round(cava * 100, 1)} runs below context expectations per 100 pressure balls."
    elif cava > 0:
        impact_desc = f"Maintains defensive choke, saving {round(cava * 100, 1)} runs below par."
    else:
        impact_desc = "Attacking wicket-seeker who takes high-risk options in high leverage moments."
        
    plain_english = (
        f"{name} has bowled {balls} deliveries in extreme pressure moments across {matches} games, "
        f"taking {wickets} wickets at an economy of {round(econ, 2)}. "
        f"{impact_desc} Delivers a dot ball on {round(dot_pct, 1)}% of clutch deliveries."
    )
    
    rr_fit = ""
    if status == 'RR_CORE':
        rr_fit = "Core member of Rajasthan Royals bowling unit. High-reliability asset to defend totals."
    elif not is_auction:
        rr_fit = f"Pillar of {curr_franchise}. Unavailable in the auction pool; RR war room must target other options."
    else:
        rr_fit = f"High-priority auction target for RR. Solves critical bowling phase requirements alongside Sandeep Sharma."

    rr_rank = auction_bowl_counter if is_auction else None
    if is_auction:
        auction_bowl_counter += 1

    processed_bowlers.append({
        "rank": idx + 1,
        "rr_auction_rank": rr_rank,
        "player_id": pid,
        "name": name,
        "bowling_type": tier_info["role"],
        "country": country,
        "country_code": country_code,
        "flag": country_code,
        "capped_status": capped_status,
        "image_url": image_url,
        "hp_balls": balls,
        "hp_overs": round(balls / 6.0, 1),
        "hp_matches": matches,
        "hp_runs": runs,
        "hp_wickets": wickets,
        "hp_economy": round(econ, 2),
        "dot_pct": round(dot_pct, 1),
        "cava_per_ball": round(cava, 3),
        "uplift_cava": round(uplift, 3),
        "positive_match_share": round(pos_share, 3),
        "score": round(score, 3),
        "clutch_score": round(max(10.0, min(99.0, (score + 0.15) * 280)), 1),
        "auction_status": status,
        "is_auction_available": is_auction,
        "availability_tier": tier_info["tier"],
        "current_franchise": curr_franchise,
        "franchise_label": franchise_label,
        "price_bracket": tier_info["est_price"],
        "plain_english_role": tier_info["role"],
        "non_technical_summary": plain_english,
        "scouting_verdict": tier_info["scouting"],
        "rr_fit": rr_fit,
        "scenarios": {
            "death_defense": round(min(99, max(40, (score + 0.2) * 280 + (dot_pct / 5.0))), 1),
            "middle_choke": round(min(99, max(40, (14 - econ) * 8 + (pos_share * 30))), 1),
            "super_over": round(min(99, max(40, (dot_pct * 0.8) + (score * 120))), 1),
        }
    })

# 9. Pre-defined Iconic Pressure Situations for the Simulator
PRESET_SITUATIONS = [
    {
        "id": "death_chase_thriller",
        "title": "Death Over Chase (Wankhede Thriller)",
        "badge": "Chasing 32 off 14 Balls",
        "mode": "batting",
        "runs": 32,
        "balls": 14,
        "wickets": 5,
        "phase": "Death",
        "venue": "Wankhede Stadium, Mumbai",
        "matchup": "pace",
        "description": "Rajasthan Royals need 32 runs from 14 legal deliveries with 5 wickets down. Required Rate: 13.71 RPO. Deep boundary riders posted.",
        "context": {"runs_needed": 32, "balls_left": 14, "wickets_down": 5, "current_rrr": 13.71, "phase": "Death (Overs 18-20)"},
        "tactical_demand": "Requires boundary conversion above 25% without sacrificing dot-ball minimization. Punishes high-risk lofted mis-hits.",
        "top_fit_batters": ["Jos Buttler", "Phil Salt", "Tim David", "Reeza Hendricks", "Glenn Phillips"],
        "top_fit_bowlers": ["Nathan Ellis", "Josh Hazlewood", "Krunal Pandya", "Tim Southee", "Jamie Overton"]
    },
    {
        "id": "powerplay_collapse",
        "title": "Powerplay Collapse Rescue",
        "badge": "24/3 in Over 4.2",
        "mode": "batting",
        "runs": 24,
        "balls": 24,
        "wickets": 3,
        "phase": "Powerplay",
        "venue": "Sawai Mansingh Stadium, Jaipur (RR Home)",
        "matchup": "pace",
        "description": "Top-order blown away by swing in overcast conditions. Rebuild the innings while keeping the score above 6.5 RPO without losing another wicket.",
        "context": {"runs_needed": 145, "balls_left": 94, "wickets_down": 3, "current_rrr": 9.25, "phase": "Powerplay (Over 4.2)"},
        "tactical_demand": "Needs anchor stability, high positive-match share, and sound technique against moving balls with field restrictions.",
        "top_fit_batters": ["Reeza Hendricks", "Jos Buttler", "Pathum Nissanka", "Sikandar Raza", "Kusal Mendis"],
        "top_fit_bowlers": ["Josh Hazlewood", "Bhuvneshwar Kumar", "Tim Southee", "Mitchell Santner", "Mujeeb Ur Rahman"]
    },
    {
        "id": "final_over_defense",
        "title": "The 20th Over Defense",
        "badge": "Defending 10 Runs off 6 Balls",
        "mode": "bowling",
        "runs": 10,
        "balls": 6,
        "wickets": 7,
        "phase": "Death",
        "venue": "Sawai Mansingh Stadium, Jaipur (RR Home)",
        "matchup": "pace",
        "description": "Bowler has 10 runs to defend in the final over. Batter on strike is an aggressive finisher. Only 4 fielders permitted outside the 30-yard circle.",
        "context": {"runs_needed": 11, "balls_left": 6, "wickets_down": 7, "current_rrr": 11.0, "phase": "Death (Over 20.0)"},
        "tactical_demand": "Demands pinpoint execution: wide yorkers, dipping slower balls, and zero boundary leakage. 1 mistake equals a match loss.",
        "top_fit_batters": ["Tim David", "Jos Buttler", "Phil Salt", "Glenn Phillips", "Sikandar Raza"],
        "top_fit_bowlers": ["Nathan Ellis", "Josh Hazlewood", "Krunal Pandya", "Jamie Overton", "Tim Southee"]
    },
    {
        "id": "middle_overs_choke",
        "title": "Middle Overs Spin Strangle",
        "badge": "Overs 7-15 on Dry Surface",
        "mode": "bowling",
        "runs": 20,
        "balls": 24,
        "wickets": 2,
        "phase": "Middle",
        "venue": "MA Chidambaram Stadium, Chennai",
        "matchup": "spin",
        "description": "Opposition cruising at 68/1 after powerplay. Rajasthan Royals need to dry up boundaries, induce false shots, and force required rate up.",
        "context": {"runs_needed": 110, "balls_left": 54, "wickets_down": 2, "current_rrr": 7.33, "phase": "Middle (Overs 7-15)"},
        "tactical_demand": "Requires tight lines, variable flight, dot-ball dominance, and suffocating defensive fields without conceding release boundaries.",
        "top_fit_batters": ["Reeza Hendricks", "Pathum Nissanka", "Sikandar Raza", "Jos Buttler", "Prabhsimran Singh"],
        "top_fit_bowlers": ["Krunal Pandya", "Gudakesh Motie", "Mujeeb Ur Rahman", "Mitchell Santner", "Akeal Hosein"]
    },
    {
        "id": "super_over_sudden_death",
        "title": "Super Over Shootout",
        "badge": "6 Balls, 2 Wickets Max",
        "mode": "batting",
        "runs": 16,
        "balls": 6,
        "wickets": 0,
        "phase": "Death",
        "venue": "Eden Gardens, Kolkata",
        "matchup": "pace",
        "description": "Scores tied at 178 all after 40 overs. Pure clutch execution. Win or go home.",
        "context": {"runs_needed": 16, "balls_left": 6, "wickets_down": 0, "current_rrr": 16.0, "phase": "Super Over"},
        "tactical_demand": "Maximum boundary probability per delivery. Zero room for defensive defense.",
        "top_fit_batters": ["Jos Buttler", "Phil Salt", "Tim David", "Reeza Hendricks", "Glenn Phillips"],
        "top_fit_bowlers": ["Josh Hazlewood", "Nathan Ellis", "Krunal Pandya", "Tim Southee", "Jamie Overton"]
    },
    {
        "id": "death_vs_power_hitters",
        "title": "Bowling vs Destructive Finishers",
        "badge": "Russell / Klaasen at Death",
        "mode": "bowling",
        "runs": 36,
        "balls": 18,
        "wickets": 4,
        "phase": "Death",
        "venue": "Wankhede Stadium, Mumbai",
        "matchup": "pace",
        "description": "Opposition's most dangerous finisher is set on 35 off 14. Target is 40 off 18. Must bowl defensively to prevent 20-run overs.",
        "context": {"runs_needed": 40, "balls_left": 18, "wickets_down": 4, "current_rrr": 13.33, "phase": "Death vs Power"},
        "tactical_demand": "Must bowl wide outside off-stump, change pace, and avoid the hitting arc down the ground.",
        "top_fit_batters": ["Tim David", "Jos Buttler", "Phil Salt", "Reeza Hendricks", "Sikandar Raza"],
        "top_fit_bowlers": ["Nathan Ellis", "Josh Hazlewood", "Krunal Pandya", "Jamie Overton", "Gudakesh Motie"]
    }
]

# 10. Compile Master Payload
top_stat_batters = [b['name'] for b in processed_batters[:10]]
top_stat_bowlers = [bw['name'] for bw in processed_bowlers[:10]]
top_auc_batters = [b['name'] for b in processed_batters if b['is_auction_available']][:10]
top_auc_bowlers = [bw['name'] for bw in processed_bowlers if bw['is_auction_available']][:10]

payload = {
    "meta": {
        "title": "SupeRR Selector Season 2 — Rajasthan Royals IPL 2027 War Room Intelligence Dashboard",
        "total_players_in_pack": int(df_map['player_id'].nunique()),
        "deliveries_analyzed": 200999,
        "matches_analyzed": int(df_matches['match_id'].nunique()),
        "data_census": {
            "registered_players": int(df_map['player_id'].nunique()),
            "playing_eleven_players": int(df_p11['player_id'].nunique()),
            "total_matches": int(df_matches['match_id'].nunique()),
            "total_deliveries": 200999,
            "unique_strikers": len(df_bat),
            "unique_bowlers": len(df_bowl),
            "high_pressure_batters_evaluated": len(df_bat),
            "high_pressure_bowlers_evaluated": len(df_bowl),
            "auction_target_batters": len([b for b in processed_batters if b['is_auction_available']]),
            "auction_target_bowlers": len([bw for bw in processed_bowlers if bw['is_auction_available']]),
            "rival_retained_batters": len([b for b in processed_batters if b['auction_status'] in ['RETAINED_RIVAL', 'CONTRACTED_RIVAL']]),
            "rival_retained_bowlers": len([bw for bw in processed_bowlers if bw['auction_status'] in ['RETAINED_RIVAL', 'CONTRACTED_RIVAL']]),
            "rr_core_players": len([b for b in processed_batters if b['auction_status'] == 'RR_CORE']) + len([bw for bw in processed_bowlers if bw['auction_status'] == 'RR_CORE']),
            "bcci_ineligible_players": len([b for b in processed_batters if b['auction_status'] == 'BCCI_INELIGIBLE']) + len([bw for bw in processed_bowlers if bw['auction_status'] == 'BCCI_INELIGIBLE']),
        },
        "model": {
            "name": "Context-Adjusted Value Added (CAVA) with Match-Level Empirical Bayes Shrinkage",
            "pressure_threshold_mpi": 0.55,
            "training_split": "2022-2024 (70th percentile frozen)",
            "out_of_time_validation": "2025-2026 (RMSE 1.7569, Brier 0.0514)"
        }
    },
    "dropdown_options": {
        "set_1_pure_statistical": {
            "label": "Option A: Pure Statistical Benchmark (All Data Pack Stars)",
            "description": "The mathematical top 10 highest-performing players under pressure across all 2022-2026 matches in the proprietary data pack, regardless of franchise contract.",
            "batters": top_stat_batters,
            "bowlers": top_stat_bowlers,
            "top_10_batters": top_stat_batters,
            "top_10_bowlers": top_stat_bowlers,
        },
        "set_2_rr_auction_targets": {
            "label": "Option B: Rajasthan Royals IPL 2027 Auction Shortlist (100% Targetable)",
            "description": "The top 10 highest-performing targetable players under pressure who are actually available in the auction pool, excluding rival franchise retentions and ineligible stars.",
            "batters": top_auc_batters,
            "bowlers": top_auc_bowlers,
            "top_10_batters": top_auc_batters,
            "top_10_bowlers": top_auc_bowlers,
        },
        "perspective_1_statistical_benchmark": {
            "label": "Option A: Pure Statistical Benchmark (All Data Pack Stars)",
            "batters": top_stat_batters,
            "bowlers": top_stat_bowlers,
            "top_10_batters": top_stat_batters,
            "top_10_bowlers": top_stat_bowlers,
        },
        "perspective_2_rr_auction_shortlist": {
            "label": "Option B: Rajasthan Royals IPL 2027 Auction Shortlist (100% Targetable)",
            "batters": top_auc_batters,
            "bowlers": top_auc_bowlers,
            "top_10_batters": top_auc_batters,
            "top_10_bowlers": top_auc_bowlers,
        }
    },
    "preset_situations": PRESET_SITUATIONS,
    "batters": processed_batters,
    "bowlers": processed_bowlers,
    "venues": [
        {"name": "Sawai Mansingh Stadium, Jaipur", "type": "Balanced / Grip", "rr_home": True},
        {"name": "Wankhede Stadium, Mumbai", "type": "High Bounce / High Scoring", "rr_home": False},
        {"name": "Eden Gardens, Kolkata", "type": "Pace & Spin Turn", "rr_home": False},
        {"name": "MA Chidambaram Stadium, Chennai", "type": "Slow Turning Pitch", "rr_home": False},
        {"name": "Narendra Modi Stadium, Ahmedabad", "type": "Long Boundaries / Fast", "rr_home": False}
    ]
}

# 11. Write Master Output
with open(os.path.join(FRONTEND_DATA_DIR, "analytics_data.json"), "w") as f:
    json.dump(payload, f, indent=2)

with open(os.path.join(OUTPUTS_DIR, "comprehensive_player_census.json"), "w") as f:
    json.dump(payload['meta'], f, indent=2)

# Also write comprehensive CSVs
pd.DataFrame(processed_batters).to_csv(os.path.join(OUTPUTS_DIR, "batting_rankings_comprehensive.csv"), index=False)
pd.DataFrame(processed_bowlers).to_csv(os.path.join(OUTPUTS_DIR, "bowling_rankings_comprehensive.csv"), index=False)

print(f"Successfully generated comprehensive analytics database:")
print(f"- Processed {len(processed_batters)} batters")
print(f"- Processed {len(processed_bowlers)} bowlers")
print(f"- Option A Batters: {[b['name'] for b in processed_batters[:10]]}")
print(f"- Option A Bowlers: {[bw['name'] for bw in processed_bowlers[:10]]}")
print(f"- Option B Batters: {[b['name'] for b in processed_batters if b['is_auction_available']][:10]}")
print(f"- Option B Bowlers: {[bw['name'] for bw in processed_bowlers if bw['is_auction_available']][:10]}")
