import Image from "next/image";
import { Sparkles } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/75 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="relative h-10 w-28 overflow-hidden rounded-md border border-white/15 bg-black">
            <Image src="/evervfx-logo.png" alt="EverVFX logo" fill className="object-contain p-1" sizes="112px" priority />
          </div>
          <div>
            <p className="text-sm font-black tracking-wide text-white">EverVFX AI</p>
            <p className="text-xs text-slate-400">Analyze. Improve. Publish.</p>
          </div>
        </div>

        <div className="hidden items-center gap-6 text-sm font-medium text-slate-300 md:flex">
          <a href="#dashboard" className="transition hover:text-cyan-200">Dashboard</a>
          <a href="#reports" className="transition hover:text-cyan-200">Reports</a>
          <a href="#how-it-works" className="transition hover:text-cyan-200">How It Works</a>
          <a href="#samples" className="transition hover:text-cyan-200">Samples</a>
        </div>

        <a
          href="#dashboard"
          className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-cyan-400 to-violet-500 px-4 py-2 text-sm font-bold text-white shadow-[0_0_24px_rgba(34,211,238,.25)] transition hover:scale-[1.02]"
        >
          <Sparkles className="h-4 w-4" />
          Analyze Content
        </a>
      </nav>
    </header>
  );
}

