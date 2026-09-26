export type IssueCategory = 'performance' | 'network' | 'storage' | 'security';
export type SeverityLevel = 'critical' | 'warning' | 'info';
export type IssueStatus = 'detected' | 'healing' | 'healed' | 'failed' | 'ignored';
export type VerdictType = 'Software-Solvable' | 'Hardware-Warning' | 'Configuration-Anomaly';

export interface IssueItem {
  id: string;
  category: IssueCategory;
  title: string;
  symptom: string;
  root_cause: string;
  verdict: VerdictType;
  verdict_detail: string;
  severity: SeverityLevel;
  fix_title: string;
  fix_description: string;
  fix_commands_windows: string[];
  fix_commands_unix: string[];
  requires_admin: boolean;
  estimated_heal_time_ms: number;
  reclaimed_bytes?: number;
  reclaimed_ram_mb?: number;
  status: IssueStatus;
  tags: string[];
  timestamp: string;
}

export interface CategoryScores {
  performance: number;
  network: number;
  storage: number;
  security: number;
}

export interface SystemMetrics {
  cpu_percent: number;
  cpu_cores: number;
  ram_percent: number;
  ram_used_gb: number;
  ram_total_gb: number;
  disk_percent: number;
  disk_free_gb: number;
  disk_total_gb: number;
  active_connections: number;
  process_count: number;
  temp_size_mb: number;
  dns_latency_ms: number;
  network_sent_mb: number;
  network_recv_mb: number;
}

export interface OSInfo {
  system: string;
  release: string;
  version: string;
  arch: string;
  hostname: string;
  boot_time_hours: number;
  is_admin: boolean;
  python_version: string;
}

export interface ScanResult {
  scan_id: string;
  timestamp: string;
  scan_duration_ms: number;
  is_simulator_mode: boolean;
  os_info: OSInfo;
  health_score: number;
  category_scores: CategoryScores;
  metrics: SystemMetrics;
  issues: IssueItem[];
  total_issues: number;
  critical_issues: number;
  warning_issues: number;
}

export interface HealLogEntry {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS' | 'HEALED';
  module: string;
  command?: string;
  output: string;
  exit_code?: number;
}

export interface HealResult {
  success: boolean;
  issue_id: string;
  status: IssueStatus;
  logs: HealLogEntry[];
  duration_ms: number;
  freed_ram_mb: number;
  freed_disk_mb: number;
}

export interface BatchHealResponse {
  batch_id: string;
  timestamp: string;
  total_requested: number;
  healed_count: number;
  failed_count: number;
  before_score: number;
  after_score: number;
  total_freed_ram_mb: number;
  total_freed_disk_mb: number;
  results: HealResult[];
  summary_message: string;
}

export interface FaultScenario {
  id: string;
  name: string;
  badge: string;
  icon: string;
  description: string;
  category: IssueCategory;
  injected_issues: string[];
  impact_description: string;
  simulated_metrics_impact: Record<string, any>;
}

export interface HardwareTriageItem {
  id: string;
  component: string;
  hardware_name: string;
  status: 'PHYSICAL_HEALTHY' | 'PHYSICAL_WARNING' | 'PHYSICAL_CRITICAL';
  is_physical_issue: boolean;
  confidence_pct: number;
  diagnostics_reading: string;
  actionable_repair_guide: string[];
}
