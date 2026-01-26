"use client";

import { FileText, Search } from "lucide-react";
import { Button } from "@/components/ui/button";

interface SidebarProps {
  onFeatureSelect: (feature: string) => void;
}

export function Sidebar({ onFeatureSelect }: SidebarProps) {
  return (
    <aside className="w-64 h-screen bg-ui-secondary border-r border-ui-border p-6 flex flex-col gap-4">
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-ui-foreground">Features</h2>
      </div>
      
      <Button
        onClick={() => onFeatureSelect("resume-to-portfolio")}
        className="w-full justify-start gap-3 bg-brand-primary hover:bg-brand-primary-dark text-white"
        variant="default"
      >
        <FileText className="w-5 h-5" />
        Resume to Portfolio
      </Button>

      <Button
        onClick={() => {
          // TODO: Add route for Check Jobfit
          onFeatureSelect("check-jobfit");
        }}
        className="w-full justify-start gap-3 bg-brand-primary hover:bg-brand-primary-dark text-white"
        variant="default"
      >
        <Search className="w-5 h-5" />
        Check Jobfit
      </Button>
    </aside>
  );
}
