import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Set broadcast-grade page layout
st.set_page_config(
    page_title="SupeRR Selector | RR IPL 2027 Auction War Room",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling (IPL Broadcast / Rajasthan Royals Theme)
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #070B14 0%, #0F172A 50%, #0A1128 100%);
        color: #F8FAFC;
    }
    
    /* Top Banner */
    .rr-banner {
        background: linear-gradient(90deg, #EA1A85 0%, #254AA5 70%, #0A1128 100%);
        padding: 24px 32px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(234, 26, 133, 0.25);
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .rr-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .rr-subtitle {
        font-size: 1.05rem;
        color: #E2E8F0;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Player Cards */
    .player-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .player-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
        border-color: #EA1A85;
    }
    .card-available {
        border-left: 6px solid #10B981 !important;
    }
    .card-retained {
        border-left: 6px solid #EF4444 !important;
    }
    .card-restricted {
        border-left: 6px solid #F59E0B !important;
    }
    
    /* Badges */
    .badge-available {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-retained {
        background: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-restricted {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    
    /* Stat Chips */
    .stat-chip {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 10px;
        padding: 10px 14px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-val {
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .stat-lbl {
        font-size: 0.72rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    /* Highlight text */
    .text-pink { color: #EA1A85; font-weight: 700; }
    .text-blue { color: #38BDF8; font-weight: 700; }
    .text-gold { color: #FBBF24; font-weight: 700; }
    
    /* Section Headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 15px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_all_data():
    bat = pd.read_csv('outputs/batting_rankings.csv')
    bowl = pd.read_csv('outputs/bowling_rankings.csv')
    with open('outputs/enriched_player_profiles.json', 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    with open('outputs/player_evidence_cards.json', 'r', encoding='utf-8') as f:
        evidence = json.load(f)
    with open('outputs/RR_role_fit.json', 'r', encoding='utf-8') as f:
        rr_fit = json.load(f)
    with open('outputs/pressure_config.json', 'r', encoding='utf-8') as f:
        p_cfg = json.load(f)
    with open('outputs/validation_metrics.json', 'r', encoding='utf-8') as f:
        val_met = json.load(f)
    return bat, bowl, profiles, evidence, rr_fit, p_cfg, val_met

bat_df, bowl_df, enriched_profiles, evidence_cards, rr_role_fit, pressure_cfg, val_metrics = load_all_data()

# Sidebar Setup
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/1200px-Rajasthan_Royals_Logo.svg.png", width=120)
st.sidebar.markdown("### 👑 RAJASTHAN ROYALS")
st.sidebar.markdown("**IPL 2027 Auction War Room**\nPressure Intelligence Engine v2.4")

nav_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "📋 Official Unstop Submission Hub",
        "🎯 RR 2027 Auction War Room",
        "🃏 Professional Player Cards Gallery",
        "⚔️ Scout Head-to-Head Compare",
        "⚡ Match Pressure & Turning Points",
        "🛡️ Model Transparency & Audit"
    ]
)

st.sidebar.markdown("---")
filter_mode = st.sidebar.selectbox(
    "Availability Filter",
    ["Show All Candidates (Unstop Submission)", "RR Realistic Auction Targets Only", "Retained / Ineligible Only"]
)

st.sidebar.caption("Data: 2022-2026 | 200,999 Deliveries | 867 Matches\nOut-of-Time Validated | Non-Leaking Pre-Ball State")

# Top Header Banner across all pages
st.markdown("""
<div class="rr-banner">
    <div>
        <h1 class="rr-title">SUPERR SELECTOR: ROUND 1</h1>
        <div class="rr-subtitle">Identify the Most Reliable Players Under Pressure — Rajasthan Royals IPL 2027 Strategy</div>
    </div>
    <div style="text-align: right; background: rgba(0,0,0,0.25); padding: 10px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);">
        <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Submission Status</div>
        <div style="font-size: 1.1rem; font-weight: 800; color: #34D399;">✓ UNSTOP READY</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------
# PAGE 1: OFFICIAL UNSTOP SUBMISSION HUB
# --------------------------------------------------------------------------------------------------
if nav_choice == "📋 Official Unstop Submission Hub":
    st.markdown('<div class="section-title">📋 Official Unstop Dropdown Selections (Rank 1 to 10)</div>', unsafe_allow_html=True)
    st.markdown("Use these exact ordered selections in the Unstop dropdown fields (**Batsman 1–10** and **Bowler 1–10**). Every player is mathematically verified from historical match data with zero duplicate selections.")

    tab_bat_sub, tab_bowl_sub = st.tabs(["🏏 Top 10 Batters (Batsman 1–10)", "🎯 Top 10 Bowlers (Bowler 1–10)"])

    with tab_bat_sub:
        st.info("💡 **Unstop Instruction**: Select each player in the exact order below for **Batsman 1** through **Batsman 10**.")
        for idx, row in bat_df.head(10).iterrows():
            pname = row['player_name']
            p_meta = enriched_profiles['batters'].get(pname, {})
            avail_badge = f"<span class='badge-available'>🎯 RR Auction Target</span>" if p_meta.get('is_auction_available') else f"<span class='badge-retained'>🔒 Retained: {p_meta.get('current_franchise', 'Franchise Core')}</span>"
            
            c1, c2, c3 = st.columns([1, 4, 2])
            with c1:
                st.markdown(f"<div style='font-size: 2rem; font-weight: 900; color: #EA1A85; text-align: center; padding-top: 10px;'>#{int(row['rank'])}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='padding-top: 4px;'>
                    <span style='font-size: 1.3rem; font-weight: 800; color: #FFFFFF;'>{pname}</span> {p_meta.get('flag', '')} 
                    &nbsp;{avail_badge}
                    <div style='font-size: 0.85rem; color: #94A3B8; margin-top: 2px;'>{p_meta.get('plain_english_role', 'Specialist')} | Hand: {row['batting_type']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style='display: flex; gap: 8px; justify-content: flex-end;'>
                    <div class='stat-chip'><div class='stat-val text-pink'>{row['hp_sr']:.1f}</div><div class='stat-lbl'>Pressure SR</div></div>
                    <div class='stat-chip'><div class='stat-val text-blue'>{row['hp_balls']}</div><div class='stat-lbl'>Balls Faced</div></div>
                    <div class='stat-chip'><div class='stat-val text-gold'>{row['pressure_rank_score']:.4f}</div><div class='stat-lbl'>Score</div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 6px 0 14px 0;'/>", unsafe_allow_html=True)

    with tab_bowl_sub:
        st.info("💡 **Unstop Instruction**: Select each player in the exact order below for **Bowler 1** through **Bowler 10**.")
        for idx, row in bowl_df.head(10).iterrows():
            pname = row['player_name']
            p_meta = enriched_profiles['bowlers'].get(pname, {})
            avail_badge = f"<span class='badge-available'>🎯 RR Auction Target</span>" if p_meta.get('is_auction_available') else (
                f"<span class='badge-restricted'>🚫 {p_meta.get('auction_status')}</span>" if "BCCI" in p_meta.get('auction_status', '') else f"<span class='badge-retained'>🔒 Retained: {p_meta.get('current_franchise', 'Franchise Core')}</span>"
            )
            
            c1, c2, c3 = st.columns([1, 4, 2])
            with c1:
                st.markdown(f"<div style='font-size: 2rem; font-weight: 900; color: #38BDF8; text-align: center; padding-top: 10px;'>#{int(row['rank'])}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='padding-top: 4px;'>
                    <span style='font-size: 1.3rem; font-weight: 800; color: #FFFFFF;'>{pname}</span> {p_meta.get('flag', '')} 
                    &nbsp;{avail_badge}
                    <div style='font-size: 0.85rem; color: #94A3B8; margin-top: 2px;'>{p_meta.get('plain_english_role', 'Specialist')} | Style: {row['bowling_type']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style='display: flex; gap: 8px; justify-content: flex-end;'>
                    <div class='stat-chip'><div class='stat-val text-blue'>{row['hp_econ']:.2f}</div><div class='stat-lbl'>Pressure Econ</div></div>
                    <div class='stat-chip'><div class='stat-val text-pink'>{row['hp_wickets']}</div><div class='stat-lbl'>Wickets</div></div>
                    <div class='stat-chip'><div class='stat-val text-gold'>{row['pressure_rank_score']:.4f}</div><div class='stat-lbl'>Score</div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 6px 0 14px 0;'/>", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------
# PAGE 2: RR 2027 AUCTION WAR ROOM
# --------------------------------------------------------------------------------------------------
elif nav_choice == "🎯 RR 2027 Auction War Room":
    st.markdown('<div class="section-title">🎯 Rajasthan Royals IPL 2027 Auction Strategy & Availability Matrix</div>', unsafe_allow_html=True)
    st.markdown("Separating the **Academic Rankings** from **Real-World Auction Feasibility**. While players like Suryakumar Yadav and Jasprit Bumrah top the raw statistical tables, they are retained by their respective franchises and unavailable in the auction. Below is Rajasthan Royals' actionable acquisition roadmap.")

    # Top Level Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Prime RR Batting Target", "Jos Buttler / Tristan Stubbs", "Top Priority Auction Targets")
    m2.metric("Prime RR Bowling Target", "Josh Hazlewood / Pathirana", "High-Impact Pace Spearheads")
    m3.metric("Key Domestic Target", "Krunal Pandya", "6.03 Econ in Pressure Matches")
    m4.metric("Retention Choke Benchmark", "Suryakumar & Narine", "Untouchable Franchise Pillars")

    st.markdown("---")

    # Three Tier Breakdown
    t1, t2, t3 = st.tabs(["🟢 Tier 1: Prime RR Auction Targets (Available)", "🔒 Tier 2: Retained Franchise Pillars (Unavailable)", "🚫 Tier 3: BCCI Policy Ineligible"])

    with t1:
        st.subheader("Actionable Targets for Rajasthan Royals' IPL 2027 Auction Table")
        st.markdown("These players combine **proven statistical reliability under pressure** with **realistic auction or trade availability**.")
        
        # Grid layout for available targets
        available_bats = [p for p, data in enriched_profiles['batters'].items() if data['is_auction_available']]
        available_bowls = [p for p, data in enriched_profiles['bowlers'].items() if data['is_auction_available']]

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🏏 Available Batting Enforcers & Finishers")
            for pname in available_bats:
                meta = enriched_profiles['batters'][pname]
                b_row = bat_df[bat_df['player_name'] == pname].iloc[0]
                st.markdown(f"""
                <div class="player-card card-available">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">{pname}</span> {meta['flag']}
                            <div style="font-size: 0.85rem; color: #38BDF8; font-weight: 600;">{meta['plain_english_role']}</div>
                        </div>
                        <span class="badge-available">Auction Target</span>
                    </div>
                    <p style="font-size: 0.9rem; color: #E2E8F0; margin: 10px 0 6px 0;"><strong>Why RR Should Buy:</strong> {meta['non_technical_summary']}</p>
                    <p style="font-size: 0.85rem; color: #F472B6; margin: 0 0 10px 0;"><strong>Tactical Role in RR:</strong> {meta['rr_fit']}</p>
                    <div style="display: flex; gap: 8px;">
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-pink">{b_row['hp_sr']:.1f}</div><div class="stat-lbl">Pressure SR</div></div>
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-blue">+{b_row['uplift_cava']:.3f}</div><div class="stat-lbl">Pressure Uplift</div></div>
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-gold">{b_row['hp_balls']}</div><div class="stat-lbl">Sample Balls</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown("#### 🎯 Available Lockdown Bowlers & Match Winners")
            for pname in available_bowls:
                meta = enriched_profiles['bowlers'][pname]
                bw_row = bowl_df[bowl_df['player_name'] == pname].iloc[0]
                st.markdown(f"""
                <div class="player-card card-available">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">{pname}</span> {meta['flag']}
                            <div style="font-size: 0.85rem; color: #38BDF8; font-weight: 600;">{meta['plain_english_role']}</div>
                        </div>
                        <span class="badge-available">Auction Target</span>
                    </div>
                    <p style="font-size: 0.9rem; color: #E2E8F0; margin: 10px 0 6px 0;"><strong>Why RR Should Buy:</strong> {meta['non_technical_summary']}</p>
                    <p style="font-size: 0.85rem; color: #F472B6; margin: 0 0 10px 0;"><strong>Tactical Role in RR:</strong> {meta['rr_fit']}</p>
                    <div style="display: flex; gap: 8px;">
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-blue">{bw_row['hp_econ']:.2f}</div><div class="stat-lbl">Pressure Econ</div></div>
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-pink">{bw_row['hp_wickets']}</div><div class="stat-lbl">Wickets</div></div>
                        <div class="stat-chip" style="flex: 1;"><div class="stat-val text-gold">+{bw_row['uplift_cava']:.3f}</div><div class="stat-lbl">Pressure Uplift</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with t2:
        st.subheader("🔒 Retained Franchise Pillars (Unattainable in Auction)")
        st.markdown("These players objectively perform at an elite level under pressure, but are **locked into long-term retentions** by their home franchises. We keep them in our primary rankings because the official Unstop prompt asks for the *best-performing players under pressure from the dataset*, but RR should not waste scouting resources pursuing them in the auction.")
        
        retained_bats = [p for p, data in enriched_profiles['batters'].items() if not data['is_auction_available'] and 'BCCI' not in data.get('auction_status', '')]
        retained_bowls = [p for p, data in enriched_profiles['bowlers'].items() if not data['is_auction_available'] and 'BCCI' not in data.get('auction_status', '')]

        for pname in (retained_bats + retained_bowls):
            meta = enriched_profiles['batters'].get(pname, enriched_profiles['bowlers'].get(pname, {}))
            st.markdown(f"""
            <div class="player-card card-retained">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">{pname}</span> {meta.get('flag', '')}
                        <span style="color: #94A3B8; font-size: 0.85rem;"> — {meta.get('current_franchise', 'Core Pillar')}</span>
                    </div>
                    <span class="badge-retained">Retained / Unavailable</span>
                </div>
                <div style="margin-top: 6px; font-size: 0.88rem; color: #CBD5E1;">
                    <strong>Scouting Verdict:</strong> {meta.get('scouting_verdict', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with t3:
        st.subheader("🚫 BCCI Policy Restricted (Pakistani Nationals)")
        st.markdown("Per BCCI administrative policy, Pakistani players do not participate in the IPL auction. They appear in our raw tables solely because the dataset includes all international T20 matches since 2022.")
        
        restricted_bowls = [p for p, data in enriched_profiles['bowlers'].items() if 'BCCI' in data.get('auction_status', '')]
        for pname in restricted_bowls:
            meta = enriched_profiles['bowlers'][pname]
            st.markdown(f"""
            <div class="player-card card-restricted">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">{pname}</span> {meta.get('flag', '')}
                        <span style="color: #94A3B8; font-size: 0.85rem;"> — Pakistan National Team</span>
                    </div>
                    <span class="badge-restricted">BCCI Ineligible</span>
                </div>
                <div style="margin-top: 6px; font-size: 0.88rem; color: #CBD5E1;">
                    <strong>Status:</strong> Ineligible for IPL auction due to BCCI regulations.
                </div>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------
# PAGE 3: PROFESSIONAL PLAYER CARDS GALLERY
# --------------------------------------------------------------------------------------------------
elif nav_choice == "🃏 Professional Player Cards Gallery":
    st.markdown('<div class="section-title">🃏 Professional Player Evidence Cards Gallery</div>', unsafe_allow_html=True)
    st.markdown("Comprehensive, non-technical player dossiers designed for scouts, analysts, and franchise leadership.")

    role_filter = st.radio("Select Role Category:", ["Batters", "Bowlers"], horizontal=True)

    if role_filter == "Batters":
        target_dict = enriched_profiles['batters']
        for pname, meta in target_dict.items():
            if filter_mode == "RR Realistic Auction Targets Only" and not meta['is_auction_available']:
                continue
            if filter_mode == "Retained / Ineligible Only" and meta['is_auction_available']:
                continue
                
            b_row = bat_df[bat_df['player_name'] == pname].iloc[0]
            card_class = "card-available" if meta['is_auction_available'] else "card-retained"
            avail_tag = "<span class='badge-available'>Auction Target</span>" if meta['is_auction_available'] else f"<span class='badge-retained'>{meta['current_franchise']}</span>"
            
            st.markdown(f"""
            <div class="player-card {card_class}">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <img src="{meta['image_url']}" style="width: 85px; height: 85px; border-radius: 50%; object-fit: cover; border: 3px solid #EA1A85; background: #1E293B;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/847/847969.png'"/>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.4rem; font-weight: 900; color: #FFFFFF;">{pname}</span> 
                                <span style="font-size: 1.1rem;">{meta['flag']}</span> &nbsp;{avail_tag}
                                <div style="font-size: 0.88rem; color: #38BDF8; font-weight: 700; margin-top: 2px;">{meta['plain_english_role']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Clutch Rating</div>
                                <div style="font-size: 1.8rem; font-weight: 900; color: #FBBF24;">{meta['clutch_score']}<span style="font-size: 0.9rem; color: #64748B;">/100</span></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="margin: 14px 0 10px 0; font-size: 0.95rem; line-height: 1.5; color: #F1F5F9;">
                    <strong>Why They Win Games:</strong> {meta['non_technical_summary']}
                </div>
                <div style="font-size: 0.88rem; color: #F472B6; margin-bottom: 14px;">
                    <strong>RR Scouting Verdict:</strong> {meta['scouting_verdict']}
                </div>
                <div style="display: flex; gap: 10px;">
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-pink">{b_row['hp_sr']:.1f}</div><div class="stat-lbl">Pressure Strike Rate</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-blue">+{b_row['hp_cava_per_ball']:.3f}</div><div class="stat-lbl">Runs Added / Ball</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-gold">+{b_row['uplift_cava']:.3f}</div><div class="stat-lbl">Pressure Uplift</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val" style="color: #34D399;">{b_row['positive_match_share']*100:.0f}%</div><div class="stat-lbl">Positive Match %</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        target_dict = enriched_profiles['bowlers']
        for pname, meta in target_dict.items():
            if filter_mode == "RR Realistic Auction Targets Only" and not meta['is_auction_available']:
                continue
            if filter_mode == "Retained / Ineligible Only" and meta['is_auction_available']:
                continue

            bw_row = bowl_df[bowl_df['player_name'] == pname].iloc[0]
            card_class = "card-available" if meta['is_auction_available'] else ("card-restricted" if "BCCI" in meta.get('auction_status', '') else "card-retained")
            avail_tag = "<span class='badge-available'>Auction Target</span>" if meta['is_auction_available'] else (
                "<span class='badge-restricted'>BCCI Restricted</span>" if "BCCI" in meta.get('auction_status', '') else f"<span class='badge-retained'>{meta['current_franchise']}</span>"
            )

            st.markdown(f"""
            <div class="player-card {card_class}">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <img src="{meta['image_url']}" style="width: 85px; height: 85px; border-radius: 50%; object-fit: cover; border: 3px solid #254AA5; background: #1E293B;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/847/847969.png'"/>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.4rem; font-weight: 900; color: #FFFFFF;">{pname}</span> 
                                <span style="font-size: 1.1rem;">{meta['flag']}</span> &nbsp;{avail_tag}
                                <div style="font-size: 0.88rem; color: #38BDF8; font-weight: 700; margin-top: 2px;">{meta['plain_english_role']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Clutch Rating</div>
                                <div style="font-size: 1.8rem; font-weight: 900; color: #FBBF24;">{meta['clutch_score']}<span style="font-size: 0.9rem; color: #64748B;">/100</span></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="margin: 14px 0 10px 0; font-size: 0.95rem; line-height: 1.5; color: #F1F5F9;">
                    <strong>Why They Win Games:</strong> {meta['non_technical_summary']}
                </div>
                <div style="font-size: 0.88rem; color: #38BDF8; margin-bottom: 14px;">
                    <strong>RR Scouting Verdict:</strong> {meta['scouting_verdict']}
                </div>
                <div style="display: flex; gap: 10px;">
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-blue">{bw_row['hp_econ']:.2f}</div><div class="stat-lbl">Pressure Economy</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-pink">{bw_row['hp_wickets']}</div><div class="stat-lbl">Pressure Wickets</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val text-gold">+{bw_row['uplift_cava']:.3f}</div><div class="stat-lbl">Pressure Uplift</div></div>
                    <div class="stat-chip" style="flex: 1;"><div class="stat-val" style="color: #34D399;">{bw_row['positive_match_share']*100:.0f}%</div><div class="stat-lbl">Positive Match %</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------
# PAGE 4: SCOUT HEAD-TO-HEAD COMPARE
# --------------------------------------------------------------------------------------------------
elif nav_choice == "⚔️ Scout Head-to-Head Compare":
    st.markdown('<div class="section-title">⚔️ Scout Head-to-Head Pressure Comparison</div>', unsafe_allow_html=True)
    st.markdown("Side-by-side comparison for coaching staff and analysts evaluating tactical choices.")

    role_cmp = st.radio("Comparison Category:", ["Batters", "Bowlers"], horizontal=True)

    if role_cmp == "Batters":
        b_names = bat_df['player_name'].head(20).tolist()
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Select Player 1 (Left):", b_names, index=0)
        with c2:
            p2_name = st.selectbox("Select Player 2 (Right):", b_names, index=1)

        p1_row = bat_df[bat_df['player_name'] == p1_name].iloc[0]
        p2_row = bat_df[bat_df['player_name'] == p2_name].iloc[0]
        p1_meta = enriched_profiles['batters'].get(p1_name, {})
        p2_meta = enriched_profiles['batters'].get(p2_name, {})

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(f"""
            <div class="player-card">
                <h3 style="color:#EA1A85; margin:0;">{p1_name} {p1_meta.get('flag', '')}</h3>
                <p style="color:#38BDF8; font-weight:600;">{p1_meta.get('plain_english_role', '')}</p>
                <p>{p1_meta.get('non_technical_summary', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown(f"""
            <div class="player-card">
                <h3 style="color:#254AA5; margin:0;">{p2_name} {p2_meta.get('flag', '')}</h3>
                <p style="color:#38BDF8; font-weight:600;">{p2_meta.get('plain_english_role', '')}</p>
                <p>{p2_meta.get('non_technical_summary', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        # Radar Comparison
        radar_categories = ['Strike Rate', 'Runs Added (CAVA)', 'Pressure Uplift', 'Consistency %', 'Experience (Balls)']
        p1_vals = [
            min(100, (p1_row['hp_sr'] / 185) * 100),
            min(100, max(0, (p1_row['hp_cava_per_ball'] / 0.45) * 100)),
            min(100, max(0, (p1_row['uplift_cava'] / 0.35) * 100)),
            p1_row['positive_match_share'] * 100,
            min(100, (p1_row['hp_balls'] / 700) * 100)
        ]
        p2_vals = [
            min(100, (p2_row['hp_sr'] / 185) * 100),
            min(100, max(0, (p2_row['hp_cava_per_ball'] / 0.45) * 100)),
            min(100, max(0, (p2_row['uplift_cava'] / 0.35) * 100)),
            p2_row['positive_match_share'] * 100,
            min(100, (p2_row['hp_balls'] / 700) * 100)
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=p1_vals, theta=radar_categories, fill='toself', name=p1_name, line_color='#EA1A85'))
        fig_radar.add_trace(go.Scatterpolar(r=p2_vals, theta=radar_categories, fill='toself', name=p2_name, line_color='#38BDF8'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC')
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    else:
        bw_names = bowl_df['player_name'].head(20).tolist()
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Select Bowler 1 (Left):", bw_names, index=0)
        with c2:
            p2_name = st.selectbox("Select Bowler 2 (Right):", bw_names, index=1)

        p1_row = bowl_df[bowl_df['player_name'] == p1_name].iloc[0]
        p2_row = bowl_df[bowl_df['player_name'] == p2_name].iloc[0]
        p1_meta = enriched_profiles['bowlers'].get(p1_name, {})
        p2_meta = enriched_profiles['bowlers'].get(p2_name, {})

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(f"""
            <div class="player-card">
                <h3 style="color:#38BDF8; margin:0;">{p1_name} {p1_meta.get('flag', '')}</h3>
                <p style="color:#FBBF24; font-weight:600;">{p1_meta.get('plain_english_role', '')}</p>
                <p>{p1_meta.get('non_technical_summary', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown(f"""
            <div class="player-card">
                <h3 style="color:#EA1A85; margin:0;">{p2_name} {p2_meta.get('flag', '')}</h3>
                <p style="color:#FBBF24; font-weight:600;">{p2_meta.get('plain_english_role', '')}</p>
                <p>{p2_meta.get('non_technical_summary', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        radar_categories = ['Run Containment', 'Wicket Strike Power', 'Runs Saved (CAVA)', 'Pressure Uplift', 'Consistency %']
        p1_vals = [
            max(0, min(100, (12.0 - p1_row['hp_econ']) / 6.5 * 100)),
            min(100, (p1_row['hp_wickets'] / 45) * 100),
            min(100, max(0, (p1_row['hp_cava_per_ball'] / 0.50) * 100)),
            min(100, max(0, (p1_row['uplift_cava'] / 0.35) * 100)),
            p1_row['positive_match_share'] * 100
        ]
        p2_vals = [
            max(0, min(100, (12.0 - p2_row['hp_econ']) / 6.5 * 100)),
            min(100, (p2_row['hp_wickets'] / 45) * 100),
            min(100, max(0, (p2_row['hp_cava_per_ball'] / 0.50) * 100)),
            min(100, max(0, (p2_row['uplift_cava'] / 0.35) * 100)),
            p2_row['positive_match_share'] * 100
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=p1_vals, theta=radar_categories, fill='toself', name=p1_name, line_color='#38BDF8'))
        fig_radar.add_trace(go.Scatterpolar(r=p2_vals, theta=radar_categories, fill='toself', name=p2_name, line_color='#EA1A85'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC')
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# --------------------------------------------------------------------------------------------------
# PAGE 5: MATCH PRESSURE & TURNING POINTS
# --------------------------------------------------------------------------------------------------
elif nav_choice == "⚡ Match Pressure & Turning Points":
    st.markdown('<div class="section-title">⚡ Match Pressure & Win Probability Timeline Explorer</div>', unsafe_allow_html=True)
    st.markdown("Inspect any match ball-by-ball to visualize match turning points, win probability swings, and high-pressure moments.")

    df_sample = pd.read_parquet('data_processed/fact_delivery_cava.parquet')
    matches_meta = df_sample[['match_id', 'match_date', 'comp_name', 'year']].drop_duplicates().sort_values('match_date', ascending=False)
    
    match_dict = {f"{r['match_date']} | {r['comp_name']} (Match #{r['match_id']})": r['match_id'] for _, r in matches_meta.head(100).iterrows()}
    chosen_match_label = st.selectbox("Choose Match:", list(match_dict.keys()))
    mid = match_dict[chosen_match_label]

    m_deliveries = df_sample[df_sample['match_id'] == mid].sort_values(['innings', 'overid', 'over_ball_num'])

    st.write(f"Showing **{len(m_deliveries)} deliveries** for Match ID: `{mid}`")

    # MPI Timeline
    fig_mpi = px.line(
        m_deliveries,
        x='innings_ball_num',
        y='match_pressure_index',
        color='innings',
        hover_data=['overid', 'over_ball_num', 'striker_name', 'bowler_name', 'runs', 'is_wicket'],
        title=f"Match Pressure Index (MPI) Progression — Match #{mid}",
        labels={'innings_ball_num': 'Ball in Innings', 'match_pressure_index': 'Pressure Index (MPI)'}
    )
    fig_mpi.add_hline(y=pressure_cfg['frozen_high_pressure_threshold'], line_dash="dash", line_color="#EF4444", annotation_text="High Pressure Threshold (0.55)")
    fig_mpi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
    st.plotly_chart(fig_mpi, use_container_width=True)

    # Chase Win Probability Curve
    inn2_m = m_deliveries[m_deliveries['innings'] == 2]
    if len(inn2_m) > 0 and 'win_probability' in inn2_m:
        fig_wp = px.line(
            inn2_m,
            x='innings_ball_num',
            y='win_probability',
            hover_data=['overid', 'over_ball_num', 'runs_required', 'legal_balls_remaining', 'wickets_in_hand', 'striker_name', 'bowler_name'],
            title="Innings 2: Win Probability Progression (Chasing Team)",
            labels={'innings_ball_num': 'Ball in Chase', 'win_probability': 'Chasing Team Win Probability'}
        )
        fig_wp.update_layout(yaxis_range=[0, 1], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
        st.plotly_chart(fig_wp, use_container_width=True)

# --------------------------------------------------------------------------------------------------
# PAGE 6: MODEL TRANSPARENCY & AUDIT
# --------------------------------------------------------------------------------------------------
elif nav_choice == "🛡️ Model Transparency & Audit":
    st.markdown('<div class="section-title">🛡️ Data Engineering & Model Calibration Audit</div>', unsafe_allow_html=True)
    st.markdown("Full transparency report ensuring zero data leakage, chronological rolling-origin splits, and complete auditability.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches in Pack", "883 Matches", "867 with BBB, 16 Abandoned")
    col2.metric("Deliveries Modeled", "200,999 Balls", "100% Pre-Ball Reconstructed")
    col3.metric("Wicket Brier Score", f"{val_metrics['expected_wicket_metrics']['brier_score']:.4f}", "Out-of-Time Test Set")
    col4.metric("Score Reconciliation", "100.0%", "Zero Scoring Discrepancies")

    st.markdown("---")
    c_a, c_b = st.columns(2)
    with c_a:
        st.subheader("Model Evaluation Strategy")
        st.markdown("""
        - **Training Split**: 2022–2024 (512 matches, 120,248 deliveries).
        - **Out-of-Time Test Split**: 2025–2026 (355 matches, 80,751 deliveries).
        - **Leakage Prevention**: Every feature is strictly calculated up to delivery $t-1$. Venue par used for Innings 1 instead of match final score.
        - **Expected Runs RMSE**: `1.7569`
        - **Expected Wickets AUC**: `0.5955`
        """)
        st.json(val_metrics)

    with c_b:
        st.subheader("Frozen Pressure Configuration")
        st.markdown(f"""
        - **Pressure Threshold (MPI >= 0.55)**: Frozen at the 70th percentile of training data.
        - **High Pressure Deliveries**: 57,769 balls (28.7% of all deliveries).
        - **Death Phase Exposure**: 61.6% of death deliveries classified as high pressure.
        - **Innings Exposure**: Innings 1: 17.7% | Innings 2: 41.0% | Super Overs: 100.0%.
        """)
        st.json(pressure_cfg)

st.sidebar.markdown("---")
st.sidebar.caption("Rajasthan Royals Analytical War Room | Version 2.5 Broadcast Suite")
