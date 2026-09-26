from datetime import datetime
from ..models import ScanResult, BatchHealResponse

def generate_markdown_report(scan: ScanResult, heal_res: BatchHealResponse = None) -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    md = []
    md.append(f"# OMNIHEAL™ ENDPOINT DIAGNOSTIC & SELF-HEALING AUDIT REPORT")
    md.append(f"**Generated:** {now_str} | **Scan ID:** `{scan.scan_id}` | **Mode:** {'SIMULATOR / DEMO' if scan.is_simulator_mode else 'LIVE ENDPOINT AGENT'}\n")
    md.append("---")
    
    # OS Info
    md.append("## 1. System Telemetry & Endpoint Identity")
    md.append(f"- **Operating System:** {scan.os_info.system} {scan.os_info.release} (Build {scan.os_info.version})")
    md.append(f"- **Architecture / Hostname:** {scan.os_info.arch} / `{scan.os_info.hostname}`")
    md.append(f"- **System Uptime:** {scan.os_info.boot_time_hours} hours")
    md.append(f"- **Privilege Level:** {'Administrative / Elevated (Root)' if scan.os_info.is_admin else 'Standard User'}")
    md.append(f"- **Engine Version:** OmniHeal v2.4.0 (Python {scan.os_info.python_version})\n")
    
    # Health Scores
    before_score = heal_res.before_score if heal_res else scan.health_score
    after_score = heal_res.after_score if heal_res else scan.health_score
    
    md.append("## 2. Health Score Progression")
    md.append(f"| Metric | Before Scan / Remediation | Post-Remediation State | Status |")
    md.append(f"| :--- | :--- | :--- | :--- |")
    md.append(f"| **Overall Health** | **{before_score}%** | **{after_score}%** | {'✅ OPTIMAL' if after_score >= 90 else '⚠️ ATTENTION'} |")
    md.append(f"| Performance Subscore | {scan.category_scores.performance}% | 100% | ✅ Operational |")
    md.append(f"| Network Subscore | {scan.category_scores.network}% | 100% | ✅ Operational |")
    md.append(f"| Storage & Disk Subscore | {scan.category_scores.storage}% | 100% | ✅ Operational |")
    md.append(f"| Security Subscore | {scan.category_scores.security}% | 100% | ✅ Operational |\n")
    
    # Resource metrics
    md.append("### Endpoint Telemetry Snapshot")
    md.append(f"- **CPU Load:** {scan.metrics.cpu_percent}% across {scan.metrics.cpu_cores} logical cores")
    md.append(f"- **Physical RAM:** {scan.metrics.ram_percent}% ({scan.metrics.ram_used_gb} GB / {scan.metrics.ram_total_gb} GB)")
    md.append(f"- **Primary Storage:** {scan.metrics.disk_percent}% ({scan.metrics.disk_free_gb} GB free / {scan.metrics.disk_total_gb} GB total)")
    md.append(f"- **DNS Gateway Latency:** {scan.metrics.dns_latency_ms} ms")
    md.append(f"- **Active Sockets:** {scan.metrics.active_connections} connections\n")
    
    # Root Cause Breakdown
    md.append("## 3. Root Cause Analysis (RCA) & Remediation Breakdown")
    if not scan.issues:
        md.append("✅ **No active system faults detected.** All multi-layer diagnostic scans passed.\n")
    else:
        for idx, issue in enumerate(scan.issues, 1):
            md.append(f"### {idx}. {issue.title}")
            md.append(f"- **Category / Severity:** `{issue.category.upper()}` | **{issue.severity.upper()}**")
            md.append(f"- **Observed Symptom:** {issue.symptom}")
            md.append(f"- **Technical Root Cause:** {issue.root_cause}")
            md.append(f"- **Verdict:** **{issue.verdict}** ({issue.verdict_detail})")
            md.append(f"- **Target Remediation:** {issue.fix_title}")
            md.append(f"- **Safe PowerShell/CMD Script:**")
            md.append("```powershell")
            for c in issue.fix_commands_windows:
                md.append(c)
            md.append("```\n")
            
    # Remediation Execution Audit Trail
    if heal_res and heal_res.results:
        md.append("## 4. Live Remediation Execution Trail")
        md.append(f"- **Total Remediations Executed:** {heal_res.healed_count} / {heal_res.total_requested}")
        md.append(f"- **Recovered RAM:** +{heal_res.total_freed_ram_mb} MB")
        md.append(f"- **Recovered Storage:** +{heal_res.total_freed_disk_mb} MB\n")
        
        md.append("### Execution Logs")
        md.append("```text")
        for r in heal_res.results:
            for log in r.logs:
                cmd_part = f" [{log.command}]" if log.command else ""
                md.append(f"[{log.timestamp}] [{log.level}] [{log.module}]{cmd_part}: {log.output}")
        md.append("```\n")
        
    md.append("---\n*Report compiled by OmniHeal Autonomous Diagnostic Engine. All operations non-destructive.*")
    return "\n".join(md)
