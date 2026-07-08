"use client";

import { Copy, WandSparkles } from "lucide-react";

interface ImprovedCaptionCardProps {
  caption: string;
}

export default function ImprovedCaptionCard({ caption }: ImprovedCaptionCardProps) {
  async function copyCaption() {
    await navigator.clipboard.writeText(caption);
  }

  return (
    <section className="relative overflow-hidden rounded-2xl border border-cyan-300/25 bg-gradient-to-br from-cyan-400/15 via-violet-500/15 to-white/5 p-5 shadow-[0_0_40px_rgba(34,211,238,.12)]">
      <div className="absolute -right-16 -top-16 h-36 w-36 rounded-full bg-cyan-300/20 blur-3xl" />
      <div className="relative mb-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-cyan-300/25 bg-cyan-300/10 p-2 text-cyan-100">
            <WandSparkles className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold uppercase tracking-[0.18em] text-cyan-100">Improved Caption</h3>
            <p className="text-xs text-slate-400">Generated based on selected brand tone, campaign goal, and platform.</p>
          </div>
        </div>
        <button
          type="button"
          onClick={copyCaption}
          className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-xs font-bold text-white transition hover:bg-white/15"
        >
          <Copy className="h-4 w-4" />
          Copy Improved Caption
        </button>
      </div>
      <p className="relative whitespace-pre-line text-sm leading-7 text-white">{caption}</p>
    </section>
  );
}
