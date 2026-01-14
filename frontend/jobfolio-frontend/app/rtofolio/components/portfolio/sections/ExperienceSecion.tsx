"use client"

const ExperienceSection = ({ section }: { section: any }) => {
    const items = section?.items || [];
    
    return (
        <section style={{ width: "100%", padding: "2rem 1rem" }}>
             <h2 style={{ marginBottom: "1.5rem" }}>Experience</h2>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                {items.length > 0 ? items.map((exp: any, idx: number) => (
                    <li key={idx} style={{ 
                        marginBottom: "1.5rem", 
                        borderLeft: "2px solid #e5e7eb", 
                        paddingLeft: "1rem" 
                    }}>
                        <h3 style={{ margin: "0 0 0.25rem 0" }}>{exp.role || "Role Position"}</h3>
                        <div style={{ color: "#666", fontSize: "0.9rem", marginBottom: "0.5rem" }}>
                            {exp.company || "Company Name"} | {exp.date || "Date Range"}
                        </div>
                        <p style={{ margin: 0 }}>{exp.description || "Description of roles and responsibilities."}</p>
                    </li>
                )) : (
                    <p style={{color: "#666"}}>No experience listed.</p>
                )}
            </ul>
        </section>
    )
}

export default ExperienceSection;