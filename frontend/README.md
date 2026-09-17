# EverVFX Frontend Dashboard

Next.js, TypeScript, Tailwind CSS, lucide-react, and @react-pdf/renderer dashboard for the EverVFX AI Brand Content Analyzer.

## Run With Full App

From the project root:

```powershell
.\run_app.bat
```

## Run Frontend Only

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Then run:

```powershell
npm install
npm run dev
```

Open `http://localhost:3000`.

If the analysis API cannot connect, confirm the backend URL opens in the browser:

```text
http://127.0.0.1:8000
```

## Vercel

The repository root includes `vercel.json`, so Vercel can build the frontend from the monorepo root.

Set this environment variable in Vercel:

```env
NEXT_PUBLIC_API_URL=https://your-hosted-fastapi-backend-url
```

## Features

- Premium EverVFX dark glassmorphism UI
- Logo-based navbar and branded hero
- Analyzer dashboard with Agency Mode
- Competitor caption comparison
- Campaign brief, design direction, and calendar suggestions
- PDF client report export
- JSON export
- Responsive layout
