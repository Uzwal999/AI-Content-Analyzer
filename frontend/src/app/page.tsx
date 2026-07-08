import AnalyzerForm from "@/components/AnalyzerForm";
import HeroSection from "@/components/HeroSection";
import Navbar from "@/components/Navbar";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950">
      <Navbar />
      <HeroSection />

      <section className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="absolute inset-x-4 top-10 -z-0 h-72 rounded-full bg-cyan-400/10 blur-3xl" />
        <div className="relative z-10">
          <AnalyzerForm />
        </div>
      </section>

      <section id="how-it-works" className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
        <div className="glass-card p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-cyan-200">How it works</p>
          <div className="mt-4 grid gap-4 md:grid-cols-4">
            {["Add brand and platform details", "Run local rule-based AI analysis", "Review caption, design, and campaign insights", "Export a client-ready PDF report"].map((step, index) => (
              <div key={step} className="rounded-lg border border-white/10 bg-white/5 p-4">
                <span className="text-2xl font-black text-cyan-200">0{index + 1}</span>
                <p className="mt-3 text-sm leading-6 text-slate-300">{step}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-white/10 px-4 py-8 text-center text-sm text-slate-500">
        (c) EverVFX AI Tools
      </footer>
    </main>
  );
}
