import { BarChart3, FileText, Palette, WandSparkles } from "lucide-react";

const features = [
  { title: "Brand Match Scoring", icon: BarChart3 },
  { title: "AI Caption Improvement", icon: WandSparkles },
  { title: "Design Direction", icon: Palette },
  { title: "PDF Client Reports", icon: FileText }
];

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden border-b border-white/10">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_15%,rgba(34,211,238,.25),transparent_26rem),radial-gradient(circle_at_85%_10%,rgba(139,92,246,.28),transparent_24rem)]" />
      <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="max-w-4xl">
          <span className="inline-flex rounded-full border border-cyan-300/30 bg-cyan-300/10 px-4 py-2 text-xs font-bold uppercase tracking-[0.2em] text-cyan-100">
            Built by EverVFX
          </span>
          <h1 className="mt-6 text-5xl font-black tracking-tight text-white sm:text-6xl lg:text-7xl">
            EverVFX AI Brand Content Analyzer
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
            Analyze brand fit, caption quality, CTA strength, tone, platform performance, and campaign relevance before your content goes live.
          </p>
          <p className="mt-4 text-xl font-semibold text-cyan-100">Analyze. Improve. Publish with confidence.</p>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div key={feature.title} className="glass-card p-5">
                <Icon className="h-6 w-6 text-cyan-200" />
                <h3 className="mt-4 text-sm font-bold text-white">{feature.title}</h3>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

