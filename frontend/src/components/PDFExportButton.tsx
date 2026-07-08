"use client";

import { pdf } from "@react-pdf/renderer";
import { Download } from "lucide-react";

import { BrandReportDocument } from "@/lib/pdf";
import type { AnalysisResult, AnalyzeRequest } from "@/lib/types";

export default function PDFExportButton({ result, request }: { result: AnalysisResult; request: AnalyzeRequest }) {
  async function exportPdf() {
    const blob = await pdf(<BrandReportDocument result={result} request={request} />).toBlob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `evervfx-brand-content-report-${Date.now()}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  return (
    <button
      type="button"
      onClick={exportPdf}
      className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-cyan-400 to-violet-500 px-4 py-2 text-sm font-bold text-white shadow-[0_0_24px_rgba(34,211,238,.25)] transition hover:scale-[1.02]"
    >
      <Download className="h-4 w-4" />
      Export PDF Report
    </button>
  );
}

