from typing import List, Dict, Any, Optional
import time
from ..models import FaultScenario, IssueItem, ScanResult, OSInfo, SystemMetrics, CategoryScores, HealResult, HealLogEntry

FAULT_SCENARIOS: List[FaultScenario] = [
    FaultScenario(
        id="dns_blackout",
        name="No-Internet DNS Blackout & Socket Hijack",
        badge="CRITICAL NETWORK",
        icon="WifiOff",
        description="Simulates corrupted DNS resolver cache and exhausted TCP ephemeral socket pool.",
        category="network",
        injected_issues=["dns_cache_failure", "tcp_ephemeral_exhaustion"],
        impact_description="Internet is connected, but all browser lookups fail with ERR_NAME_NOT_RESOLVED. Socket pool exhausted.",
        simulated_metrics_impact={"dns_latency_ms": 999.0, "active_connections": 394}
    ),
    FaultScenario(
        id="ram_leak_zombie",
        name="Slow Boot, Memory Leak & Zombie Swarm",
        badge="CRITICAL PERFORMANCE",
        icon="Cpu",
        description="Simulates an unconstrained memory leak spiking RAM to 93% and spawning 18 orphaned zombie process threads.",
        category="performance",
        injected_issues=["ram_exhaustion_leak", "zombie_processes", "high_cpu_thread_lock"],
        impact_description="Heavy system paging; fans spinning at max RPM; UI micro-stutters and input lag.",
        simulated_metrics_impact={"cpu_percent": 88.5, "ram_percent": 93.4, "ram_used_gb": 14.9}
    ),
    FaultScenario(
        id="disk_bloat_update_lock",
        name="Storage Cache Bloat & Stuck Update Lock",
        badge="STORAGE BOTTLENECK",
        icon="HardDrive",
        description="Simulates 12.4 GB of corrupted installer temp caches and a locked Windows Update staging service.",
        category="storage",
        injected_issues=["bloated_temp_cache", "stuck_update_cache"],
        impact_description="C: drive space exhaustion; Windows Update frozen at 0% with transaction lock.",
        simulated_metrics_impact={"disk_percent": 94.2, "temp_size_mb": 12480.0}
    ),
    FaultScenario(
        id="malware_hosts_hijack",
        name="Malware Hosts Hijack & Disabled Firewall",
        badge="CRITICAL SECURITY",
        icon="ShieldAlert",
        description="Simulates an adware payload disabling Windows Firewall and diverting security updates in hosts file.",
        category="security",
        injected_issues=["hosts_file_tampering", "firewall_profile_disabled", "rogue_listening_ports"],
        impact_description="Security update servers blocked; rogue listener detected on port 4444.",
        simulated_metrics_impact={"rogue_ports_count": 1, "firewall_disabled": True}
    ),
    FaultScenario(
        id="full_meltdown",
        name="Catastrophic Multi-Layer PC Bottleneck",
        badge="MULTI-VECTOR FAILURE",
        icon="Flame",
        description="Simulates a complete cascade failure across Performance, Network, Storage, and Security simultaneously.",
        category="performance",
        injected_issues=[
            "dns_cache_failure", 
            "ram_exhaustion_leak", 
            "bloated_temp_cache", 
            "hosts_file_tampering", 
            "zombie_processes", 
            "firewall_profile_disabled"
        ],
        impact_description="System Health Score drops to 24%. Severe multi-vector bottleneck requiring 1-Click Master Heal.",
        simulated_metrics_impact={
            "cpu_percent": 84.0, 
            "ram_percent": 91.0, 
            "disk_percent": 92.5, 
            "dns_latency_ms": 850.0
        }
    )
]

def get_scenario_by_id(scenario_id: str) -> Optional[FaultScenario]:
    for s in FAULT_SCENARIOS:
        if s.id == scenario_id:
            return s
    return None

