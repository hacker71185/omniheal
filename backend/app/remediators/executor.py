import subprocess
import platform
import time
from datetime import datetime
from typing import List, Optional
from ..models import HealLogEntry, HealResult, IssueStatus

def execute_os_command(
    command_str: str, 
    module_name: str, 
    dry_run: bool = False,
    timeout_sec: int = 15
) -> HealLogEntry:
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    if dry_run:
        return HealLogEntry(
            timestamp=timestamp,
            level="INFO",
            module=module_name,
            command=f"[DRY-RUN] {command_str}",
            output=f"Simulated command execution completed successfully (Dry-Run Guard Active).",
            exit_code=0
        )
        
    system = platform.system()
    try:
        if system == "Windows":
            # Execute with PowerShell
            cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command_str]
        else:
            cmd = ["/bin/bash", "-c", command_str]
            
        res = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout_sec,
            errors="replace"
        )
        
        output_txt = (res.stdout.strip() + ("\n" + res.stderr.strip() if res.stderr.strip() else "")).strip()
        if not output_txt:
            output_txt = "Command executed with standard exit code 0."
            
        level = "SUCCESS" if res.returncode == 0 else "ERROR"
        return HealLogEntry(
            timestamp=timestamp,
            level=level,
            module=module_name,
            command=command_str,
            output=output_txt,
            exit_code=res.returncode
        )
    except subprocess.TimeoutExpired:
        return HealLogEntry(
            timestamp=timestamp,
            level="ERROR",
            module=module_name,
            command=command_str,
            output=f"Execution timed out after {timeout_sec}s.",
            exit_code=-1
        )
    except Exception as e:
        return HealLogEntry(
            timestamp=timestamp,
            level="ERROR",
            module=module_name,
            command=command_str,
            output=f"Execution error: {str(e)}",
            exit_code=1
        )
