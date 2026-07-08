import { AlertTriangle } from "lucide-react";

export default function ProblemCard({ text }: { text: string }) {
  return (
    <div className="flex gap-3 rounded-lg border border-amber-300/20 bg-amber-400/10 p-3 text-sm leading-6 text-amber-50">
      <AlertTriangle className="mt-0.5 h-4 w-4 flex-none text-amber-300" />
      <span>{text}</span>
    </div>
  );
}

