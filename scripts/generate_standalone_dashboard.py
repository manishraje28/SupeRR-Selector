import json
import os

with open("frontend/data/analytics_data.json", "r") as f:
    data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SupeRR Selector Season 2 — Rajasthan Royals War Room Intelligence</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #070B14;
      color: #F8FAFC;
    }}
    .glass {{
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .rr-pink {{ color: #EA1A85; }}
    .bg-rr-pink {{ background-color: #EA1A85; }}
    .border-rr-pink {{ border-color: #EA1A85; }}
    .rr-blue {{ color: #254AA5; }}
    .bg-rr-blue {{ background-color: #254AA5; }}
  </style>
</head>
<body class="selection:bg-pink-600 selection:text-white pb-20">

  <!-- Header -->
  <header class="sticky top-0 z-50 glass border-b border-white/10 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-[#EA1A85] to-[#254AA5] flex items-center justify-center font-black text-xl shadow-lg">👑</div>
      <div>
        <div class="flex items-center gap-2">
          <span class="font-black text-xl text-white">SupeRR Selector</span>
          <span class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-[#EA1A85]/20 text-[#EA1A85] border border-[#EA1A85]/40">ROUND 1 WAR ROOM</span>
        </div>
        <p class="text-xs text-slate-400">Rajasthan Royals • IPL 2027 Auction Intelligence Hub</p>
      </div>
    </div>
    <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
      <span>1,217 Players • 200,999 Deliveries • 883 Matches Audited</span>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 pt-6 space-y-8">

    <!-- Hero Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#EA1A85]/25 via-[#254AA5]/20 to-slate-900 border border-white/10 p-6 sm:p-8">
      <div class="max-w-3xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-[#EA1A85]/20 text-[#EA1A85] border border-[#EA1A85]/30 mb-3">
          RAJASTHAN ROYALS AUCTION STRATEGY • IPL 2027
        </div>
        <h1 class="text-3xl sm:text-4xl font-black text-white leading-tight">
          Identifying the Most Reliable <span class="text-[#EA1A85]">Clutch Performers</span> Under Pressure
        </h1>
        <p class="mt-2 text-slate-300 text-xs sm:text-sm leading-relaxed">
          RR already retained <strong>Samson, Jaiswal, Parag, Jurel, Hetmyer</strong>, and <strong>Sandeep Sharma</strong>. Below is the data-driven intelligence on targetable players versus rival-retained pillars to dominate the IPL 2027 Auction.
        </p>
      </div>
    </div>

    <!-- UNSTOP SUBMISSION DROPDOWN CHEAT SHEET -->
    <div class="glass p-6 rounded-2xl border border-white/10 space-y-4">
      <div class="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 class="text-xl font-black text-white">📋 Unstop Submission Dropdown Selections</h2>
          <p class="text-xs text-slate-400">Copy these exact ordered names directly into the Unstop submission fields (Batsman 1-10 & Bowler 1-10).</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Set 2: RR Auction Targets -->
        <div class="bg-slate-900/90 p-5 rounded-xl border border-emerald-500/40 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-emerald-400 tracking-wider">👑 SET 2: RR AUCTION SHORTLIST (REALISTIC)</span>
            <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold">100% Targetable</span>
          </div>
          <div class="text-xs text-slate-300 space-y-1">
            <p><strong>Top 10 Batters:</strong></p>
            <ol class="list-decimal list-inside pl-1 text-slate-200 font-mono text-[11px] space-y-0.5">
              {"".join([f"<li>{name}</li>" for name in data["dropdown_options"]["set_2_rr_auction_targets"]["batters"]])}
            </ol>
            <p class="pt-2"><strong>Top 10 Bowlers:</strong></p>
            <ol class="list-decimal list-inside pl-1 text-slate-200 font-mono text-[11px] space-y-0.5">
              {"".join([f"<li>{name}</li>" for name in data["dropdown_options"]["set_2_rr_auction_targets"]["bowlers"]])}
            </ol>
          </div>
        </div>

        <!-- Set 1: Pure Statistical Benchmark -->
        <div class="bg-slate-900/90 p-5 rounded-xl border border-blue-500/40 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-blue-400 tracking-wider">🏆 SET 1: STATISTICAL BENCHMARK (ALL STARS)</span>
            <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-bold">Historical Truth</span>
          </div>
          <div class="text-xs text-slate-300 space-y-1">
            <p><strong>Top 10 Batters:</strong></p>
            <ol class="list-decimal list-inside pl-1 text-slate-200 font-mono text-[11px] space-y-0.5">
              {"".join([f"<li>{name}</li>" for name in data["dropdown_options"]["set_1_pure_statistical"]["batters"]])}
            </ol>
            <p class="pt-2"><strong>Top 10 Bowlers:</strong></p>
            <ol class="list-decimal list-inside pl-1 text-slate-200 font-mono text-[11px] space-y-0.5">
              {"".join([f"<li>{name}</li>" for name in data["dropdown_options"]["set_1_pure_statistical"]["bowlers"]])}
            </ol>
          </div>
        </div>
      </div>
    </div>

    <!-- 1-CLICK MATCH SITUATION SIMULATOR -->
    <div class="glass p-6 rounded-2xl border border-white/10 space-y-4">
      <div class="flex items-center gap-3">
        <div class="p-2.5 rounded-xl bg-[#EA1A85]/20 text-[#EA1A85]">⚡</div>
        <div>
          <h2 class="text-xl font-black text-white">Tactical Match Pressure Situation Simulator</h2>
          <p class="text-xs text-slate-400">Pre-defined iconic match situations and recommended player response profiles for Rajasthan Royals.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
        {"".join([f'''
        <div class="bg-slate-900/80 p-4 rounded-xl border border-white/5 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-white text-xs">{p["title"]}</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-pink-500/20 text-[#EA1A85]">{p["badge"]}</span>
          </div>
          <p class="text-xs text-slate-400">{p["description"]}</p>
          <div class="pt-2 border-t border-white/5 text-[11px] space-y-1">
            <div class="text-emerald-400"><strong>Recommended Batters:</strong> {", ".join(p["top_fit_batters"][:3])}</div>
            <div class="text-blue-400"><strong>Recommended Bowlers:</strong> {", ".join(p["top_fit_bowlers"][:3])}</div>
          </div>
        </div>
        ''' for p in data["preset_situations"]])}
      </div>
    </div>

    <!-- PLAYER DOSSIERS -->
    <div class="space-y-4">
      <div class="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 class="text-xl font-black text-white">🃏 Top Player Pressure Dossiers (Auction Targets & Retained Rivals)</h2>
          <p class="text-xs text-slate-400">Complete performance metrics, franchise contract labels, and Rajasthan Royals tactical fit.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {"".join([f'''
        <div class="glass p-5 rounded-2xl border {"border-emerald-500/50" if b["is_auction_available"] else "border-rose-500/30"} flex flex-col justify-between">
          <div>
            <div class="flex items-start gap-4">
              <img src="{b["image_url"]}" alt="{b["name"]}" class="w-16 h-16 rounded-2xl object-cover bg-slate-800 border-2 border-white/10" onerror="this.src='https://cdn-icons-png.flaticon.com/512/847/847969.png'">
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-black px-2 py-0.5 rounded bg-white/10 text-slate-300">{"RR TARGET #" + str(b["rr_auction_rank"]) if b["is_auction_available"] else "OVERALL #" + str(b["rank"])}</span>
                  <span class="text-xs font-black text-amber-400">{b["clutch_score"]}/100 Clutch</span>
                </div>
                <h3 class="font-extrabold text-base text-white mt-1 truncate">{b["name"]} {b["flag"]}</h3>
                <div class="text-[11px] text-[#38BDF8] font-semibold truncate">{b["plain_english_role"]} • {b["capped_status"]}</div>
              </div>
            </div>

            <div class="mt-3 flex items-center justify-between flex-wrap gap-2 text-xs">
              <span class="px-2.5 py-0.5 rounded-full font-bold {"bg-emerald-500/20 text-emerald-400 border border-emerald-500/40" if b["is_auction_available"] else "bg-rose-500/20 text-rose-400 border border-rose-500/40"}">
                {"🎯 Prime RR Target" if b["is_auction_available"] else b["franchise_label"]}
              </span>
              <span class="font-bold text-amber-400 text-[11px]">{b["price_bracket"]}</span>
            </div>

            <div class="mt-3 bg-slate-900/80 rounded-xl p-3 border border-white/5 space-y-1 text-xs">
              <p class="text-slate-300"><strong>Performance:</strong> {b["non_technical_summary"]}</p>
              <p class="text-pink-300"><strong>RR Fit:</strong> {b["rr_fit"]}</p>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-white/10 grid grid-cols-3 gap-2 text-center text-xs">
            <div class="bg-slate-900/60 p-2 rounded-lg">
              <div class="text-[10px] text-slate-400 font-semibold">Pressure SR</div>
              <div class="font-black text-[#EA1A85]">{b["hp_sr"]}</div>
            </div>
            <div class="bg-slate-900/60 p-2 rounded-lg">
              <div class="text-[10px] text-slate-400 font-semibold">Uplift</div>
              <div class="font-black text-[#38BDF8]">+{b["uplift_cava"]}</div>
            </div>
            <div class="bg-slate-900/60 p-2 rounded-lg">
              <div class="text-[10px] text-slate-400 font-semibold">Balls</div>
              <div class="font-black text-amber-400">{b["hp_balls"]}b</div>
            </div>
          </div>
        </div>
        ''' for b in data["batters"][:15]])}
      </div>
    </div>

  </main>
</body>
</html>
"""

with open("outputs/dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone dashboard at outputs/dashboard.html ({len(html_content)} bytes)")
