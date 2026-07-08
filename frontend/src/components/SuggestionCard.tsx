import { CheckCircle2 } from "lucide-react";

export default function SuggestionCard({ text }: { text: string }) {
  return (
    <div className="flex gap-3 rounded-lg border border-emerald-300/20 bg-emerald-400/10 p-3 text-sm leading-6 text-emerald-50">
      <CheckCircle2 className="mt-0.5 h-4 w-4 flex-none text-emerald-300" />
      <span>{text}</span>
    </div>
  );
}

