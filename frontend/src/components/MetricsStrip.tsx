import React from 'react';
import { Cpu, MemoryStick, HardDrive, Wifi } from 'lucide-react';
import type { SystemMetrics } from '../types';

interface MetricsStripProps {
  metrics: SystemMetrics;
}

export const MetricsStrip: React.FC<MetricsStripProps> = ({ metrics }) => {
  const getLoadColor = (pct: number) => {
    if (pct >= 85) return 'text-rose-400 bg-rose-500/20 border-rose-500/30';
    if (pct >= 70) return 'text-amber-400 bg-amber-500/20 border-amber-500/30';
    return 'text-cyber-cyan bg-cyan-500/20 border-cyan-500/30';
  };

  const getBarColor = (pct: number) => {
    if (pct >= 85) return 'bg-rose-500';
    if (pct >= 70) return 'bg-amber-500';
    return 'bg-cyber-cyan';
  };

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
      
      {/* CPU Utilization */}
      <div className="cyber-card rounded-xl p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyber-cyan">
              <Cpu className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono uppercase text-cyber-muted block">CPU Load</span>
              <span className="text-xs font-semibold text-slate-300 font-mono">{metrics.cpu_cores} Logical Cores</span>
            </div>
          </div>
          <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${getLoadColor(metrics.cpu_percent)}`}>
            {metrics.cpu_percent}%
          </span>
        </div>
        <div className="mt-3">
          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div 
              className={`h-1.5 rounded-full transition-all duration-500 ${getBarColor(metrics.cpu_percent)}`}
              style={{ width: `${Math.min(100, metrics.cpu_percent)}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[10px] font-mono text-cyber-dim mt-1.5">
            <span>{metrics.process_count} Processes</span>
            <span>Task Manager Sync</span>
          </div>
        </div>
      </div>

      {/* Memory Utilization */}
      <div className="cyber-card rounded-xl p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400">
              <MemoryStick className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono uppercase text-cyber-muted block">Physical RAM</span>
              <span className="text-xs font-semibold text-slate-300 font-mono">{metrics.ram_used_gb} / {metrics.ram_total_gb} GB</span>
            </div>
          </div>
          <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${getLoadColor(metrics.ram_percent)}`}>
            {metrics.ram_percent}%
          </span>
        </div>
        <div className="mt-3">
          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div 
              className={`h-1.5 rounded-full transition-all duration-500 ${getBarColor(metrics.ram_percent)}`}
              style={{ width: `${Math.min(100, metrics.ram_percent)}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[10px] font-mono text-cyber-dim mt-1.5">
            <span>Standby: {(metrics.ram_total_gb - metrics.ram_used_gb).toFixed(1)} GB Free</span>
            <span>Working Sets Active</span>
          </div>
        </div>
      </div>

      {/* Primary Storage */}
      <div className="cyber-card rounded-xl p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
              <HardDrive className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono uppercase text-cyber-muted block">System Storage</span>
              <span className="text-xs font-semibold text-slate-300 font-mono">{metrics.disk_free_gb} GB Free</span>
            </div>
          </div>
          <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${getLoadColor(metrics.disk_percent)}`}>
            {metrics.disk_percent}%
          </span>
        </div>
        <div className="mt-3">
          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div 
              className={`h-1.5 rounded-full transition-all duration-500 ${getBarColor(metrics.disk_percent)}`}
              style={{ width: `${Math.min(100, metrics.disk_percent)}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[10px] font-mono text-cyber-dim mt-1.5">
            <span>Temp Cache: {metrics.temp_size_mb} MB</span>
            <span>Volume Healthy</span>
          </div>
        </div>
      </div>

      {/* Network Stack */}
      <div className="cyber-card rounded-xl p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
              <Wifi className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono uppercase text-cyber-muted block">DNS / Sockets</span>
              <span className="text-xs font-semibold text-slate-300 font-mono">
                {metrics.dns_latency_ms > 500 ? 'Blackout / Degraded' : `${metrics.dns_latency_ms} ms Latency`}
              </span>
            </div>
          </div>
          <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${
            metrics.dns_latency_ms > 200 ? 'text-rose-400 bg-rose-500/20 border-rose-500/30' : 'text-emerald-400 bg-emerald-500/20 border-emerald-500/30'
          }`}>
            {metrics.active_connections} Sockets
          </span>
        </div>
        <div className="mt-3">
          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div 
              className={`h-1.5 rounded-full transition-all duration-500 ${metrics.dns_latency_ms > 200 ? 'bg-rose-500' : 'bg-emerald-400'}`}
              style={{ width: `${Math.min(100, (metrics.active_connections / 400) * 100)}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[10px] font-mono text-cyber-dim mt-1.5">
            <span>Tx: {metrics.network_sent_mb}MB / Rx: {metrics.network_recv_mb}MB</span>
            <span>Winsock Bound</span>
          </div>
        </div>
      </div>

    </div>
  );
};
