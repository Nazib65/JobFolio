import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "./providers";

// Clean sans-serif font (similar to Helvetica)
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "JobFolio - AI-Powered Job Fit Analysis & Portfolio Generation",
  description: "Transform your resume into an AI-powered portfolio and discover your perfect job match with intelligent skill analysis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) { 
  return (
    <html
      lang="en"
      className={`${inter.variable}`}
      style={{ scrollBehavior: "smooth" }}
    >
      <body className="antialiased font-sans">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