def generate_simulated_scan(active_scenario_ids: List[str] = None) -> ScanResult:
    if not active_scenario_ids:
        active_scenario_ids = ["dns_blackout"]
        
    injected_issue_ids = set()
    metrics_overrides = {}
    
    for s_id in active_scenario_ids:
        scenario = get_scenario_by_id(s_id)
        if scenario:
            for iss in scenario.injected_issues:
                injected_issue_ids.add(iss)
            metrics_overrides.update(scenario.simulated_metrics_impact)
            
    # Assemble standard issue database
    catalog = {
        "dns_cache_failure": IssueItem(
            id="dns_cache_failure",
            category="network",
            title="DNS Resolver Cache Corruption & Socket Desynchronization",
            symptom="Internet connected to Wi-Fi/LAN, but websites fail to load (ERR_NAME_NOT_RESOLVED).",
            root_cause="Stale recursive DNS resolver cache holding invalid TTL records & desynchronized Winsock catalog.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Flush DNS Resolver Cache & Reset Winsock Stack",
            fix_description="Flushes client DNS resolver cache, unregisters stale multicast entries, and resets the Winsock catalog.",
            fix_commands_windows=[
                "ipconfig /flushdns",
                "ipconfig /registerdns",
                "netsh winsock reset",
                "netsh int ip reset"
            ],
            fix_commands_unix=[
                "resolvectl flush-caches",
                "sudo killall -HUP mDNSResponder"
            ],
            requires_admin=True,
            estimated_heal_time_ms=2100,
            tags=["DNS", "Winsock", "NetworkStack"]
        ),
        "tcp_ephemeral_exhaustion": IssueItem(
            id="tcp_ephemeral_exhaustion",
            category="network",
            title="Ephemeral TCP Socket Port Exhaustion (394 Stale Handles)",
            symptom="New outgoing connections hang in TIME_WAIT or fail intermittently.",
            root_cause="Stale socket handles remaining in TIME_WAIT state without prompt kernel reaping.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning",
            fix_title="Flush TCP TIME_WAIT Pool & Reclaim Ephemeral Ports",
            fix_description="Accelerates TCP TIME_WAIT recycling and flushes dead socket pools.",
            fix_commands_windows=[
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters' -Name 'TcpTimedWaitDelay' -Value 30 -Type DWord",
                "nbtstat -R"
            ],
            fix_commands_unix=["sysctl -w net.ipv4.tcp_tw_reuse=1"],
            requires_admin=True,
            estimated_heal_time_ms=1400,
            tags=["TCP", "Sockets", "TIME_WAIT"]
        ),
        "ram_exhaustion_leak": IssueItem(
            id="ram_exhaustion_leak",
            category="performance",
            title="Critical RAM Saturation & Working-Set Memory Bloat (93.4%)",
            symptom="System responsiveness severely degraded; high paging file activity causing UI stutter.",
            root_cause="Unreleased standby memory and runaway working set pools in background worker processes.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Trim Working Sets & Purge Standby Memory",
            fix_description="Trims bloated process working sets, triggers GC on hung system services, and purges standby memory caches.",
            fix_commands_windows=[
                "[System.GC]::Collect()",
                "Get-Process | Where-Object { $_.WorkingSet64 -gt 250MB } | ForEach-Object { [System.Diagnostics.Process]::GetProcessById($_.Id).EmptyWorkingSet() }"
            ],
            fix_commands_unix=["sync; echo 3 > /proc/sys/vm/drop_caches"],
            requires_admin=False,
            estimated_heal_time_ms=1800,
            reclaimed_ram_mb=3420,
            tags=["RAM", "Paging", "StandbyCache"]
        ),
        "zombie_processes": IssueItem(
            id="zombie_processes",
            category="performance",
            title="18 Orphaned Zombie / Hung Process Threads Detected",
            symptom="CPU micro-stutters and thread handles retained indefinitely in kernel memory.",
            root_cause="Terminated parent processes abandoned child PID locks without reaping exit codes.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning",
            fix_title="Terminate Orphaned Process Trees & Clean Thread Handles",
            fix_description="Safely terminates abandoned process IDs and releases kernel handles.",
            fix_commands_windows=[
                "Get-CimInstance Win32_Process | Where-Object { $_.ExecutionState -eq 3 } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
            ],
            fix_commands_unix=["ps -elf | grep 'Z' | awk '{print $5}' | xargs -r kill -9"],
            requires_admin=False,
            estimated_heal_time_ms=1200,
            tags=["ZombieProcesses", "KernelHandles"]
        ),
        "high_cpu_thread_lock": IssueItem(
            id="high_cpu_thread_lock",
            category="performance",
            title="Runaway Process Thread Consuming 88% CPU (host_indexer.exe)",
            symptom="Loud fan spin, thermal throttling, and overall CPU load spiking at 88%.",
            root_cause="Worker process PID 14280 trapped in an unyielding spin-lock loop.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Throttle & Cycle Runaway Process Thread",
            fix_description="Safely terminates the stuck worker process and resets thread priority back to normal.",
            fix_commands_windows=[
                "Stop-Process -Name 'host_indexer' -Force -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=["killall -9 host_indexer"],
            requires_admin=False,
            estimated_heal_time_ms=1100,
            tags=["CPU", "ThermalThrottling", "WorkerThread"]
        ),
        "bloated_temp_cache": IssueItem(
            id="bloated_temp_cache",
            category="storage",
            title="OS Temporary Files & Shader Cache Bloat (12,480 MB Detected)",
            symptom="Sluggish file system indexer, fragmented MFT sectors, and lost storage headroom.",
            root_cause="Orphaned crash dumps, abandoned application installers, and browser shader caches.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Purge Temporary File Trees & Clear Shader Caches",
            fix_description="Safely removes locked and orphaned temporary files older than 24 hours.",
            fix_commands_windows=[
                "Remove-Item -Path \"$env:TEMP\\*\" -Recurse -Force -ErrorAction SilentlyContinue",
                "Remove-Item -Path \"C:\\Windows\\Temp\\*\" -Recurse -Force -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=["rm -rf /tmp/* /var/tmp/*"],
            requires_admin=False,
            estimated_heal_time_ms=2400,
            reclaimed_bytes=12480 * 1024 * 1024,
            tags=["TempFiles", "ShaderCache", "StorageRecovery"]
        ),
        "stuck_update_cache": IssueItem(
            id="stuck_update_cache",
            category="storage",
            title="Corrupted Windows Update Staging Cache (Error 0x80240034)",
            symptom="Windows Update hangs indefinitely at 0% with transaction lock.",
            root_cause="Stuck background update download payload locked by wuauserv service.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning",
            fix_title="Reset Windows Update Services & Flush Download Cache",
            fix_description="Stops wuauserv and bits services, flushes corrupt payload files, and re-registers the update agent catalog.",
            fix_commands_windows=[
                "net stop wuauserv",
                "net stop bits",
                "Remove-Item -Path 'C:\\Windows\\SoftwareDistribution\\Download\\*' -Recurse -Force -ErrorAction SilentlyContinue",
                "net start bits",
                "net start wuauserv"
            ],
            fix_commands_unix=["sudo rm -f /var/lib/dpkg/lock*"],
            requires_admin=True,
            estimated_heal_time_ms=2900,
            tags=["WindowsUpdate", "wuauserv", "CacheLock"]
        ),
        "hosts_file_tampering": IssueItem(
            id="hosts_file_tampering",
            category="security",
            title="Modified Local DNS Routing in OS Hosts File",
            symptom="Security updates, banking portals, or telemetry rerouted to loopback or rogue IP addresses.",
            root_cause="Adware / PUP diverted 'update.microsoft.com' and 'antivirus-cloud.net' to 127.0.0.1.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Sanitize & Restore Default Factory OS Hosts File",
            fix_description="Safely removes malicious diversion lines and restores pristine default localhost mappings.",
            fix_commands_windows=[
                "Set-Content -Path 'C:\\Windows\\System32\\drivers\\etc\\hosts' -Value @('# Copyright (c) Microsoft Corp.', '127.0.0.1       localhost', '::1             localhost') -Force"
            ],
            fix_commands_unix=["echo -e '127.0.0.1 localhost\\n::1 localhost' | tee /etc/hosts"],
            requires_admin=True,
            estimated_heal_time_ms=1300,
            tags=["HostsFile", "DNSHijack", "Integrity"]
        ),
        "firewall_profile_disabled": IssueItem(
            id="firewall_profile_disabled",
            category="security",
            title="Windows Defender Firewall Profile Disabled",
            symptom="Inbound port filtering bypassed; device exposed to zero-click LAN probes.",
            root_cause="Private and Public firewall profiles were toggled to OFF state by an external installer.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Enforce State-Full Firewall Profiles (Domain, Private, Public)",
            fix_description="Re-enables all firewall profiles and resets baseline packet inspection filters.",
            fix_commands_windows=["netsh advfirewall set allprofiles state on"],
            fix_commands_unix=["ufw enable"],
            requires_admin=True,
            estimated_heal_time_ms=1100,
            tags=["Firewall", "ZeroTrust", "LANShield"]
        ),
        "rogue_listening_ports": IssueItem(
            id="rogue_listening_ports",
            category="security",
            title="Vulnerable Inbound Listener on Port 4444 (Metasploit Default)",
            symptom="Unauthenticated inbound endpoint exposed on 0.0.0.0:4444.",
            root_cause="High-risk backdoor listener or debug server active (PID 6720).",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Terminate Rogue Listener & Block Inbound Port Rules",
            fix_description="Terminates unauthorized process binding and generates explicit local firewall block rules.",
            fix_commands_windows=[
                "netsh advfirewall firewall add rule name='OmniHeal-Block-4444' dir=in action=block protocol=TCP localport=4444",
                "Stop-Process -Id 6720 -Force -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=["iptables -A INPUT -p tcp --dport 4444 -j DROP"],
            requires_admin=True,
            estimated_heal_time_ms=1500,
            tags=["Firewall", "PortSecurity", "InboundBlock"]
        )
    }
    
    selected_issues = [catalog[iss_id] for iss_id in injected_issue_ids if iss_id in catalog]
    
    # Calculate scores based on selected issues
    perf_count = sum(1 for i in selected_issues if i.category == "performance")
    net_count = sum(1 for i in selected_issues if i.category == "network")
    stor_count = sum(1 for i in selected_issues if i.category == "storage")
    sec_count = sum(1 for i in selected_issues if i.category == "security")
    
    perf_score = max(15, 100 - (perf_count * 38))
    net_score = max(10, 100 - (net_count * 45))
    stor_score = max(20, 100 - (stor_count * 40))
    sec_score = max(15, 100 - (sec_count * 42))
    
    overall = int((perf_score * 0.25) + (net_score * 0.30) + (stor_score * 0.20) + (sec_score * 0.25))
    
    metrics = SystemMetrics(
        cpu_percent=metrics_overrides.get("cpu_percent", 78.4 if perf_count else 14.2),
        cpu_cores=8,
        ram_percent=metrics_overrides.get("ram_percent", 91.8 if perf_count else 54.0),
        ram_used_gb=metrics_overrides.get("ram_used_gb", 14.6 if perf_count else 8.6),
        ram_total_gb=16.0,
        disk_percent=metrics_overrides.get("disk_percent", 94.0 if stor_count else 62.0),
        disk_free_gb=18.4 if stor_count else 180.0,
        disk_total_gb=512.0,
        active_connections=metrics_overrides.get("active_connections", 380 if net_count else 44),
        process_count=238 if perf_count else 142,
        temp_size_mb=metrics_overrides.get("temp_size_mb", 12480.0 if stor_count else 340.0),
        dns_latency_ms=metrics_overrides.get("dns_latency_ms", 999.0 if net_count else 16.5),
        network_sent_mb=182.4,
        network_recv_mb=890.1
    )
    
    os_info = OSInfo(
        system="Windows",
        release="11 Pro",
        version="10.0.26100",
        arch="x86_64",
        hostname="OMNIHEAL-WORKSTATION",
        boot_time_hours=48.2,
        is_admin=True,
        python_version="3.14.7"
    )
    
    critical_count = sum(1 for i in selected_issues if i.severity == "critical")
    warning_count = sum(1 for i in selected_issues if i.severity == "warning")
    
    return ScanResult(
        scan_id=f"sim-{int(time.time())}",
        scan_duration_ms=840,
        is_simulator_mode=True,
        os_info=os_info,
        health_score=overall,
        category_scores=CategoryScores(
            performance=perf_score,
            network=net_score,
            storage=stor_score,
            security=sec_score
        ),
        metrics=metrics,
        issues=selected_issues,
        total_issues=len(selected_issues),
        critical_issues=critical_count,
        warning_issues=warning_count
    )

def simulate_heal_issue(issue_id: str) -> HealResult:
    """Produces realistic step-by-step logs with exit codes and metrics."""
    time_str = time.strftime("%H:%M:%S")
    logs = [
        HealLogEntry(
            timestamp=time_str,
            level="INFO",
            module="SimulatorEngine",
            output=f"Simulating remediation pipeline for '{issue_id}'..."
        )
    ]
    
    freed_ram = 0
    freed_disk = 0
    
    if issue_id == "dns_cache_failure":
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="NetworkHealer", command="ipconfig /flushdns", output="Successfully flushed the DNS Resolver Cache.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="INFO", module="NetworkHealer", command="ipconfig /registerdns", output="Registration of the DNS resource records for all adapters has been initiated.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="INFO", module="NetworkHealer", command="netsh winsock reset catalog", output="Successfully reset the Winsock Catalog. You must restart the computer in order to complete the reset.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="NetworkHealer", output="[HEALED] DNS resolver synced. Socket descriptor table restored.", exit_code=0)
        ])
    elif issue_id == "ram_exhaustion_leak":
        freed_ram = 3420
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="MemoryHealer", command="[System.GC]::Collect()", output="CLR garbage collection cycle completed across 3 generations.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="INFO", module="MemoryHealer", command="EmptyWorkingSet()", output="Trimmed working sets of 14 background services.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="MemoryHealer", output=f"[HEALED] Reclaimed {freed_ram} MB of working memory; standby cache flushed.", exit_code=0)
        ])
    elif issue_id == "bloated_temp_cache":
        freed_disk = 12480
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="CacheHealer", command="Remove-Item $env:TEMP\\*", output="Deleted 4,821 temporary files and orphaned log traces.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="INFO", module="CacheHealer", command="Remove-Item C:\\Windows\\Temp\\*", output="Purged 1,104 installer cache fragments.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="CacheHealer", output=f"[HEALED] Storage recovered: +{freed_disk} MB free headroom.", exit_code=0)
        ])
    elif issue_id == "hosts_file_tampering":
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="SystemHealer", command="Set-Content hosts", output="Stripped 8 malicious diversion rules. Restored standard 127.0.0.1 localhost.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="SystemHealer", output="[HEALED] OS hosts file integrity verified and locked.", exit_code=0)
        ])
    elif issue_id == "firewall_profile_disabled":
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="SystemHealer", command="netsh advfirewall set allprofiles state on", output="Ok.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="SystemHealer", output="[HEALED] Domain, Private, and Public firewall profiles enforced.", exit_code=0)
        ])
    else:
        logs.extend([
            HealLogEntry(timestamp=time_str, level="INFO", module="AutoHealer", command=f"Remediate {issue_id}", output="Completed non-destructive system recovery.", exit_code=0),
            HealLogEntry(timestamp=time_str, level="HEALED", module="AutoHealer", output=f"[HEALED] Issue '{issue_id}' successfully mitigated.", exit_code=0)
        ])
        
    return HealResult(
        success=True,
        issue_id=issue_id,
        status="healed",
        logs=logs,
        duration_ms=1250,
        freed_ram_mb=freed_ram,
        freed_disk_mb=freed_disk
    )
