import type { BeforeAfter } from "@/lib/types";

export default function BeforeAfterComparison({ beforeAfter }: { beforeAfter: BeforeAfter }) {
  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Before vs After Caption</h3>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-white/10 bg-black/20 p-4">
          <p className="text-xs font-bold uppercase tracking-widest text-slate-500">Original</p>
          <p className="mt-3 whitespace-pre-line text-sm leading-7 text-slate-300">{beforeAfter.original || "No original caption provided."}</p>
        </div>
        <div className="rounded-lg border border-cyan-300/20 bg-cyan-300/10 p-4">
          <p className="text-xs font-bold uppercase tracking-widest text-cyan-200">Improved</p>
          <p className="mt-3 whitespace-pre-line text-sm leading-7 text-white">{beforeAfter.improved}</p>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {beforeAfter.key_improvements.map((item) => (
          <span key={item} className="rounded-full border border-violet-300/25 bg-violet-400/10 px-3 py-1 text-xs font-semibold text-violet-100">
            {item}
          </span>
        ))}
      </div>
    </section>
  );
}

