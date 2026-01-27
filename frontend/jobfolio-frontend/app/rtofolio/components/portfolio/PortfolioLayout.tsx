"use client"

import { ReactNode } from "react"
import SchemaEditor from "./SchemaEditor"
import PortfolioRenderer from "./PortfolioRenderer"
import { PortfolioSchema } from "@/types/portfolio"

type PortfolioLayoutProps = {
    portfolioSchema: PortfolioSchema | null
    isLoading?: boolean
    error?: Error | null
    isSaving?: boolean
    onSave?: (schema: PortfolioSchema) => void
    children?: ReactNode
}

const PortfolioLayout = ({
    portfolioSchema,
    isLoading = false,
    error = null,
    isSaving = false,
    onSave,
    children,
}: PortfolioLayoutProps) => {
    return (
        <div className="flex min-h-screen flex-col lg:flex-row">
            {/* Fixed Sidebar - SchemaEditor */}
            <aside className="w-full border-b border-ui-border bg-ui-background lg:fixed lg:left-0 lg:top-0 lg:z-40 lg:h-screen lg:w-1/3 lg:max-w-[420px] lg:border-b-0 lg:border-r overflow-y-auto">
                {portfolioSchema && onSave && (
                    <SchemaEditor
                        schema={portfolioSchema}
                        isSaving={isSaving}
                        onSave={onSave}
                    />
                )}
                {!portfolioSchema && isLoading && (
                    <div className="p-4 text-sm text-ui-muted-foreground">Loading editor...</div>
                )}
                {error && (
                    <div className="p-4 text-sm text-ui-destructive">
                        {(error as Error).message}
                    </div>
                )}
            </aside>

            {/* Main Content Area - PortfolioRenderer */}
            <main className="relative flex-1 lg:ml-[420px] min-h-screen overflow-x-hidden px-4">
                {children}
                {portfolioSchema && <PortfolioRenderer portfolioSchema={portfolioSchema} />}
                {!portfolioSchema && isLoading && (
                    <div className="p-6 text-sm text-ui-muted-foreground">Loading preview...</div>
                )}
            </main>
        </div>
    )
}

export default PortfolioLayout
