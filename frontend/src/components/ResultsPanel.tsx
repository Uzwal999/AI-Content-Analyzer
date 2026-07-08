"use client";

import { FileJson, Target } from "lucide-react";

import type { AnalysisResult, AnalyzeRequest } from "@/lib/types";

import Badge from "./Badge";
import BeforeAfterComparison from "./BeforeAfterComparison";
import CalendarSuggestionCard from "./CalendarSuggestionCard";
import CampaignBriefCard from "./CampaignBriefCard";
import CircularScore from "./CircularScore";
import ClientReportPreview from "./ClientReportPreview";
import CompetitorComparison from "./CompetitorComparison";
import DesignDirectionCard from "./DesignDirectionCard";
import EmptyState from "./EmptyState";
import ErrorState from "./ErrorState";
import ImprovedCaptionCard from "./ImprovedCaptionCard";
import LoadingState from "./LoadingState";
import PDFExportButton from "./PDFExportButton";
import ProblemCard from "./ProblemCard";
import ScoreBar from "./ScoreBar";
import ScoreCard from "./ScoreCard";
import SuggestionCard from "./SuggestionCard";

interface ResultsPanelProps {
  result: AnalysisResult | null;
  request: AnalyzeRequest | null;
  loading: boolean;
  error: string;
}

function exportJson(result: AnalysisResult) {
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `evervfx-brand-analysis-${Date.now()}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function DetailCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="glass-card p-5">
      <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">{title}</h3>
      <div className="mt-4 text-sm leading-6 text-slate-300">{children}</div>
    </section>
  );
}

export default function ResultsPanel({ result, request, loading, error }: ResultsPanelProps) {
  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} />;
  if (!result) return <EmptyState />;

  return (
    <div className="space-y-5">
      <section className="glass-card overflow-hidden p-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
            <CircularScore value={result.overall_score} label="Score" />
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-200">Overall Brand Match Score</p>
              <h2 className="mt-3 text-3xl font-black tracking-tight text-white">{result.publish_readiness}</h2>
              <p className="mt-3 max-w-xl text-sm leading-6 text-slate-300">{result.final_recommendation}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                <Badge label={result.score_label} />
                <Badge label={`${result.brand_voice_score}/100 Brand Voice`} tone="cyan" />
                <Badge label={result.content_type} />
                <Badge label={result.content_pillar} />
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => exportJson(result)}
              className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-bold text-white transition hover:bg-white/15"
            >
              <FileJson className="h-4 w-4" />
              Export JSON
            </button>
            {request ? <PDFExportButton result={result} request={request} /> : null}
          </div>
        </div>
      </section>

      <section className="glass-card p-5">
        <div className="mb-4 flex items-center gap-2">
          <Target className="h-5 w-5 text-cyan-200" />
          <h3 className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Score Breakdown</h3>
        </div>
        <div className="grid gap-4 lg:grid-cols-2">
          {Object.entries(result.score_breakdown).map(([label, item]) => (
            <ScoreBar key={label} value={item.score} max={item.max_score} label={label} />
          ))}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-3">
        <ScoreCard title="Hook Strength" score={result.hook_analysis.hook_score} max={10}>
          <Badge label={result.hook_analysis.hook_strength} />
          <p className="mt-3 font-semibold text-white">First line</p>
          <p>{result.hook_analysis.first_line || "No hook detected"}</p>
          <p className="mt-3">{result.hook_analysis.comment}</p>
        </ScoreCard>

        <ScoreCard title="Tone Analysis" score={result.tone_analysis.tone_score} max={15}>
          <div className="mb-3 flex flex-wrap gap-2">
            {result.tone_analysis.detected_tone.map((tone) => <Badge key={tone} label={tone} />)}
          </div>
          {result.tone_analysis.comment}
        </ScoreCard>

        <ScoreCard title="CTA Strength" score={result.cta_analysis.cta_strength} max={15}>
          <p>{result.cta_analysis.comment}</p>
          <p className="mt-2 font-semibold text-white">Detected: {result.cta_analysis.detected_cta || "None"}</p>
          <p className="mt-2 text-slate-400">Recommended: {result.cta_analysis.recommended_ctas.join(", ")}</p>
        </ScoreCard>

        <ScoreCard title="Keyword Match" score={result.keyword_analysis.keyword_score} max={20}>
          <p className="font-semibold text-white">Matched keywords</p>
          <p>{result.keyword_analysis.matched_keywords.join(", ") || "None yet"}</p>
          <p className="mt-2 font-semibold text-white">Missing opportunities</p>
          <p>{result.keyword_analysis.missing_keywords.join(", ") || "No major gaps"}</p>
        </ScoreCard>

        <ScoreCard title="Hashtag Quality" score={result.hashtag_analysis.hashtag_score} max={5}>
          <p>{result.hashtag_analysis.comment}</p>
          <p className="mt-2">Count: {result.hashtag_analysis.hashtag_count}</p>
          <p className="mt-2">Relevant: {result.hashtag_analysis.relevant_hashtags.join(", ") || "None detected"}</p>
          <p>Generic: {result.hashtag_analysis.generic_hashtags.join(", ") || "None detected"}</p>
        </ScoreCard>

        <ScoreCard title="Caption Quality" score={result.caption_quality.clarity_score} max={15}>
          <p>{result.caption_quality.comment}</p>
          <p className="mt-2">
            {result.caption_quality.word_count} words | {result.caption_quality.character_count} characters | {result.caption_quality.emoji_count} emojis
          </p>
        </ScoreCard>

        <ScoreCard title="Campaign Goal Relevance" score={result.campaign_goal_relevance.score} max={10}>
          {result.campaign_goal_relevance.comment}
        </ScoreCard>

        <DetailCard title="Platform Suggestions">
          <p className="mb-3 font-semibold text-white">{result.platform_suggestions.platform}</p>
          <ul className="space-y-2">
            {result.platform_suggestions.suggestions.map((item) => <li key={item}>- {item}</li>)}
          </ul>
        </DetailCard>

        <DetailCard title="Brand Safety Risk">
          <Badge label={result.risk_analysis.risk_level} />
          <p className="mt-3">{result.risk_analysis.comment}</p>
          <p className="mt-2 text-slate-400">Risky terms: {result.risk_analysis.risky_terms.join(", ") || "None detected"}</p>
        </DetailCard>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <section className="glass-card p-5">
          <h3 className="mb-4 text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Problems Found</h3>
          <div className="space-y-3">
            {result.problems.length ? result.problems.map((item) => <ProblemCard key={item} text={item} />) : <p className="text-sm text-slate-400">No major problems found.</p>}
          </div>
        </section>

        <section className="glass-card p-5">
          <h3 className="mb-4 text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Improvement Suggestions</h3>
          <div className="space-y-3">
            {result.suggestions.map((item) => <SuggestionCard key={item} text={item} />)}
          </div>
        </section>
      </div>

      <BeforeAfterComparison beforeAfter={result.before_after} />
      <ImprovedCaptionCard caption={result.improved_caption} />

      <div className="grid gap-5 xl:grid-cols-2">
        <CampaignBriefCard brief={result.campaign_brief} />
        <DesignDirectionCard direction={result.design_direction} />
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <CalendarSuggestionCard calendar={result.calendar_suggestion} />
        <CompetitorComparison comparison={result.competitor_comparison} />
      </div>

      {request ? <ClientReportPreview result={result} request={request} /> : null}
    </div>
  );
}
