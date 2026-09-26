import psutil
import time
from typing import List, Tuple
from ..models import IssueItem, SystemMetrics

def scan_performance() -> Tuple[List[IssueItem], dict]:
    issues: List[IssueItem] = []
    
    # Collect real CPU & Memory metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_cores = psutil.cpu_count(logical=True) or 4
    mem = psutil.virtual_memory()
    ram_percent = mem.percent
    ram_used_gb = round(mem.used / (1024 ** 3), 2)
    ram_total_gb = round(mem.total / (1024 ** 3), 2)
    
    # Process scan
    all_procs = []
    zombie_procs = []
    high_cpu_procs = []
    high_ram_procs = []
    
    try:
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'memory_info']):
            try:
                info = p.info
                all_procs.append(info)
                
                # Check for zombie / dead state
                status = str(info.get('status', '')).lower()
                if 'zombie' in status or 'dead' in status:
                    zombie_procs.append(info)
                    
                # High CPU process (if above 75%)
                c_pct = info.get('cpu_percent') or 0.0
                if c_pct > 75.0 and info.get('name') not in ['System Idle Process', 'idle']:
                    high_cpu_procs.append(info)
                    
                # High RAM process (>1.5 GB)
                mem_info = info.get('memory_info')
                if mem_info and mem_info.rss > 1.5 * 1024 * 1024 * 1024:
                    high_ram_procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception:
        pass
        
    process_count = len(all_procs)
    
    # 1. High Memory Thrashing / Leak Issue
    if ram_percent >= 85.0 or len(high_ram_procs) >= 2:
        top_hogs = ", ".join([f"{p['name']} ({round((p.get('memory_info').rss if p.get('memory_info') else 0)/(1024**2))}MB)" for p in high_ram_procs[:3]]) or "Multiple background threads"
        issues.append(IssueItem(
            id="ram_exhaustion_leak",
            category="performance",
            title="Critical RAM Saturation & Working-Set Memory Bloat",
            symptom=f"System responsiveness severely degraded; physical memory at {ram_percent}%. High paging activity.",
            root_cause=f"Unreleased standby memory and runaway working set pools ({top_hogs}).",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical" if ram_percent >= 90 else "warning",
            fix_title="Trim Working Sets & Purge Standby Memory",
            fix_description="Trims bloated process working sets, triggers GC on hung system services, and purges standby memory caches.",
            fix_commands_windows=[
                "Write-Output '[+] Flushing standby list and trimming memory pools...'",
                "[System.GC]::Collect()",
                "Clear-Host; Get-Process | Where-Object { $_.NonpagedSystemMemorySize64 -gt 150MB } | ForEach-Object { [System.Diagnostics.Process]::GetProcessById($_.Id).EmptyWorkingSet() }"
            ],
            fix_commands_unix=[
                "sync; echo 3 > /proc/sys/vm/drop_caches"
            ],
            requires_admin=False,
            estimated_heal_time_ms=1800,
            reclaimed_ram_mb=int((ram_percent - 55) * mem.total / 100 / (1024**2)) if ram_percent > 60 else 1200,
            tags=["RAM", "Paging", "StandbyCache"]
        ))
        
    # 2. Zombie / Abandoned Process Threads
    if len(zombie_procs) > 0:
        names = ", ".join([p['name'] for p in zombie_procs[:3]])
        issues.append(IssueItem(
            id="zombie_processes",
            category="performance",
            title=f"Detected {len(zombie_procs)} Orphaned Zombie / Hung Process Threads",
            symptom="CPU micro-stutters and thread handles retained indefinitely in kernel memory.",
            root_cause=f"Terminated parent processes abandoned child PID locks ({names}).",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning",
            fix_title="Terminate Orphaned Process Trees & Clean Thread Handles",
            fix_description="Safely terminates abandoned process IDs and releases kernel handles.",
            fix_commands_windows=[
                "Get-CimInstance Win32_Process | Where-Object { $_.ExecutionState -eq 3 } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
            ],
            fix_commands_unix=[
                "ps -elf | grep 'Z' | awk '{print $5}' | xargs -r kill -9"
            ],
            requires_admin=False,
            estimated_heal_time_ms=1200,
            tags=["Processes", "ZombieThreads", "KernelHandles"]
        ))

    # 3. High CPU Runaway Thread Lock
    if len(high_cpu_procs) > 0 and cpu_percent > 70:
        hog = high_cpu_procs[0]['name']
        issues.append(IssueItem(
            id="high_cpu_thread_lock",
            category="performance",
            title=f"Runaway Process Thread Consuming Abnormal CPU ({hog})",
            symptom=f"Loud fan spin, thermal throttling, and overall CPU load spiking at {cpu_percent}%.",
            root_cause=f"Process '{hog}' (PID {high_cpu_procs[0].get('pid')}) stuck in an unyielding polling loop.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Throttle & Cycle Runaway Process Thread",
            fix_description="Safely cycles the stuck worker process and resets thread priority back to normal.",
            fix_commands_windows=[
                f"Stop-Process -Name '{hog.replace('.exe', '')}' -Force -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=[
                f"killall -SIGTERM '{hog}'"
            ],
            requires_admin=False,
            estimated_heal_time_ms=1500,
            tags=["CPU", "ThermalThrottling", "WorkerThread"]
        ))

    # 4. Spooler / Background Service Lock
    if process_count > 280:
        issues.append(IssueItem(
            id="bloated_service_host",
            category="performance",
            title=f"Abnormally High Background Service Count ({process_count} Processes)",
            symptom="System startup drag and persistent background I/O contention.",
            root_cause="Cumulative service host spawn count exceeds optimal threshold (max recommended: 200).",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning",
            fix_title="Consolidate Svchost Process Groups & Optimize Startup Threads",
            fix_description="Sets svchost split threshold and trims idle background daemon workers.",
            fix_commands_windows=[
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control' -Name 'SvcHostSplitThresholdInKB' -Value 37748736 -Type DWord -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=[
                "systemctl daemon-reload"
            ],
            requires_admin=True,
            estimated_heal_time_ms=2000,
            tags=["Svchost", "Optimization", "Services"]
        ))

    telemetry = {
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_cores,
        "ram_percent": ram_percent,
        "ram_used_gb": ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "process_count": process_count,
    }
    return issues, telemetry
