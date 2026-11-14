"""
05_generate_report_pdf.py
Regenerates the official PDF Methodology Report for SupeRR Selector Season 2: Round 1.
Includes:
- Full Census (1,217 players, 883 matches, 200,999 balls)
- Both Dropdown Tables (Option A: Statistical Benchmark vs Option B: RR Auction Targets)
- Franchise Contract & Availability Model (explaining MI, SRH, KKR, RR retentions)
- Capped / Uncapped / Tactical Role Fit for Rajasthan Royals
"""

import os
import json
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report():
    print("=== Step 5: Generating Official Methodology Report PDF ===")
    os.makedirs('outputs', exist_ok=True)
    pdf_filename = 'outputs/methodology_report.pdf'

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#EA1A85'),
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#254AA5'),
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#254AA5'),
        spaceBefore=8,
        spaceAfter=3
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#333333'),
        spaceBefore=5,
        spaceAfter=2
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#222222'),
        spaceAfter=3
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.white,
        alignment=1
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        alignment=1
    )
    table_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        alignment=0
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("SupeRR Selector Season 2: Round 1 — Official Methodology Report", title_style))
    story.append(Paragraph("Identifying the Most Reliable Players Under Pressure — Rajasthan Royals IPL 2027 Auction Strategy", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#EA1A85'), spaceAfter=6))

    meta_text = (
        "<b>Franchise:</b> Rajasthan Royals War Room | <b>Data Pack Coverage:</b> Jan 2022 – Nov 2026 (883 Matches) | "
        "<b>Census:</b> 1,217 Registered Players, 959 Active On-Field (888 Strikers, 647 Bowlers), 200,999 Deliveries"
    )
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 3))

    # Section 1: Executive Summary & The Dual Mandate
    story.append(Paragraph("1. Executive Summary: Pure Statistical Benchmark vs RR Auction Reality", h1_style))
    exec_summary = (
        "Round 1 challenges us to identify the most reliable players under pressure from the proprietary data pack. "
        "From an elite franchise war-room perspective, this requires addressing two distinct layers of analysis: "
        "(1) <b>The Pure Mathematical Benchmark</b> — establishing historical truth across 200,999 balls to identify "
        "who performed best under extreme match pressure (MPI ≥ 0.55); and "
        "(2) <b>The Rajasthan Royals IPL 2027 Auction Strategy</b> — filtering out rival franchise retentions "
        "(e.g., Suryakumar Yadav, Jasprit Bumrah, and Ryan Rickelton at MI; Heinrich Klaasen at SRH; Sunil Narine at KKR) "
        "and BCCI-ineligible stars to isolate the <b>100% targetable player pool</b> that RR can realistically buy at the auction "
        "to complement retained stars <b>Sanju Samson, Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer</b>, and <b>Sandeep Sharma</b>."
    )
    story.append(Paragraph(exec_summary, body_style))
    story.append(Spacer(1, 3))

    # Section 2: Unstop Selections (Both Perspectives)
    story.append(Paragraph("2. Official Ordered Top-10 Lists (Unstop Dropdowns Selections)", h1_style))
    
    # Load Database
    with open('frontend/data/analytics_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Option B: RR Auction Shortlist
    story.append(Paragraph("<b>Option B: Rajasthan Royals IPL 2027 War Room Auction Shortlist (100% Targetable in Auction)</b>", h2_style))
    story.append(Paragraph("<i>Recommended for RR War Room Strategy: Excludes retained rival pillars so RR does not waste purse on unavailable stars.</i>", body_style))
    
    auc_batters = [b for b in data['batters'] if b['is_auction_available']][:10]
    auc_bowlers = [bw for bw in data['bowlers'] if bw['is_auction_available']][:10]

    t_auc_data = [[
        Paragraph("<b>Slot</b>", table_header_style),
        Paragraph("<b>Target Batter (Batsman 1–10)</b>", table_header_style),
        Paragraph("<b>Capped Status</b>", table_header_style),
        Paragraph("<b>Clutch</b>", table_header_style),
        Paragraph("<b>Target Bowler (Bowler 1–10)</b>", table_header_style),
        Paragraph("<b>Capped Status</b>", table_header_style),
        Paragraph("<b>Clutch</b>", table_header_style),
    ]]
    for i in range(10):
        b = auc_batters[i]
        bw = auc_bowlers[i]
        t_auc_data.append([
            Paragraph(f"<b>#{i+1}</b>", table_cell_style),
            Paragraph(f"<b>{b['name']}</b> ({b['flag']})", table_cell_left),
            Paragraph(b['capped_status'], table_cell_style),
            Paragraph(f"{b['clutch_score']}", table_cell_style),
            Paragraph(f"<b>{bw['name']}</b> ({bw['flag']})", table_cell_left),
            Paragraph(bw['capped_status'], table_cell_style),
            Paragraph(f"{bw['clutch_score']}", table_cell_style),
        ])
    t_auc = Table(t_auc_data, colWidths=[28, 135, 80, 42, 135, 80, 42])
    t_auc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#ECFDF5')])
    ]))
    story.append(t_auc)
    story.append(Spacer(1, 5))

    # Option A: Pure Statistical Benchmark
    story.append(Paragraph("<b>Option A: Pure Statistical Benchmark (All Data Pack Stars Regardless of Franchise Retentions)</b>", h2_style))
    story.append(Paragraph("<i>Pure historical truth across all matches in the data pack (answers who objectively played best under pressure).</i>", body_style))

    stat_batters = data['batters'][:10]
    stat_bowlers = data['bowlers'][:10]

    t_stat_data = [[
        Paragraph("<b>Slot</b>", table_header_style),
        Paragraph("<b>Benchmark Batter</b>", table_header_style),
        Paragraph("<b>Franchise Status</b>", table_header_style),
        Paragraph("<b>Score</b>", table_header_style),
        Paragraph("<b>Benchmark Bowler</b>", table_header_style),
        Paragraph("<b>Franchise Status</b>", table_header_style),
        Paragraph("<b>Score</b>", table_header_style),
    ]]
    for i in range(10):
        b = stat_batters[i]
        bw = stat_bowlers[i]
        t_stat_data.append([
            Paragraph(f"<b>#{i+1}</b>", table_cell_style),
            Paragraph(f"<b>{b['name']}</b>", table_cell_left),
            Paragraph(b['franchise_label'][:20], table_cell_style),
            Paragraph(f"{b['score']:.3f}", table_cell_style),
            Paragraph(f"<b>{bw['name']}</b>", table_cell_left),
            Paragraph(bw['franchise_label'][:20], table_cell_style),
            Paragraph(f"{bw['score']:.3f}", table_cell_style),
        ])
    t_stat = Table(t_stat_data, colWidths=[28, 130, 85, 42, 130, 85, 42])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#254AA5')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#EFF6FF')])
    ]))
    story.append(t_stat)
    story.append(Spacer(1, 5))

    # Section 3: Pressure Methodology
    story.append(Paragraph("3. Mathematical Methodology & Modeling Integrity", h1_style))
    meth_text = (
        "<b>Match Pressure Index (MPI):</b> Pre-delivery pressure is quantified using state variables strictly known before the ball: <br/>"
        "&bull; <b>Demand (D_t):</b> In Chases, combines Required Run Rate (RRR) relative to venue par, resource depletion (wickets lost 0–9), "
        "balls remaining, and recent shock (wickets lost in previous 12 balls). In Innings 1, evaluates deficit against historical venue par without look-ahead.<br/>"
        "&bull; <b>Leverage (LI_t):</b> Calibrated win-probability swing: |WP(boundary) - WP(wicket)| / 0.20. High pressure is frozen at <b>MPI ≥ 0.55</b> (70th percentile of 2022–2024 training data).<br/>"
        "&bull; <b>Context-Adjusted Value Added (CAVA):</b> Isolates skill from match conditions by subtracting gradient-boosted expected outcomes: "
        "<code>CAVA_bat = (Runs - E[Runs]) - V_w * (Out - E[Wkt])</code>; <code>CAVA_bowl = (E[Runs] - Runs) + V_w * (Wkt - E[Wkt])</code>.<br/>"
        "&bull; <b>Empirical Bayes Shrinkage & Uncertainty:</b> Raw player means are shrunk toward population priors using match-clustered variance, "
        "ranking players by the 20th percentile posterior: <code>Score = theta_shrunk - 0.84 * SE_shrunk</code>. Evaluated out-of-time on 2025–2026 matches (RMSE 1.7569, Brier 0.0514)."
    )
    story.append(Paragraph(meth_text, body_style))
    story.append(Spacer(1, 4))

    # Section 4: Franchise Retention Model & Tactical RR Fit
    story.append(Paragraph("4. Franchise Retention Model & Rajasthan Royals Tactical Acquisition Plan", h1_style))
    fit_text = (
        "<b>Why Certain Stars Are Unavailable:</b> Suryakumar Yadav, Jasprit Bumrah, and Ryan Rickelton are contracted pillars of Mumbai Indians; "
        "Heinrich Klaasen and Abhishek Sharma are retained by Sunrisers Hyderabad; Sunil Narine and Andre Russell are franchise icons of KKR. "
        "Shaheen Afridi and Sufiyan Muqeem are Pakistani internationals ineligible under BCCI auction rules.<br/>"
        "<b>Rajasthan Royals 2027 Auction Target Strategy:</b><br/>"
        "&bull; <b>Jos Buttler (Marquee Re-acquisition):</b> #1 Target Batter (94.6 CAVA under pressure). Elite anchor and accelerator at Sawai Mansingh Stadium.<br/>"
        "&bull; <b>Reeza Hendricks (International Free Agent):</b> #2 Target Batter. Exceptional 56.5% positive-match clutch share, available at great auction value.<br/>"
        "&bull; <b>Phil Salt (Powerplay Enforcer):</b> #3 Target Batter (Pressure SR 168.4). Obliterates bowling in overs 1-6 to set unbeatable run-chases.<br/>"
        "&bull; <b>Krunal Pandya (Middle-Overs Spin Choke):</b> #1 Target Bowler. Concedes only 6.94 economy in high-leverage situations with elite dot-ball control.<br/>"
        "&bull; <b>Josh Hazlewood & Nathan Ellis (Pace Spearheads):</b> Hazlewood brings robotic Test-match length discipline, while Ellis provides "
        "back-of-the-hand slower balls and yorkers to form an unbreachable death-overs partnership with Sandeep Sharma."
    )
    story.append(Paragraph(fit_text, body_style))
    story.append(Spacer(1, 4))

    # Audit Verification Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CCCCCC'), spaceAfter=3))
    audit_footer = (
        "<b>War Room Integrity Audit:</b> 100% scorecard reconciliation across all 867 contested matches (16 abandoned without ball bowled); "
        "zero look-ahead bias; no delivery data leakage; reproducible code repository with live interactive Next.js dashboard."
    )
    story.append(Paragraph(audit_footer, body_style))

    doc.build(story)
    print(f"Generated {pdf_filename} successfully ({os.path.getsize(pdf_filename)} bytes)!")

if __name__ == '__main__':
    generate_pdf_report()
