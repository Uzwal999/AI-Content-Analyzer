import { WifiOff } from "lucide-react";

export default function ErrorState({ message }: { message: string }) {
  return (
    <section className="glass-card border-red-400/30 bg-red-500/10 p-6">
      <div className="flex items-start gap-3">
        <WifiOff className="h-5 w-5 flex-none text-red-200" />
        <div>
          <h2 className="text-lg font-bold text-red-100">Unable to connect to analysis API</h2>
          <p className="mt-2 text-sm leading-6 text-red-100/80">
            {message || "Please make sure the FastAPI backend is running on port 8000."}
          </p>
        </div>
      </div>
    </section>
  );
}
