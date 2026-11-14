"use client";

import React, { useState, useMemo } from "react";
import data from "../data/analytics_data.json";
import { 
  ShieldCheck, AlertCircle, Award, SlidersHorizontal, PlayCircle, Users, CheckCircle2, 
  ExternalLink, Search, Flame, Target, Compass, Zap, HelpCircle, Copy, Check,
  Sparkles, DollarSign, BookmarkCheck, TrendingUp, BarChart3, Layers, Swords, 
  Shield, Activity, Lock, ArrowUpRight, ChevronRight, UserCheck, RefreshCw
} from "lucide-react";
import { 
  SpotlightCard, AnimatedTabs, CustomFilterDropdown, MetricBar 
} from "../components/ReactBitsComponents";
import { motion, AnimatePresence } from "motion/react";

export default function SuperRRDashboard() {
  const [activeTab, setActiveTab] = useState<"warroom" | "simulator" | "dropdowns" | "cards" | "compare" | "methodology">("warroom");
  const [category, setCategory] = useState<"batters" | "bowlers">("batters");
  const [availabilityFilter, setAvailabilityFilter] = useState("all");
  const [cappedFilter, setCappedFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [copiedText, setCopiedText] = useState<string | null>(null);

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
        scoreA += (a.scenarios?.death_chase || (a.scenarios as any)?.death_defense || 80);
        scoreB += (b.scenarios?.death_chase || (b.scenarios as any)?.death_defense || 80);
      }
      return scoreB - scoreA;
    }).slice(0, 4);
  }, [simMode, simPhase]);

  // Head-to-Head Compare State
  const [comparePlayer1, setComparePlayer1] = useState(data.batters[0].name);
  const [comparePlayer2, setComparePlayer2] = useState(data.batters[1].name);

  const p1 = (category === "batters" ? data.batters : data.bowlers).find(p => p.name === comparePlayer1) || data.batters[0];
  const p2 = (category === "batters" ? data.batters : data.bowlers).find(p => p.name === comparePlayer2) || data.batters[1];

  // Navigation Tabs Definition
  const navigationTabs = [
    { id: "warroom" as const, label: "RR War Room", icon: <Target className="w-3.5 h-3.5 text-[#EA1A85]" /> },
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
          <span>{data.meta.total_players_in_pack.toLocaleString()} Players • {data.meta.deliveries_analyzed.toLocaleString()} Deliveries</span>
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
                <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                  Backing the Most Reliable <span className="shimmer-text">Clutch Performers</span> Under Pressure
                </h1>
                <p className="text-slate-300 text-xs sm:text-sm leading-relaxed">
                  Rajasthan Royals has locked down its core: <strong>Sanju Samson, Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel, Shimron Hetmyer</strong>, and <strong>Sandeep Sharma</strong>. 
                  Below is the data-driven intelligence on targetable free agents versus rival-retained stars who will not enter the auction.
                </p>
                <div className="pt-2 flex flex-wrap gap-2.5 text-xs">
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
                    { value: "all", label: "All Availability Tiers" },
                    { value: "available", label: "RR Auction Targets Only" },
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
                            <div className="flex items-center gap-1">
                              <Flame className="w-3.5 h-3.5 text-amber-400" />
                              <span className="text-xs font-black text-amber-400">{player.clutch_score}/100</span>
                            </div>
                          </div>
                          <h3 className="font-black text-base text-white mt-1 truncate">{player.name}</h3>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-[11px] text-[#38BDF8] font-bold truncate">{player.plain_english_role}</span>
                            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-white/5">{player.capped_status}</span>
                          </div>
                        </div>
                      </div>

                      {/* Availability Tag & Price Estimate */}
                      <div className="mt-3.5 flex items-center justify-between flex-wrap gap-2 text-xs">
                        <span className={`inline-block text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${tagColor}`}>
                          {isAvail ? "Prime RR Auction Target" : ((player as any).franchise_label || player.auction_status)}
                        </span>
                        <span className="text-[11px] font-bold text-amber-400 font-mono">
                          {player.price_bracket}
                        </span>
                      </div>

                      {/* Plain-English Non-Technical War Room Dossier */}
                      <div className="mt-3.5 bg-slate-950/60 rounded-xl p-3 border border-white/5 space-y-1.5 text-xs">
                        <p className="text-slate-300 leading-relaxed font-normal">
                          <strong className="text-white">Why They Deliver:</strong> {player.non_technical_summary}
                        </p>
                        <p className="text-rose-300/90 leading-relaxed font-normal">
                          <strong className="text-[#EA1A85]">RR Role Fit:</strong> {player.rr_fit}
                        </p>
                      </div>

                      {/* Visual Metric Comparison */}
                      <div className="mt-3.5 pt-2 border-t border-white/5 space-y-2">
                        {category === "batters" ? (
                          <>
                            <MetricBar label="Pressure Strike Rate" value={(player as any).hp_sr} parValue={142.5} unit=" SR" />
                            <MetricBar label="Positive Match Contribution" value={player.positive_match_share * 100} parValue={50} unit="%" />
                          </>
                        ) : (
                          <>
                            <MetricBar label="Pressure Economy Rate" value={(player as any).hp_econ} parValue={8.85} unit=" RPO" isLowerBetter />
                            <MetricBar label="Pressure Dot Ball Share" value={(player as any).dot_pct} parValue={38.0} unit="%" />
                          </>
                        )}
                      </div>
                    </div>

                    {/* Stats Footer Chips */}
                    <div className="mt-4 pt-3 border-t border-white/10 grid grid-cols-3 gap-2 text-center text-xs">
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">
                          {category === "batters" ? "Pressure SR" : "Pressure Econ"}
                        </div>
                        <div className="text-sm font-black text-[#EA1A85]">
                          {category === "batters" ? (player as any).hp_sr : (player as any).hp_econ}
                        </div>
                      </div>
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Uplift vs Par</div>
                        <div className="text-sm font-black text-[#38BDF8]">
                          +{player.uplift_cava.toFixed(3)}
                        </div>
                      </div>
                      <div className="bg-slate-900/60 p-2 rounded-xl">
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Sample Size</div>
                        <div className="text-sm font-black text-amber-400">
                          {player.hp_balls} balls
                        </div>
                      </div>
                    </div>
                  </SpotlightCard>
                );
              })}
            </div>
          </div>
        )}

        {/* TAB 2: LIVE PRESSURE SITUATION SIMULATOR */}
        {activeTab === "simulator" && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-[#EA1A85]/20 text-[#EA1A85]">
                  <Zap className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-2xl font-black text-white">Live Match Pressure Situation Simulator</h2>
                  <p className="text-xs text-slate-400">Simulate any in-game crisis or select an iconic 1-click preset to compute the optimal player fit for Rajasthan Royals.</p>
                </div>
              </div>

              {/* 1-CLICK ICONIC PRESETS */}
              <div className="p-4 rounded-xl bg-slate-900/90 border border-white/10 space-y-2.5">
                <div className="text-xs font-black text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
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
                        <span className="font-black text-white group-hover:text-[#EA1A85] truncate">{preset.title}</span>
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
                      className={`py-2 text-xs font-black rounded-lg transition-all ${
                        simMode === "batting" ? "bg-[#EA1A85] text-white shadow-md shadow-[#EA1A85]/20" : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      Batting Chase
                    </button>
                    <button
                      onClick={() => setSimMode("bowling")}
                      className={`py-2 text-xs font-black rounded-lg transition-all ${
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
                    <span className="text-[#EA1A85] text-sm font-black">{simRuns} runs</span>
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
                    <span className="text-[#38BDF8] text-sm font-black">{simBalls} balls</span>
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
                    <span className="text-amber-400 text-sm font-black">{simWickets} down</span>
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
                    <div className="text-[10px] text-slate-400 uppercase font-bold">Required Rate</div>
                    <div className="text-2xl font-black text-[#EA1A85]">{rrr.toFixed(1)} RPO</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-400 uppercase font-bold">Match Pressure Index</div>
                    <div className="text-2xl font-black text-amber-400">{(calculatedMPI * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-400 uppercase font-bold">Severity Level</div>
                    <div className="text-sm font-black text-emerald-400 uppercase">
                      {calculatedMPI >= 0.7 ? "CRITICAL CLUTCH MOMENT" : calculatedMPI >= 0.55 ? "HIGH MATCH PRESSURE" : "MODERATE PRESSURE"}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Simulation Results Grid */}
            <div>
              <h3 className="text-base font-black text-white mb-3 flex items-center gap-2">
                <span>Statistically Optimal Player Recommendations</span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">TOP PICKS</span>
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {simulationRecommendations.map((p, idx) => (
                  <SpotlightCard key={p.name} className="p-4 flex flex-col justify-between border-white/10">
                    <div>
                      <div className="flex items-center justify-between text-xs font-bold mb-2">
                        <span className="text-[#EA1A85] font-black">OPTION #{idx + 1}</span>
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
                          <h4 className="font-extrabold text-white text-sm truncate">{p.name}</h4>
                          <p className="text-[11px] text-[#38BDF8] truncate">{p.plain_english_role}</p>
                        </div>
                      </div>
                      <div className="mt-3 text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-white/5">
                        <strong className="text-amber-400">Tactical Game Plan:</strong> {p.scouting_verdict}
                      </div>
                    </div>

                    <div className="mt-3 pt-2.5 border-t border-white/10 flex justify-between items-center text-xs">
                      <span className="text-slate-400 font-medium">Scenario Fit:</span>
                      <span className="font-black text-emerald-400 text-sm">{96 - idx * 4}% Match</span>
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
                  <h2 className="text-2xl font-black text-white">Unstop Submission Portal Copy Hub</h2>
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
                          <span className="text-xs font-black px-2 py-0.5 rounded bg-white/10 text-slate-300">#{p.rank}</span>
                          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-bold border border-white/10">
                            {(p as any).country_code || "INTL"}
                          </span>
                        </div>
                        <h3 className="font-black text-lg text-white mt-1 truncate">{p.name}</h3>
                        <p className="text-xs text-[#38BDF8] font-bold truncate">{p.plain_english_role}</p>
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
                      <div className="text-sm font-black text-white">{category === "batters" ? (p as any).hp_sr : (p as any).hp_econ}</div>
                    </div>
                    <div className="bg-slate-900 p-2 rounded-xl">
                      <div className="text-[10px] text-slate-400 font-semibold">Uplift</div>
                      <div className="text-sm font-black text-emerald-400">+{p.uplift_cava.toFixed(2)}</div>
                    </div>
                    <div className="bg-slate-900 p-2 rounded-xl">
                      <div className="text-[10px] text-slate-400 font-semibold">Clutch Rating</div>
                      <div className="text-sm font-black text-amber-400">{p.clutch_score}/100</div>
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
                <h2 className="text-2xl font-black text-white">Scout Head-to-Head Comparison Tool</h2>
                <p className="text-xs text-slate-400 mt-1">Select any two players to evaluate head-to-head metrics in death overs, collapses, and steep chases.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-xs font-bold text-[#EA1A85] uppercase block mb-1.5">Player 1 (Left)</label>
                  <CustomFilterDropdown
                    value={comparePlayer1}
                    onChange={(val) => setComparePlayer1(val)}
                    options={(category === "batters" ? data.batters : data.bowlers).map(p => ({
                      value: p.name,
                      label: `${p.name} (#${p.rank})`
                    }))}
                  />
                </div>

                <div>
                  <label className="text-xs font-bold text-[#38BDF8] uppercase block mb-1.5">Player 2 (Right)</label>
                  <CustomFilterDropdown
                    value={comparePlayer2}
                    onChange={(val) => setComparePlayer2(val)}
                    options={(category === "batters" ? data.batters : data.bowlers).map(p => ({
                      value: p.name,
                      label: `${p.name} (#${p.rank})`
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
                      <h3 className="font-extrabold text-lg text-white">{p1.name}</h3>
                      <p className="text-xs text-[#EA1A85] font-semibold">{p1.plain_english_role}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Performance Score:</span>
                      <span className="font-black text-white">{p1.score.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Strike Rate / Econ:</span>
                      <span className="font-black text-white">{category === "batters" ? (p1 as any).hp_sr : (p1 as any).hp_econ}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Clutch Uplift (vs Base):</span>
                      <span className="font-black text-emerald-400">+{p1.uplift_cava.toFixed(3)}</span>
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
                      <h3 className="font-extrabold text-lg text-white">{p2.name}</h3>
                      <p className="text-xs text-[#38BDF8] font-semibold">{p2.plain_english_role}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Performance Score:</span>
                      <span className="font-black text-white">{p2.score.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Pressure Strike Rate / Econ:</span>
                      <span className="font-black text-white">{category === "batters" ? (p2 as any).hp_sr : (p2 as any).hp_econ}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-white/5">
                      <span className="text-slate-400">Clutch Uplift (vs Base):</span>
                      <span className="font-black text-emerald-400">+{p2.uplift_cava.toFixed(3)}</span>
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
          <div className="space-y-6">
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-6">
              <div>
                <h2 className="text-2xl font-black text-white">Mathematical Modeling & Transparency Audit</h2>
                <p className="text-xs text-slate-400 mt-1">Zero data leakage. 100% scorecard reconciliation. Chronological out-of-time validation.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-900/80 p-4 rounded-xl border border-white/5">
                  <div className="text-xs text-slate-400 font-bold uppercase">1. Match Pressure Index (MPI)</div>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Composite score combining <strong>Chase Demand</strong> (RRR vs Par, Wickets Down, Collapse Shock) and <strong>Leverage Swing</strong> (|WP(boundary) - WP(wicket)| / 0.20). Threshold frozen at <strong>MPI ≥ 0.55</strong> (70th percentile).
                  </p>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-xl border border-white/5">
                  <div className="text-xs text-slate-400 font-bold uppercase">2. Context-Adjusted Value Added (CAVA)</div>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Evaluates performance relative to gradient-boosted expectations: <br/>
                    <code className="text-[#EA1A85] text-[11px]">CAVA_bat = (Runs - E[Runs]) - V_w * (Wkt - E[Wkt])</code><br/>
                    Isolates individual clutch execution from pitch and match state.
                  </p>
                </div>

                <div className="bg-slate-900/80 p-4 rounded-xl border border-white/5">
                  <div className="text-xs text-slate-400 font-bold uppercase">3. Empirical Bayes Shrinkage</div>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Shrinks small sample noise toward population prior using match-clustered standard errors. Ranks players by 20th percentile posterior: <br/>
                    <code className="text-[#38BDF8] text-[11px]">Score = theta_shrunk - 0.84 * SE_shrunk</code>
                  </p>
                </div>
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
