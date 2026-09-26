import React, { useState, useEffect } from 'react';
import { 
  X, 
  Wrench, 
  ShieldCheck, 
  AlertTriangle, 
  Cpu, 
  HardDrive, 
  MemoryStick, 
  Wifi, 
  Battery, 
  CheckCircle2,
  RefreshCw
} from 'lucide-react';
import type { HardwareTriageItem } from '../types';
import { fetchHardwareTriage } from '../services/api';

interface HardwareAdvisorModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HardwareAdvisorModal: React.FC<HardwareAdvisorModalProps> = ({
  isOpen,
  onClose
}) => {
  const [items, setItems] = useState<HardwareTriageItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadTriage();
    }
  }, [isOpen]);

  const loadTriage = async () => {
    setLoading(true);
    const data = await fetchHardwareTriage();
    setItems(data);
    setLoading(false);
  };

  if (!isOpen) return null;

  const getComponentIcon = (comp: string) => {
    if (comp.toLowerCase().includes('storage')) return <HardDrive className="w-5 h-5 text-purple-400" />;
    if (comp.toLowerCase().includes('thermal') || comp.toLowerCase().includes('cpu')) return <Cpu className="w-5 h-5 text-cyan-400" />;
    if (comp.toLowerCase().includes('memory') || comp.toLowerCase().includes('ram')) return <MemoryStick className="w-5 h-5 text-blue-400" />;
    if (comp.toLowerCase().includes('network') || comp.toLowerCase().includes('antenna')) return <Wifi className="w-5 h-5 text-emerald-400" />;
    return <Battery className="w-5 h-5 text-amber-400" />;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="cyber-card rounded-2xl w-full max-w-4xl overflow-hidden border border-cyber-cyan/40 shadow-2xl flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-cyber-border bg-[#0d1322]">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-500/20 border border-cyan-500/30 text-cyber-cyan">
              <Wrench className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-white tracking-tight">
                  Hardware S.M.A.R.T. & Physical Damage Advisor
                </h2>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold">
                  LIVE CONTROLLER SCAN
                </span>
              </div>
              <p className="text-xs text-cyber-muted font-mono">
                Identifies physical component wear and provides step-by-step hardware repair guides
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={loadTriage}
              disabled={loading}
              className="p-1.5 rounded-lg text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors"
              title="Refresh Hardware Telemetry"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-cyber-cyan' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors ml-2"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-4 bg-cyber-bg/95">
          
          {/* Top Banner: Verification Guarantee */}
          <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 flex items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0" />
              <div>
                <span className="text-xs font-bold text-white font-mono block">
                  PHYSICAL VS. SOFTWARE VERDICT CONFIRMED
                </span>
                <span className="text-[11px] text-slate-300">
                  OmniHeal automatically checks storage controller S.M.A.R.T. tables, CPU thermal throttling clamps, and memory address parity to separate software bugs from physical hardware damage.
                </span>
              </div>
            </div>
            <span className="text-[10px] font-mono px-2 py-1 rounded bg-black/40 text-emerald-400 border border-emerald-500/30 font-bold whitespace-nowrap">
              PHYSICS ENGINE ACTIVE
            </span>
          </div>

          {/* Hardware Components Grid */}
          <div className="space-y-3.5">
            {items.map((item) => {
              const isHealthy = item.status === 'PHYSICAL_HEALTHY';
              const isWarning = item.status === 'PHYSICAL_WARNING';
              
              return (
                <div 
                  key={item.id}
                  className={`p-4.5 rounded-xl border transition-all ${
                    isHealthy
                      ? 'border-cyber-border bg-cyber-card'
                      : isWarning
                        ? 'border-amber-500/40 bg-amber-950/15'
                        : 'border-rose-500/40 bg-rose-950/15 shadow-cyber-rose'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-cyber-border/60 pb-2.5">
                    <div className="flex items-center gap-2.5">
                      <div className="p-2 rounded-lg bg-slate-900 border border-cyber-border">
                        {getComponentIcon(item.component)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-xs font-bold font-mono text-white">
                            {item.component}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            [{item.hardware_name}]
                          </span>
                        </div>
                        <span className="text-[11px] text-slate-300 font-mono">
                          {item.diagnostics_reading}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold flex items-center gap-1 border ${
                        isHealthy
                          ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                          : isWarning
                            ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                            : 'bg-rose-500/15 text-rose-300 border-rose-500/30 animate-pulse'
                      }`}>
                        {isHealthy ? <CheckCircle2 className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                        <span>{isHealthy ? '100% HEALTHY' : isWarning ? 'PHYSICAL WEAR' : 'PHYSICAL FAILURE'}</span>
                      </span>
                    </div>
                  </div>

                  {/* Physical Repair Guidance */}
                  <div className="mt-3">
                    <span className="text-[10px] font-mono font-bold text-cyber-cyan uppercase tracking-wider block mb-1">
                      Actionable Physical Repair & Maintenance Guidance:
                    </span>
                    <ul className="space-y-1">
                      {item.actionable_repair_guide.map((step, sIdx) => (
                        <li key={sIdx} className="text-xs text-slate-300 flex items-start gap-2">
                          <span className="text-cyber-cyan select-none font-mono">›</span>
                          <span>{step}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                </div>
              );
            })}
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-cyber-border bg-[#090e18] flex items-center justify-between text-xs font-mono text-cyber-muted">
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 font-bold">OmniHeal™ Hardware Diagnostic Engine</span>
            <span className="text-cyber-dim">•</span>
            <span className="text-slate-300">Architected & Designed by hacker71185</span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-300 hover:text-white"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
