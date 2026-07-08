import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#14213d",
        mist: "#f6f8fb",
        line: "#e3e8ef",
        accent: "#2563eb",
        success: "#15803d",
        warning: "#b45309",
        danger: "#b91c1c"
      },
      boxShadow: {
        soft: "0 18px 45px rgba(20, 33, 61, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;

