"use client"

import { useState, useEffect } from "react";
import { useDeviceSize } from "../DeviceSizeContext";
import { Theme } from "@/types/portfolio";

const FooterSection = ({ section, theme }: { section: any; theme?: Theme }) => {
    const contextDeviceSize = useDeviceSize();
    const layout = section?.layout || {};
    const props = section?.props || {};
    
    // 1. Mobile State Detection
    const [isMobile, setIsMobile] = useState(false);

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

    // Get colors from theme
    const colorPalette = theme?.color_palette ?? theme?.colorPalette ?? [];
    const primaryColor = colorPalette[0] || "#1917fc";
    const secondaryColor = colorPalette[1] || "#134331";
    const accentColor = colorPalette[2] || "#ed2f25";

    // 2. Determine Active Column Count
    const desktopCols = layout?.columns?.desktop || 2;
    const mobileCols = layout?.columns?.mobile || 1;
    const activeCols = isMobile ? mobileCols : desktopCols;

    const footerStyle: React.CSSProperties = {
        display: "grid",
        // Dynamically create the grid columns (e.g., "1fr 1fr" or "1fr")
        gridTemplateColumns: `repeat(${activeCols}, 1fr)`,
        gap: layout?.gap ?? "2rem",
        padding: layout?.padding ?? "2rem",
        marginTop: "auto",
        width: "100%",
        // Optional: Center text on mobile for better aesthetics
        textAlign: isMobile ? "center" : "left",
        borderTop: `1px solid ${secondaryColor || "#e5e7eb"}`,
    };

    const slots = layout?.slots || {};

    const renderSlot = (slotName: string) => {
        switch (slotName.toLowerCase()) {
            case "logo":
                return props.logo ? (
                    <img src={props.logo} alt="Logo" className="h-10 w-10 object-contain" />
                ) : null;
            case "name":
                return props.name ? (
                    <span 
                        className="font-semibold"
                        style={{ color: primaryColor }}
                    >
                        {props.name}
                    </span>
                ) : null;
            case "links":
                return (props.links || []).length ? (
                    <div className="flex flex-col gap-2">
                        {(props.links || []).map((link: any, idx: number) => (
                            <a
                                key={idx}
                                href={link.url || "#"}
                                className="text-sm text-muted-foreground hover:text-foreground"
                            >
                                {link.label || "Footer Link"}
                            </a>
                        ))}
                    </div>
                ) : null;
            default:
                return null;
        }
    };

    const renderSlotGroup = (slotData: any) => {
        if (!slotData) return null;
        const items = Array.isArray(slotData) ? slotData : [slotData];
        return items.map((item: any, idx: number) => {
            const name = typeof item === "string" ? item : item?.name;
            if (!name) return null;
            return <div key={`${name}-${idx}`}>{renderSlot(name)}</div>;
        });
    };

    return (
        <footer id="footer" className="w-full border-t border-border bg-background text-foreground" style={footerStyle}>
            {/* Left Slot */}
            <div
                className="flex flex-col gap-2"
                style={{ alignItems: isMobile ? "center" : "flex-start" }}
            >
                {renderSlotGroup(slots?.left) ?? (
                    <>
                        {renderSlot("logo")}
                        {renderSlot("name")}
                    </>
                )}
                <p className="m-0 text-sm text-muted-foreground">
                    © {new Date().getFullYear()} All rights reserved.
                </p>
            </div>

            {/* Right Slot */}
            <div
                className="flex flex-col gap-2"
                style={{ alignItems: isMobile ? "center" : "flex-start" }}
            >
                {slots?.right ? (
                    renderSlotGroup(slots?.right)
                ) : (
                    <>
                        <span className="font-semibold">Links</span>
                        {renderSlot("links")}
                    </>
                )}
            </div>
        </footer>
    )
}

export default FooterSection;