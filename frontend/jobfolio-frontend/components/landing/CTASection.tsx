"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export function CTASection() {
  return (
    <section className="py-20 px-6 bg-[#5e6ad2] text-white">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-5xl md:text-6xl font-bold mb-6 tracking-tight">
          Ready to Transform Your Job Search?
        </h2>
        <p className="text-xl mb-10 text-white/90 font-light leading-relaxed">
          Join thousands of professionals who have accelerated their careers with JobFolio
        </p>
        <Button 
          size="lg" 
          className="px-10 py-6 text-base font-medium bg-white text-[#5e6ad2] hover:bg-gray-50 shadow-xl hover:shadow-2xl transition-all"
          style={{
            boxShadow: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05), inset 0 -2px 4px 0 rgba(0, 0, 0, 0.05)"
          }}
        >
          Start Free Trial
          <ArrowRight className="ml-2 w-5 h-5" />
        </Button>
        <p className="mt-6 text-sm text-white/80">
          No credit card required • 14-day free trial • Cancel anytime
        </p>
      </div>
    </section>
  );
}
