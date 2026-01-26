"use client";

import {
  Navigation,
  HeroSection,
  FeaturesSection,
  HowItWorksSection,
  CTASection,
  Footer
} from "@/components/landing";

export default function Home() {
  return (
    <div className="min-h-screen bg-linear-to-b from-white to-gray-50">
      <Navigation />
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <CTASection />
      <Footer />
    </div>
  );
}
