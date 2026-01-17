"use client"

import { use } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import PortfolioRenderer from "../../components/portfolio/PortfolioRenderer"
import { PortfolioSchema } from "@/types/portfolio"
import ThemeApplier from "../../components/portfolio/ThemeApplier"
import { normalizePortfolioSchema } from "../../components/portfolio/normalizePortfolioSchema"
import SchemaEditor from "../../components/portfolio/SchemaEditor"

const Preview = ({ params }: { params: Promise<{ protfolioID: string }> }) => {
    const resolvedParams = use(params)
    const queryClient = useQueryClient()

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
        const t = theme ?? {}
        return {
            ...t,
            color_palette: t.colorPalette ?? t.color_palette,
            max_width: t.maxWidth ?? t.max_width,
            flex_direction: t.flexDirection ?? t.flex_direction,
            align_items: t.alignItems ?? t.align_items,
        }
    }

    const denormalizeSchema = (schema: PortfolioSchema) => ({
        ...schema,
        schema_version: (schema as any).schemaVersion ?? (schema as any).schema_version,
        theme: denormalizeTheme((schema as any).theme),
    })

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
                throw new Error("Failed to update portfolio schema")
            }
            return response.json()
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["portfolio", resolvedParams.protfolioID] })
        },
    })

	const font = portfolioSchema?.theme?.font as "sans" | "mono" | undefined

    return(
        <div className="flex min-h-screen flex-col lg:flex-row">
            <ThemeApplier palette={portfolioSchema?.theme?.colorPalette} font={font} />
            <aside className="w-full border-b border-border lg:h-screen lg:w-1/3 lg:max-w-[420px] lg:border-b-0 lg:border-r lg:overflow-y-auto">
                {portfolioSchema && (
                    <SchemaEditor
                        schema={portfolioSchema}
                        isSaving={updateMutation.isPending}
                        onSave={(nextSchema) => updateMutation.mutate(nextSchema)}
                    />
                )}
                {!portfolioSchema && isLoading && (
                    <div className="p-4 text-sm text-muted-foreground">Loading editor...</div>
                )}
                {error && (
                    <div className="p-4 text-sm text-destructive">
                        {(error as Error).message}
                    </div>
                )}
            </aside>
            <main className="flex-1 overflow-x-hidden">
                {portfolioSchema && <PortfolioRenderer portfolioSchema={portfolioSchema} />}
                {!portfolioSchema && isLoading && (
                    <div className="p-6 text-sm text-muted-foreground">Loading preview...</div>
                )}
            </main>
        </div>
    )
}

export default Preview