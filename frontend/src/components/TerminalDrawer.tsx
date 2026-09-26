import React, { useState, useEffect, useRef } from 'react';
import { 
  Terminal, 
  X, 
  Trash2, 
  Maximize2, 
  Minimize2, 
  Clock
} from 'lucide-react';
import type { HealLogEntry } from '../types';

interface TerminalDrawerProps {
  logs: HealLogEntry[];
  isOpen: boolean;
  onClose: () => void;
  onClear: () => void;
}

export const TerminalDrawer: React.FC<TerminalDrawerProps> = ({
  logs,
  isOpen,
  onClose,
  onClear
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const logContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (autoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, autoScroll]);

  if (!isOpen) return null;

  const getLevelBadge = (level: string) => {
    switch (level) {
      case 'HEALED':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-glow-emerald">[HEALED]</span>;
      case 'SUCCESS':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">[SUCCESS]</span>;
      case 'WARN':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">[WARN]</span>;
      case 'ERROR':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">[ERROR]</span>;
      default:
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">[INFO]</span>;
    }
  };

  return (
    <div className={`fixed bottom-0 left-0 right-0 z-50 border-t border-cyber-cyan/30 terminal-window transition-all duration-300 ${
      isExpanded ? 'h-[75vh]' : 'h-72'
    }`}>
      
      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#090e18] border-b border-cyber-border text-xs font-mono select-none">
        
        {/* Left: Indicator & Title */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block" />
          </div>
          <span className="text-cyber-dim">|</span>
          <div className="flex items-center gap-1.5 text-cyber-cyan font-bold tracking-wider">
            <Terminal className="w-3.5 h-3.5" />
            <span>OMNIHEAL REMEDIATION CONSOLE // CLI-AUDIT-STREAM</span>
          </div>
          <span className="text-[11px] text-cyber-dim">
            ({logs.length} stream events recorded)
          </span>
        </div>

        {/* Right: Controls */}
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5 text-cyber-muted text-[11px] cursor-pointer">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
              className="accent-cyber-cyan w-3 h-3 rounded"
            />
            <span>Auto-Scroll</span>
          </label>

          <button
            onClick={onClear}
            className="p-1 rounded text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors"
            title="Clear Console"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 rounded text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors"
            title={isExpanded ? 'Restore' : 'Maximize'}
          >
            {isExpanded ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>

          <button
            onClick={onClose}
            className="p-1 rounded text-cyber-muted hover:text-rose-400 hover:bg-slate-800 transition-colors"
            title="Close Terminal"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

      </div>

      {/* Terminal Log Stream Area */}
      <div 
        ref={logContainerRef}
        className="p-4 h-[calc(100%-36px)] overflow-y-auto font-mono text-xs space-y-1.5 bg-[#06090f]/95 selection:bg-cyber-cyan selection:text-black"
      >
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-cyber-dim space-y-2">
            <Terminal className="w-8 h-8 opacity-40 text-cyber-cyan" />
            <p>Remediation terminal initialized. Awaiting diagnostic scan or heal trigger.</p>
            <span className="text-[11px] font-mono text-cyber-dim">
              All remediation commands execute safely in dry-run or privileged mode with automatic verification.
            </span>
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="flex flex-col space-y-0.5 border-b border-white/[0.03] pb-1">
              <div className="flex items-center gap-2 flex-wrap text-[11px]">
                <span className="text-cyber-dim flex items-center gap-1">
                  <Clock className="w-2.5 h-2.5" />
                  {log.timestamp}
                </span>
                {getLevelBadge(log.level)}
                <span className="text-purple-400 font-semibold">[{log.module}]</span>
                {log.command && (
                  <span className="text-slate-300 bg-slate-900/90 px-2 py-0.5 rounded border border-slate-800 font-mono">
                    <span className="text-cyber-cyan select-none">$ </span>
                    {log.command}
                  </span>
                )}
                {log.exit_code !== undefined && log.exit_code !== null && (
                  <span className={`text-[10px] px-1 rounded ${log.exit_code === 0 ? 'text-emerald-400 bg-emerald-500/10' : 'text-rose-400 bg-rose-500/10'}`}>
                    exit {log.exit_code}
                  </span>
                )}
              </div>
              <div className="pl-6 text-slate-300 whitespace-pre-wrap leading-relaxed text-xs">
                {log.output}
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
};
