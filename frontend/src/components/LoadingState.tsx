export default function LoadingState() {
  return (
    <section className="glass-card p-6">
      <div className="flex items-center gap-3">
        <div className="h-5 w-5 animate-spin rounded-full border-2 border-cyan-300 border-t-transparent" />
        <p className="text-sm font-semibold text-cyan-100">Generating EverVFX AI analysis...</p>
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="h-28 animate-pulse rounded-lg border border-white/10 bg-white/8" />
        ))}
      </div>
    </section>
  );
}

