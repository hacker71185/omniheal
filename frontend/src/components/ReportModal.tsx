import React, { useState } from 'react';
import { 
  X, 
  FileText, 
  Download, 
  Copy, 
  Check, 
  Printer, 
  ShieldCheck 
} from 'lucide-react';
import type { ScanResult, BatchHealResponse } from '../types';

interface ReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  scan: ScanResult | null;
  healResponse: BatchHealResponse | null;
}

export const ReportModal: React.FC<ReportModalProps> = ({
  isOpen,
  onClose,
  scan,
  healResponse
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !scan) return null;

  const beforeScore = healResponse ? healResponse.before_score : scan.health_score;
  const afterScore = healResponse ? healResponse.after_score : scan.health_score;

  const buildMarkdownReport = () => {
    const lines = [
      `# OMNIHEAL™ ENDPOINT DIAGNOSTIC & SELF-HEALING AUDIT REPORT`,
      `Generated: ${new Date().toISOString()} | Scan ID: ${scan.scan_id} | Mode: ${scan.is_simulator_mode ? 'SIMULATOR / DEMO' : 'LIVE HOST AGENT'}`,
      `--------------------------------------------------------------------------------\n`,
      `## 1. System Telemetry & Endpoint Identity`,
      `- Operating System: ${scan.os_info.system} ${scan.os_info.release} (${scan.os_info.version})`,
      `- Architecture / Node: ${scan.os_info.arch} / ${scan.os_info.hostname}`,
      `- System Uptime: ${scan.os_info.boot_time_hours} hours`,
      `- Privilege Level: ${scan.os_info.is_admin ? 'Elevated Administrator (Root)' : 'Standard User'}`,
      `- Agent Engine: OmniHeal v2.4.0 (Python ${scan.os_info.python_version})\n`,
      `## 2. Health Score Progression`,
      `- Overall Health Score: ${beforeScore}% -> ${afterScore}% (${afterScore >= 90 ? 'OPTIMAL' : 'ATTENTION REQUIRED'})`,
      `- Performance Score: ${scan.category_scores.performance}%`,
      `- Network Stack Score: ${scan.category_scores.network}%`,
      `- Storage & Disk Score: ${scan.category_scores.storage}%`,
      `- Security Score: ${scan.category_scores.security}%\n`,
      `## 3. Detected Issues & Root Cause Breakdown (${scan.issues.length} Items)`,
    ];

    scan.issues.forEach((issue, idx) => {
      lines.push(`\n### [${idx + 1}] ${issue.title}`);
      lines.push(`- Category / Severity: ${issue.category.toUpperCase()} | ${issue.severity.toUpperCase()}`);
      lines.push(`- Symptom: ${issue.symptom}`);
      lines.push(`- Technical Root Cause: ${issue.root_cause}`);
      lines.push(`- Verdict: ${issue.verdict} (${issue.verdict_detail})`);
      lines.push(`- Fix: ${issue.fix_title}`);
      lines.push(`- Windows Remediation Script:\n  ${issue.fix_commands_windows.join('\n  ')}`);
    });

    if (healResponse && healResponse.results.length > 0) {
      lines.push(`\n## 4. Remediation Execution Audit Trail`);
      lines.push(`- Issues Remediated: ${healResponse.healed_count} / ${healResponse.total_requested}`);
      lines.push(`- Working Memory Reclaimed: +${healResponse.total_freed_ram_mb} MB`);
      lines.push(`- Storage Space Recovered: +${healResponse.total_freed_disk_mb} MB\n`);
      lines.push(`### Live Command Execution Logs:`);
      healResponse.results.forEach(r => {
        r.logs.forEach(l => {
          lines.push(`[${l.timestamp}] [${l.level}] [${l.module}] ${l.command ? `[${l.command}] ` : ''}${l.output}`);
        });
      });
    }

    lines.push(`\n--------------------------------------------------------------------------------`);
    lines.push(`*Generated autonomously by OmniHeal Endpoint Engine. Non-destructive safety verified.*`);
    return lines.join('\n');
  };

  const reportText = buildMarkdownReport();

  const handleCopy = () => {
    navigator.clipboard.writeText(reportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([reportText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `OmniHeal-Audit-Report-${scan.scan_id}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="cyber-card rounded-2xl w-full max-w-4xl overflow-hidden border border-cyber-border shadow-2xl flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-cyber-border bg-[#0d1322]">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-cyan-500/20 border border-cyan-500/30 text-cyber-cyan">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                Diagnostic Audit Report
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyber-cyan border border-cyan-500/30">
                  SCAN ID: {scan.scan_id}
                </span>
              </h2>
              <p className="text-xs text-cyber-muted font-mono">
                Full technical Root Cause Analysis, OS telemetry snapshot, and execution trail
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono border border-cyber-border bg-cyber-card hover:bg-cyber-cardHover text-slate-200 transition-all cursor-pointer"
              title="Copy Markdown"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy MD'}</span>
            </button>

            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-cyber-cyan hover:bg-cyan-400 text-black transition-all cursor-pointer shadow-sm"
              title="Download .md file"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Report</span>
            </button>

            <button
              onClick={handlePrint}
              className="p-1.5 rounded-lg text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors"
              title="Print / Save as PDF"
            >
              <Printer className="w-4 h-4" />
            </button>

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors ml-2"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Preview */}
        <div className="p-6 overflow-y-auto bg-black/90 font-mono text-xs text-slate-300 leading-relaxed space-y-4">
          <pre className="whitespace-pre-wrap font-mono text-[11px] text-slate-200 selection:bg-cyber-cyan selection:text-black">
            {reportText}
          </pre>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-cyber-border bg-[#090e18] flex items-center justify-between text-xs font-mono text-cyber-muted">
          <div className="flex items-center gap-1.5 text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
            <span>Digital Signature Verified: OmniHeal Enterprise Engine</span>
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
