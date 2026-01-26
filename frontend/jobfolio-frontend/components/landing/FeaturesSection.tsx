import { Card } from "@/components/ui/card";
import { 
  Target, 
  Zap, 
  CheckCircle2,
  BarChart3,
  FileText
} from "lucide-react";

export function FeaturesSection() {
  return (
    <section id="features" className="py-20 px-6 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-bold mb-4 tracking-tight">
            Everything You Need
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto font-light">
            Powerful tools to help you stand out in the competitive job market
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-12 md:auto-rows-[1fr]">
          {/* Feature 1 */}
          <Card className="p-8 border-gray-100 hover:shadow-lg transition-shadow bg-linear-to-br from-white to-gray-50 md:col-span-7 md:row-span-1">
            <div className="w-12 h-12 bg-[#5e6ad2]/10 rounded-2xl flex items-center justify-center mb-6">
              <Target className="w-6 h-6 text-[#5e6ad2]" />
            </div>
            <h3 className="text-2xl font-semibold mb-3">Job Fit Analysis</h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              Advanced AI analyzes your resume against job descriptions to calculate precise match scores and identify skill gaps
            </p>
            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Coverage, depth & bonus scoring</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Skill gap identification</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Personalized recommendations</span>
              </li>
            </ul>
          </Card>

          <Card className="p-8 border-gray-100 hover:shadow-lg transition-shadow bg-linear-to-br from-white to-gray-50 md:col-span-5">
            <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center mb-6">
              <Zap className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-3">AI Portfolio Generator</h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              Transform your resume into a stunning, professional portfolio website in seconds
            </p>
            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Automated design generation</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Multiple layout options</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>One-click deployment</span>
              </li>
            </ul>
          </Card>

          {/* Feature 3 */}
          <Card className="p-8 border-gray-100 hover:shadow-lg transition-shadow bg-linear-to-br from-white to-gray-50 md:col-span-5">
            <div className="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center mb-6">
              <BarChart3 className="w-6 h-6 text-emerald-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-3">Smart Analytics</h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              Get detailed insights into your strengths, weaknesses, and career trajectory
            </p>
            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Skill strength visualization</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Career path suggestions</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Market trend analysis</span>
              </li>
            </ul>
          </Card>

          {/* Feature 4 */}
          <Card className="p-8 border-gray-100 hover:shadow-lg transition-shadow bg-linear-to-br from-white to-gray-50 md:col-span-7">
            <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mb-6">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-3">ATS-Ready Resume</h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              Optimize your resume for applicant tracking systems and highlight the most relevant experience for each role
            </p>
            <ul className="space-y-2">
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Keyword alignment</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>Role-specific tailoring</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
                <span>ATS compatibility checks</span>
              </li>
            </ul>
          </Card>
        </div>
      </div>
    </section>
  );
}
