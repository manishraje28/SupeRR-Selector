# 👑 SupeRR Selector Season 2 — Round 1
## Rajasthan Royals IPL 2027 Auction Strategy: Identifying the Most Reliable Players Under Pressure

An end-to-end cricket analytics and machine learning system built for **Rajasthan Royals** to identify, evaluate, and recruit the most reliable players under extreme match pressure for the IPL 2027 Auction.

---

## 🎯 Project Overview

This repository contains the complete analytical pipeline, predictive models, interactive Next.js war-room dashboard, and methodology report developed for Round 1 of **SupeRR Selector Season 2**.

The system addresses two critical dimensions:
1. **Pure Mathematical Benchmark (Option A)**: Evaluates who objectively performed best in high-pressure match situations across 200,999 deliveries (883 matches, Jan 2022 – Nov 2026).
2. **Rajasthan Royals War Room Auction Shortlist (Option B)**: Classifies player franchise contracts to separate rival-retained stars (e.g., Suryakumar Yadav, Jasprit Bumrah, Ryan Rickelton at MI; Heinrich Klaasen at SRH; Sunil Narine at KKR) from **100% targetable auction players** to build a dominant XI around RR's core (*Sanju Samson, Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer, Sandeep Sharma*).

---

## 🏗️ System Architecture & Methodology

```
                                [ RAW CRICKET DATA PACK ]
                               (883 Matches, 200,999 Balls)
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │      1. Pre-Ball State Reconstruction         │
                    │   (Legal balls, RRR, wickets, venue par,      │
                    │   recent shock — ZERO future look-ahead)      │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │       2. Match Pressure Engine (MPI)          │
                    │   Composite score: Chase Demand + WP Leverage │
                    │   Threshold frozen at MPI ≥ 0.55 (P70)        │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │       3. Context-Adjusted Value Added (CAVA)  │
                    │   Gradient-boosted expected runs & wickets    │
                    │   evaluated out-of-time (2025-26 test set)    │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │    4. Empirical Bayes Shrinkage & Ranking     │
                    │   Match-clustered SEs; 20th percentile        │
                    │   conservative posterior rank scores          │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │  5. Franchise Retention & Availability Model  │
                    │   Separates rival retentions vs RR targets    │
                    └───────┬───────────────────────────────┬───────┘
                            │                               │
                            ▼                               ▼
               [ Interactive Next.js Dashboard ]   [ Official PDF Report ]
              (3D Cards, Live Situation Sim)      (Unstop Submission Upload)
```

---

## 🏆 Unstop Submission Dropdown Selections

### Option B: Rajasthan Royals IPL 2027 Auction Shortlist *(Recommended for RR War Room)*
*100% targetable in auction — excludes retained franchise pillars so RR bids only on attainable talent.*

| Dropdown Field | Recommended Batter (Batsman 1–10) | Recommended Bowler (Bowler 1–10) |
| :---: | :--- | :--- |
| **1** | **Jos Buttler** | **Krunal Pandya** |
| **2** | **Reeza Hendricks** | **Josh Hazlewood** |
| **3** | **Phil Salt** | **Tim Southee** |
| **4** | **Sikandar Raza** | **Jamie Overton** |
| **5** | **Tim David** | **Nathan Ellis** |
| **6** | **Pathum Nissanka** | **Gudakesh Motie** |
| **7** | **Prabhsimran Singh** | **Mujeeb Ur Rahman** |
| **8** | **Akeal Hosein** | **Bhuvneshwar Kumar** |
| **9** | **Kusal Mendis** | **Mitchell Santner** |
| **10** | **Shikhar Dhawan** | **Lockie Ferguson** |

### Option A: Pure Statistical Benchmark *(All League Stars)*
*Mathematical ranking across all 883 matches, regardless of franchise contract.*

