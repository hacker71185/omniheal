import React from 'react';
import { 
  Zap, 
  RefreshCw, 
  Terminal, 
  FileText, 
  Bug, 
  Sliders, 
  Lock, 
  Unlock,
  Radio
} from 'lucide-react';
import type { ScanResult } from '../types';

interface HeaderProps {
  scan: ScanResult | null;
  isScanning: boolean;
  isHealing: boolean;
  isAgentOnline: boolean;
  simulatorMode: boolean;
  onToggleSimulator: (val: boolean) => void;
  onScan: () => void;
  onHealAll: () => void;
  onOpenInjector: () => void;
  onOpenReport: () => void;
  onToggleTerminal: () => void;
  terminalOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  scan,
  isScanning,
  isHealing,
  isAgentOnline,
  simulatorMode,
  onToggleSimulator,
  onScan,
  onHealAll,
  onOpenInjector,
  onOpenReport,
  onToggleTerminal,
  terminalOpen
}) => {
  const detectedCount = scan?.issues.filter(i => i.status !== 'healed').length || 0;

  return (
    <header className="border-b border-cyber-border bg-cyber-bg/90 backdrop-blur-md sticky top-0 z-40 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand & System Status */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-start">
          <div className="flex items-center gap-2.5">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 via-blue-600/30 to-purple-600/20 border border-cyber-cyan/40 shadow-cyber-cyan">
              <Zap className="w-5 h-5 text-cyber-cyan animate-pulse" />
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-cyber-cyan animate-ping" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold tracking-wider text-lg bg-gradient-to-r from-white via-slate-100 to-cyber-cyan bg-clip-text text-transparent">
                  OMNI<span className="text-cyber-cyan font-black">HEAL</span>
                </span>
                <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30 font-bold tracking-widest">
                  v2.4 Pro
                </span>
              </div>
              <p className="text-[11px] text-cyber-muted font-mono tracking-tight">
                Autonomous Endpoint Diagnostics & Self-Healing Engine
              </p>
            </div>
          </div>

          {/* Mode Switcher Pill */}
          <div className="hidden sm:flex items-center bg-cyber-card border border-cyber-border rounded-lg p-1 text-xs">
            <button
              onClick={() => onToggleSimulator(false)}
              className={`px-2.5 py-1 rounded-md font-mono flex items-center gap-1.5 transition-all ${
                !simulatorMode 
                  ? 'bg-blue-600/30 text-cyber-cyan border border-cyber-cyan/40 shadow-sm font-semibold' 
                  : 'text-cyber-muted hover:text-white'
              }`}
              title="Execute real scans and safe remediation on host OS"
            >
              <Radio className={`w-3 h-3 ${isAgentOnline && !simulatorMode ? 'text-cyber-emerald animate-pulse' : 'text-cyber-muted'}`} />
              Live Host Agent
            </button>
            <button
              onClick={() => onToggleSimulator(true)}
              className={`px-2.5 py-1 rounded-md font-mono flex items-center gap-1.5 transition-all ${
                simulatorMode 
                  ? 'bg-purple-600/30 text-purple-300 border border-purple-500/40 shadow-sm font-semibold' 
                  : 'text-cyber-muted hover:text-white'
              }`}
              title="Interactive sandbox with instant fault injection for demo/recruiter review"
            >
              <Sliders className="w-3 h-3 text-purple-400" />
              Demo Simulator
            </button>
          </div>
        </div>

        {/* Center OS / Admin Badge */}
        {scan && (
          <div className="hidden xl:flex items-center gap-2 bg-cyber-card/60 border border-cyber-border px-3 py-1.5 rounded-lg text-xs font-mono text-cyber-muted">
            <div className="flex items-center gap-1.5 text-slate-200">
              <span className="w-2 h-2 rounded-full bg-cyber-cyan animate-pulse" />
              <span>{scan.os_info.system} {scan.os_info.release}</span>
            </div>
            <span className="text-cyber-dim">|</span>
            <span className="text-slate-400 font-mono">{scan.os_info.hostname}</span>
            <span className="text-cyber-dim">|</span>
            <span className={`flex items-center gap-1 px-1.5 py-0.2 rounded text-[10px] font-semibold ${
              scan.os_info.is_admin ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-700/30 text-slate-400'
            }`}>
              {scan.os_info.is_admin ? <Lock className="w-2.5 h-2.5" /> : <Unlock className="w-2.5 h-2.5" />}
              {scan.os_info.is_admin ? 'ELEVATED' : 'USER'}
            </span>
          </div>
        )}

        {/* Action Controls */}
        <div className="flex items-center gap-2.5 w-full md:w-auto justify-end flex-wrap">
          
          {/* Fault Injector Button */}
          <button
            onClick={onOpenInjector}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono border border-purple-500/30 bg-purple-950/30 text-purple-300 hover:bg-purple-900/40 hover:border-purple-400 transition-all cursor-pointer shadow-sm"
            title="Inject real-world PC faults into the sandbox"
          >
            <Bug className="w-3.5 h-3.5 text-purple-400" />
            <span>Simulate Fault</span>
          </button>

          {/* Deep Scan Button */}
          <button
            onClick={onScan}
            disabled={isScanning || isHealing}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono border border-cyber-border bg-cyber-card hover:bg-cyber-cardHover text-slate-200 hover:border-cyber-cyan/50 transition-all cursor-pointer ${
              isScanning ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            <RefreshCw className={`w-3.5 h-3.5 text-cyber-cyan ${isScanning ? 'animate-spin' : ''}`} />
            <span>{isScanning ? 'X-Ray Scanning...' : 'Scan Endpoint'}</span>
          </button>

          {/* Master 1-Click Heal All Button */}
          <button
            onClick={onHealAll}
            disabled={isHealing || isScanning || detectedCount === 0}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-bold font-mono tracking-wide transition-all shadow-lg cursor-pointer ${
              detectedCount > 0
                ? 'cyber-btn-primary animate-pulse'
                : 'bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed'
            }`}
          >
            <Zap className={`w-4 h-4 ${isHealing ? 'animate-spin' : ''}`} />
            <span>
              {isHealing 
                ? 'Auto-Healing System...' 
                : detectedCount > 0 
                  ? `1-Click Heal All (${detectedCount})`
                  : 'System Pristine'}
            </span>
          </button>

          {/* Terminal Drawer Toggle */}
          <button
            onClick={onToggleTerminal}
            className={`p-2 rounded-lg border transition-all ${
              terminalOpen 
                ? 'bg-cyber-cyan/20 border-cyber-cyan text-cyber-cyan shadow-cyber-cyan' 
                : 'bg-cyber-card border-cyber-border text-cyber-muted hover:text-white'
            }`}
            title="Toggle Live Streaming Remediation Terminal"
          >
            <Terminal className="w-4 h-4" />
          </button>

          {/* Audit Report */}
          <button
            onClick={onOpenReport}
            className="p-2 rounded-lg bg-cyber-card border border-cyber-border text-cyber-muted hover:text-white hover:border-slate-500 transition-all"
            title="View & Download Diagnostic Audit Report"
          >
            <FileText className="w-4 h-4" />
          </button>

        </div>

      </div>
    </header>
  );
};
