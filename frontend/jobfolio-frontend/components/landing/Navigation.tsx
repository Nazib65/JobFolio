"use client";

import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";

export function Navigation() {
  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-[#5e6ad2]" />
          <span className="text-2xl font-semibold tracking-tight">JobFolio</span>
        </div>
        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            Features
          </a>
          <a href="#how-it-works" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            How it Works
          </a>
          <a href="#pricing" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            Pricing
          </a>
          <Button variant="outline" size="sm">
            Sign In
          </Button>
        </div>
      </div>
    </nav>
  );
}
