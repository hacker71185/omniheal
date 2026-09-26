import React, { useState } from 'react';
import { 
  AlertCircle, 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  Code, 
  Cpu, 
  HardDrive, 
  Shield, 
  Wifi, 
  Wrench, 
  Zap, 
  Check, 
  Copy
} from 'lucide-react';
import type { IssueItem } from '../types';

interface IssueCardProps {
  issue: IssueItem;
  onFix: (issueId: string) => void;
  isHealing: boolean;
}

export const IssueCard: React.FC<IssueCardProps> = ({ issue, onFix, isHealing }) => {
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'windows' | 'unix'>('windows');

  const isHealed = issue.status === 'healed';
  const isCurrentlyHealing = issue.status === 'healing';

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'performance': return <Cpu className="w-4 h-4 text-cyan-400" />;
      case 'network': return <Wifi className="w-4 h-4 text-blue-400" />;
      case 'storage': return <HardDrive className="w-4 h-4 text-purple-400" />;
      case 'security': return <Shield className="w-4 h-4 text-emerald-400" />;
      default: return <Wrench className="w-4 h-4 text-slate-400" />;
    }
  };

  const copyScript = () => {
    const cmds = activeTab === 'windows' ? issue.fix_commands_windows : issue.fix_commands_unix;
    navigator.clipboard.writeText(cmds.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`cyber-card rounded-xl p-5 transition-all ${
      isHealed 
        ? 'border-emerald-500/30 bg-emerald-950/10' 
        : issue.severity === 'critical' 
          ? 'border-rose-500/30 bg-cyber-card cyber-card-danger' 
          : 'border-amber-500/30 bg-cyber-card'
    }`}>
      
      {/* Top Banner: Category, Severity, and Healing Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-cyber-border">
        
        <div className="flex items-center gap-2 flex-wrap">
          {/* Category Tag */}
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-semibold bg-cyber-cardHover border border-cyber-border text-slate-200">
            {getCategoryIcon(issue.category)}
            <span className="uppercase text-[11px]">{issue.category}</span>
          </span>

          {/* Severity Tag */}
          <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold uppercase tracking-wider ${
            issue.severity === 'critical' 
              ? 'bg-rose-500/15 text-rose-400 border border-rose-500/30' 
              : 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
          }`}>
            {issue.severity}
          </span>

          {/* Verdict Tag: Non-Physical / Software-Solvable */}
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 shadow-sm">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>100% Non-Physical / Software-Solvable</span>
          </span>
        </div>

        {/* Action Button: Auto-Fix Now */}
        <div>
          {isHealed ? (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
              <Check className="w-3.5 h-3.5" />
              <span>HEALED & VERIFIED</span>
            </div>
          ) : (
            <button
              onClick={() => onFix(issue.id)}
              disabled={isCurrentlyHealing || isHealing}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold transition-all cursor-pointer ${
                isCurrentlyHealing
                  ? 'bg-cyan-500/30 text-cyber-cyan border border-cyber-cyan/50 animate-pulse'
                  : 'cyber-btn-primary'
              }`}
            >
              <Zap className={`w-3.5 h-3.5 ${isCurrentlyHealing ? 'animate-spin' : ''}`} />
              <span>{isCurrentlyHealing ? 'Healing Subsystem...' : 'Auto-Fix Now'}</span>
            </button>
          )}
        </div>

      </div>

      {/* Title */}
      <h3 className="text-base font-bold text-white tracking-tight mt-3">
        {issue.title}
      </h3>

      {/* Symptom & Root Cause Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
        
        {/* Symptom Box */}
        <div className="bg-cyber-bg/70 border border-rose-500/20 rounded-lg p-3">
          <div className="flex items-center gap-1.5 text-[11px] font-mono font-bold text-rose-400 uppercase tracking-wider mb-1">
            <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
            <span>Observed Symptom</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed font-sans">
            {issue.symptom}
          </p>
        </div>

        {/* Root Cause Analysis Box */}
        <div className="bg-cyber-bg/70 border border-cyan-500/20 rounded-lg p-3">
          <div className="flex items-center gap-1.5 text-[11px] font-mono font-bold text-cyber-cyan uppercase tracking-wider mb-1">
            <Wrench className="w-3.5 h-3.5 text-cyber-cyan" />
            <span>Technical Root Cause</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed font-sans">
            {issue.root_cause}
          </p>
        </div>

      </div>

      {/* Target Fix Summary & Code Preview Toggle */}
      <div className="mt-3.5 pt-3 border-t border-cyber-border/60 flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono text-cyber-muted font-bold">REMEDIATION:</span>
            <span className="text-xs text-slate-200 font-medium">{issue.fix_title}</span>
          </div>
          <button
            onClick={() => setShowCode(!showCode)}
            className="flex items-center gap-1 text-xs font-mono text-cyber-cyan hover:text-white transition-colors cursor-pointer"
          >
            <Code className="w-3.5 h-3.5" />
            <span>{showCode ? 'Hide Fix Script' : 'Preview Fix Script'}</span>
            {showCode ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Expandable Fix Script Preview */}
        {showCode && (
          <div className="mt-2 bg-black/80 border border-cyber-border rounded-lg overflow-hidden font-mono text-xs">
            {/* Tab header */}
            <div className="flex items-center justify-between px-3 py-1.5 bg-slate-900 border-b border-cyber-border">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab('windows')}
                  className={`px-2 py-0.5 rounded text-[11px] transition-all ${
                    activeTab === 'windows' 
                      ? 'bg-cyber-cyan/20 text-cyber-cyan font-bold border border-cyber-cyan/30' 
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  PowerShell (Windows)
                </button>
                <button
                  onClick={() => setActiveTab('unix')}
                  className={`px-2 py-0.5 rounded text-[11px] transition-all ${
                    activeTab === 'unix' 
                      ? 'bg-cyber-cyan/20 text-cyber-cyan font-bold border border-cyber-cyan/30' 
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Bash (Linux / macOS)
                </button>
              </div>

              <button
                onClick={copyScript}
                className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white transition-colors cursor-pointer"
                title="Copy script"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>

            {/* Script body */}
            <div className="p-3 text-slate-300 font-mono text-[11px] leading-relaxed overflow-x-auto space-y-1">
              {(activeTab === 'windows' ? issue.fix_commands_windows : issue.fix_commands_unix).map((cmd, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-cyber-dim select-none">{i + 1}</span>
                  <span className="text-cyber-cyan select-none">$</span>
                  <span className="text-slate-200">{cmd}</span>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>

    </div>
  );
};
