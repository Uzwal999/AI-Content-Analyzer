interface BadgeProps {
  label: string;
  tone?: "default" | "success" | "warning" | "danger" | "cyan";
}

function badgeClass(label: string, tone: BadgeProps["tone"]): string {
  if (tone === "success" || label === "Strong" || label === "Ready to Publish" || label === "Low") {
    return "border-emerald-400/40 bg-emerald-400/10 text-emerald-200";
  }
  if (tone === "warning" || label === "Good" || label === "Needs Improvement" || label === "Medium") {
    return "border-amber-400/40 bg-amber-400/10 text-amber-200";
  }
  if (tone === "danger" || label === "Weak" || label === "High" || label === "Not Ready") {
    return "border-red-400/40 bg-red-400/10 text-red-200";
  }
  if (tone === "cyan") return "border-cyan-400/40 bg-cyan-400/10 text-cyan-100";
  return "border-white/15 bg-white/8 text-slate-200";
}

export default function Badge({ label, tone = "default" }: BadgeProps) {
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${badgeClass(label, tone)}`}>
      {label}
    </span>
  );
}

