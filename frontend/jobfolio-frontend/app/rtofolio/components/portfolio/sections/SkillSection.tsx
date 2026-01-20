"use client"

import { useState, useEffect } from "react";
import { useDeviceSize } from "../DeviceSizeContext";

const SkillsSection = ({ section }: { section: any }) => {
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
        border: "1px solid #e5e7eb",
        borderRadius: "8px",
        minWidth: "120px", 
        
        // 4. Apply the calculated width
        flexBasis: cardWidth,
        // Ensure it doesn't grow beyond the calculated width to keep the grid strict
        flexGrow: 0, 
        flexShrink: 0 
    };

    return (
        <section style={{ width: "100%", padding: "0 1rem" }}>
            <h2 style={{ textAlign: "center", marginBottom: "1rem" }} className="text-4xl font-bold text-foreground mb-4 leading-tight mt-4">Skills</h2>
            <div style={containerStyle}>
                {items.length > 0 ? items.map((skill: any, idx: number) => (
                    <div key={idx} style={cardStyle}>
                        {skill.icon && (
                            <img src={skill.icon} alt={skill.name} style={{ width: "40px", height: "40px" }} />
                        )}
                        <span className="text-foreground text-lg leading-relaxed mb-4">{skill.name || "Skill Name"}</span>
                    </div>
                )) : (
                    <p style={{color: "#666"}} className="text-muted-foreground text-lg leading-relaxed mb-4">No skills listed yet.</p>
                )}
            </div>
        </section>
    )
}

export default SkillsSection;