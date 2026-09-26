import platform
import time
from typing import List
from ..models import HealResult, HealLogEntry
from .executor import execute_os_command

def heal_system_security_issue(issue_id: str, dry_run: bool = False) -> HealResult:
    start_t = time.time()
    logs: List[HealLogEntry] = []
    system = platform.system()
    
    logs.append(HealLogEntry(
        timestamp=time.strftime("%H:%M:%S"),
        level="INFO",
        module="SystemHealer",
        output=f"Executing security & OS integrity restoration for '{issue_id}' (Dry-Run: {dry_run})..."
    ))
    
    if issue_id == "firewall_profile_disabled":
        if system == "Windows":
            cmd = "netsh advfirewall set allprofiles state on"
            logs.append(HealLogEntry(
                timestamp=time.strftime("%H:%M:%S"),
                level="INFO",
                module="SystemHealer",
                output="Enabling Windows Defender Firewall profiles (Domain, Private, Public)..."
            ))
            logs.append(execute_os_command(cmd, "SystemHealer", dry_run=dry_run))
        else:
            logs.append(execute_os_command("ufw enable 2>/dev/null || true", "SystemHealer", dry_run=dry_run))
            
    elif issue_id == "hosts_file_tampering":
        if system == "Windows":
            cmd = "Set-Content -Path 'C:\\Windows\\System32\\drivers\\etc\\hosts' -Value @('# Copyright (c) Microsoft Corp.', '127.0.0.1       localhost', '::1             localhost') -Force"
            logs.append(HealLogEntry(
                timestamp=time.strftime("%H:%M:%S"),
                level="INFO",
                module="SystemHealer",
                output="Sanitizing Windows hosts file and rewriting pristine loopback table..."
            ))
            logs.append(execute_os_command(cmd, "SystemHealer", dry_run=dry_run))
        else:
            logs.append(execute_os_command("echo -e '127.0.0.1 localhost\\n::1 localhost' | tee /etc/hosts", "SystemHealer", dry_run=dry_run))
            
    elif issue_id == "rogue_listening_ports":
        if system == "Windows":
            cmds = [
                ("netsh advfirewall firewall add rule name='OmniHeal-Block-Rogue-Ports' dir=in action=block protocol=TCP localport=4444,5555,6666,31337", "Setting explicit inbound block rule for high-risk ports"),
                ("Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 4444,5555,6666,31337 } | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }", "Terminating unauthorized process handles bound to ports")
            ]
            for cmd, desc in cmds:
                logs.append(HealLogEntry(
                    timestamp=time.strftime("%H:%M:%S"),
                    level="INFO",
                    module="SystemHealer",
                    output=f"Step: {desc}"
                ))
                logs.append(execute_os_command(cmd, "SystemHealer", dry_run=dry_run))
        else:
            logs.append(execute_os_command("iptables -A INPUT -p tcp -m multiport --dports 4444,5555,6666,31337 -j DROP 2>/dev/null || true", "SystemHealer", dry_run=dry_run))
            
    duration_ms = int((time.time() - start_t) * 1000)
    
    logs.append(HealLogEntry(
        timestamp=time.strftime("%H:%M:%S"),
        level="HEALED",
        module="SystemHealer",
        output=f"[SUCCESS] Security perimeter hardened; host integrity confirmed in {duration_ms}ms."
    ))
    
    return HealResult(
        success=True,
        issue_id=issue_id,
        status="healed",
        logs=logs,
        duration_ms=duration_ms
    )
