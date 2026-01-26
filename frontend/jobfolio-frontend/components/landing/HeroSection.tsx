"use client";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowRight } from "lucide-react";

export function HeroSection() {
  return (
    <section className="pt-32 pb-20 px-6">
      <div className="max-w-6xl mx-auto text-center">
        <Badge 
          variant="secondary" 
          className="mb-6 px-4 py-1.5 text-sm font-medium bg-[#5e6ad2]/10 text-[#5e6ad2] border-[#5e6ad2]/20"
        >
          AI-Powered Career Intelligence
        </Badge>
        
        <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6 bg-linear-to-br from-gray-900 via-gray-800 to-gray-600 bg-clip-text text-transparent">
          Land Your Dream Job
        </h1>
        
        <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
          Transform your resume into an AI-powered portfolio and discover your perfect job match with intelligent skill analysis
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button 
            size="lg" 
            className="px-8 py-6 text-base font-medium shadow-lg hover:shadow-xl transition-all bg-[#5e6ad2] hover:bg-brand-primary-dark text-white"
            style={{
              boxShadow: "inset 0 2px 4px 0 rgba(255, 255, 255, 0.1), inset 0 -2px 4px 0 rgba(0, 0, 0, 0.1)"
            }}
          >
            Get Started Free
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
          <Button 
            size="lg" 
            variant="outline"
            className="px-8 py-6 text-base font-medium border-2"
          >
            Watch Demo
          </Button>
        </div>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">98%</div>
            <div className="text-sm text-gray-600">Match Accuracy</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">10k+</div>
            <div className="text-sm text-gray-600">Portfolios Created</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-gray-900 mb-2">2.5x</div>
            <div className="text-sm text-gray-600">Interview Rate</div>
          </div>
        </div>
      </div>
    </section>
  );
}
