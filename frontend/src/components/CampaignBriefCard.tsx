import type { CampaignBrief } from "@/lib/types";

export default function CampaignBriefCard({ brief }: { brief: CampaignBrief }) {
  const rows = [
    ["Campaign goal", brief.campaign_goal],
    ["Target audience", brief.target_audience],
    ["Recommended post type", brief.recommended_post_type],
    ["Content angle", brief.content_angle],
    ["Caption tone", brief.caption_tone],
    ["Recommended CTA", brief.recommended_cta],
    ["Key message", brief.key_message],
    ["Follow-up", brief.suggested_follow_up_content]
  ];

  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Campaign Brief</h3>
      <div className="mt-4 space-y-3">
        {rows.map(([label, value]) => (
          <div key={label} className="rounded-lg border border-white/10 bg-white/5 p-3">
            <p className="text-xs font-bold uppercase tracking-widest text-cyan-200">{label}</p>
            <p className="mt-1 text-sm leading-6 text-slate-200">{value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

