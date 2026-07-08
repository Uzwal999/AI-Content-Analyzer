import type { AnalysisResult, AnalyzeRequest } from "@/lib/types";

export default function ClientReportPreview({ result, request }: { result: AnalysisResult; request: AnalyzeRequest }) {
  return (
    <section id="reports" className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Client Report Preview</h3>
      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <div className="rounded-lg border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-bold uppercase tracking-widest text-cyan-200">Client</p>
          <p className="mt-2 text-lg font-bold text-white">{request.client_details.client_name || request.brand}</p>
          <p className="mt-1 text-sm text-slate-400">{request.client_details.campaign_name || request.campaign_goal}</p>
        </div>
        <div className="rounded-lg border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-bold uppercase tracking-widest text-cyan-200">Score Summary</p>
          <p className="mt-2 text-lg font-bold text-white">{result.overall_score}/100 - {result.score_label}</p>
          <p className="mt-1 text-sm text-slate-400">{result.publish_readiness}</p>
        </div>
        <div className="rounded-lg border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-bold uppercase tracking-widest text-cyan-200">Prepared By</p>
          <p className="mt-2 text-lg font-bold text-white">{request.client_details.prepared_by || "EverVFX"}</p>
          <p className="mt-1 text-sm text-slate-400">{request.client_details.brand_manager_name || "EverVFX AI Tools"}</p>
        </div>
      </div>
      <div className="mt-4 rounded-lg border border-white/10 bg-black/20 p-4">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-500">Included in PDF</p>
        <p className="mt-2 text-sm leading-6 text-slate-300">
          Original caption, improved caption, problems, suggestions, campaign brief, design direction, content calendar, competitor comparison, and final recommendation.
        </p>
      </div>
    </section>
  );
}
