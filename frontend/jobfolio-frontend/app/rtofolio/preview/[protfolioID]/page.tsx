"use client"

import { use, useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import PortfolioRenderer from "../../components/portfolio/PortfolioRenderer"
import { PortfolioSchema } from "@/types/portfolio"
import ThemeApplier from "../../components/portfolio/ThemeApplier"
import { normalizePortfolioSchema } from "../../components/portfolio/normalizePortfolioSchema"
import PortfolioLayout from "../../components/portfolio/PortfolioLayout"
import FullscreenPreviewModal from "../../components/portfolio/FullscreenPreviewModal"
import { Maximize2 } from "lucide-react"

const Preview = ({ params }: { params: Promise<{ protfolioID: string }> }) => {
    const resolvedParams = use(params)
    const queryClient = useQueryClient()
    const [isFullscreenOpen, setIsFullscreenOpen] = useState(false)

    const fetchSchema = async () => {
        const response = await fetch(`/api/v1/portfolio/${resolvedParams.protfolioID}`)
        if (!response.ok) {
            throw new Error("Failed to load portfolio schema")
        }
        const data = await response.json()
        return normalizePortfolioSchema(data)
    }

    const { data: portfolioSchema, isLoading, error } = useQuery({
        queryKey: ["portfolio", resolvedParams.protfolioID],
        queryFn: fetchSchema,
        enabled: Boolean(resolvedParams?.protfolioID),
    })

    const denormalizeTheme = (theme: any) => {
        if (!theme) return {}
        const t = theme as Record<string, any>
        
        // Handle color_palette - convert string to array if needed
        let colorPalette = t.colorPalette ?? t.color_palette
        if (typeof colorPalette === 'string') {
            // Split comma-separated string into array
            colorPalette = colorPalette.split(',').map((c: string) => c.trim()).filter((c: string) => c.length > 0)
        } else if (!Array.isArray(colorPalette)) {
            colorPalette = null
        }
        
        return {
            style: t.style,
            color_palette: colorPalette,
            font: t.font,
            tone: t.tone,
            max_width: t.maxWidth ?? t.max_width ?? "1280px",
            width: t.width ?? "100%",
            margin: t.margin ?? "0 auto",
            display: t.display ?? "flex",
            flex_direction: t.flexDirection ?? t.flex_direction ?? "column",
            align_items: t.alignItems ?? t.align_items ?? "center",
        }
    }

    const denormalizeSchema = (schema: PortfolioSchema) => {
        const s = schema as any
        // Ensure profile has required role field
        const profile = s.profile || {}
        if (!profile.role) {
            profile.role = profile.role || "Developer" // Default value if missing
        }
        
        return {
            schema_version: s.schemaVersion ?? s.schema_version ?? "1.0",
            profile: {
                role: profile.role,
                industry: profile.industry ?? null,
                seniority: profile.seniority ?? null,
            },
            theme: denormalizeTheme(s.theme),
            sections: s.sections ?? [],
        }
    }

    const updateMutation = useMutation({
        mutationFn: async (schema: PortfolioSchema) => {
            const response = await fetch(`/api/v1/portfolio/${resolvedParams.protfolioID}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(denormalizeSchema(schema)),
            })
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: "Unknown error" }))
                console.error("Validation error details:", errorData)
                throw new Error(`Failed to update portfolio schema: ${JSON.stringify(errorData.detail || errorData)}`)
            }
            return response.json()
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["portfolio", resolvedParams.protfolioID] })
        },
    })

	const font = portfolioSchema?.theme?.font as "sans" | "mono" | undefined
    const colorPalette = portfolioSchema?.theme?.colorPalette as string[] | undefined

    return(
        <>
            <ThemeApplier palette={colorPalette?.join(",")} font={font} />
            <PortfolioLayout
                portfolioSchema={portfolioSchema ?? null}
                isLoading={isLoading}
                error={error as Error | null}
                isSaving={updateMutation.isPending}
                onSave={(nextSchema) => updateMutation.mutate(nextSchema)}
            >
                {/* Fullscreen button */}
                {portfolioSchema && (
                    <button
                        onClick={() => setIsFullscreenOpen(true)}
                        className="fixed bottom-6 right-6 z-10 flex items-center gap-2 rounded-lg bg-ui-primary px-4 py-3 text-sm font-medium text-ui-primary-foreground shadow-lg transition-all hover:bg-ui-primary/90 hover:shadow-xl"
                        title="Open Fullscreen Preview"
                    >
                        <Maximize2 size={18} />
                        <span>Fullscreen Preview</span>
                    </button>
                )}
            </PortfolioLayout>

            {/* Fullscreen Preview Modal */}
            {portfolioSchema && (
                <FullscreenPreviewModal
                    portfolioSchema={portfolioSchema}
                    isOpen={isFullscreenOpen}
                    onClose={() => setIsFullscreenOpen(false)}
                />
            )}
        </>
    )
}

export default Preview