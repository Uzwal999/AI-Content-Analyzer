import type { AnalysisResult, AnalyzeRequest, BrandProfile } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {})
    }
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchBrands(): Promise<Record<string, BrandProfile>> {
  return request<Record<string, BrandProfile>>("/brands");
}

export function analyzeCaption(payload: AnalyzeRequest): Promise<AnalysisResult> {
  return request<AnalysisResult>("/analyze", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

