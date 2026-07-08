import type { CompetitorComparison as CompetitorComparisonType } from "@/lib/types";

export default function CompetitorComparison({ comparison }: { comparison: CompetitorComparisonType }) {
  if (!comparison.available) {
    return (
      <section className="glass-card p-5">
        <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Competitor Comparison</h3>
        <p className="mt-4 text-sm leading-6 text-slate-300">{comparison.summary}</p>
      </section>
    );
  }

  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Competitor Comparison</h3>
      <p className="mt-4 text-sm leading-6 text-slate-200">{comparison.summary}</p>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-emerald-300/20 bg-emerald-400/10 p-4">
          <p className="text-sm font-bold text-emerald-100">Your strengths</p>
          <ul className="mt-3 space-y-2 text-sm text-emerald-50">
            {comparison.your_strengths.map((item) => <li key={item}>- {item}</li>)}
          </ul>
        </div>
        <div className="rounded-lg border border-violet-300/20 bg-violet-400/10 p-4">
          <p className="text-sm font-bold text-violet-100">Competitor strengths</p>
          <ul className="mt-3 space-y-2 text-sm text-violet-50">
            {comparison.competitor_strengths.map((item) => <li key={item}>- {item}</li>)}
          </ul>
        </div>
      </div>
      <p className="mt-4 rounded-lg border border-white/10 bg-white/5 p-3 text-sm leading-6 text-slate-200">{comparison.recommendation}</p>
    </section>
  );
}
