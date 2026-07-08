import type { CalendarSuggestion } from "@/lib/types";

export default function CalendarSuggestionCard({ calendar }: { calendar: CalendarSuggestion }) {
  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Content Calendar Suggestion</h3>
      <div className="mt-4 rounded-lg border border-cyan-300/20 bg-cyan-300/10 p-4">
        <p className="text-sm text-slate-300">Suggested day</p>
        <p className="text-2xl font-black text-white">{calendar.suggested_day}</p>
        <p className="mt-1 text-sm text-cyan-100">{calendar.content_role}</p>
      </div>
      <div className="mt-4 grid gap-3 lg:grid-cols-2">
        <div>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest text-slate-400">Follow-up posts</p>
          <ul className="space-y-2 text-sm text-slate-300">
            {calendar.follow_up_posts.map((item) => <li key={item}>- {item}</li>)}
          </ul>
        </div>
        <div>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest text-slate-400">Weekly sequence</p>
          <ul className="space-y-2 text-sm text-slate-300">
            {calendar.weekly_sequence.map((item) => <li key={item}>- {item}</li>)}
          </ul>
        </div>
      </div>
    </section>
  );
}

