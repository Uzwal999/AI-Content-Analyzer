"use client";

import { FormEvent, useEffect, useState } from "react";
import { RotateCcw, Send, WandSparkles } from "lucide-react";

import { sampleCaptions } from "@/data/sampleCaptions";
import { API_URL, analyzeCaption, fetchBrands } from "@/lib/api";
import type { AnalysisResult, AnalyzeRequest, BrandName, CampaignGoal, Platform, PostType } from "@/lib/types";

import ResultsPanel from "./ResultsPanel";

const BRAND_OPTIONS: BrandName[] = ["The ISMA", "TMB Bar", "AESN", "EverVFX", "Custom Brand"];
const PLATFORM_OPTIONS: Platform[] = ["Instagram", "LinkedIn", "Facebook", "TikTok", "X/Twitter"];
const POST_TYPES: PostType[] = [
  "Static Post",
  "Carousel",
  "Reel",
  "Story",
  "LinkedIn Post",
  "Product Post",
  "Hiring Post",
  "Event Post",
  "Service Promotion",
  "Testimonial Post"
];
const CAMPAIGN_GOALS: CampaignGoal[] = [
  "Awareness",
  "Engagement",
  "Sales",
  "Hiring",
  "Website Traffic",
  "Lead Generation",
  "Brand Trust",
  "Community Building"
];

const emptyRequest: AnalyzeRequest = {
  brand: "EverVFX",
  platform: "LinkedIn",
  post_type: "Service Promotion",
  campaign_goal: "Lead Generation",
  caption: "",
  audience: "",
  hashtags: "",
  competitor_caption: "",
  agency_mode: false,
  client_details: {
    client_name: "",
    campaign_name: "",
    prepared_by: "EverVFX",
    report_notes: "",
    brand_manager_name: "",
    date_generated: ""
  },
  custom_brand: null
};

const emptyCustomBrand = {
  brand_name: "",
  industry: "",
  desired_tone: "",
  keywords: "",
  avoid_words: "",
  cta_examples: "",
  target_audience: "",
  brand_personality: "",
  visual_style: ""
};

