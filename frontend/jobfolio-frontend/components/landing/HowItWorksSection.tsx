"use client";

import {
  Upload,
  Target,
  Sparkles,
  ChevronDown
} from "lucide-react";

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="relative h-screen overflow-y-auto snap-y snap-mandatory scrollbar-hide">

      {/* Step 1 */}
      <div className="h-screen snap-start flex items-center justify-center px-6 bg-linear-to-b from-gray-50 to-white">
        <div className="max-w-4xl w-full text-center">
          <div className="mb-8">
            <h2 className="text-5xl md:text-6xl font-bold mb-4 tracking-tight">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto font-light">
              Three simple steps to accelerate your job search
            </p>
          </div>
          
          <div className="max-w-2xl w-full mx-auto bg-white rounded-3xl shadow-xl p-12 border-2 border-[#5e6ad2]/20">
            <Upload className="w-16 h-16 text-[#5e6ad2] mx-auto mb-6" />
            <h3 className="text-4xl font-bold mb-4">Upload Resume</h3>
            <p className="text-xl text-gray-600 leading-relaxed max-w-lg mx-auto">
              Upload your resume in PDF format. Our AI extracts your experience, skills, and projects automatically.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <span className="px-4 py-2 bg-[#5e6ad2]/10 text-[#5e6ad2] rounded-full text-sm font-medium">
                PDF Support
              </span>
              <span className="px-4 py-2 bg-[#5e6ad2]/10 text-[#5e6ad2] rounded-full text-sm font-medium">
                AI Extraction
              </span>
              <span className="px-4 py-2 bg-[#5e6ad2]/10 text-[#5e6ad2] rounded-full text-sm font-medium">
                Instant Parse
              </span>
            </div>
          </div>

          <div className="mt-8 flex items-center justify-center gap-2 text-sm text-gray-500 animate-bounce">
            <ChevronDown className="w-5 h-5" />
            <span>Scroll down to continue</span>
            <ChevronDown className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Step 2 */}
      <div className="h-screen snap-start flex items-center justify-center px-6 bg-linear-to-b from-white to-purple-50">
        <div className="max-w-4xl w-full text-center">
          <div className="max-w-2xl w-full mx-auto bg-white rounded-3xl shadow-xl p-12 border-2 border-purple-600/20">
            
            <Target className="w-16 h-16 text-purple-600 mx-auto mb-6" />
            <h3 className="text-4xl font-bold mb-4">Analyze Jobs</h3>
            <p className="text-xl text-gray-600 leading-relaxed max-w-lg mx-auto">
              Paste job descriptions to get instant fit scores, skill gap analysis, and tailored recommendations.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <span className="px-4 py-2 bg-purple-100 text-purple-600 rounded-full text-sm font-medium">
                Match Score
              </span>
              <span className="px-4 py-2 bg-purple-100 text-purple-600 rounded-full text-sm font-medium">
                Skill Gaps
              </span>
              <span className="px-4 py-2 bg-purple-100 text-purple-600 rounded-full text-sm font-medium">
                AI Insights
              </span>
            </div>
          </div>

          <div className="mt-8 flex items-center justify-center gap-2 text-sm text-gray-500 animate-bounce">
            <ChevronDown className="w-5 h-5" />
            <span>Keep scrolling</span>
            <ChevronDown className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Step 3 */}
      <div className="h-screen snap-start flex items-center justify-center px-6 bg-linear-to-b from-purple-50 to-emerald-50">
        <div className="max-w-4xl w-full text-center">
          <div className="max-w-2xl w-full mx-auto bg-white rounded-3xl shadow-xl p-12 border-2 border-emerald-600/20">
            <Sparkles className="w-16 h-16 text-emerald-600 mx-auto mb-6" />
            <h3 className="text-4xl font-bold mb-4">Generate Portfolio</h3>
            <p className="text-xl text-gray-600 leading-relaxed max-w-lg mx-auto">
              Create a stunning portfolio website in seconds. Share your unique link with recruiters.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <span className="px-4 py-2 bg-emerald-100 text-emerald-600 rounded-full text-sm font-medium">
                Auto Design
              </span>
              <span className="px-4 py-2 bg-emerald-100 text-emerald-600 rounded-full text-sm font-medium">
                One-Click Deploy
              </span>
              <span className="px-4 py-2 bg-emerald-100 text-emerald-600 rounded-full text-sm font-medium">
                Share Link
              </span>
            </div>
          </div>

          <div className="mt-8 text-sm text-gray-500">
            That's it! You're ready to get started 🚀
          </div>
        </div>
      </div>

      <style jsx>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </section>
  );
}
