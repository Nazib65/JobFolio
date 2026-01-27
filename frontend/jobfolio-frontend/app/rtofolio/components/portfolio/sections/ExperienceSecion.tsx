"use client"

import { Theme } from "@/types/portfolio";

const ExperienceSection = ({ section, theme }: { section: any; theme?: Theme }) => {
    const items = section?.items || [];
    
    // Get colors from theme
    const colorPalette = theme?.color_palette ?? theme?.colorPalette ?? [];
    const primaryColor = colorPalette[0] || "#1917fc";
    const secondaryColor = colorPalette[1] || "#134331";
    const accentColor = colorPalette[2] || "#ed2f25";
    
    return (
        <section id="experience" style={{ width: "100%", padding: "2rem 1rem" }}>
             <h2 style={{ marginBottom: "1.5rem", color: primaryColor }}>Experience</h2>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                {items.length > 0 ? items.map((exp: any, idx: number) => (
                    <li key={idx} style={{ 
                        marginBottom: "1.5rem", 
                        borderLeft: `2px solid ${primaryColor}`, 
                        paddingLeft: "1rem" 
                    }}>
                        <h3 style={{ margin: "0 0 0.25rem 0", color: primaryColor }}>{exp.role || "Role Position"}</h3>
                        <div style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>
                            <span style={{ color: accentColor, fontWeight: "600" }}>
                                {exp.company || "Company Name"}
                            </span>
                            <span style={{ color: secondaryColor || "#666", margin: "0 0.5rem" }}>|</span>
                            <span style={{ color: secondaryColor || "#666" }}>
                                {exp.date || "Date Range"}
                            </span>
                        </div>
                        <p style={{ margin: 0 }}>{exp.description || "Description of roles and responsibilities."}</p>
                    </li>
                )) : (
                    <p style={{color: secondaryColor || "#666"}}>No experience listed.</p>
                )}
            </ul>
        </section>
    )
}

export default ExperienceSection;