function splitList(value: string): string[] {
  return value
    .split(/[,;\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function countWords(value: string): number {
  return value.trim() ? value.trim().split(/\s+/).length : 0;
}

export default function AnalyzerForm() {
  const [form, setForm] = useState<AnalyzeRequest>(emptyRequest);
  const [customBrand, setCustomBrand] = useState(emptyCustomBrand);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [submittedRequest, setSubmittedRequest] = useState<AnalyzeRequest | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiStatus, setApiStatus] = useState("Checking FastAPI connection...");

  useEffect(() => {
    fetchBrands()
      .then((brands) => setApiStatus(`${Object.keys(brands).length} brand profiles loaded from FastAPI`))
      .catch(() => setApiStatus(`FastAPI backend not connected yet. Expected API: ${API_URL}`));
  }, []);

  function updateField<Key extends keyof AnalyzeRequest>(key: Key, value: AnalyzeRequest[Key]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function updateClientDetail<Key extends keyof AnalyzeRequest["client_details"]>(key: Key, value: AnalyzeRequest["client_details"][Key]) {
    setForm((current) => ({
      ...current,
      client_details: {
        ...current.client_details,
        [key]: value
      }
    }));
  }

  function buildPayload(): AnalyzeRequest {
    if (form.brand !== "Custom Brand") {
      return { ...form, custom_brand: null };
    }

    return {
      ...form,
      custom_brand: {
        brand_name: customBrand.brand_name,
        industry: customBrand.industry,
        desired_tone: splitList(customBrand.desired_tone),
        keywords: splitList(customBrand.keywords),
        avoid_words: splitList(customBrand.avoid_words),
        cta_examples: splitList(customBrand.cta_examples),
        target_audience: customBrand.target_audience,
        brand_personality: customBrand.brand_personality,
        visual_style: customBrand.visual_style
      }
    };
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (!form.caption.trim()) {
      setError("Please enter a caption before running the analysis.");
      return;
    }

    const payload = buildPayload();
    setLoading(true);
    try {
      const analysis = await analyzeCaption(payload);
      setResult(analysis);
      setSubmittedRequest(payload);
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to analyze this caption.";
      setError(message.includes("Failed to fetch") ? `Unable to connect to analysis API at ${API_URL}. Start the backend or run run_app.bat.` : message);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setForm(emptyRequest);
    setCustomBrand(emptyCustomBrand);
    setResult(null);
    setSubmittedRequest(null);
    setError("");
  }

  function loadSample(sample: AnalyzeRequest) {
    setForm(sample);
    setCustomBrand(emptyCustomBrand);
    setResult(null);
    setSubmittedRequest(null);
    setError("");
  }

  const captionCharacters = form.caption.length;
  const captionWords = countWords(form.caption);

  return (
    <div id="dashboard" className="grid gap-6 xl:grid-cols-[460px_minmax(0,1fr)]">
      <form onSubmit={handleSubmit} className="glass-card h-fit p-5">
        <div className="mb-5 rounded-lg border border-white/10 bg-white/5 p-3 text-xs font-medium leading-5 text-slate-400">{apiStatus}</div>

        <div className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="form-label">Brand</span>
              <select value={form.brand} onChange={(event) => updateField("brand", event.target.value as BrandName)} className="form-control">
                {BRAND_OPTIONS.map((brand) => <option key={brand}>{brand}</option>)}
              </select>
            </label>

            <label className="block">
              <span className="form-label">Platform</span>
              <select value={form.platform} onChange={(event) => updateField("platform", event.target.value as Platform)} className="form-control">
                {PLATFORM_OPTIONS.map((platform) => <option key={platform}>{platform}</option>)}
              </select>
            </label>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="form-label">Post Type</span>
              <select value={form.post_type} onChange={(event) => updateField("post_type", event.target.value as PostType)} className="form-control">
                {POST_TYPES.map((type) => <option key={type}>{type}</option>)}
              </select>
            </label>

            <label className="block">
              <span className="form-label">Campaign Goal</span>
              <select value={form.campaign_goal} onChange={(event) => updateField("campaign_goal", event.target.value as CampaignGoal)} className="form-control">
                {CAMPAIGN_GOALS.map((goal) => <option key={goal}>{goal}</option>)}
              </select>
            </label>
          </div>

          <label className="block">
            <span className="form-label">Audience</span>
            <input value={form.audience} onChange={(event) => updateField("audience", event.target.value)} placeholder="Example: small business owners and marketing managers" className="form-control" />
          </label>

          <label className="block">
            <span className="form-label">Caption</span>
            <textarea
              value={form.caption}
              onChange={(event) => updateField("caption", event.target.value)}
              rows={8}
              placeholder="Paste the social media caption here..."
              className="form-control resize-y leading-6"
            />
            <div className="mt-2 flex flex-wrap gap-2 text-xs font-medium text-slate-400">
              <span className="rounded-full bg-white/8 px-3 py-1">{captionCharacters} characters</span>
              <span className="rounded-full bg-white/8 px-3 py-1">{captionWords} words</span>
              <span className="rounded-full bg-white/8 px-3 py-1">
                {captionCharacters < 30 ? "Too short" : captionCharacters > 600 ? "Long caption" : "Good draft length"}
              </span>
            </div>
          </label>

          <label className="block">
            <span className="form-label">Hashtags</span>
            <input value={form.hashtags} onChange={(event) => updateField("hashtags", event.target.value)} placeholder="#branding #socialmedia #AIcontent" className="form-control" />
          </label>

          <label className="block">
            <span className="form-label">Competitor Caption Optional</span>
            <textarea
              value={form.competitor_caption}
              onChange={(event) => updateField("competitor_caption", event.target.value)}
              rows={4}
              placeholder="Paste a competitor caption for comparison..."
              className="form-control resize-y leading-6"
            />
          </label>

          <label className="flex cursor-pointer items-center justify-between rounded-lg border border-white/10 bg-white/5 p-3">
            <span>
              <span className="block text-sm font-bold text-white">Agency Mode</span>
              <span className="text-xs text-slate-400">Enable client report details and PDF context.</span>
            </span>
            <input type="checkbox" checked={form.agency_mode} onChange={(event) => updateField("agency_mode", event.target.checked)} className="h-5 w-5 accent-cyan-400" />
          </label>

          {form.agency_mode ? (
            <div className="rounded-xl border border-cyan-300/20 bg-cyan-300/10 p-4">
              <h3 className="mb-3 text-sm font-bold text-cyan-100">Agency Report Details</h3>
              <div className="grid gap-3 sm:grid-cols-2">
                <input value={form.client_details.client_name} onChange={(event) => updateClientDetail("client_name", event.target.value)} placeholder="Client name" className="form-control" />
                <input value={form.client_details.campaign_name} onChange={(event) => updateClientDetail("campaign_name", event.target.value)} placeholder="Campaign name" className="form-control" />
                <input value={form.client_details.prepared_by} onChange={(event) => updateClientDetail("prepared_by", event.target.value)} placeholder="Prepared by" className="form-control" />
                <input value={form.client_details.brand_manager_name} onChange={(event) => updateClientDetail("brand_manager_name", event.target.value)} placeholder="Brand manager name" className="form-control" />
                <input type="date" value={form.client_details.date_generated} onChange={(event) => updateClientDetail("date_generated", event.target.value)} className="form-control" />
                <input value={form.client_details.report_notes} onChange={(event) => updateClientDetail("report_notes", event.target.value)} placeholder="Report notes" className="form-control" />
              </div>
            </div>
          ) : null}

          {form.brand === "Custom Brand" ? (
            <div className="rounded-xl border border-violet-300/20 bg-violet-400/10 p-4">
              <h3 className="mb-3 text-sm font-bold text-violet-100">Custom Brand Profile</h3>
              <div className="space-y-3">
                <input value={customBrand.brand_name} onChange={(event) => setCustomBrand((current) => ({ ...current, brand_name: event.target.value }))} placeholder="Brand name" className="form-control" />
                <input value={customBrand.industry} onChange={(event) => setCustomBrand((current) => ({ ...current, industry: event.target.value }))} placeholder="Industry" className="form-control" />
                <input value={customBrand.desired_tone} onChange={(event) => setCustomBrand((current) => ({ ...current, desired_tone: event.target.value }))} placeholder="Desired tone, comma separated" className="form-control" />
                <input value={customBrand.keywords} onChange={(event) => setCustomBrand((current) => ({ ...current, keywords: event.target.value }))} placeholder="Brand keywords, comma separated" className="form-control" />
                <input value={customBrand.avoid_words} onChange={(event) => setCustomBrand((current) => ({ ...current, avoid_words: event.target.value }))} placeholder="Words to avoid, comma separated" className="form-control" />
                <input value={customBrand.cta_examples} onChange={(event) => setCustomBrand((current) => ({ ...current, cta_examples: event.target.value }))} placeholder="Preferred CTA style, comma separated" className="form-control" />
                <input value={customBrand.target_audience} onChange={(event) => setCustomBrand((current) => ({ ...current, target_audience: event.target.value }))} placeholder="Target audience" className="form-control" />
                <input value={customBrand.brand_personality} onChange={(event) => setCustomBrand((current) => ({ ...current, brand_personality: event.target.value }))} placeholder="Brand personality" className="form-control" />
                <input value={customBrand.visual_style} onChange={(event) => setCustomBrand((current) => ({ ...current, visual_style: event.target.value }))} placeholder="Visual style preference" className="form-control" />
              </div>
            </div>
          ) : null}

          <div id="samples" className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Sample Captions</p>
            <div className="grid gap-2 sm:grid-cols-2">
              {sampleCaptions.map((sample) => (
                <button
                  key={`${sample.brand}-${sample.campaign_goal}`}
                  type="button"
                  onClick={() => loadSample(sample)}
                  className="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-left text-xs font-semibold text-slate-200 transition hover:border-cyan-300/30 hover:bg-cyan-300/10"
                >
                  {sample.brand} - {sample.campaign_goal}
                </button>
              ))}
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-[1fr_auto]">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 to-violet-500 px-5 py-3 text-sm font-black text-white shadow-[0_0_24px_rgba(34,211,238,.25)] transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? <WandSparkles className="h-4 w-4 animate-pulse" /> : <Send className="h-4 w-4" />}
              {loading ? "Analyzing..." : "Analyze Content"}
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/15 bg-white/10 px-5 py-3 text-sm font-bold text-white transition hover:bg-white/15"
            >
              <RotateCcw className="h-4 w-4" />
              Reset
            </button>
          </div>
        </div>
      </form>

      <ResultsPanel result={result} request={submittedRequest} loading={loading} error={error} />
    </div>
  );
}
