"use client";

import React, { useState, useEffect } from "react";
// Assuming types are updated, otherwise use 'any' for now to prevent errors
import { Hero } from "@/types/portfolio";
import { useDeviceSize } from "../DeviceSizeContext";

const HeroSection = ({ section }: { section: Hero | any }) => {
  const contextDeviceSize = useDeviceSize();
  const { layout, props } = section;
  const [isMobile, setIsMobile] = useState(false);

  // 1. Handle Screen Resize
  useEffect(() => {
    // If we have a context device size (from modal), use that
    if (contextDeviceSize !== null) {
      const shouldBeMobile = contextDeviceSize === "phone" || contextDeviceSize === "tablet";
      setIsMobile(shouldBeMobile);
      return; // Skip window listener when context is provided
    }

    // Otherwise, use window width detection
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    handleResize(); // Initial check
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [contextDeviceSize]);

  // 2. Determine Active Configuration
  // We use desktop slots as the source of truth for CONTENT,
  // but switch the container STYLE based on the device.
  const activeLayout = isMobile ? layout?.mobile : layout?.desktop;
  const contentSlots = layout?.desktop?.slots || {};

  // 3. Define Container Styles based on active layout type
  const isGrid = activeLayout?.type === "grid";

  const containerStyle: React.CSSProperties = {
    display: isGrid ? "grid" : "flex",
    // Grid specific props
    gridTemplateColumns: isGrid ? "1fr 1fr" : undefined,
    // Flex specific props
    flexDirection: isGrid ? undefined : "column",
    // Shared props
    gap: activeLayout?.gap || "2rem",
    alignItems: activeLayout?.align || "center",
    justifyContent: activeLayout?.justify || "center",
    // Add padding for mobile to prevent edge touching
    padding: isMobile ? "2rem 1rem" : "0",
    // Add these theme-based variables
  };

  // Helper to get slot data safely
  const leftSlot = contentSlots["left"];
  const rightSlot = contentSlots["right"];

  // 4. Render Items (Updated for new JSON keys)
  const renderSlotItem = (slotName: string) => {
    // Fallback to empty object to prevent crashes
    const p = props || {};

    // Normalize slot name to lowercase to match JSON "cta" vs "CTA"
    switch (slotName.toLowerCase()) {
      case "text":
        return (
          <div>
            {p.name && (
              <h1 className={isMobile ? "text-4xl" : "text-5xl"}>{p.name}</h1>
            )}
            {p.hero_text && (
              <p className="mt-2 text-muted-foreground leading-relaxed">
                {p.hero_text}
              </p>
            )}
          </div>
        );
      case "cta":
        return p.cta_label ? (
          <a
            href={p.cta_url}
            target="_blank"
            rel="noreferrer"
            className="inline-block mt-5"
          >
            <button className="px-6 py-3 rounded-lg bg-primary text-primary-foreground">
              {p.cta_label}
            </button>
          </a>
        ) : null;
      case "image":
        if (!p.image) return null;

        // Sane defaults for portfolio hero images (with optional schema overrides)
        const imageMaxWidth =
          p.image_max_width ?? p.imageMaxWidth ?? (isMobile ? "320px" : "520px");
        const imageAspectRatio =
          p.image_aspect_ratio ??
          p.imageAspectRatio ??
          (isMobile ? "4 / 3" : "1 / 1");
        const imageMaxHeight = p.image_max_height ?? p.imageMaxHeight ?? undefined;

        return (
          <div
            style={{
              width: "100%",
              maxWidth: imageMaxWidth,
              aspectRatio: imageAspectRatio,
              maxHeight: imageMaxHeight,
              overflow: "hidden",
              borderRadius: 12,
              boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
            }}
          >
            <img
              src={p.image}
              alt={p.name || "hero image"}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                display: "block",
              }}
            />
          </div>
        );
      default:
        return null;
    }
  };

  // Helper to map through slot arrays (handles "left": ["text", "cta"])
  const renderSlotContent = (slotData: any) => {
    if (!slotData) return null;
    const items = Array.isArray(slotData) ? slotData : [slotData];

    return items.map((item: any, idx: number) => {
      const key = typeof item === "string" ? item : item.name;
      return <div key={idx}>{renderSlotItem(key)}</div>;
    });
  };

  return (
    <section
      style={{
        width: "100%",
        maxWidth: "1280px",
        margin: "2rem auto",
      }}
      className="bg-background text-foreground"
    >
      <div style={containerStyle}>
        {/* In Mobile (Flex Column), the Left div appears first, then Right div.
                   If you wanted Image first on mobile, you could use CSS 'order' property.
                */}

        {/* Left Column/Row */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: isMobile ? "center" : "flex-start",
            textAlign: isMobile ? "center" : "left",
          }}
        >
          {renderSlotContent(leftSlot)}
        </div>

        {/* Right Column/Row */}
        <div
          style={{ width: "100%", display: "flex", justifyContent: "center" }}
        >
          {renderSlotContent(rightSlot)}
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
