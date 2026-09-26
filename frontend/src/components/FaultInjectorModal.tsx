import { 
  X, 
  Bug, 
  WifiOff, 
  Cpu, 
  HardDrive, 
  ShieldAlert, 
  Flame, 
  Zap, 
  ArrowRight
} from 'lucide-react';
import { CLIENT_FAULT_SCENARIOS } from '../services/api';

interface FaultInjectorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onInject: (scenarioId: string) => void;
  activeScenarioId?: string;
}

export const FaultInjectorModal: React.FC<FaultInjectorModalProps> = ({
  isOpen,
  onClose,
  onInject,
  activeScenarioId
}) => {
  if (!isOpen) return null;

  const getScenarioIcon = (iconName: string) => {
    switch (iconName) {
      case 'WifiOff': return <WifiOff className="w-5 h-5 text-blue-400" />;
      case 'Cpu': return <Cpu className="w-5 h-5 text-cyan-400" />;
      case 'HardDrive': return <HardDrive className="w-5 h-5 text-purple-400" />;
      case 'ShieldAlert': return <ShieldAlert className="w-5 h-5 text-rose-400" />;
      case 'Flame': return <Flame className="w-5 h-5 text-amber-400" />;
      default: return <Bug className="w-5 h-5 text-purple-400" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="cyber-card rounded-2xl w-full max-w-3xl overflow-hidden border border-purple-500/40 shadow-2xl flex flex-col max-h-[90vh]">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-cyber-border bg-[#0d1322]">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-500/20 border border-purple-500/30 text-purple-300">
              <Bug className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                Interactive Fault Injector
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  DEMO / PORTFOLIO SANDBOX
                </span>
              </h2>
              <p className="text-xs text-cyber-muted font-mono">
                Select a real-world PC failure scenario to test OmniHeal's root cause analysis and auto-healer
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-cyber-muted hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Scenarios Grid */}
        <div className="p-6 overflow-y-auto space-y-3.5 bg-cyber-bg/95">
          {CLIENT_FAULT_SCENARIOS.map((scenario) => {
            const isSelected = activeScenarioId === scenario.id;

            return (
              <div
                key={scenario.id}
                className={`p-4 rounded-xl border transition-all cursor-pointer relative ${
                  isSelected
                    ? 'border-purple-400 bg-purple-950/20 shadow-cyber-purple'
                    : 'border-cyber-border bg-cyber-card hover:border-slate-600 hover:bg-cyber-cardHover'
                }`}
                onClick={() => {
                  onInject(scenario.id);
                  onClose();
                }}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  
                  <div className="flex items-start gap-3.5">
                    <div className="p-2.5 rounded-xl bg-slate-900 border border-cyber-border mt-0.5">
                      {getScenarioIcon(scenario.icon)}
                    </div>

                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="text-sm font-bold text-white tracking-tight">
                          {scenario.name}
                        </h3>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.2 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                          {scenario.badge}
                        </span>
                      </div>
                      
                      <p className="text-xs text-slate-300 mt-1">
                        {scenario.description}
                      </p>

                      <div className="mt-2 text-[11px] font-mono text-rose-400 bg-rose-950/20 border border-rose-500/20 px-2.5 py-1 rounded inline-block">
                        ⚠️ Impact: {scenario.impact_description}
                      </div>
                    </div>
                  </div>

                  {/* Inject Trigger Button */}
                  <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onInject(scenario.id);
                        onClose();
                      }}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-purple-600 hover:bg-purple-500 text-white transition-all shadow-md cursor-pointer"
                    >
                      <Zap className="w-3.5 h-3.5" />
                      <span>Inject Fault</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>

                </div>
              </div>
            );
          })}
        </div>

        {/* Footer Notes */}
        <div className="px-6 py-3 border-t border-cyber-border bg-[#090e18] flex items-center justify-between text-xs font-mono text-cyber-muted">
          <span>Sandbox Mode: Host OS system files remain 100% untouched.</span>
          <button
            onClick={onClose}
            className="text-slate-300 hover:text-white"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
