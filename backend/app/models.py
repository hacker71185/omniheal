from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

IssueCategory = Literal["performance", "network", "storage", "security"]
SeverityLevel = Literal["critical", "warning", "info"]
IssueStatus = Literal["detected", "healing", "healed", "failed", "ignored"]
VerdictType = Literal["Software-Solvable", "Hardware-Warning", "Configuration-Anomaly"]

class IssueItem(BaseModel):
    id: str
    category: IssueCategory
    title: str
    symptom: str
    root_cause: str
    verdict: VerdictType = "Software-Solvable"
    verdict_detail: str = "100% Non-Physical / Safe Software Remediation"
    severity: SeverityLevel
    fix_title: str
    fix_description: str
    fix_commands_windows: List[str] = []
    fix_commands_unix: List[str] = []
    requires_admin: bool = False
    estimated_heal_time_ms: int = 1500
    reclaimed_bytes: Optional[int] = 0
    reclaimed_ram_mb: Optional[int] = 0
    status: IssueStatus = "detected"
    tags: List[str] = []
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class CategoryScores(BaseModel):
    performance: int = 100
    network: int = 100
    storage: int = 100
    security: int = 100

class SystemMetrics(BaseModel):
    cpu_percent: float = 0.0
    cpu_cores: int = 4
    ram_percent: float = 0.0
    ram_used_gb: float = 0.0
    ram_total_gb: float = 16.0
    disk_percent: float = 0.0
    disk_free_gb: float = 0.0
    disk_total_gb: float = 512.0
    active_connections: int = 0
    process_count: int = 0
    temp_size_mb: float = 0.0
    dns_latency_ms: float = 0.0
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0

class OSInfo(BaseModel):
    system: str
    release: str
    version: str
    arch: str
    hostname: str
    boot_time_hours: float
    is_admin: bool
    python_version: str

class ScanResult(BaseModel):
    scan_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    scan_duration_ms: int = 0
    is_simulator_mode: bool = False
    os_info: OSInfo
    health_score: int = 100
    category_scores: CategoryScores
    metrics: SystemMetrics
    issues: List[IssueItem] = []
    total_issues: int = 0
    critical_issues: int = 0
    warning_issues: int = 0

class HealRequest(BaseModel):
    issue_ids: Optional[List[str]] = None  # None or empty = Heal all
    dry_run: bool = False
    simulator_override: Optional[bool] = None

class HealLogEntry(BaseModel):
    timestamp: str
    level: Literal["INFO", "WARN", "ERROR", "SUCCESS", "HEALED"]
    module: str
    command: Optional[str] = None
    output: str
    exit_code: Optional[int] = 0

class HealResult(BaseModel):
    success: bool
    issue_id: str
    status: IssueStatus
    logs: List[HealLogEntry]
    duration_ms: int
    freed_ram_mb: int = 0
    freed_disk_mb: int = 0

class BatchHealResponse(BaseModel):
    batch_id: str
    timestamp: str
    total_requested: int
    healed_count: int
    failed_count: int
    before_score: int
    after_score: int
    total_freed_ram_mb: int
    total_freed_disk_mb: int
    results: List[HealResult]
    summary_message: str

class FaultScenario(BaseModel):
    id: str
    name: str
    badge: str
    icon: str
    description: str
    category: IssueCategory
    injected_issues: List[str]
    impact_description: str
    simulated_metrics_impact: Dict[str, Any] = {}

class InjectFaultRequest(BaseModel):
    scenario_id: str
