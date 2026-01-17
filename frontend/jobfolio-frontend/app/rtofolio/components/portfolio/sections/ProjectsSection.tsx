"use client";

import type { CSSProperties } from "react";
import { Projects } from "@/types/portfolio";

const ProjectsSection = ({ section }: { section: Projects }) => {
  const { layout, itemLayout, items } = section;

  // Keep section alignment consistent with other sections (Experience/Skills)
  const outerSectionStyle: CSSProperties = {
    width: "100%",
    padding: "2rem 1rem",
  };

  // Layout affects the inner container, not the section wrapper
  const containerStyle: CSSProperties = {
    display: layout?.type || "flex",
    flexDirection: "row",
    gap: layout?.gap || "1rem",
    width: "100%",
    // Default to stretch so cards align with other section content; schema can override.
    alignItems: (layout as any)?.alignItems ?? "stretch",
    justifyContent: (layout as any)?.justifyContent ?? "flex-start",
  };

  const cardStyle = {
    maxWidth: itemLayout?.constraints?.maxWidth,
    width: "32rem",
    border: "1px solid #e5e7eb",
    borderRadius: "12px",
    padding: "16px",
  } as CSSProperties;

  const cardInnerStyle = {
    display: "flex",
    flexDirection: itemLayout?.layout?.direction || "column",
    gap: itemLayout?.layout?.gap || "1rem",
  } as CSSProperties;

  return (
    <section style={outerSectionStyle}>
      <h2 style={{ margin: 0 }} className="text-foreground font-bold text-2xl mt-4 mb-4 text-center py-4 leading-tight">Projects</h2>
      <div style={containerStyle}>
        {(items || []).map((project: any, idx: number) => (
          <div key={project.id || idx} style={cardStyle}>
            <div style={cardInnerStyle}>
              {/* slot: image */}
              {project.image ? (
                <img
                  src={project.image}
                  alt={project.title || "Project image"}
                  style={{ width: "100%", borderRadius: "10px" }}
                />
              ) : null}

              {/* slot: title */}
              {project.title ? (
                <h3
                  style={{ margin: 0 }}
                  className="text-foreground font-bold text-2xl mt-4 mb-2 leading-tight"
                >
                  {project.title}
                </h3>
              ) : null}

              {/* slot: description */}
              {project.description ? (
                <p
                  style={{ margin: 0, opacity: 0.8 }}
                  className="text-muted-foreground text-lg leading-relaxed mb-4"
                >
                  {project.description}
                </p>
              ) : null}

              {/* slot: linkButton */}
              {project.linkButton || project.link ? (
                <a
                  href={project.linkButton || project.link}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "inline-block",
                    marginTop: "4px",
                    textDecoration: "none",
                    border: "1px solid #e5e7eb",
                    borderRadius: "10px",
                    padding: "10px 12px",
                  }}
                >
                  <button className="w-full cursor-pointer bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive">
                    Live Link
                  </button>
                </a>
              ) : null}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProjectsSection;