| Dropdown Field | Benchmark Batter (Batsman 1–10) | Benchmark Bowler (Bowler 1–10) |
| :---: | :--- | :--- |
| **1** | **Suryakumar Yadav** (MI Retained) | **Sunil Narine** (KKR Retained) |
| **2** | **Jos Buttler** (RR Target) | **Jasprit Bumrah** (MI Retained) |
| **3** | **Reeza Hendricks** (RR Target) | **Kuldeep Yadav** (DC Retained) |
| **4** | **Heinrich Klaasen** (SRH Retained) | **Krunal Pandya** (RR Target) |
| **5** | **Phil Salt** (RR Target) | **Sufiyan Muqeem** (Ineligible) |
| **6** | **Ryan Rickelton** (MI Contracted) | **Shaheen Afridi** (Ineligible) |
| **7** | **Abhishek Sharma** (SRH Retained) | **Josh Hazlewood** (RR Target) |
| **8** | **Andre Russell** (KKR Retained) | **Matheesha Pathirana** (CSK Retained) |
| **9** | **Tristan Stubbs** (DC Retained) | **Rashid Khan** (GT Retained) |
| **10** | **Sikandar Raza** (RR Target) | **Abrar Ahmed** (Ineligible) |

---

## 📁 Repository Directory Structure

```
├── outputs/                                # Core deliverables & verified artifacts
│   ├── methodology_report.pdf              # Official PDF methodology report for Unstop upload
│   ├── dashboard.html                      # Standalone single-file HTML dashboard (offline view)
│   ├── batting_rankings.csv                # Overall statistical batting rankings
│   ├── bowling_rankings.csv                # Overall statistical bowling rankings
│   ├── batting_rankings_rr_auction.csv     # Targetable batting shortlist for RR
│   ├── bowling_rankings_rr_auction.csv     # Targetable bowling shortlist for RR
│   ├── comprehensive_player_census.json    # Complete census (1,217 players, 883 matches)
│   ├── score_reconciliation_report.json    # 100% scorecard verification log
│   └── validation_metrics.json             # Out-of-time model validation metrics
│
├── frontend/                               # Professional Next.js 16 War Room Dashboard
│   ├── app/                                # App router pages & components
│   ├── data/analytics_data.json            # Consolidated JSON payload
│   ├── public/players/                     # 45 verified authentic player headshots
│   └── package.json                        # Dependencies & scripts
│
├── src/                                    # Analytical pipeline scripts
│   ├── 01_data_pipeline.py                 # Delivery cleaning & state reconstruction
│   ├── 02_pressure_engine.py               # Win probability & leverage modeling
│   ├── 03_performance_cava.py              # Gradient-boosted expected outcomes
│   ├── 04_ratings_and_rankings.py          # Empirical Bayes shrinkage & ranking
│   ├── 05_generate_report_pdf.py           # ReportLab methodology PDF generator
│   └── build_comprehensive_database.py     # Master database compiler & franchise classifier
│
├── dashboard/                              # Streamlit dashboard
│   └── app.py                              # Streamlit interactive application
│
├── scripts/                                # Helper scripts
│   ├── generate_standalone_dashboard.py    # Generates outputs/dashboard.html
│   └── fetch_cricbuzz_images.py            # Verified portrait image fetcher
│
├── run_all.py                              # End-to-end 1-command pipeline orchestrator
└── README.md                               # Project documentation
```

---

## ⚡ Quickstart & Reproducibility

### 1. Run the Entire Analytics Pipeline
```bash
python run_all.py
```
*Executes all 7 stages: raw ingestion, pre-ball reconstruction, pressure engine, CAVA calculation, Bayesian shrinkage, database compilation, and PDF report generation.*

### 2. Launch the Next.js War Room Dashboard
```bash
cd frontend
pnpm install
pnpm dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔒 Confidentiality & Data Policy
Proprietary ball-by-ball competition data (`Data Pack/` and raw `.parquet` extracts) are kept strictly separate from the public repository in accordance with official competition guidelines.
