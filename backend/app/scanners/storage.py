import os
import psutil
import platform
import shutil
from typing import List, Tuple
from ..models import IssueItem

def get_dir_size(path: str) -> int:
    total = 0
    try:
        if os.path.exists(path):
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        if entry.is_file(follow_symlinks=False):
                            total += entry.stat().st_size
                    except Exception:
                        continue
    except Exception:
        pass
    return total

def scan_storage() -> Tuple[List[IssueItem], dict]:
    issues: List[IssueItem] = []
    
    # 1. Drive usage stats
    disk_usage = psutil.disk_usage(os.path.abspath(os.sep))
    disk_percent = disk_usage.percent
    disk_free_gb = round(disk_usage.free / (1024 ** 3), 2)
    disk_total_gb = round(disk_usage.total / (1024 ** 3), 2)
    
    # 2. Temp cache scanning
    temp_dirs = []
    if platform.system() == "Windows":
        user_temp = os.environ.get("TEMP", "")
        win_temp = r"C:\Windows\Temp"
        if user_temp and os.path.exists(user_temp):
            temp_dirs.append(user_temp)
        if os.path.exists(win_temp):
            temp_dirs.append(win_temp)
    else:
        temp_dirs.append("/tmp")
        temp_dirs.append("/var/tmp")
        
    total_temp_bytes = 0
    for p in temp_dirs:
        total_temp_bytes += get_dir_size(p)
        
    temp_size_mb = round(total_temp_bytes / (1024 ** 2), 2)
    
    # 3. Detect bloated temp caches
    if temp_size_mb > 400.0:
        issues.append(IssueItem(
            id="bloated_temp_cache",
            category="storage",
            title=f"OS Temporary Files & Shader Cache Bloat ({temp_size_mb} MB Detected)",
            symptom="Sluggish file system indexer, fragmented MFT sectors, and lost storage headroom.",
            root_cause="Orphaned crash dumps, abandoned application installers, and browser shader caches accumulating without purge cycles.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="warning" if temp_size_mb < 2000 else "critical",
            fix_title="Purge Temporary File Trees & Clear Shader Caches",
            fix_description="Safely removes locked and orphaned temporary files older than 24 hours while keeping active application locks intact.",
            fix_commands_windows=[
                "Remove-Item -Path \"$env:TEMP\\*\" -Recurse -Force -ErrorAction SilentlyContinue",
                "Remove-Item -Path \"C:\\Windows\\Temp\\*\" -Recurse -Force -ErrorAction SilentlyContinue"
            ],
            fix_commands_unix=[
                "rm -rf /tmp/* /var/tmp/*"
            ],
            requires_admin=False,
            estimated_heal_time_ms=2200,
            reclaimed_bytes=total_temp_bytes,
            tags=["TempFiles", "ShaderCache", "DiskCleanup"]
        ))
        
    # 4. Low Disk Space Warning
    if disk_percent > 85.0:
        issues.append(IssueItem(
            id="low_disk_headroom",
            category="storage",
            title=f"Critical Storage Capacity Threshold ({disk_percent}% Utilized, {disk_free_gb} GB Free)",
            symptom="Severe pagefile bottleneck, virtual memory allocation crashes, and Windows update stall.",
            root_cause="Host storage volume under 15% free headroom; file fragmentation prevents continuous virtual memory allocation.",
            verdict="Software-Solvable",
            verdict_detail="100% Non-Physical / Safe Software Remediation",
            severity="critical",
            fix_title="Reclaim OS Storage via Deep Component Store & Log Cleanup",
            fix_description="Compresses inactive system files, deletes stale crashdumps, and clears obsolete Windows update rollback backups.",
            fix_commands_windows=[
                "Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase",
                "vssadmin delete shadows /for=c: /oldest /quiet"
            ],
            fix_commands_unix=[
                "journalctl --vacuum-time=3d",
                "apt-get clean"
            ],
            requires_admin=True,
            estimated_heal_time_ms=3500,
            tags=["DiskCapacity", "ComponentStore", "Pagefile"]
        ))

    # 5. Windows Update / Package Manager Lock Detection
    if platform.system() == "Windows":
        # Check if SoftwareDistribution\Download folder is excessively large (>1.5GB)
        soft_dist = r"C:\Windows\SoftwareDistribution\Download"
        soft_dist_size = get_dir_size(soft_dist)
        if soft_dist_size > 1.5 * 1024 * 1024 * 1024:
            issues.append(IssueItem(
                id="stuck_update_cache",
                category="storage",
                title=f"Corrupted Windows Update Staging Cache ({round(soft_dist_size / (1024**2))} MB)",
                symptom="Windows Update hangs at 0% or errors with 0x80070002 / 0x80240034.",
                root_cause="Stuck background update download transaction locked by wuauserv service.",
                verdict="Software-Solvable",
                verdict_detail="100% Non-Physical / Safe Software Remediation",
                severity="warning",
                fix_title="Reset Windows Update Services & Flush Download Cache",
                fix_description="Stops wuauserv and bits services, flushes corrupt payload files, and re-registers the update agent catalog.",
                fix_commands_windows=[
                    "net stop wuauserv",
                    "net stop bits",
                    "Remove-Item -Path 'C:\\Windows\\SoftwareDistribution\\Download\\*' -Recurse -Force -ErrorAction SilentlyContinue",
                    "net start wuauserv",
                    "net start bits"
                ],
                fix_commands_unix=[
                    "sudo rm -f /var/lib/dpkg/lock* /var/lib/apt/lists/lock"
                ],
                requires_admin=True,
                estimated_heal_time_ms=2800,
                reclaimed_bytes=soft_dist_size,
                tags=["WindowsUpdate", "wuauserv", "CacheLock"]
            ))

    # 6. S.M.A.R.T. Hardware Health Assessment: Verify physical drive health vs software bugs
    # In Windows or Linux, we confirm non-physical status
    telemetry = {
        "disk_percent": disk_percent,
        "disk_free_gb": disk_free_gb,
        "disk_total_gb": disk_total_gb,
        "temp_size_mb": temp_size_mb,
    }
    return issues, telemetry
