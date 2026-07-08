import type { AnalyzeRequest } from "@/lib/types";

export type SampleCaption = AnalyzeRequest;

const baseClientDetails = {
  client_name: "",
  campaign_name: "",
  prepared_by: "EverVFX",
  report_notes: "",
  brand_manager_name: "",
  date_generated: ""
};

export const sampleCaptions: SampleCaption[] = [
  {
    brand: "The ISMA",
    platform: "Instagram",
    post_type: "Product Post",
    campaign_goal: "Sales",
    audience: "UK skincare buyers",
    hashtags: "#skincare #glow #natural #selfcare",
    competitor_caption: "Glow up fast with the best skincare deal. Buy now before it is gone.",
    agency_mode: false,
    client_details: { ...baseClientDetails, client_name: "The ISMA", campaign_name: "Product Awareness Campaign" },
    custom_brand: null,
    caption:
      "A soft, clean glow starts with gentle skincare made for your daily self-care routine. Discover our natural clay and serum range for fresh, calm-looking skin. Shop now."
  },
  {
    brand: "TMB Bar",
    platform: "Instagram",
    post_type: "Event Post",
    campaign_goal: "Lead Generation",
    audience: "Wedding planners and corporate event teams",
    hashtags: "#mobilebar #events #cocktails #wedding",
    competitor_caption: "We do drinks for events. Message us for prices.",
    agency_mode: false,
    client_details: { ...baseClientDetails, client_name: "TMB Bar", campaign_name: "Event Booking Campaign" },
    custom_brand: null,
    caption:
      "Make your next celebration feel unforgettable. TMB Bar brings a premium mobile bar, elegant cocktails, and a polished guest experience to weddings, parties, and corporate events. Enquire today."
  },
  {
    brand: "AESN",
    platform: "LinkedIn",
    post_type: "Hiring Post",
    campaign_goal: "Hiring",
    audience: "Healthcare job seekers",
    hashtags: "#hiring #jobs #career",
    competitor_caption: "Urgent staff needed now. Easy money. Apply fast.",
    agency_mode: false,
    client_details: { ...baseClientDetails, client_name: "AESN", campaign_name: "Healthcare Hiring Push" },
    custom_brand: null,
    caption:
      "Looking for your next healthcare career opportunity? AESN connects reliable candidates with employers who need trusted staff, clear role details, and workforce support. Send your CV today."
  },
  {
    brand: "EverVFX",
    platform: "LinkedIn",
    post_type: "Service Promotion",
    campaign_goal: "Lead Generation",
    audience: "Small business owners and marketing managers",
    hashtags: "#branding #socialmedia #AIcontent #contentstrategy",
    competitor_caption: "We create posts and designs for your business. Contact us today.",
    agency_mode: true,
    client_details: {
      ...baseClientDetails,
      client_name: "EverVFX Demo Client",
      campaign_name: "Agency Growth Campaign",
      prepared_by: "EverVFX",
      report_notes: "Initial caption and campaign review"
    },
    custom_brand: null,
    caption:
      "Your brand needs more than random posts. Build a sharper content strategy with branding, design, reels, AI workflows, and digital storytelling that supports measurable growth. Book a free strategy call."
  }
];
