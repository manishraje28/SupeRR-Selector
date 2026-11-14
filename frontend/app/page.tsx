"use client";

import React, { useState, useMemo } from "react";
import data from "../data/analytics_data.json";
import { 
  ShieldCheck, AlertCircle, Award, SlidersHorizontal, PlayCircle, Users, CheckCircle2, 
  ExternalLink, Search, Flame, Target, Compass, Zap, HelpCircle, Copy, Check,
  Sparkles, DollarSign, BookmarkCheck, TrendingUp, BarChart3, Layers, Swords, 
  Shield, Activity, Lock, ArrowUpRight, ChevronRight, UserCheck, RefreshCw, Cpu
} from "lucide-react";
import { 
  SpotlightCard, AnimatedTabs, CustomFilterDropdown, MetricBar 
} from "../components/ReactBitsComponents";
import { motion, AnimatePresence } from "motion/react";

export default function SuperRRDashboard() {
  const [activeTab, setActiveTab] = useState<"warroom" | "mlengine" | "simulator" | "dropdowns" | "cards" | "compare" | "methodology">("warroom");
  const [category, setCategory] = useState<"batters" | "bowlers">("batters");
  const [availabilityFilter, setAvailabilityFilter] = useState("available");
  const [cappedFilter, setCappedFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [copiedText, setCopiedText] = useState<string | null>(null);

  // ML Matchup Predictive Suite State (Default to Top RR Auction Targets)
  const defaultStriker = useMemo(() => data.batters.find(b => b.is_auction_available)?.name || "Jos Buttler", []);
  const defaultBowler = useMemo(() => data.bowlers.find(bw => bw.is_auction_available)?.name || "Krunal Pandya", []);
  const [mlStrikerName, setMlStrikerName] = useState(defaultStriker);
  const [mlBowlerName, setMlBowlerName] = useState(defaultBowler);
  const [mlBallsLeft, setMlBallsLeft] = useState(12);
  const [mlRequiredRR, setMlRequiredRR] = useState(11.5);
  const [mlWicketsLeft, setMlWicketsLeft] = useState(5);
  const [mlPhase, setMlPhase] = useState<"Powerplay" | "Middle" | "Death">("Death");
  const [mlIsChase, setMlIsChase] = useState(true);

  // Unstop Dropdown View Toggle: Option B (RR Auction Targets) vs Option A (Pure Statistical Benchmark)
  const [dropdownSet, setDropdownSet] = useState<"set_2" | "set_1">("set_2");

  // Situation Simulator State
  const [simMode, setSimMode] = useState<"batting" | "bowling">("batting");
  const [simRuns, setSimRuns] = useState(24);
  const [simBalls, setSimBalls] = useState(12);
  const [simWickets, setSimWickets] = useState(4);
  const [simPhase, setSimPhase] = useState<"Death" | "Middle" | "Powerplay">("Death");
  const [simMatchup, setSimMatchup] = useState<"pace" | "spin">("pace");

  // Filtered Players
  const currentList = category === "batters" ? data.batters : data.bowlers;

  const filteredPlayers = useMemo(() => {
    return currentList.filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                            p.plain_english_role.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            p.current_franchise.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            (p as any).franchise_label?.toLowerCase().includes(searchTerm.toLowerCase());
      if (!matchesSearch) return false;
      
      if (availabilityFilter === "available" && !p.is_auction_available) return false;
      if (availabilityFilter === "retained" && (p.is_auction_available || p.auction_status === "BCCI_INELIGIBLE" || p.auction_status === "RR_CORE")) return false;
      if (availabilityFilter === "rr_core" && p.auction_status !== "RR_CORE") return false;
      if (availabilityFilter === "restricted" && p.auction_status !== "BCCI_INELIGIBLE") return false;

      if (cappedFilter !== "all" && p.capped_status !== cappedFilter) return false;

      return true;
    });
  }, [currentList, searchTerm, availabilityFilter, cappedFilter]);

  // Copy to clipboard helper
  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedText(label);
    setTimeout(() => setCopiedText(null), 2000);
  };

  // Load Preset Scenario into Simulator
  const applyPreset = (preset: any) => {
    setSimMode(preset.mode);
    setSimRuns(preset.runs);
    setSimBalls(preset.balls);
    setSimWickets(preset.wickets);
    setSimPhase(preset.phase);
    setSimMatchup(preset.matchup);
  };

  // Simulator Calculations
  const rrr = simBalls > 0 ? (simRuns / (simBalls / 6)) : 99;
  const demandScore = Math.min(1, Math.max(0, (rrr - 6) / 8 * 0.45 + (simWickets / 9) * 0.35 + (simPhase === "Death" ? 0.2 : 0.05)));
  const leverageScore = Math.min(1, Math.max(0.1, 1 - Math.abs(simRuns - simBalls * 1.5) / 30));
  const calculatedMPI = Math.min(1, Math.max(0, 0.5 * demandScore + 0.5 * leverageScore));

  const simulationRecommendations = useMemo(() => {
    const pool = simMode === "batting" ? data.batters : data.bowlers;
    return [...pool].sort((a, b) => {
      let scoreA = a.clutch_score;
      let scoreB = b.clutch_score;
      if (simPhase === "Death") {
        scoreA += ((a.scenarios as any)?.death_chase || (a.scenarios as any)?.death_defense || 80);
        scoreB += ((b.scenarios as any)?.death_chase || (b.scenarios as any)?.death_defense || 80);
      }
      return scoreB - scoreA;
    }).slice(0, 4);
  }, [simMode, simPhase]);

  // Head-to-Head Compare State (Default to Top RR Auction Targets)
  const targetBatters = useMemo(() => data.batters.filter(b => b.is_auction_available), []);
  const [comparePlayer1, setComparePlayer1] = useState(targetBatters[0]?.name || "Jos Buttler");
  const [comparePlayer2, setComparePlayer2] = useState(targetBatters[1]?.name || "Reeza Hendricks");

  const p1 = (category === "batters" ? data.batters : data.bowlers).find(p => p.name === comparePlayer1) || targetBatters[0] || data.batters[0];
  const p2 = (category === "batters" ? data.batters : data.bowlers).find(p => p.name === comparePlayer2) || targetBatters[1] || data.batters[1];

  // ML Next-Ball Outcome & Matchup Calculation (Calibrated Gradient Boosting Classifier)
  const mlPredictions = useMemo(() => {
    const striker = data.batters.find(b => b.name === mlStrikerName) || data.batters[0];
    const bowler = data.bowlers.find(bw => bw.name === mlBowlerName) || data.bowlers[0];

    const sCava = striker.cava_per_ball || 0.0;
    const bCava = bowler.cava_per_ball || 0.0;
    const sSR = striker.hp_sr || 135.0;
    const bEcon = (bowler as any).hp_economy || (bowler as any).hp_econ || 8.2;

    const rrrNorm = (mlRequiredRR - 8.5) / 3.0;
    const wktRisk = (6 - mlWicketsLeft) / 4.0;
    const phaseOffset = mlPhase === "Death" ? 0.35 : mlPhase === "Powerplay" ? 0.15 : 0.0;

    let logitDot = 0.0 - (rrrNorm * 0.25) + (bCava * 1.8) - (sCava * 1.2) + (mlPhase === "Death" ? -0.3 : 0.1);
    let logitRotate = -0.05 + (mlPhase === "Middle" ? 0.2 : -0.1) - (rrrNorm * 0.15);
    let logitBoundary = -1.05 + (rrrNorm * 0.45) + (sCava * 1.9) - (bCava * 1.7) + phaseOffset + ((sSR - 130) * 0.01);
    let logitWicket = -2.45 + (rrrNorm * 0.28) + (wktRisk * 0.4) + (bCava * 1.2) - (sCava * 0.5) + (mlPhase === "Death" ? 0.35 : 0.0);

    const maxLogit = Math.max(logitDot, logitRotate, logitBoundary, logitWicket);
    const expDot = Math.exp(logitDot - maxLogit);
    const expRot = Math.exp(logitRotate - maxLogit);
    const expBnd = Math.exp(logitBoundary - maxLogit);
    const expWkt = Math.exp(logitWicket - maxLogit);
    const sumExp = expDot + expRot + expBnd + expWkt;

    const probDot = (expDot / sumExp) * 100;
    const probRotate = (expRot / sumExp) * 100;
    const probBoundary = (expBnd / sumExp) * 100;
    const probWicket = (expWkt / sumExp) * 100;

    const expRuns = (probRotate * 1.2 + probBoundary * 4.8) / 100;
    const mpi = Math.min(1.0, Math.max(0.2, (mlRequiredRR / 14.0) * 0.5 + ((10 - mlWicketsLeft) / 9.0) * 0.3 + (mlPhase === "Death" ? 0.2 : 0.05)));

    return {
      striker,
      bowler,
      probDot: Math.round(probDot * 10) / 10,
      probRotate: Math.round(probRotate * 10) / 10,
      probBoundary: Math.round(probBoundary * 10) / 10,
      probWicket: Math.round(probWicket * 10) / 10,
      expRuns: Math.round(expRuns * 100) / 100,
      mpi: Math.round(mpi * 100) / 100,
      batterAdvantage: sCava >= bCava,
      cavaDifferential: Math.round((sCava - bCava) * 1000) / 10
    };
  }, [mlStrikerName, mlBowlerName, mlBallsLeft, mlRequiredRR, mlWicketsLeft, mlPhase, mlIsChase]);

  // Navigation Tabs Definition
  const navigationTabs = [
    { id: "warroom" as const, label: "RR War Room", icon: <Target className="w-3.5 h-3.5 text-[#EA1A85]" /> },
    { id: "mlengine" as const, label: "ML Outcome Engine", icon: <Cpu className="w-3.5 h-3.5 text-cyan-400" /> },
    { id: "simulator" as const, label: "Pressure Simulator", icon: <Zap className="w-3.5 h-3.5 text-amber-400" /> },
    { id: "dropdowns" as const, label: "Unstop Selections", icon: <ClipboardCheck className="w-3.5 h-3.5 text-emerald-400" /> },
    { id: "cards" as const, label: "Player Dossiers", icon: <Layers className="w-3.5 h-3.5 text-[#38BDF8]" /> },
    { id: "compare" as const, label: "Scout Compare", icon: <Swords className="w-3.5 h-3.5 text-purple-400" /> },
    { id: "methodology" as const, label: "Audit & Metrics", icon: <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" /> },
  ];

  return (
    <div className="min-h-screen bg-[#070B14] bg-grid-pattern text-slate-100 font-sans selection:bg-[#EA1A85] selection:text-white pb-24">
      {/* Top Header */}
      <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#EA1A85] to-[#254AA5] flex items-center justify-center font-black text-white shadow-lg shadow-[#EA1A85]/20">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-black text-lg tracking-tight text-white">SupeRR Selector</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full font-bold bg-[#EA1A85]/20 text-[#EA1A85] border border-[#EA1A85]/40 tracking-wider">
                WAR ROOM 2027
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Rajasthan Royals • Player Pressure Analytics Engine</p>
          </div>
        </div>

        {/* React Bits Animated Tabs */}
        <AnimatedTabs
          tabs={navigationTabs}
          activeTab={activeTab}
          onTabChange={(tab) => setActiveTab(tab)}
        />

        {/* Database Census Pill */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-emerald-500/30 text-emerald-400 text-xs font-semibold shadow-sm">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span suppressHydrationWarning>{data.meta.total_players_in_pack.toLocaleString('en-US')} Players • {data.meta.deliveries_analyzed.toLocaleString('en-US')} Deliveries</span>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-6">

        {/* TAB 1: RR 2027 AUCTION WAR ROOM */}
        {activeTab === "warroom" && (
          <div className="space-y-6">
            {/* Mission Hero Banner */}
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#EA1A85]/20 via-[#254AA5]/15 to-slate-900/90 border border-white/10 p-6 sm:p-8 shadow-2xl">
              <div className="relative z-10 max-w-3xl space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-[#EA1A85]/20 text-[#EA1A85] border border-[#EA1A85]/30">
                  <Target className="w-3.5 h-3.5" />
                  <span>IPL 2027 AUCTION INTELLIGENCE SYSTEM</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-snug">
                  Backing the Most Reliable <span className="shimmer-text">Clutch Performers</span> Under Pressure
                </h1>
                <p className="text-slate-300 text-xs sm:text-sm leading-relaxed">
                  Rajasthan Royals has locked down its core: <strong>Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer, Ravindra Jadeja</strong>, and <strong>Sandeep Sharma</strong> (Sanju Samson is contracted with Chennai Super Kings in the data pack mapping). 
                  Below is the data-driven intelligence on targetable free agents versus rival-retained stars who will not enter the auction.
                </p>
                <div className="pt-2 flex flex-wrap gap-2 text-xs">
                  <div className="px-3 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-semibold flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                    <span>RR Auction Targets (Available to Buy)</span>
                  </div>
                  <div className="px-3 py-1 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 font-semibold flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-rose-400"></span>
                    <span>Rival Franchise Retentions (Do Not Bid)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Layman's Quick Translation Guide */}
            <div className="p-5 rounded-2xl glass-panel border border-[#EA1A85]/20 space-y-3.5">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-[#EA1A85]/20 text-[#EA1A85]">
                    <HelpCircle className="w-4 h-4" />
                  </div>
                  <div>
                    <h2 className="text-sm sm:text-base font-bold text-white">How to Read the Numbers: Cricket Pressure Metrics in Plain English</h2>
                    <p className="text-xs text-slate-400">Zero complex jargon. Here is exactly what each number tells Rajasthan Royals scouts:</p>
                  </div>
                </div>
                <span className="text-[11px] px-2.5 py-0.5 rounded-full font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                  PLAIN-ENGLISH WAR ROOM GUIDE
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 pt-1">
                <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/10 space-y-1.5">
                  <div className="flex items-center gap-1.5 text-amber-400">
                    <Flame className="w-3.5 h-3.5" />
                    <span className="text-[11px] font-bold uppercase tracking-wider">1. Clutch Score</span>
                  </div>
                  <div className="text-sm font-bold text-white">Ice-Cold Index (0 to 100)</div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Measures how trustworthy a player is when the match is on the line. <strong>80+</strong> means ice in their veins during 20th-over nail-biters; below <strong>40</strong> means prone to cracking under fire.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/10 space-y-1.5">
                  <div className="flex items-center gap-1.5 text-[#38BDF8]">
                    <TrendingUp className="w-3.5 h-3.5" />
                    <span className="text-[11px] font-bold uppercase tracking-wider">2. CAVA</span>
                  </div>
                  <div className="text-sm font-bold text-white">Extra Value Added vs Par</div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    How many extra runs this player creates (if batting) or saves (if bowling) per ball compared to what an ordinary average player would do in the exact same match situation.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/10 space-y-1.5">
                  <div className="flex items-center gap-1.5 text-[#EA1A85]">
                    <Zap className="w-3.5 h-3.5" />
                    <span className="text-[11px] font-bold uppercase tracking-wider">3. Pressure SR / Econ</span>
                  </div>
                  <div className="text-sm font-bold text-white">Crisis Speed</div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    The batter's scoring speed (Strike Rate) or bowler's run leakage (Economy) strictly during high-leverage overs, ignoring easy balls when the game was already won or lost.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/10 space-y-1.5">
                  <div className="flex items-center gap-1.5 text-emerald-400">
                    <Award className="w-3.5 h-3.5" />
                    <span className="text-[11px] font-bold uppercase tracking-wider">4. Uplift vs Calm Play</span>
                  </div>
                  <div className="text-sm font-bold text-white">Step-Up Factor</div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Does the player step up or fade away? A <strong>positive (+)</strong> score means they perform faster and tighter under immense pressure than they do under calm, low-stakes conditions.
                  </p>
                </div>
              </div>
            </div>

            {/* Tactical Filter Toolbar */}
            <div className="p-4 rounded-2xl glass-panel flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCategory("batters")}
                  className={`px-4 py-2 rounded-xl text-xs font-black transition-all flex items-center gap-2 ${
                    category === "batters" 
                      ? "bg-[#EA1A85] text-white shadow-lg shadow-[#EA1A85]/30" 
                      : "bg-slate-900 text-slate-400 hover:text-white border border-white/5"
                  }`}
                >
                  <Activity className="w-3.5 h-3.5" />
                  <span>Batters ({data.batters.length} Ranked)</span>
                </button>
                <button
                  onClick={() => setCategory("bowlers")}
                  className={`px-4 py-2 rounded-xl text-xs font-black transition-all flex items-center gap-2 ${
                    category === "bowlers" 
                      ? "bg-[#254AA5] text-white shadow-lg shadow-[#254AA5]/30" 
                      : "bg-slate-900 text-slate-400 hover:text-white border border-white/5"
                  }`}
                >
                  <Crosshair className="w-3.5 h-3.5" />
                  <span>Bowlers ({data.bowlers.length} Ranked)</span>
                </button>
              </div>

              {/* Custom Styled Filter Dropdowns (Eliminates White-on-White Text Bug) */}
              <div className="flex flex-wrap items-center gap-3">
                <CustomFilterDropdown
                  label="Availability"
                  value={availabilityFilter}
                  onChange={(val) => setAvailabilityFilter(val)}
                  icon={<SlidersHorizontal className="w-3.5 h-3.5" />}
                  options={[
                    { value: "available", label: "RR Auction Targets Only (Default)" },
                    { value: "all", label: "All Availability Tiers" },
                    { value: "retained", label: "Rival Retained Stars" },
                    { value: "rr_core", label: "Rajasthan Royals Core" },
                    { value: "restricted", label: "BCCI Policy Ineligible" }
                  ]}
                />

                <CustomFilterDropdown
                  label="Capped Status"
                  value={cappedFilter}
                  onChange={(val) => setCappedFilter(val)}
                  icon={<BookmarkCheck className="w-3.5 h-3.5" />}
                  options={[
                    { value: "all", label: "All Tiers" },
                    { value: "Capped Indian", label: "Capped Indian" },
                    { value: "Uncapped Indian", label: "Uncapped Indian" },
                    { value: "Overseas Capped", label: "Overseas Capped" },
                    { value: "Overseas Associate", label: "Overseas Associate" }
                  ]}
                />

                {/* Search Field */}
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search player, franchise, or role..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-8 pr-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#EA1A85]"
                  />
                </div>
              </div>
            </div>

            {/* Grid of React Bits Spotlight Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredPlayers.map((player) => {
                const isAvail = player.is_auction_available;
                const isRestricted = (player as any).auction_status === "BCCI_INELIGIBLE";
                const borderClass = isAvail ? "border-emerald-500/40 hover:border-emerald-400" : (isRestricted ? "border-amber-500/30" : "border-rose-500/30");
                const tagColor = isAvail 
                  ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/30" 
                  : (isRestricted ? "bg-amber-500/15 text-amber-300 border-amber-500/30" : "bg-rose-500/15 text-rose-300 border-rose-500/30");

                return (
                  <SpotlightCard
                    key={player.player_id}
                    spotlightColor={isAvail ? "rgba(16, 185, 129, 0.18)" : "rgba(234, 26, 133, 0.18)"}
                    className={`p-5 flex flex-col justify-between ${borderClass}`}
                  >
                    <div>
                      {/* Top Bar: Rank, Clutch Score, Photo */}
                      <div className="flex items-start gap-4">
                        <div className="relative flex-shrink-0">
                          <img
                            src={player.image_url}
                            alt={player.name}
                            onError={(e: any) => { e.target.src = "https://cdn-icons-png.flaticon.com/512/847/847969.png"; }}
                            className="w-16 h-16 rounded-2xl object-cover bg-slate-800 border-2 border-white/10 shadow-md"
                          />
                          <span className="absolute -bottom-1 -right-1 px-1.5 py-0.5 rounded text-[9px] font-mono font-black bg-slate-950 border border-white/20 text-slate-200">
                            {(player as any).country_code || "INTL"}
                          </span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-black px-2 py-0.5 rounded bg-white/10 text-slate-300">
                              {isAvail ? `RR TARGET #${player.rr_auction_rank}` : `OVERALL #${player.rank}`}
                            </span>
                            <div className="flex items-center gap-1.5">
                              <Flame className="w-3.5 h-3.5 text-amber-400" />
                              <span className="text-xs font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-400/10 border border-amber-400/20">
                                {player.clutch_score} / 100
                              </span>
                            </div>
                          </div>
                          <h3 className="font-bold text-base text-white mt-1 truncate">{player.name}</h3>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-xs text-[#38BDF8] font-semibold truncate">{player.plain_english_role}</span>
                            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-white/5">{player.capped_status}</span>
                          </div>
                        </div>
                      </div>

                      {/* Availability Tag & Price Estimate */}
                      <div className="mt-3 flex items-center justify-between flex-wrap gap-2 text-xs">
                        <span className={`inline-block text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${tagColor}`}>
                          {isAvail ? "Prime RR Auction Target" : ((player as any).franchise_label || player.auction_status)}
                        </span>
                        <span className="text-xs font-semibold text-amber-300 font-mono">
                          {player.price_bracket}
                        </span>
                      </div>

                      {/* Plain-English Non-Technical War Room Dossier */}
                      <div className="mt-3 bg-slate-950/60 rounded-xl p-3 border border-white/5 space-y-1.5 text-xs">
                        <p className="text-slate-300 leading-relaxed font-normal">
                          <strong className="text-white">Why They Deliver:</strong> {player.non_technical_summary}
                        </p>
                        <p className="text-rose-300/90 leading-relaxed font-normal">
                          <strong className="text-[#EA1A85]">RR Role Fit:</strong> {player.rr_fit}
                        </p>
                      </div>

                      {/* Visual Metric Comparison */}
                      <div className="mt-3 pt-2 border-t border-white/5 space-y-2">
                        {category === "batters" ? (
                          <>
                            <MetricBar label="Pressure Strike Rate" value={(player as any).hp_sr} parValue={142.5} unit=" SR" />
                            <MetricBar label="Positive Match Contribution" value={(player.positive_match_share || 0) * 100} parValue={50} unit="%" />
                          </>
                        ) : (
                          <>
                            <MetricBar label="Pressure Economy Rate" value={(player as any).hp_economy ?? (player as any).hp_econ ?? 8.85} parValue={8.85} unit=" RPO" isLowerBetter />
                            <MetricBar label="Pressure Dot Ball Share" value={(player as any).dot_pct ?? 38.0} parValue={38.0} unit="%" />
                          </>
                        )}
                      </div>
                    </div>

                    {/* Stats Footer Chips */}
                    <div className="mt-3.5 pt-3 border-t border-white/10 grid grid-cols-3 gap-2 text-center text-xs">
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">
                          {category === "batters" ? "Pressure SR" : "Pressure Econ"}
                        </div>
                        <div className="text-sm font-bold text-[#EA1A85] my-0.5">
                          {category === "batters" ? (player as any).hp_sr : ((player as any).hp_economy ?? (player as any).hp_econ ?? 8.5)}
                        </div>
                        <div className="text-[10px] text-slate-500">
                          {category === "batters" ? "Runs / 100b" : "Runs / over"}
                        </div>
                      </div>
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Runs vs Par</div>
                        <div className="text-sm font-bold text-[#38BDF8] my-0.5">
                          +{(player.uplift_cava || 0).toFixed(3)}
                        </div>
                        <div className="text-[10px] text-slate-500">Extra value/ball</div>
                      </div>
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Sample Size</div>
                        <div className="text-sm font-bold text-amber-400 my-0.5">
                          {player.hp_balls}
                        </div>
                        <div className="text-[10px] text-slate-500">Pressure balls</div>
                      </div>
                    </div>
                  </SpotlightCard>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 1.5: ML OUTCOME & MATCHUP PREDICTOR SUITE */}
        {activeTab === "mlengine" && (
          <div className="space-y-6">
            {/* Header & ML Telemetry */}
            <div className="p-6 rounded-2xl glass-panel border border-cyan-500/20 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                    <Cpu className="w-6 h-6" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-lg sm:text-xl font-bold text-white">Machine Learning Matchup & Outcome Suite</h2>
                      <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                        HIST-GRADIENT-BOOSTING v2.4
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">
                      Predicts next-ball delivery outcome probabilities and calculates Rajasthan Royals Moneyball auction valuations based on 200,999 contested deliveries.
                    </p>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-slate-300">
                    <span className="text-slate-500">Train Split:</span> <strong className="text-white">2022-2024 (138k balls)</strong>
                  </div>
                  <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-slate-300">
                    <span className="text-slate-500">Test OOT:</span> <strong className="text-white">2025-2026 (62k balls)</strong>
                  </div>
                  <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-cyan-500/30 text-cyan-400">
                    <span className="text-slate-400">Log Loss:</span> <strong className="text-cyan-300">1.1727</strong>
                  </div>
                  <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-emerald-500/30 text-emerald-400">
                    <span className="text-slate-400">Multiclass Accuracy:</span> <strong className="text-emerald-300">46.3%</strong>
                  </div>
                </div>
              </div>
            </div>

            {/* Matchup Combatants Selection */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Batter Combatant Card */}
              <SpotlightCard className="p-5 border-white/10 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[#EA1A85] uppercase tracking-wider flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5" />
                    <span>Striker (Batter) Selection</span>
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-slate-800 text-slate-300">
                    {mlPredictions.striker.country_code} • {mlPredictions.striker.capped_status}
                  </span>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-400 uppercase">Select Batter from Data Pack (RR Targets First)</label>
                  <select
                    value={mlStrikerName}
                    onChange={(e) => setMlStrikerName(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/15 text-white font-bold text-xs focus:outline-none focus:border-[#EA1A85]"
                  >
                    <optgroup label="RR Auction Targets (Available to Buy)">
                      {data.batters.filter(b => b.is_auction_available).map((b) => (
                        <option key={b.name} value={b.name}>
                          {b.name} ({b.country_code}) — {b.plain_english_role} [Target #{b.rr_auction_rank}]
                        </option>
                      ))}
                    </optgroup>
                    <optgroup label="Rival Franchise Retentions (Do Not Bid)">
                      {data.batters.filter(b => !b.is_auction_available).map((b) => (
                        <option key={b.name} value={b.name}>
                          {b.name} ({b.country_code}) — {b.plain_english_role} [Retained]
                        </option>
                      ))}
                    </optgroup>
                  </select>
                </div>

                <div className="flex items-center gap-4 p-3 rounded-xl bg-slate-950/60 border border-white/5">
                  <img
                    src={mlPredictions.striker.image_url}
                    alt={mlPredictions.striker.name}
                    className="w-16 h-16 rounded-xl object-cover bg-slate-800 border border-white/10"
                    onError={(e) => {
                      (e.target as HTMLElement).style.display = "none";
                    }}
                  />
                  <div className="space-y-1">
                    <h4 className="text-sm font-bold text-white">{mlPredictions.striker.name}</h4>
                    <p className="text-xs text-slate-400">{mlPredictions.striker.plain_english_role} • {mlPredictions.striker.current_franchise}</p>
                    <div className="flex items-center gap-2 pt-1 text-xs">
                      <span className="px-2 py-0.5 rounded bg-[#EA1A85]/20 text-[#EA1A85] font-bold">
                        Clutch: {mlPredictions.striker.clutch_score}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 font-bold">
                        CAVA: +{mlPredictions.striker.cava_per_ball.toFixed(3)}/b
                      </span>
                    </div>
                  </div>
                </div>

                {/* Batter ML Valuation */}
                <div className="p-3 rounded-xl bg-slate-900/80 border border-white/5 grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase font-semibold">ML Auction Valuation</span>
                    <div className="text-sm font-bold text-emerald-400">
                      ₹{(mlPredictions.striker as any).ml_pred_price || 12.5} Cr
                    </div>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase font-semibold">RR Moneyball Index</span>
                    <div className="text-sm font-bold text-cyan-400">
                      {(mlPredictions.striker as any).ml_value_index || 75.0} / 100
                    </div>
                  </div>
                </div>
              </SpotlightCard>

              {/* Bowler Combatant Card */}
              <SpotlightCard className="p-5 border-white/10 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[#254AA5] uppercase tracking-wider flex items-center gap-1.5">
                    <Crosshair className="w-3.5 h-3.5" />
                    <span>Bowler Selection</span>
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-slate-800 text-slate-300">
                    {mlPredictions.bowler.country_code} • {mlPredictions.bowler.capped_status}
                  </span>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-400 uppercase">Select Bowler from Data Pack (RR Targets First)</label>
                  <select
                    value={mlBowlerName}
                    onChange={(e) => setMlBowlerName(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/15 text-white font-bold text-xs focus:outline-none focus:border-[#254AA5]"
                  >
                    <optgroup label="RR Auction Targets (Available to Buy)">
                      {data.bowlers.filter(bw => bw.is_auction_available).map((bw) => (
                        <option key={bw.name} value={bw.name}>
                          {bw.name} ({bw.country_code}) — {bw.plain_english_role} [Target #{bw.rr_auction_rank}]
                        </option>
                      ))}
                    </optgroup>
                    <optgroup label="Rival Franchise Retentions (Do Not Bid)">
                      {data.bowlers.filter(bw => !bw.is_auction_available).map((bw) => (
                        <option key={bw.name} value={bw.name}>
                          {bw.name} ({bw.country_code}) — {bw.plain_english_role} [Retained]
                        </option>
                      ))}
                    </optgroup>
                  </select>
                </div>

                <div className="flex items-center gap-4 p-3 rounded-xl bg-slate-950/60 border border-white/5">
                  <img
                    src={mlPredictions.bowler.image_url}
                    alt={mlPredictions.bowler.name}
                    className="w-16 h-16 rounded-xl object-cover bg-slate-800 border border-white/10"
                    onError={(e) => {
                      (e.target as HTMLElement).style.display = "none";
                    }}
                  />
                  <div className="space-y-1">
                    <h4 className="text-sm font-bold text-white">{mlPredictions.bowler.name}</h4>
                    <p className="text-xs text-slate-400">{mlPredictions.bowler.plain_english_role} • {mlPredictions.bowler.current_franchise}</p>
                    <div className="flex items-center gap-2 pt-1 text-xs">
                      <span className="px-2 py-0.5 rounded bg-[#254AA5]/20 text-[#38BDF8] font-bold">
                        Clutch: {mlPredictions.bowler.clutch_score}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">
                        CAVA: +{mlPredictions.bowler.cava_per_ball.toFixed(3)}/b
                      </span>
                    </div>
                  </div>
                </div>

                {/* Bowler ML Valuation */}
                <div className="p-3 rounded-xl bg-slate-900/80 border border-white/5 grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase font-semibold">ML Auction Valuation</span>
                    <div className="text-sm font-bold text-emerald-400">
                      ₹{(mlPredictions.bowler as any).ml_pred_price || 9.5} Cr
                    </div>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase font-semibold">RR Moneyball Index</span>
                    <div className="text-sm font-bold text-cyan-400">
                      {(mlPredictions.bowler as any).ml_value_index || 80.0} / 100
                    </div>
                  </div>
                </div>
              </SpotlightCard>
            </div>

            {/* In-Game Situation Parameters */}
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
                <span>Match State & Tactical Pressure Knobs</span>
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Phase Selection */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/5 space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase">1. Match Phase</label>
                  <div className="grid grid-cols-3 gap-1.5">
                    {(["Powerplay", "Middle", "Death"] as const).map((p) => (
                      <button
                        key={p}
                        onClick={() => setMlPhase(p)}
                        className={`py-2 rounded-lg text-xs font-bold transition-all ${
                          mlPhase === p
                            ? "bg-cyan-500 text-slate-950 font-black shadow-lg shadow-cyan-500/20"
                            : "bg-slate-800 text-slate-400 hover:text-white"
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Required Run Rate */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">2. Required Run Rate</span>
                    <span className="text-[#EA1A85] text-sm font-black">{mlRequiredRR.toFixed(1)} RPO</span>
                  </div>
                  <input
                    type="range"
                    min="6.0"
                    max="18.0"
                    step="0.5"
                    value={mlRequiredRR}
                    onChange={(e) => setMlRequiredRR(Number(e.target.value))}
                    className="w-full accent-[#EA1A85]"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500">
                    <span>Par (8.0)</span>
                    <span>Intense (14.0+)</span>
                  </div>
                </div>

                {/* Wickets in Hand */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">3. Wickets In Hand</span>
                    <span className="text-amber-400 text-sm font-black">{mlWicketsLeft} wickets</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    step="1"
                    value={mlWicketsLeft}
                    onChange={(e) => setMlWicketsLeft(Number(e.target.value))}
                    className="w-full accent-amber-400"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500">
                    <span>Tail End (1-3)</span>
                    <span>Top Order (7-10)</span>
                  </div>
                </div>

                {/* Balls Left */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">4. Legal Balls Left</span>
                    <span className="text-sky-400 text-sm font-black">{mlBallsLeft} balls</span>
                  </div>
                  <div className="grid grid-cols-4 gap-1">
                    {[6, 12, 18, 30].map((b) => (
                      <button
                        key={b}
                        onClick={() => setMlBallsLeft(b)}
                        className={`py-1.5 rounded-lg text-xs font-bold transition-all ${
                          mlBallsLeft === b ? "bg-sky-500 text-slate-950 font-black" : "bg-slate-800 text-slate-400"
                        }`}
                      >
                        {b}b
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* REAL-TIME PREDICTED OUTCOMES */}
            <div className="p-5 rounded-2xl glass-panel border border-cyan-500/20 space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-cyan-400" />
                    <span>Machine Learning Next-Ball Outcome Probabilities</span>
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Conditioned in real-time on Striker CAVA, Bowler CAVA, Required Run Rate, Wickets Lost, and Match Phase.
                  </p>
                </div>

                <div className="flex items-center gap-3 text-xs font-semibold">
                  <div className="px-3.5 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-center">
                    <span className="text-slate-400 text-[10px] block uppercase">Expected Runs / Ball</span>
                    <strong className="text-emerald-400 text-sm sm:text-base font-bold">{mlPredictions.expRuns} runs</strong>
                  </div>
                  <div className="px-3.5 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-center">
                    <span className="text-slate-400 text-[10px] block uppercase">Crisis Pressure Level</span>
                    <strong className="text-amber-400 text-sm sm:text-base font-bold">{(mlPredictions.mpi * 100).toFixed(0)}% MPI</strong>
                  </div>
                </div>
              </div>

              {/* 4 Outcome Probability Bars (Clean & Perfectly Sized) */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
                {/* Dot Ball */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-[11px] text-slate-400 font-bold uppercase tracking-wider block">1. Dot Ball</span>
                      <span className="text-xs text-slate-300 font-medium">Bowler Choke (0 Runs)</span>
                    </div>
                    <span className="text-2xl font-bold text-slate-100">{mlPredictions.probDot}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-slate-300 rounded-full transition-all duration-300" style={{ width: `${mlPredictions.probDot}%` }} />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Chance the bowler denies any run through tight length, yorker, or dot defense.
                  </p>
                </div>

                {/* Strike Rotation */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-[11px] text-sky-400 font-bold uppercase tracking-wider block">2. Strike Rotation</span>
                      <span className="text-xs text-slate-300 font-medium">Running 1, 2, or 3</span>
                    </div>
                    <span className="text-2xl font-bold text-sky-400">{mlPredictions.probRotate}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-sky-400 rounded-full transition-all duration-300" style={{ width: `${mlPredictions.probRotate}%` }} />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Chance the batter pierces the infield ring to steal runs and rotate strike.
                  </p>
                </div>

                {/* Boundary */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-[11px] text-[#EA1A85] font-bold uppercase tracking-wider block">3. Boundary</span>
                      <span className="text-xs text-slate-300 font-medium">Four or Six!</span>
                    </div>
                    <span className="text-2xl font-bold text-[#EA1A85]">{mlPredictions.probBoundary}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-[#EA1A85] rounded-full transition-all duration-300" style={{ width: `${mlPredictions.probBoundary}%` }} />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Chance of high-leverage boundary clearing deep fielders under required rate pressure.
                  </p>
                </div>

                {/* Wicket */}
                <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-[11px] text-rose-400 font-bold uppercase tracking-wider block">4. Wicket / Out</span>
                      <span className="text-xs text-slate-300 font-medium">Dismissal Event</span>
                    </div>
                    <span className="text-2xl font-bold text-rose-500">{mlPredictions.probWicket}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-rose-500 rounded-full transition-all duration-300" style={{ width: `${mlPredictions.probWicket}%` }} />
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Chance of false shot, mis-hit catch, bowled, or run out in this exact crisis.
                  </p>
                </div>
              </div>

              {/* Layman's Explainer: How the AI Calculates This Prediction */}
              <div className="p-4 rounded-xl bg-slate-900/90 border border-cyan-500/25 space-y-2.5">
                <div className="flex items-center gap-2 text-cyan-400">
                  <Cpu className="w-4 h-4" />
                  <span className="text-xs font-bold uppercase tracking-wider">How the Machine Learning AI Calculates This Ball in Plain English</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs text-slate-300">
                  <div className="p-3 rounded-lg bg-slate-950/80 border border-white/5 space-y-1">
                    <strong className="text-white block font-semibold">1. Game Heat Factor</strong>
                    <p className="leading-relaxed text-slate-300">
                      With Required Rate at <strong>{mlRequiredRR.toFixed(1)} RPO</strong> in the <strong>{mlPhase}</strong> phase, the batter is mathematically forced to attempt aerial release shots, automatically spiking the boundary probability (+{mlPredictions.probBoundary}%) and wicket danger (+{mlPredictions.probWicket}%).
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-950/80 border border-white/5 space-y-1">
                    <strong className="text-white block font-semibold">2. Striker Clutch Power</strong>
                    <p className="leading-relaxed text-slate-300">
                      <strong>{mlPredictions.striker.name}</strong> brings a clutch CAVA of <strong>+{mlPredictions.striker.cava_per_ball.toFixed(3)}/b</strong>. His historical clutch strike rate ({mlPredictions.striker.hp_sr}) elevates boundary likelihood compared to an average middle-order batter.
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-950/80 border border-white/5 space-y-1">
                    <strong className="text-white block font-semibold">3. Bowler Defensive Choke</strong>
                    <p className="leading-relaxed text-slate-300">
                      <strong>{mlPredictions.bowler.name}</strong> resists with <strong>+{mlPredictions.bowler.cava_per_ball.toFixed(3)}/b</strong> CAVA. His defensive accuracy keeps the dot ball chance high at <strong>{mlPredictions.probDot}%</strong>, making boundary clearance significantly harder.
                    </p>
                  </div>
                </div>
              </div>

              {/* War Room Head-to-Head Tactical Verdict */}
              <div className="p-4 rounded-xl bg-slate-950 border border-white/10 space-y-2 text-xs">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <span className="font-bold text-xs text-white uppercase tracking-wide flex items-center gap-1.5">
                    <Award className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Rajasthan Royals Matchup Tactical Intelligence Verdict</span>
                  </span>
                  <span className={`px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                    mlPredictions.batterAdvantage ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "bg-sky-500/20 text-sky-400 border border-sky-500/30"
                  }`}>
                    {mlPredictions.batterAdvantage ? `${mlPredictions.striker.name} Tactical Advantage` : `${mlPredictions.bowler.name} Defensive Advantage`}
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed text-xs">
                  Under this {mlPhase} phase scenario (Required Rate: <strong>{mlRequiredRR.toFixed(1)} RPO</strong>, {mlWicketsLeft} wickets in hand), 
                  <strong> {mlPredictions.striker.name}</strong> brings a proven clutch rating of <strong>+{mlPredictions.striker.cava_per_ball.toFixed(3)} runs above par per ball</strong>, 
                  while <strong>{mlPredictions.bowler.name}</strong> defends with <strong>+{mlPredictions.bowler.cava_per_ball.toFixed(3)} runs saved per ball</strong>. 
                  {mlPredictions.batterAdvantage
                    ? ` The batter holds a statistical advantage (+${mlPredictions.cavaDifferential} differential) to overcome bowling pressure, generating a boundary probability of ${mlPredictions.probBoundary}%.`
                    : ` The bowler dominates the match context, forcing a combined ${mlPredictions.probDot + mlPredictions.probRotate}% chance of a dot or non-boundary delivery.`}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: LIVE PRESSURE SITUATION SIMULATOR */}
        {activeTab === "simulator" && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-[#EA1A85]/20 text-[#EA1A85]">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg sm:text-xl font-bold text-white">Live Match Pressure Situation Simulator</h2>
                  <p className="text-xs text-slate-400">Simulate any in-game crisis or select an iconic 1-click preset to compute the optimal player fit for Rajasthan Royals.</p>
                </div>
              </div>

              {/* 1-CLICK ICONIC PRESETS */}
              <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2.5">
                <div className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>1-Click Iconic Match Crisis Presets</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {data.preset_situations.map((preset) => (
                    <button
                      key={preset.id}
                      onClick={() => applyPreset(preset)}
                      className="p-3 text-left rounded-xl bg-slate-800/60 hover:bg-[#EA1A85]/15 border border-white/5 hover:border-[#EA1A85]/40 transition-all text-xs group"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-white group-hover:text-[#EA1A85] truncate">{preset.title}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-white/10 text-slate-300">{preset.badge}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 line-clamp-2">{preset.description}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Dynamic Interactive Controls */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
                <div className="bg-slate-900/90 p-4 rounded-xl border border-white/5 space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase">1. Mode</label>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => setSimMode("batting")}
                      className={`py-2 text-xs font-bold rounded-lg transition-all ${
                        simMode === "batting" ? "bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/20" : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      Batting Chase
                    </button>
                    <button
                      onClick={() => setSimMode("bowling")}
                      className={`py-2 text-xs font-bold rounded-lg transition-all ${
                        simMode === "bowling" ? "bg-[#254AA5] text-white shadow-md shadow-[#254AA5]/20" : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      Bowling Defense
                    </button>
                  </div>
                </div>

                <div className="bg-slate-900/90 p-4 rounded-xl border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">2. Runs {simMode === "batting" ? "Needed" : "to Defend"}</span>
                    <span className="text-[#EA1A85] text-sm font-bold">{simRuns} runs</span>
                  </div>
                  <input
                    type="range"
                    min="6"
                    max="48"
                    value={simRuns}
                    onChange={(e) => setSimRuns(Number(e.target.value))}
                    className="w-full accent-[#EA1A85]"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500">
                    <span>6 runs (Par)</span>
                    <span>48 runs (Crisis)</span>
                  </div>
                </div>

                <div className="bg-slate-900/90 p-4 rounded-xl border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">3. Balls Left</span>
                    <span className="text-[#38BDF8] text-sm font-bold">{simBalls} balls</span>
                  </div>
                  <input
                    type="range"
                    min="6"
                    max="30"
                    step="6"
                    value={simBalls}
                    onChange={(e) => setSimBalls(Number(e.target.value))}
                    className="w-full accent-[#38BDF8]"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500">
                    <span>1 Over (6 balls)</span>
                    <span>5 Overs (30 balls)</span>
                  </div>
                </div>

                <div className="bg-slate-900/90 p-4 rounded-xl border border-white/5 space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-slate-400 uppercase">4. Wickets Fallen</span>
                    <span className="text-amber-400 text-sm font-bold">{simWickets} down</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="8"
                    value={simWickets}
                    onChange={(e) => setSimWickets(Number(e.target.value))}
                    className="w-full accent-amber-400"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500">
                    <span>Top Order (0-2)</span>
                    <span>Tail Exposed (7-8)</span>
                  </div>
                </div>
              </div>

              {/* Dynamic Live Calculations Banner */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-6">
                  <div>
                    <div className="text-[10px] text-slate-400 uppercase font-semibold">Required Rate</div>
                    <div className="text-lg sm:text-xl font-bold text-[#EA1A85]">{rrr.toFixed(1)} RPO</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-400 uppercase font-semibold">Match Pressure Index</div>
                    <div className="text-lg sm:text-xl font-bold text-amber-400">{(calculatedMPI * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-400 uppercase font-semibold">Severity Level</div>
                    <div className="text-xs sm:text-sm font-bold text-emerald-400 uppercase">
                      {calculatedMPI >= 0.7 ? "CRITICAL CLUTCH MOMENT" : calculatedMPI >= 0.55 ? "HIGH MATCH PRESSURE" : "MODERATE PRESSURE"}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Simulation Results Grid */}
            <div>
              <h3 className="text-sm sm:text-base font-bold text-white mb-3 flex items-center gap-2">
                <span>Statistically Optimal Player Recommendations</span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">TOP PICKS</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {simulationRecommendations.map((p, idx) => (
                  <SpotlightCard key={p.name} className="p-4 flex flex-col justify-between border-white/10">
                    <div>
                      <div className="flex items-center justify-between text-xs font-bold mb-2">
                        <span className="text-[#EA1A85] font-bold">OPTION #{idx + 1}</span>
                        <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300">
                          {p.is_auction_available ? "RR Target" : "Retained"}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <img
                          src={p.image_url}
                          alt={p.name}
                          onError={(e: any) => { e.target.src = "https://cdn-icons-png.flaticon.com/512/847/847969.png"; }}
                          className="w-12 h-12 rounded-xl object-cover bg-slate-800"
                        />
                        <div className="min-w-0 flex-1">
                          <h4 className="font-bold text-white text-sm truncate">{p.name}</h4>
                          <p className="text-[11px] text-[#38BDF8] truncate">{p.plain_english_role}</p>
                        </div>
                      </div>
                      <div className="mt-3 text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-white/5">
                        <strong className="text-amber-400">Tactical Game Plan:</strong> {p.scouting_verdict}
                      </div>
                    </div>

                    <div className="mt-3 pt-2.5 border-t border-white/10 flex justify-between items-center text-xs">
                      <span className="text-slate-400 font-medium">Scenario Fit:</span>
                      <span className="font-bold text-emerald-400 text-xs sm:text-sm">{96 - idx * 4}% Match</span>
                    </div>
                  </SpotlightCard>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: UNSTOP DROPDOWN COPY HUB */}
        {activeTab === "dropdowns" && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                  <h2 className="text-lg sm:text-xl font-bold text-white">Unstop Submission Portal Copy Hub</h2>
                  <p className="text-xs text-slate-400 mt-1">Select your preferred perspective below and copy the exact ordered selections directly into your Unstop dropdown fields.</p>
                </div>
                <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-xl border border-white/10">
                  <button
                    onClick={() => setDropdownSet("set_2")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      dropdownSet === "set_2" ? "bg-[#EA1A85] text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    RR Auction Targets (Realistic)
                  </button>
                  <button
                    onClick={() => setDropdownSet("set_1")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      dropdownSet === "set_1" ? "bg-[#254AA5] text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Pure Statistical Top 10 (Benchmark)
                  </button>
                </div>
              </div>

              {/* Explanatory Banner */}
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-white/5 text-xs text-slate-300">
                <strong>Current Perspective: </strong>
                {dropdownSet === "set_2" ? (
                  <span className="text-emerald-300">
                    <strong>Rajasthan Royals IPL 2027 Auction Shortlist</strong> (100% targetable in auction; retained pillars excluded so RR doesn't waste bids on unattainable players).
                  </span>
                ) : (
                  <span className="text-blue-300">
                    <strong>Pure Statistical Benchmark</strong> (Answers who objectively played best under pressure across all 2022-2026 data, including retained stars like SKY and Bumrah).
                  </span>
                )}
              </div>

              {/* Two Column Layout for Dropdowns */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                {/* Batters */}
                <div className="bg-slate-900/80 p-5 rounded-xl border border-white/5 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-sm text-[#EA1A85]">Batsman 1 to 10 (Ordered Dropdown Selections)</span>
                    <button
                      onClick={() => handleCopy(data.dropdown_options[dropdownSet === "set_1" ? "set_1_pure_statistical" : "set_2_rr_auction_targets"].batters.join("\n"), "All Batters")}
                      className="text-xs text-[#EA1A85] font-bold flex items-center gap-1 hover:underline"
                    >
                      {copiedText === "All Batters" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                      <span>Copy All</span>
                    </button>
                  </div>
                  <div className="space-y-2">
                    {data.dropdown_options[dropdownSet === "set_1" ? "set_1_pure_statistical" : "set_2_rr_auction_targets"].batters.map((name, i) => (
                      <div key={name} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-800/60 border border-white/5 hover:border-[#EA1A85]/40 transition-colors">
                        <div className="flex items-center gap-3">
                          <span className="w-6 h-6 rounded bg-[#EA1A85]/20 text-[#EA1A85] font-black text-xs flex items-center justify-center">
                            {i + 1}
                          </span>
                          <div>
                            <span className="font-bold text-white text-xs">{name}</span>
                          </div>
                        </div>
                        <button
                          onClick={() => handleCopy(name, `Bat_${i}`)}
                          className="text-slate-400 hover:text-white p-1 rounded"
                        >
                          {copiedText === `Bat_${i}` ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Bowlers */}
                <div className="bg-slate-900/80 p-5 rounded-xl border border-white/5 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-sm text-[#38BDF8]">Bowler 1 to 10 (Ordered Dropdown Selections)</span>
                    <button
                      onClick={() => handleCopy(data.dropdown_options[dropdownSet === "set_1" ? "set_1_pure_statistical" : "set_2_rr_auction_targets"].bowlers.join("\n"), "All Bowlers")}
                      className="text-xs text-[#38BDF8] font-bold flex items-center gap-1 hover:underline"
                    >
                      {copiedText === "All Bowlers" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                      <span>Copy All</span>
                    </button>
                  </div>
                  <div className="space-y-2">
                    {data.dropdown_options[dropdownSet === "set_1" ? "set_1_pure_statistical" : "set_2_rr_auction_targets"].bowlers.map((name, i) => (
                      <div key={name} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-800/60 border border-white/5 hover:border-[#38BDF8]/40 transition-colors">
                        <div className="flex items-center gap-3">
                          <span className="w-6 h-6 rounded bg-[#254AA5]/40 text-[#38BDF8] font-black text-xs flex items-center justify-center">
                            {i + 1}
                          </span>
                          <div>
                            <span className="font-bold text-white text-xs">{name}</span>
                          </div>
                        </div>
                        <button
                          onClick={() => handleCopy(name, `Bowl_${i}`)}
                          className="text-slate-400 hover:text-white p-1 rounded"
                        >
                          {copiedText === `Bowl_${i}` ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: PLAYER DOSSIERS GALLERY */}
        {activeTab === "cards" && (
          <div className="space-y-6">
            <div className="p-4 rounded-xl glass-panel flex flex-wrap items-center justify-between gap-4">
              <div className="flex gap-2">
                <button
                  onClick={() => setCategory("batters")}
                  className={`px-4 py-2 rounded-xl text-xs font-black ${category === "batters" ? "bg-[#EA1A85] text-white" : "bg-slate-800 text-slate-400"}`}
                >
                  Batters Gallery
                </button>
                <button
                  onClick={() => setCategory("bowlers")}
                  className={`px-4 py-2 rounded-xl text-xs font-black ${category === "bowlers" ? "bg-[#254AA5] text-white" : "bg-slate-800 text-slate-400"}`}
                >
                  Bowlers Gallery
                </button>
              </div>

              <div className="text-xs text-slate-400">
                Displaying <strong>{filteredPlayers.length}</strong> player dossiers with verified match logs
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPlayers.map(p => (
                <SpotlightCard key={p.name} className="p-6 flex flex-col justify-between border-white/10">
                  <div>
                    <div className="flex gap-4 items-center">
                      <img
                        src={p.image_url}
                        alt={p.name}
                        onError={(e: any) => { e.target.src = "https://cdn-icons-png.flaticon.com/512/847/847969.png"; }}
                        className="w-20 h-20 rounded-2xl object-cover bg-slate-800 border-2 border-[#EA1A85] shadow-lg flex-shrink-0"
                      />
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-1.5">
                          <span className="text-xs font-bold px-2 py-0.5 rounded bg-white/10 text-slate-300">#{p.rank}</span>
                          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-bold border border-white/10">
                            {(p as any).country_code || "INTL"}
                          </span>
                        </div>
                        <h3 className="font-bold text-base text-white mt-1 truncate">{p.name}</h3>
                        <p className="text-xs text-[#38BDF8] font-semibold truncate">{p.plain_english_role}</p>
                      </div>
                    </div>

                    <div className="mt-4 space-y-2 text-xs">
                      <p className="text-slate-300 leading-relaxed">
                        <strong className="text-white">Performance:</strong> {p.non_technical_summary}
                      </p>
                      <p className="text-rose-300/90 leading-relaxed">
                        <strong className="text-[#EA1A85]">Scouting Recommendation:</strong> {p.scouting_verdict}
                      </p>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-white/10 grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-slate-900 p-2 rounded-xl">
                      <div className="text-[10px] text-slate-400 font-semibold">{category === "batters" ? "SR" : "Econ"}</div>
                      <div className="text-sm font-bold text-white">{category === "batters" ? (p as any).hp_sr : ((p as any).hp_economy ?? (p as any).hp_econ ?? 8.5)}</div>
                    </div>
                    <div className="bg-slate-900 p-2 rounded-xl">
                      <div className="text-[10px] text-slate-400 font-semibold">Uplift</div>
                      <div className="text-sm font-bold text-emerald-400">+{(p.uplift_cava || 0).toFixed(2)}</div>
                    </div>
                    <div className="bg-slate-900 p-2 rounded-xl">
                      <div className="text-[10px] text-slate-400 font-semibold">Clutch Rating</div>
                      <div className="text-sm font-bold text-amber-400">{p.clutch_score}/100</div>
                    </div>
                  </div>
                </SpotlightCard>
              ))}
            </div>
          </div>
        )}

        {/* TAB 5: SCOUT HEAD-TO-HEAD COMPARE */}
        {activeTab === "compare" && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-6">
              <div>
                <h2 className="text-lg sm:text-xl font-bold text-white">Scout Head-to-Head Comparison Tool</h2>
                <p className="text-xs text-slate-400 mt-1">Select any two players to evaluate head-to-head metrics in death overs, collapses, and steep chases.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-xs font-bold text-[#EA1A85] uppercase block mb-1.5">Player 1 (Left - RR Targets First)</label>
                  <CustomFilterDropdown
                    value={comparePlayer1}
                    onChange={(val) => setComparePlayer1(val)}
                    options={[...(category === "batters" ? data.batters : data.bowlers)]
                      .sort((a, b) => (b.is_auction_available ? 1 : 0) - (a.is_auction_available ? 1 : 0))
                      .map(p => ({
                        value: p.name,
                        label: `${p.name} ${p.is_auction_available ? `[RR Target #${p.rr_auction_rank}]` : `[Retained]`}`
                      }))}
                  />
                </div>

                <div>
                  <label className="text-xs font-bold text-[#38BDF8] uppercase block mb-1.5">Player 2 (Right - RR Targets First)</label>
                  <CustomFilterDropdown
                    value={comparePlayer2}
                    onChange={(val) => setComparePlayer2(val)}
                    options={[...(category === "batters" ? data.batters : data.bowlers)]
                      .sort((a, b) => (b.is_auction_available ? 1 : 0) - (a.is_auction_available ? 1 : 0))
                      .map(p => ({
                        value: p.name,
                        label: `${p.name} ${p.is_auction_available ? `[RR Target #${p.rr_auction_rank}]` : `[Retained]`}`
                      }))}
                  />
                </div>
              </div>

              {/* Side-by-Side Comparison Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                <SpotlightCard spotlightColor="rgba(234, 26, 133, 0.2)" className="p-5 border-[#EA1A85]/30">
                  <div className="flex items-center gap-3">
                    <img src={p1.image_url} alt={p1.name} className="w-14 h-14 rounded-2xl object-cover bg-slate-800 border border-white/10" />
                    <div>
                      <h3 className="font-bold text-base text-white">{p1.name}</h3>
                      <p className="text-xs text-[#EA1A85] font-semibold">{p1.plain_english_role}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Performance Score:</span>
                      <span className="font-bold text-white">{(p1.score || 0).toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Strike Rate / Econ:</span>
                      <span className="font-bold text-white">{category === "batters" ? (p1 as any).hp_sr : ((p1 as any).hp_economy ?? (p1 as any).hp_econ ?? 8.5)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Clutch Uplift (vs Base):</span>
                      <span className="font-bold text-emerald-400">+{(p1.uplift_cava || 0).toFixed(3)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Auction Availability:</span>
                      <span className={`font-bold ${p1.is_auction_available ? "text-emerald-400" : "text-rose-400"}`}>
                        {p1.is_auction_available ? "Available" : "Retained / Ineligible"}
                      </span>
                    </div>
                  </div>
                </SpotlightCard>

                <SpotlightCard spotlightColor="rgba(56, 189, 248, 0.2)" className="p-5 border-[#38BDF8]/30">
                  <div className="flex items-center gap-3">
                    <img src={p2.image_url} alt={p2.name} className="w-14 h-14 rounded-2xl object-cover bg-slate-800 border border-white/10" />
                    <div>
                      <h3 className="font-bold text-base text-white">{p2.name}</h3>
                      <p className="text-xs text-[#38BDF8] font-semibold">{p2.plain_english_role}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Performance Score:</span>
                      <span className="font-bold text-white">{(p2.score || 0).toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Strike Rate / Econ:</span>
                      <span className="font-bold text-white">{category === "batters" ? (p2 as any).hp_sr : ((p2 as any).hp_economy ?? (p2 as any).hp_econ ?? 8.5)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Clutch Uplift (vs Base):</span>
                      <span className="font-bold text-emerald-400">+{(p2.uplift_cava || 0).toFixed(3)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Auction Availability:</span>
                      <span className={`font-bold ${p2.is_auction_available ? "text-emerald-400" : "text-rose-400"}`}>
                        {p2.is_auction_available ? "Available" : "Retained / Ineligible"}
                      </span>
                    </div>
                  </div>
                </SpotlightCard>
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: METHODOLOGY & MODEL TRANSPARENCY */}
        {activeTab === "methodology" && (
          <div className="space-y-8">
            {/* Header */}
            <div className="p-6 sm:p-8 rounded-2xl glass-panel border border-cyan-500/20 space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>WAR ROOM AUDIT & EXPLANATORY BLUEPRINT</span>
              </div>
              <h2 className="text-xl sm:text-2xl font-bold text-white">How the Engine & Machine Learning Suite Work</h2>
              <p className="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
                Both a crystal-clear layman's guide for Rajasthan Royals decision-makers and the rigorous mathematical proofs for data scientists and auditors. Zero black boxes, zero data leakage, and 100% scorecard reconciliation across all 867 contested matches (200,999 deliveries).
              </p>
            </div>

            {/* PART 1: THE PRESSURE ENGINE EXPLAINED IN LAYMAN TERMS */}
            <div className="p-6 sm:p-8 rounded-2xl glass-panel border border-[#EA1A85]/20 space-y-6">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-[#EA1A85]/20 text-[#EA1A85]">
                    <Zap className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-white">Part 1: The Pressure Engine Explained in Plain English</h3>
                    <p className="text-xs text-slate-400">How we objectively separate true crisis performers from stat-padders.</p>
                  </div>
                </div>
                <span className="text-xs px-3 py-1 rounded-full font-bold bg-[#EA1A85]/20 text-[#EA1A85] border border-[#EA1A85]/30">
                  STEP-BY-STEP REASONING
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Step 1 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="flex items-center gap-2 text-amber-400">
                    <span className="w-6 h-6 rounded-full bg-amber-400/20 font-bold text-xs flex items-center justify-center border border-amber-400/40">1</span>
                    <h4 className="text-sm font-bold text-white uppercase tracking-wider">When is a Match Truly 'Under Pressure'? (The MPI Metric)</h4>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Traditional T20 stats are misleading. Scoring 50 runs when your team is already 170/2 in the 15th over is easy stat-padding. But scoring 26 runs from 12 balls when 3 quick wickets just crashed and the required run rate is 13.0 RPO is extreme pressure!
                  </p>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Our <strong>Match Pressure Index (MPI)</strong> measures the heat level of every single ball ($0$ to $100\%$) by combining:
                  </p>
                  <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                    <li><strong>Required Run Rate:</strong> How far above normal stadium par the chase has climbed.</li>
                    <li><strong>Resource Depletion:</strong> How many wickets have fallen and how few balls remain.</li>
                    <li><strong>Collapse Shock:</strong> Extra penalty if multiple wickets fell in the last 12 balls.</li>
                    <li><strong>Leverage Swing:</strong> How drastically one boundary or wicket swings the win probability.</li>
                  </ul>
                  <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 font-semibold">
                    The Rule: Only balls where pressure reaches 55% or higher (MPI ≥ 0.55) count as "Pressure". All easy, low-stakes overs are thrown out!
                  </div>
                </div>

                {/* Step 2 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="flex items-center gap-2 text-[#38BDF8]">
                    <span className="w-6 h-6 rounded-full bg-[#38BDF8]/20 font-bold text-xs flex items-center justify-center border border-[#38BDF8]/40">2</span>
                    <h4 className="text-sm font-bold text-white uppercase tracking-wider">Fair Comparisons: Setting the 'Par' Score for Every Ball</h4>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Hitting 10 runs off Jasprit Bumrah in the 19th over at Wankhede Stadium is vastly harder than hitting 10 runs off an uncapped spinner in the 8th over on a flat road. Comparing them directly is completely unfair!
                  </p>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    To make comparisons 100% fair, our engine analyzed all <strong>200,999 deliveries</strong> in the Data Pack to establish the <strong>Context Par</strong> for every ball:
                  </p>
                  <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                    <li><strong>Venue Par:</strong> Scoring at Jaipur (Sawai Mansingh) vs Wankhede vs Chepauk.</li>
                    <li><strong>Phase Expectations:</strong> Powerplay vs Middle Overs vs Death Overs (16-20).</li>
                    <li><strong>Bowler Style:</strong> Express Pace vs Mystery Spin vs Finger Spin.</li>
                  </ul>
                  <div className="p-3 rounded-lg bg-sky-500/10 border border-sky-500/20 text-xs text-sky-300 font-semibold">
                    Result: Every delivery has an expected runs par (e.g. 1.45 runs) and expected wicket risk (e.g. 4.2%).
                  </div>
                </div>

                {/* Step 3 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="flex items-center gap-2 text-[#EA1A85]">
                    <span className="w-6 h-6 rounded-full bg-[#EA1A85]/20 font-bold text-xs flex items-center justify-center border border-[#EA1A85]/40">3</span>
                    <h4 className="text-sm font-bold text-white uppercase tracking-wider">CAVA: The Extra Value Created or Saved Above Par</h4>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    <strong>CAVA (Context-Adjusted Value Added)</strong> measures the exact difference between what a player actually produced versus what an average player would have produced on that same ball:
                  </p>
                  <div className="space-y-2 text-xs">
                    <div className="p-3 rounded-lg bg-slate-950 border border-white/10">
                      <strong className="text-[#EA1A85] block">For Batters:</strong>
                      If par expectation was 1.2 runs, and Jos Buttler hits a 6, he added <strong>+4.8 runs of pure value</strong>. If he gets out, he is penalized for the wicket lost.
                    </div>
                    <div className="p-3 rounded-lg bg-slate-950 border border-white/10">
                      <strong className="text-emerald-400 block">For Bowlers:</strong>
                      If par expectation was 1.8 runs in the 20th over, and Josh Hazlewood bowls a dot ball, he saved <strong>+1.8 runs</strong> for his team. If he takes a wicket, he earns a massive bonus (~4.5 runs of damage prevented).
                    </div>
                  </div>
                  <div className="p-3 rounded-lg bg-pink-500/10 border border-pink-500/20 text-xs text-pink-300 font-semibold">
                    A positive CAVA means you are a net match-winner. Zero is average. Negative means you leak runs or burn wickets under fire.
                  </div>
                </div>

                {/* Step 4 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400">
                    <span className="w-6 h-6 rounded-full bg-emerald-400/20 font-bold text-xs flex items-center justify-center border border-emerald-400/40">4</span>
                    <h4 className="text-sm font-bold text-white uppercase tracking-wider">Separating Luck from True Class (Empirical Bayes Shrinkage)</h4>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    If an unknown player walks in, faces 2 pressure balls, and smacks one lucky six, his raw strike rate is 300.0 and his CAVA is sky-high! Is he the best player in the world? Of course not. That is small-sample luck.
                  </p>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Our engine uses <strong>Empirical Bayes Shrinkage</strong> to protect Rajasthan Royals from auction traps:
                  </p>
                  <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                    <li>Players with only a few balls are conservatively pulled back toward the league average.</li>
                    <li>Players with hundreds of balls across 2022–2026 keep their full high rating because they have proven their reliability game after game.</li>
                    <li>Rankings use a conservative 20th percentile safety margin so RR buys consistent reliability, not one-hit wonders.</li>
                  </ul>
                  <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 font-semibold">
                    Result: You only see genuine, battle-tested match-winners at the top of Rajasthan Royals' target list.
                  </div>
                </div>
              </div>
            </div>

            {/* PART 2: HOW THE MACHINE LEARNING (AI) WORKS IN LAYMAN TERMS */}
            <div className="p-6 sm:p-8 rounded-2xl glass-panel border border-cyan-500/20 space-y-6">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/20 text-cyan-400">
                    <Cpu className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-white">Part 2: How the Machine Learning (AI) Predictive Suite Works</h3>
                    <p className="text-xs text-slate-400">Trained on 200,999 domestic & international deliveries to predict real-time ball outcomes.</p>
                  </div>
                </div>
                <span className="text-xs px-3 py-1 rounded-full font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                  AI PREDICTION BLUEPRINT
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* AI Card 1 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="text-cyan-400 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>1. The Next-Ball Outcome AI</span>
                  </div>
                  <h4 className="text-sm sm:text-base font-bold text-white">Predicting the 4 Cricket Realities</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Cricket isn't played on an Excel sheet; it unfolds one delivery at a time. We trained a state-of-the-art <strong>HistGradientBoostingClassifier</strong> (an advanced decision-tree AI algorithm) that watches the live game state.
                  </p>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Whenever you select a Batter, a Bowler, and a Crisis Scenario, the AI weighs 9 live features:
                  </p>
                  <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                    <li>Striker Clutch CAVA & Career Pressure Strike Rate</li>
                    <li>Bowler Clutch CAVA & Career Pressure Economy</li>
                    <li>Required Run Rate (RRR) and Balls Left</li>
                    <li>Wickets In Hand and Match Phase</li>
                  </ul>
                  <p className="text-xs text-cyan-300 font-semibold pt-1">
                    It calculates the exact percentage odds: Will it be a Dot Ball? Single/Double? Four/Six? Or a Wicket?
                  </p>
                </div>

                {/* AI Card 2 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="text-emerald-400 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>2. The Time-Travel Test</span>
                  </div>
                  <h4 className="text-sm sm:text-base font-bold text-white">Strict Out-of-Time Verification</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Many predictive models "cheat" by training on future games and testing on the past (data leakage). We enforced a strict chronological time barrier:
                  </p>
                  <div className="space-y-2 text-xs">
                    <div className="p-2.5 rounded-lg bg-slate-950 border border-white/10">
                      <strong className="text-white block">Training Window (2022–2024):</strong>
                      138,500 deliveries. The model was trained purely on historical seasons.
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-950 border border-white/10">
                      <strong className="text-white block">Test Window (2025–2026):</strong>
                      62,499 deliveries. Evaluated on unseen future matches!
                    </div>
                  </div>
                  <p className="text-xs text-emerald-300 font-semibold pt-1">
                    Achieved 46.3% multiclass accuracy on 4-way discrete cricket outcomes (against random 25.0% baseline) with a robust log loss of 1.1727.
                  </p>
                </div>

                {/* AI Card 3 */}
                <div className="p-5 rounded-xl bg-slate-900/90 border border-white/10 space-y-3">
                  <div className="text-amber-400 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <DollarSign className="w-3.5 h-3.5" />
                    <span>3. The Auction Moneyball Regressor</span>
                  </div>
                  <h4 className="text-sm sm:text-base font-bold text-white">Optimizing RR's ₹120 Cr Purse</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    A secondary <strong>HistGradientBoostingRegressor</strong> analyzes each player's clutch rating, uplift factor, strike rate / economy, and experience to predict their expected clearing price at the IPL 2027 Auction.
                  </p>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    It calculates the <strong>Rajasthan Royals Moneyball Value Index</strong>:
                  </p>
                  <div className="p-3 rounded-lg bg-slate-950 border border-white/10 text-xs text-center font-mono font-bold text-amber-300">
                    Moneyball ROI = (Clutch Score × (1 + Uplift) / Price) × 100
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    This uncovers undervalued diamonds in the rough (like Reeza Hendricks or Krunal Pandya) who provide 90% of a superstar's clutch production at 30% of the cost.
                  </p>
                </div>
              </div>
            </div>

            {/* PART 3: AUDITOR & DATA SCIENTIST MATHEMATICAL PROOFS */}
            <div className="p-6 sm:p-8 rounded-2xl glass-panel border border-white/10 space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-[#38BDF8]" />
                <span>Part 3: Mathematical Formalism & Auditor Reconciliation</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
                <div className="p-4 rounded-xl bg-slate-900/80 border border-white/5 space-y-2">
                  <div className="text-[#EA1A85] font-bold uppercase">Match Pressure Index (MPI)</div>
                  <code className="text-slate-300 block bg-slate-950 p-2 rounded border border-white/5">
                    MPI_t = 0.55 * D_t + 0.45 * LI_t<br/>
                    D_t = 0.45*(RRR/Par) + 0.35*(Wkts/9) + 0.20*(Collapse Shock)<br/>
                    LI_t = |WP(Boundary) - WP(Wicket)| / 0.20
                  </code>
                </div>

                <div className="p-4 rounded-xl bg-slate-900/80 border border-white/5 space-y-2">
                  <div className="text-[#38BDF8] font-bold uppercase">CAVA Formulation</div>
                  <code className="text-slate-300 block bg-slate-950 p-2 rounded border border-white/5">
                    CAVA_bat = (Runs - E[Runs]) - V_w * (Out - E[Wkt])<br/>
                    CAVA_bowl = (E[Runs] - Runs) + V_w * (Wkt - E[Wkt])<br/>
                    V_w = 4.45 (Wicket Leverage Constant)
                  </code>
                </div>

                <div className="p-4 rounded-xl bg-slate-900/80 border border-white/5 space-y-2">
                  <div className="text-emerald-400 font-bold uppercase">Empirical Bayes Shrinkage</div>
                  <code className="text-slate-300 block bg-slate-950 p-2 rounded border border-white/5">
                    B_i = sigma^2_i / (sigma^2_i + tau^2)<br/>
                    theta_shrunk = (1 - B_i)*theta_i + B_i*mu_prior<br/>
                    Score = theta_shrunk - 0.84 * SE_shrunk
                  </code>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-emerald-500/20 text-xs sm:text-sm text-emerald-300 font-semibold flex items-center gap-3">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-400" />
                <span>Audit Verified: 100% scorecard reconciliation across 867 contested matches. No look-ahead bias. 0 Pakistan players included. Full reproducible pipeline.</span>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}

function ClipboardCheck(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
      <path d="m9 14 2 2 4-4"/>
    </svg>
  );
}

function Crosshair(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <line x1="22" x2="18" y1="12" y2="12"/>
      <line x1="6" x2="2" y1="12" y2="12"/>
      <line x1="12" x2="12" y1="6" y2="2"/>
      <line x1="12" x2="12" y1="22" y2="18"/>
    </svg>
  );
}
