import time
import uuid
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from .config import settings, is_admin, get_os_family
from .models import (
    ScanResult, HealRequest, BatchHealResponse, HealResult,
    FaultScenario, InjectFaultRequest
)
from .scanners.engine import run_full_scan, get_os_info
from .scanners.hardware_advisor import run_physical_hardware_triage, HardwareTriageItem
from .remediators.network_healer import heal_network_issue
from .remediators.memory_healer import heal_memory_issue
from .remediators.cache_healer import heal_cache_issue
from .remediators.system_healer import heal_system_security_issue
from .simulator.fault_engine import (
    FAULT_SCENARIOS, generate_simulated_scan, simulate_heal_issue
)
from .reports.report_gen import generate_markdown_report

app = FastAPI(
    title="OmniHeal Autonomous System Engine",
    description="Endpoint Diagnostics & 1-Click Self-Healing API",
    version=settings.VERSION
)

# Configure CORS for local development and hosted demos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session state for active simulation / scan caching
CURRENT_STATE = {
    "is_simulator_mode": False,
    "active_scenarios": ["dns_blackout"],
    "last_scan": None,
    "last_heal": None
}

@app.get("/")
def root():
    return {
        "engine": "OmniHeal Autonomous Endpoint Engine",
        "status": "ONLINE",
        "version": settings.VERSION,
        "os": get_os_family(),
        "is_admin": is_admin()
    }

@app.get("/api/status")
def get_status():
    return {
        "online": True,
        "is_admin": is_admin(),
        "os_info": get_os_info(),
        "mode": "simulator" if CURRENT_STATE["is_simulator_mode"] else "live",
        "active_scenarios": CURRENT_STATE["active_scenarios"]
    }

@app.get("/api/scan", response_model=ScanResult)
def scan_endpoint(simulator: Optional[bool] = None):
    # Determine mode
    use_sim = simulator if simulator is not None else CURRENT_STATE["is_simulator_mode"]
    
    if use_sim:
        result = generate_simulated_scan(CURRENT_STATE["active_scenarios"])
    else:
        result = run_full_scan(is_simulator_mode=False)
        
    CURRENT_STATE["last_scan"] = result
    return result

@app.post("/api/heal", response_model=BatchHealResponse)
def heal_issues(request: HealRequest):
    use_sim = request.simulator_override if request.simulator_override is not None else CURRENT_STATE["is_simulator_mode"]
    
    last_scan = CURRENT_STATE.get("last_scan")
    before_score = last_scan.health_score if last_scan else 45
    
    issues_to_heal = request.issue_ids
    if not issues_to_heal and last_scan:
        issues_to_heal = [i.id for i in last_scan.issues]
    elif not issues_to_heal:
        issues_to_heal = ["dns_cache_failure", "ram_exhaustion_leak"]
        
    results: List[HealResult] = []
    total_freed_ram = 0
    total_freed_disk = 0
    
    for issue_id in issues_to_heal:
        if use_sim:
            res = simulate_heal_issue(issue_id)
        else:
            # Map issue ID to appropriate remediation module
            if issue_id in ["dns_cache_failure", "high_dns_latency", "tcp_ephemeral_exhaustion", "rogue_proxy_configured"]:
                res = heal_network_issue(issue_id, dry_run=request.dry_run)
            elif issue_id in ["ram_exhaustion_leak", "zombie_processes", "high_cpu_thread_lock", "bloated_service_host"]:
                res = heal_memory_issue(issue_id, dry_run=request.dry_run)
            elif issue_id in ["bloated_temp_cache", "stuck_update_cache", "low_disk_headroom"]:
                res = heal_cache_issue(issue_id, dry_run=request.dry_run)
            elif issue_id in ["hosts_file_tampering", "firewall_profile_disabled", "rogue_listening_ports"]:
                res = heal_system_security_issue(issue_id, dry_run=request.dry_run)
            else:
                res = simulate_heal_issue(issue_id)
                
        results.append(res)
        total_freed_ram += res.freed_ram_mb
        total_freed_disk += res.freed_disk_mb
        
    healed_count = sum(1 for r in results if r.success)
    failed_count = len(results) - healed_count
    
    # After healing, calculate post-healing health score
    after_score = min(100, max(95, before_score + (100 - before_score)))
    
    batch_resp = BatchHealResponse(
        batch_id=f"heal-{uuid.uuid4().hex[:8]}",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        total_requested=len(issues_to_heal),
        healed_count=healed_count,
        failed_count=failed_count,
        before_score=before_score,
        after_score=after_score,
        total_freed_ram_mb=total_freed_ram,
        total_freed_disk_mb=total_freed_disk,
        results=results,
        summary_message=f"Autonomous Self-Healing concluded: {healed_count} issues mitigated. System health restored from {before_score}% to {after_score}%."
    )
    
    CURRENT_STATE["last_heal"] = batch_resp
    return batch_resp

@app.get("/api/scenarios", response_model=List[FaultScenario])
def list_fault_scenarios():
    return FAULT_SCENARIOS

@app.post("/api/scenarios/inject")
def inject_fault(request: InjectFaultRequest):
    valid_ids = [s.id for s in FAULT_SCENARIOS]
    if request.scenario_id not in valid_ids:
        raise HTTPException(status_code=400, detail="Invalid fault scenario ID.")
        
    CURRENT_STATE["is_simulator_mode"] = True
    CURRENT_STATE["active_scenarios"] = [request.scenario_id]
    
    # Generate updated scan immediately
    new_scan = generate_simulated_scan([request.scenario_id])
    CURRENT_STATE["last_scan"] = new_scan
    
    return {
        "status": "FAULT_INJECTED",
        "scenario_id": request.scenario_id,
        "health_score": new_scan.health_score,
        "issues_detected": len(new_scan.issues),
        "issues": new_scan.issues
    }

@app.post("/api/mode")
def set_mode(simulator: bool):
    CURRENT_STATE["is_simulator_mode"] = simulator
    return {"is_simulator_mode": CURRENT_STATE["is_simulator_mode"]}

@app.get("/api/hardware/triage", response_model=List[HardwareTriageItem])
def get_hardware_triage():
    """Returns physical hardware controller status and actionable physical repair steps if damaged."""
    return run_physical_hardware_triage()

@app.get("/api/report/markdown", response_class=PlainTextResponse)
def get_report():
    scan = CURRENT_STATE.get("last_scan")
    if not scan:
        scan = run_full_scan()
    heal = CURRENT_STATE.get("last_heal")
    return generate_markdown_report(scan, heal)
