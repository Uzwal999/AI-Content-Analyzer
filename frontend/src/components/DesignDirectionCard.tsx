import type { DesignDirection } from "@/lib/types";

export default function DesignDirectionCard({ direction }: { direction: DesignDirection }) {
  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Design Direction</h3>
      <p className="mt-4 text-sm leading-7 text-slate-200">{direction.visual_style}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {direction.colors.map((color) => (
          <span key={color} className="rounded-full border border-white/15 bg-white/8 px-3 py-1 text-xs font-semibold text-slate-200">
            {color}
          </span>
        ))}
      </div>
      <div className="mt-4 space-y-3 text-sm leading-6 text-slate-300">
        <p><span className="font-bold text-white">Typography:</span> {direction.typography}</p>
        <p><span className="font-bold text-white">Layout:</span> {direction.layout_suggestion}</p>
        <p><span className="font-bold text-white">Imagery:</span> {direction.imagery_suggestion}</p>
      </div>
    </section>
  );
}

