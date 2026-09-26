import time
import platform
import psutil
import uuid
import sys
from typing import List, Dict, Any
from ..models import ScanResult, OSInfo, SystemMetrics, CategoryScores, IssueItem
from ..config import is_admin
from .performance import scan_performance
from .network import scan_network
from .storage import scan_storage
from .security import scan_security

def get_os_info() -> OSInfo:
    boot_time = psutil.boot_time()
    uptime_hours = round((time.time() - boot_time) / 3600.0, 1)
    
    return OSInfo(
        system=platform.system(),
        release=platform.release(),
        version=platform.version()[:24],
        arch=platform.machine(),
        hostname=platform.node(),
        boot_time_hours=uptime_hours,
        is_admin=is_admin(),
        python_version=platform.python_version()
    )

def run_full_scan(is_simulator_mode: bool = False) -> ScanResult:
    start_t = time.time()
    scan_id = str(uuid.uuid4())[:8]
    
    os_info = get_os_info()
    all_issues: List[IssueItem] = []
    
    # Run the 4 domain scanners
    perf_issues, perf_telem = scan_performance()
    net_issues, net_telem = scan_network()
    stor_issues, stor_telem = scan_storage()
    sec_issues, sec_telem = scan_security()
    
    all_issues.extend(perf_issues)
    all_issues.extend(net_issues)
    all_issues.extend(stor_issues)
    all_issues.extend(sec_issues)
    
    # Calculate category subscores
    def calc_score(issues_subset: List[IssueItem]) -> int:
        score = 100
        for issue in issues_subset:
            if issue.severity == "critical":
                score -= 35
            elif issue.severity == "warning":
                score -= 15
            else:
                score -= 5
        return max(5, min(100, score))
        
    perf_score = calc_score([i for i in all_issues if i.category == "performance"])
    net_score = calc_score([i for i in all_issues if i.category == "network"])
    stor_score = calc_score([i for i in all_issues if i.category == "storage"])
    sec_score = calc_score([i for i in all_issues if i.category == "security"])
    
    # Weighted overall score
    overall_health = int(
        (perf_score * 0.25) +
        (net_score * 0.30) +
        (stor_score * 0.20) +
        (sec_score * 0.25)
    )
    overall_health = max(10, min(100, overall_health))
    
    category_scores = CategoryScores(
        performance=perf_score,
        network=net_score,
        storage=stor_score,
        security=sec_score
    )
    
    # Consolidated Metrics
    metrics = SystemMetrics(
        cpu_percent=perf_telem.get("cpu_percent", 12.0),
        cpu_cores=perf_telem.get("cpu_cores", 8),
        ram_percent=perf_telem.get("ram_percent", 58.0),
        ram_used_gb=perf_telem.get("ram_used_gb", 9.2),
        ram_total_gb=perf_telem.get("ram_total_gb", 16.0),
        disk_percent=stor_telem.get("disk_percent", 64.0),
        disk_free_gb=stor_telem.get("disk_free_gb", 142.0),
        disk_total_gb=stor_telem.get("disk_total_gb", 476.0),
        active_connections=net_telem.get("active_connections", 48),
        process_count=perf_telem.get("process_count", 145),
        temp_size_mb=stor_telem.get("temp_size_mb", 350.0),
        dns_latency_ms=net_telem.get("dns_latency_ms", 18.2),
        network_sent_mb=net_telem.get("network_sent_mb", 120.5),
        network_recv_mb=net_telem.get("network_recv_mb", 450.8)
    )
    
    duration_ms = int((time.time() - start_t) * 1000)
    
    critical_count = sum(1 for i in all_issues if i.severity == "critical")
    warning_count = sum(1 for i in all_issues if i.severity == "warning")
    
    return ScanResult(
        scan_id=scan_id,
        scan_duration_ms=duration_ms,
        is_simulator_mode=is_simulator_mode,
        os_info=os_info,
        health_score=overall_health,
        category_scores=category_scores,
        metrics=metrics,
        issues=all_issues,
        total_issues=len(all_issues),
        critical_issues=critical_count,
        warning_issues=warning_count
    )
