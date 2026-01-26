"use client";

import { useState } from "react";
import { Sidebar } from "@/components/dashboard/Sidebar";
import RtoFolio from "@/app/rtofolio/page";

export default function DashboardPage({
  params,
}: {
  params: { userId: string };
}) {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null);

  return (
    <div className="flex h-screen bg-ui-background">
      <Sidebar onFeatureSelect={setSelectedFeature} />
      <main className="flex-1 p-8 overflow-auto">
        {selectedFeature === "resume-to-portfolio" ? (
          <RtoFolio />
        ) : (
          <div className="max-w-4xl">
            <h1 className="text-3xl font-bold text-ui-foreground mb-4">
              Dashboard
            </h1>
            <p className="text-ui-muted-foreground">
              Welcome to your dashboard. Select a feature from the sidebar to get started.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
