"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

const RtoFolio = () => {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const router = useRouter()

    const handleClick = async (portfolioID: string) => {
        setLoading(true)
        try {
            router.push(`/rtofolio/preview/${portfolioID}`)
        } catch (error) {
            console.error("Error navigating to preview:", error)
            setError("Failed to navigate to preview page")
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <>
                <h1>R TO Folio</h1>
                <p>Loading...</p>
            </>
        )
    }

    if (error){
        return(
            <>
            <p>{error}</p>
            </>
        )
    }

    return(
        <>
            <Button onClick={() => handleClick("69666fc80fdc4df8f10aafb6")}>See Preview</Button>
        </>
    )
}

export default RtoFolio