import type { ReactNode } from "react";

import ScoreBar from "./ScoreBar";

interface ScoreCardProps {
  title: string;
  score: number;
  max: number;
  children?: ReactNode;
}

export default function ScoreCard({ title, score, max, children }: ScoreCardProps) {
  return (
    <section className="glass-card p-5 transition hover:-translate-y-0.5 hover:border-cyan-300/35">
      <div className="mb-4 flex items-start justify-between gap-4">
        <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">{title}</h3>
        <span className="text-lg font-black text-white">
          {score}
          <span className="text-sm font-semibold text-slate-500">/{max}</span>
        </span>
      </div>
      <ScoreBar value={score} max={max} label={title} />
      {children ? <div className="mt-4 text-sm leading-6 text-slate-300">{children}</div> : null}
    </section>
  );
}

