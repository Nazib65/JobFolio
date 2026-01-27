import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Dev convenience: proxy /api/* to the FastAPI backend to avoid browser CORS issues.
  // This lets client-side code call fetch("/api/...") with same-origin requests.
  // Note: /api/v1/generation is handled by a custom API route (app/api/v1/generation/route.ts)
  // to avoid timeout issues with long-running requests. API routes take precedence over rewrites.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*",
      },
    ];
  },
};

export default nextConfig;
