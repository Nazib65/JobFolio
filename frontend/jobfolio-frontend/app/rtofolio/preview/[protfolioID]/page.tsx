"use client"

import { useEffect, useState } from "react"
import { use } from "react"
import { useSearchParams } from "next/navigation"
import PortfolioRenderer from "../../components/portfolio/PortfolioRenderer"
import { PortfolioSchema } from "@/types/portfolio"
import ThemeApplier from "../../components/portfolio/ThemeApplier"
import { normalizePortfolioSchema } from "../../components/portfolio/normalizePortfolioSchema"

const Preview = ({ params }: { params: Promise<{ protfolioID: string }> }) => {
    const [portfolioSchema, setPortfolioSchema] = useState<PortfolioSchema | null>(null)
    const resolvedParams = use(params)
    const searchParams = useSearchParams()

    useEffect(() => {
        // Fetch the schema using the portfolioID from the URL
        const fetchSchema = async () => {
            try {
                const response = await fetch(`/api/v1/portfolio/${resolvedParams.protfolioID}`)
                const data = await response.json()
                setPortfolioSchema(normalizePortfolioSchema(data))
            } catch (error) {
                console.error("Error fetching portfolio:", error)
            }
        }
        fetchSchema()
    }, [resolvedParams.protfolioID])

	const font = portfolioSchema?.theme?.font as "sans" | "mono" | undefined

    return(
        <>
        <ThemeApplier palette={portfolioSchema?.theme?.colorPalette} font={font} />
            {portfolioSchema && <PortfolioRenderer portfolioSchema={portfolioSchema} />}
        </>
    )
}

export default Preview