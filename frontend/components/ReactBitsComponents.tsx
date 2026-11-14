"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, Check, Search } from "lucide-react";

/**
 * React Bits: 3D Tilt + Cursor Spotlight Card
 * Emulates the React Bits SpotlightCard with dynamic mouse-tracking lighting and spring 3D tilt.
 */
export function SpotlightCard({
  children,
  className = "",
  spotlightColor = "rgba(234, 26, 133, 0.2)"
}: {
  children: React.ReactNode;
  className?: string;
  spotlightColor?: string;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [coords, setCoords] = useState({ x: -1000, y: -1000 });
  const [isHovered, setIsHovered] = useState(false);
  const [tilt, setTilt] = useState({ rotateX: 0, rotateY: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setCoords({ x, y });

    // Calculate subtle 3D tilt
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -4.5;
    const rotateY = ((x - centerX) / centerX) * 4.5;
    setTilt({ rotateX, rotateY });
  };

  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => {
    setIsHovered(false);
    setCoords({ x: -1000, y: -1000 });
    setTilt({ rotateX: 0, rotateY: 0 });
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      animate={{
        rotateX: isHovered ? tilt.rotateX : 0,
        rotateY: isHovered ? tilt.rotateY : 0,
        y: isHovered ? -4 : 0,
        transition: { type: "spring", stiffness: 350, damping: 25 }
      }}
      style={{ transformStyle: "preserve-3d" }}
      className={`relative overflow-hidden rounded-2xl bg-slate-900/80 border border-white/10 transition-colors duration-200 ${className}`}
    >
      {/* Dynamic Cursor Spotlight Layer */}
      <div
        className="pointer-events-none absolute -inset-px transition-opacity duration-300"
        style={{
          opacity: isHovered ? 1 : 0,
          background: `radial-gradient(450px circle at ${coords.x}px ${coords.y}px, ${spotlightColor}, transparent 65%)`
        }}
      />
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}

/**
 * React Bits: Animated Pill Tabs
 * Sliding animated pill that tracks the active navigation tab.
 */
export function AnimatedTabs<T extends string>({
  tabs,
  activeTab,
  onTabChange,
  className = ""
}: {
  tabs: { id: T; label: string; icon: React.ReactNode }[];
  activeTab: T;
  onTabChange: (id: T) => void;
  className?: string;
}) {
  return (
    <div className={`flex items-center gap-1.5 p-1.5 rounded-xl bg-slate-950/80 border border-white/10 ${className}`}>
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`relative flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-colors z-10 ${
              isActive ? "text-white" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="active-pill"
                transition={{ type: "spring", bounce: 0.2, duration: 0.45 }}
                className="absolute inset-0 rounded-lg bg-gradient-to-r from-[#EA1A85] to-[#254AA5] shadow-lg shadow-[#EA1A85]/20 -z-10"
              />
            )}
            <span className="flex-shrink-0">{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}

/**
 * Custom Dropdown Select (Immune to white-on-white text bug)
 * Fully styled popover dropdown with smooth animations and zero OS styling conflicts.
 */
export function CustomFilterDropdown({
  label,
  value,
  options,
  onChange,
  icon,
  className = ""
}: {
  label?: string;
  value: string;
  options: { value: string; label: string; badge?: string }[];
  onChange: (val: string) => void;
  icon?: React.ReactNode;
  className?: string;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selectedOption = options.find((o) => o.value === value) || options[0];

  return (
    <div ref={dropdownRef} className={`relative ${className}`}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between gap-2.5 px-3.5 py-2 rounded-xl bg-slate-900 border border-white/10 hover:border-[#EA1A85]/50 transition-all text-xs font-semibold text-slate-200 shadow-sm"
      >
        <div className="flex items-center gap-2 truncate">
          {icon && <span className="text-slate-400">{icon}</span>}
          {label && <span className="text-slate-400 font-medium">{label}:</span>}
          <span className="text-white font-bold truncate">{selectedOption?.label}</span>
        </div>
        <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.98 }}
            transition={{ duration: 0.15 }}
            className="absolute left-0 mt-1.5 min-w-[220px] max-h-72 overflow-y-auto rounded-xl bg-slate-900/95 border border-white/15 p-1.5 shadow-2xl backdrop-blur-xl z-50 text-xs"
          >
            {options.map((option) => {
              const isSelected = option.value === value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => {
                    onChange(option.value);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors ${
                    isSelected ? "bg-[#EA1A85]/20 text-white font-bold" : "text-slate-300 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  <span className="truncate">{option.label}</span>
                  {isSelected && <Check className="w-3.5 h-3.5 text-[#EA1A85]" />}
                </button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/**
 * Metric Progress Comparison Bar
 * Visualizes individual metrics relative to par (e.g. Dot Ball %, Boundary %)
 */
export function MetricBar({
  label,
  value,
  parValue,
  unit = "%",
  isLowerBetter = false
}: {
  label: string;
  value: number;
  parValue: number;
  unit?: string;
  isLowerBetter?: boolean;
}) {
  const isBetter = isLowerBetter ? value <= parValue : value >= parValue;
  const barPercent = Math.min(100, Math.max(10, (value / (parValue * 1.5)) * 100));

  return (
    <div className="space-y-1 text-xs">
      <div className="flex justify-between items-center text-[11px]">
        <span className="text-slate-400">{label}</span>
        <div className="flex items-center gap-1.5">
          <span className={`font-black ${isBetter ? "text-emerald-400" : "text-rose-400"}`}>
            {value.toFixed(1)}{unit}
          </span>
          <span className="text-[10px] text-slate-500 font-mono">(Par: {parValue}{unit})</span>
        </div>
      </div>
      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden relative">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${barPercent}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className={`h-full rounded-full ${isBetter ? "bg-emerald-500" : "bg-amber-500"}`}
        />
      </div>
    </div>
  );
}
