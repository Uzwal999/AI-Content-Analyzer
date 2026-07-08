import { Sparkles } from "lucide-react";

export default function EmptyState() {
  return (
    <section className="glass-card flex min-h-[420px] flex-col items-center justify-center p-8 text-center">
      <div className="mb-5 rounded-2xl border border-cyan-300/25 bg-cyan-300/10 p-4 text-cyan-200">
        <Sparkles className="h-8 w-8" />
      </div>
      <p className="text-xs font-bold uppercase tracking-[0.24em] text-cyan-200">EverVFX AI report</p>
      <h2 className="mt-3 max-w-xl text-3xl font-black tracking-tight text-white">
        Enter your content details and run analysis to generate your EverVFX AI brand report.
      </h2>
      <p className="mt-4 max-w-lg text-sm leading-6 text-slate-400">
        Your dashboard will show brand fit, hook strength, tone, CTA quality, campaign direction, visual recommendations, and PDF export.
      </p>
    </section>
  );
}

