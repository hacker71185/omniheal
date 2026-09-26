import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, ShieldAlert, AlertTriangle, ArrowUpRight } from 'lucide-react';
import type { CategoryScores } from '../types';

interface HealthGaugeProps {
  score: number;
  categoryScores: CategoryScores;
  isHealing: boolean;
  beforeScore?: number | null;
}

export const HealthGauge: React.FC<HealthGaugeProps> = ({
  score,
  categoryScores,
  isHealing,
  beforeScore
}) => {
  // Score color logic
  const isOptimal = score >= 88;
  const isWarning = score >= 60 && score < 88;

  const strokeColor = isOptimal ? '#10b981' : isWarning ? '#f59e0b' : '#f43f5e';
  const glowShadow = isOptimal ? 'rgba(16, 185, 129, 0.4)' : isWarning ? 'rgba(245, 158, 11, 0.4)' : 'rgba(244, 63, 94, 0.5)';

  // SVG Radial Math
  const radius = 78;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="cyber-card rounded-2xl p-6 relative flex flex-col justify-between overflow-hidden">
      {/* Laser scan line effect */}
      <div className="scan-radar pointer-events-none" />

      {/* Top Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-widest text-cyber-muted flex items-center gap-1.5 font-bold">
            <span className="w-1.5 h-1.5 rounded-full bg-cyber-cyan animate-pulse" />
            Core Health Telemetry
          </span>
          <h2 className="text-base font-bold text-white tracking-tight mt-0.5">
            System Integrity Score
          </h2>
        </div>

        {/* Dynamic Status Badge */}
        <div className={`px-2.5 py-1 rounded-full text-[11px] font-mono font-bold flex items-center gap-1.5 border shadow-sm ${
          isOptimal 
            ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' 
            : isWarning 
              ? 'bg-amber-500/15 text-amber-400 border-amber-500/30' 
              : 'bg-rose-500/15 text-rose-400 border-rose-500/30 animate-pulse'
        }`}>
          {isOptimal ? <ShieldCheck className="w-3.5 h-3.5" /> : isWarning ? <AlertTriangle className="w-3.5 h-3.5" /> : <ShieldAlert className="w-3.5 h-3.5" />}
          <span>{isOptimal ? 'OPTIMAL HEALTH' : isWarning ? 'WARNING DEGRADED' : 'CRITICAL BOTTLENECK'}</span>
        </div>
      </div>

      {/* Center Gauge and Progression Display */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-8 py-2">
        
        {/* Radial SVG Gauge */}
        <div className="relative flex items-center justify-center">
          <svg className="w-44 h-44 transform -rotate-90">
            {/* Background ring */}
            <circle
              cx="88"
              cy="88"
              r={radius}
              stroke="#131c2d"
              strokeWidth="12"
              fill="transparent"
            />
            {/* Value ring with animated dashoffset */}
            <motion.circle
              cx="88"
              cy="88"
              r={radius}
              stroke={strokeColor}
              strokeWidth="12"
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset }}
              transition={{ duration: 1.2, ease: "easeOut" }}
              strokeLinecap="round"
              fill="transparent"
              style={{ filter: `drop-shadow(0 0 10px ${glowShadow})` }}
            />
          </svg>

          {/* Center Digital Display */}
          <div className="absolute flex flex-col items-center justify-center text-center">
            <motion.span 
              className="text-4xl font-extrabold tracking-tight font-mono text-white"
              key={score}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.4 }}
            >
              {score}<span className="text-xl font-normal text-cyber-muted">%</span>
            </motion.span>
            <span className="text-[10px] uppercase font-mono tracking-widest text-cyber-muted mt-0.5">
              {isHealing ? 'HEALING...' : 'HEALTH INDEX'}
            </span>
          </div>
        </div>

        {/* Before vs After Progression Card */}
        <div className="flex flex-col justify-center space-y-3 w-full sm:w-auto">
          {beforeScore !== undefined && beforeScore !== null && beforeScore !== score && (
            <div className="bg-cyber-bg/80 border border-cyber-border rounded-xl p-3 flex items-center justify-between gap-4">
              <div>
                <span className="text-[10px] text-cyber-muted font-mono block">BEFORE HEAL</span>
                <span className="text-sm font-bold font-mono text-rose-400">{beforeScore}%</span>
              </div>
              <ArrowUpRight className="w-4 h-4 text-cyber-cyan" />
              <div>
                <span className="text-[10px] text-cyber-muted font-mono block">AFTER HEAL</span>
                <span className="text-sm font-bold font-mono text-emerald-400">{score}%</span>
              </div>
            </div>
          )}

          {/* Subscores Breakdown */}
          <div className="space-y-2 text-xs font-mono w-full sm:w-48">
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-slate-400">Performance</span>
                <span className="font-bold text-slate-200">{categoryScores.performance}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <motion.div 
                  className="bg-cyber-cyan h-1.5 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryScores.performance}%` }}
                  transition={{ duration: 0.8 }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-slate-400">Network Stack</span>
                <span className="font-bold text-slate-200">{categoryScores.network}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <motion.div 
                  className="bg-blue-500 h-1.5 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryScores.network}%` }}
                  transition={{ duration: 0.8 }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-slate-400">Storage / Disk</span>
                <span className="font-bold text-slate-200">{categoryScores.storage}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <motion.div 
                  className="bg-purple-500 h-1.5 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryScores.storage}%` }}
                  transition={{ duration: 0.8 }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-slate-400">Security Perimeter</span>
                <span className="font-bold text-slate-200">{categoryScores.security}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <motion.div 
                  className="bg-emerald-500 h-1.5 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryScores.security}%` }}
                  transition={{ duration: 0.8 }}
                />
              </div>
            </div>

          </div>

        </div>

      </div>

      {/* Footer Info */}
      <div className="border-t border-cyber-border/70 pt-3 mt-3 flex items-center justify-between text-[11px] font-mono text-cyber-muted">
        <span>Remediation Safety: 100% Non-Destructive</span>
        <span className="text-cyber-cyan">Rollback Guard: ACTIVE</span>
      </div>

    </div>
  );
};
