interface CircularScoreProps {
  value: number;
  label: string;
}

export default function CircularScore({ value, label }: CircularScoreProps) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.max(0, Math.min(100, value)) / 100) * circumference;

  return (
    <div className="relative flex h-40 w-40 items-center justify-center">
      <svg className="h-40 w-40 -rotate-90" viewBox="0 0 140 140" aria-hidden="true">
        <circle cx="70" cy="70" r={radius} stroke="rgba(255,255,255,.12)" strokeWidth="12" fill="none" />
        <circle
          cx="70"
          cy="70"
          r={radius}
          stroke="url(#scoreGradient)"
          strokeWidth="12"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
        <defs>
          <linearGradient id="scoreGradient" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stopColor="#22d3ee" />
            <stop offset="55%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor="#f0abfc" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute text-center">
        <div className="text-4xl font-black text-white">{value}</div>
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">{label}</div>
      </div>
    </div>
  );
}

