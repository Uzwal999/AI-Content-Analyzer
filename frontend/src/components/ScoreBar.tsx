interface ScoreBarProps {
  value: number;
  max?: number;
  label?: string;
}

function barColor(percent: number): string {
  if (percent >= 80) return "from-emerald-400 to-cyan-300";
  if (percent >= 60) return "from-cyan-400 to-blue-400";
  if (percent >= 40) return "from-amber-300 to-orange-400";
  return "from-red-400 to-rose-500";
}

export default function ScoreBar({ value, max = 100, label }: ScoreBarProps) {
  const percent = Math.max(0, Math.min(100, (value / max) * 100));

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3 text-xs font-medium text-slate-400">
        <span className="truncate">{label ?? "Score"}</span>
        <span className="text-slate-200">
          {value}/{max}
        </span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-white/10">
        <div className={`h-full rounded-full bg-gradient-to-r ${barColor(percent)} shadow-[0_0_18px_rgba(34,211,238,.35)]`} style={{ width: `${percent}%` }} />
      </div>
    </div>
  );
}

