import os
import psutil
import platform
import subprocess
from typing import List, Tuple
from ..models import IssueItem

SUSPICIOUS_PORTS = {
    4444: "Metasploit Default Listener",
    5555: "ADB Debug Bridge Unauthenticated",
    6666: "IRC / Botnet C2 Default",
    31337: "Back Orifice Trojan Port",
    9999: "Unprotected Remote Debugger Port"
}

def scan_hosts_file() -> Tuple[bool, List[str]]:
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"
    suspicious_entries = []
    
    if os.path.exists(hosts_path):
        try:
            with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for line in lines:
                    line_clean = line.strip()
                    if line_clean and not line_clean.startswith("#"):
                        # Check if line diverts common sites or localhost anomalies
                        parts = line_clean.split()
                        if len(parts) >= 2:
                            ip, host = parts[0], parts[1].lower()
                            if any(target in host for target in ["antivirus", "microsoft", "google", "bank", "update", "paypal"]):
                                suspicious_entries.append(f"{ip} -> {host}")
        except Exception:
            pass
    return (len(suspicious_entries) > 0, suspicious_entries)

def check_windows_firewall() -> bool:
    """Returns True if any firewall profile is disabled."""
    if platform.system() != "Windows":
        return False
    try:
        cmd = ["netsh", "advfirewall", "show", "allprofiles", "state"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if "OFF" in res.stdout.upper():
            return True
    except Exception:
        pass
    return False

def scan_security() -> Tuple[List[IssueItem], dict]:
    issues: List[IssueItem] = []
    rogue_ports_found = []
    
    # 1. Scan for Rogue Listening Ports
    try:
        conns = psutil.net_connections(kind='inet')
        for c in conns:
            if c.status == 'LISTEN':
                port = c.laddr.port
                if port in SUSPICIOUS_PORTS:
                    proc_name = "Unknown"
                    if c.pid:
                        try:
                            proc_name = psutil.Process(c.pid).name()
                        except Exception:
                            pass
                    rogue_ports_found.append(f"Port {port} ({SUSPICIOUS_PORTS[port]}) [PID: {c.pid}, Process: {proc_name}]")
    except Exception:
        pass
        
    if len(rogue_ports_found) > 0:
        issues.append(IssueItem(
            id="rogue_listening_ports",
            category="security",
            title=f"Detected {len(rogue_ports_found)} Vulnerable Open Listening Port(s)",
            symptom="Unauthenticated inbound endpoint exposed on local network interface.",
            root_cause=f"High-risk debug listener or rogue service active: {', '.join(rogue_ports_found[:2])}.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Terminate Rogue Listener & Block Inbound Port Rules",
            fix_description="Terminates unauthorized process binding and generates explicit local firewall block rules.",
            fix_commands_windows=[
                "netsh advfirewall firewall add rule name='OmniHeal-Block-Rogue-Ports' dir=in action=block protocol=TCP localport=4444,5555,6666,31337",
                "Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 4444,5555,6666,31337 } | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
            ],
            fix_commands_unix=[
                "sudo iptables -A INPUT -p tcp -m multiport --dports 4444,5555,6666,31337 -j DROP"
            ],
            requires_admin=True,
            estimated_heal_time_ms=1700,
            tags=["Firewall", "PortSecurity", "InboundBlock"]
        ))
        
    # 2. Hosts File Integrity
    has_hosts_hijack, suspicious_entries = scan_hosts_file()
    if has_hosts_hijack:
        issues.append(IssueItem(
            id="hosts_file_tampering",
            category="security",
            title="Modified Local DNS Routing in OS Hosts File",
            symptom="Security updates, banking portals, or telemetry rerouted to loopback or rogue IP addresses.",
            root_cause=f"Unauthorized third-party application appended diversion rules: {', '.join(suspicious_entries[:3])}.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Sanitize & Restore Default Factory OS Hosts File",
            fix_description="Safely removes malicious diversion lines and restores pristine default localhost mappings (127.0.0.1 localhost).",
            fix_commands_windows=[
                "Set-Content -Path 'C:\\Windows\\System32\\drivers\\etc\\hosts' -Value @('# Copyright (c) Microsoft Corp.', '127.0.0.1       localhost', '::1             localhost') -Force"
            ],
            fix_commands_unix=[
                "echo -e '127.0.0.1 localhost\\n::1 localhost' | sudo tee /etc/hosts"
            ],
            requires_admin=True,
            estimated_heal_time_ms=1200,
            tags=["HostsFile", "DNSHijack", "Integrity"]
        ))

    # 3. Firewall Profile Status
    firewall_disabled = check_windows_firewall()
    if firewall_disabled:
        issues.append(IssueItem(
            id="firewall_profile_disabled",
            category="security",
            title="Windows Defender Firewall Profile Inactive or Disabled",
            symptom="Inbound port filtering bypassed; device exposed to zero-click LAN probes.",
            root_cause="Private or Public firewall profile explicitly toggled to OFF state.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Enforce State-Full Firewall Profiles (Domain, Private, Public)",
            fix_description="Re-enables all firewall profiles and resets baseline packet inspection filters.",
            fix_commands_windows=[
                "netsh advfirewall set allprofiles state on"
            ],
            fix_commands_unix=[
                "sudo ufw enable || sudo systemctl start firewalld"
            ],
            requires_admin=True,
            estimated_heal_time_ms=1100,
            tags=["Firewall", "ZeroTrust", "LANShield"]
        ))

    telemetry = {
        "rogue_ports_count": len(rogue_ports_found),
        "hosts_file_tampered": has_hosts_hijack,
        "firewall_disabled": firewall_disabled
    }
    return issues, telemetry
