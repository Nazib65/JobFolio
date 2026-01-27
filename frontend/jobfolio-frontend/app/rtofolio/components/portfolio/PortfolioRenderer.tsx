"use client"

import { PortfolioSchema } from "@/types/portfolio"
import ExperienceSection from "./sections/ExperienceSecion"
import FooterSection from "./sections/FooterSection"
import HeroSection from "./sections/HeroSection"
import NavbarSection from "./sections/NavbarSection"
import ProjectsSection from "./sections/ProjectsSection"
import SkillsSection from "./sections/SkillSection"
import { normalizeTheme } from "./normalizePortfolioSchema"

const PortfolioRenderer = ({ portfolioSchema }: { portfolioSchema: PortfolioSchema }) => {
    const sections = portfolioSchema?.sections ?? []
    // FIX 1: Use {} as fallback, not []
    const theme = normalizeTheme(portfolioSchema?.theme ?? {})

    return (
        <>
            <div style={{
                // FIX 2: Ensure keys match your JSON. 
                // If your JSON has "width", use that. If not, default to "100%".
                width: theme?.width ?? "100%", 
                
                // FIX 3: Default to 1280px if missing to prevent unlimited stretching
                maxWidth: theme?.maxWidth ?? "1280px", 
                
                // FIX 4: This is the specific property that centers the container
                margin: theme?.margin ?? "0 auto", 
                
                // Flex properties to center children
                display: theme?.display ?? "flex",
                flexDirection: (theme?.flexDirection ?? "column") as React.CSSProperties['flexDirection'],
                
                // FIX 5: Ensure this matches your JSON key (align vs alignItems)
                alignItems: theme?.alignItems ?? "center", 
                
                // Optional: Ensure it fills height
                minHeight: "100vh",
                
            }}>
                
                {sections.map((section: any, idx: number) => {
                    const key = section?.id ?? `${section?.type ?? "section"}-${idx}`

                    switch (section?.type) {
                        case "navbar":
                            return <NavbarSection key={key} section={section} theme={theme}/>
                        case "hero":
                            return <HeroSection key={key} section={section} theme={theme} />
                        case "skills":
                            return <SkillsSection key={key} section={section} theme={theme} />
                        case "experience":
                            return <ExperienceSection key={key} section={section} theme={theme}/>
                        case "projects":
                            return <ProjectsSection key={key} section={section} theme={theme} />
                        case "footer":
                            return <FooterSection key={key} section={section} theme={theme}/>
                        default:
                            return null
                    }
                })}
            </div>
        </>
    )
}

export default PortfolioRenderer;