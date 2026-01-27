"use client"

import { useState, useEffect } from "react";
import { useDeviceSize } from "../DeviceSizeContext";
import { Theme } from "@/types/portfolio";

const SkillsSection = ({ section, theme }: { section: any; theme?: Theme }) => {
    const contextDeviceSize = useDeviceSize();
    const layout = section?.layout || {};
    const items = section?.items || [];
    
    // 1. Add Mobile State Detection
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

    const containerStyle: React.CSSProperties = {
        display: "flex",
        flexWrap: "wrap",
        gap: layout?.gap || "1.5rem",
        justifyContent: "center",
        padding: "2rem 0",
        width: "100%"
    };

    // 2. Select columns based on screen size
    const desktopCols = layout?.columns?.desktop || 5;
    const mobileCols = layout?.columns?.mobile || 2;
    const activeCols = isMobile ? mobileCols : desktopCols;

    // 3. Dynamic width calculation
    // Formula: (100% - (total gap space)) / number of columns
    const gap = layout?.gap || "1.5rem";
    const cardWidth = `calc((100% - (${gap} * ${activeCols - 1})) / ${activeCols})`;

    const cardStyle: React.CSSProperties = {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "0.5rem",
        padding: "1rem",
        border: `2px solid ${secondaryColor || "#e5e7eb"}`,
        borderRadius: "8px",
        minWidth: "120px",
        transition: "all 0.3s ease",
        cursor: "pointer",
        
        // 4. Apply the calculated width
        flexBasis: cardWidth,
        // Ensure it doesn't grow beyond the calculated width to keep the grid strict
        flexGrow: 0, 
        flexShrink: 0 
    };

    return (
        <section style={{ width: "100%", padding: "0 1rem" }} id="skills">
            <h2 style={{ textAlign: "center", marginBottom: "1rem", color: primaryColor }} className="text-4xl font-bold mb-4 leading-tight mt-4">Skills</h2>
            <div style={containerStyle}>
                {items.length > 0 ? items.map((skill: any, idx: number) => {
                    // Cycle through colors for visual variety
                    const cardColor = idx % 3 === 0 ? primaryColor : idx % 3 === 1 ? secondaryColor : accentColor;
                    return (
                        <div 
                            key={idx} 
                            style={{
                                ...cardStyle,
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = accentColor;
                                e.currentTarget.style.transform = "translateY(-4px)";
                                e.currentTarget.style.boxShadow = `0 4px 12px ${accentColor}40`;
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = secondaryColor;
                                e.currentTarget.style.transform = "translateY(0)";
                                e.currentTarget.style.boxShadow = "none";
                            }}
                        >
                            {skill.icon && (
                                <img src={skill.icon} alt={skill.name} style={{ width: "40px", height: "40px" }} />
                            )}
                            <span 
                                className="text-lg leading-relaxed mb-4 font-medium"
                                style={{ color: cardColor }}
                            >
                                {skill.name || "Skill Name"}
                            </span>
                        </div>
                    );
                }) : (
                    <p style={{color: secondaryColor || "#666"}} className="text-muted-foreground text-lg leading-relaxed mb-4">No skills listed yet.</p>
                )}
            </div>
        </section>
    )
}

export default SkillsSection;