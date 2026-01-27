"use client"

import React, { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Upload } from "lucide-react"
import ColorPalette from "./components/portfolio/ColorPalette"

const RtoFolio = () => {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [markdown, setMarkdown] = useState<string | null>(null)
    const fileInputRef = useRef<HTMLInputElement>(null)
    const router = useRouter()
    const [colors, setColors] = useState<string[]>([])

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (file) {
            // Validate that the file is a PDF
            if (file.type !== "application/pdf") {
                setError("Please select a PDF file")
                setSelectedFile(null)
                return
            }
            setError(null)
            setSelectedFile(file)
            console.log("Selected file:", file.name)
            // You can add file upload logic here
        }
    }

    const handleUploadClick = () => {
        fileInputRef.current?.click()
    }

    const handleClick = async () => {
        if (!selectedFile) {
            setError("Please select a PDF file first")
            return
        }

        setLoading(true)
        setError(null)
        
        try {
            // Create FormData and append the file with the field name 'resume'
            const formData = new FormData()
            formData.append("resume", selectedFile)

            const response = await fetch(`/api/v1/resume`, {
                method: "POST",
                body: formData,
            })

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`)
            }

            const data = await response.json()
            console.log("Resume parsed:", data)
            setMarkdown(data.markdown)

            // Create an AbortController with a long timeout for the generation request
            const controller = new AbortController()
            const timeoutId = setTimeout(() => controller.abort(), 120000) // 2 minutes timeout
            
            const generationResponse = await fetch(`/api/v1/generation`, {
                method: "POST",
                signal: controller.signal,
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    resume_markdown: data.markdown,
                    color_palette: colors.length > 0 ? colors : undefined,
                }),
            })
            
            clearTimeout(timeoutId)

            if (!generationResponse.ok) {
                throw new Error(`Generation failed: ${generationResponse.statusText}`)
            }

            const portfolioData = await generationResponse.json()
            console.log("Portfolio generated:", portfolioData)

            const uploadResponse = await fetch(`/api/v1/portfolio?user_id=${"6976c18ea9f62b07169a1b31"}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(portfolioData),
            })

            if (!uploadResponse.ok) {
                throw new Error(`Portfolio upload failed: ${uploadResponse.statusText}`)
            }

            const uploadData = await uploadResponse.json()
            console.log(uploadData)

            router.push(`/rtofolio/preview/${uploadData.id}`)
        } catch (error) {
            console.error("Error uploading resume:", error)
            setError(error instanceof Error ? error.message : "Failed to upload resume")
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen gap-4 bg-ui-background">
                <h1 className="text-4xl font-bold text-ui-foreground">R TO Folio</h1>
                <p className="text-ui-muted-foreground">Loading...</p>
            </div>
        )
    }

    if (error){
        return(
            <div className="flex flex-col items-center justify-center min-h-screen gap-4 bg-ui-background">
                <h1 className="text-4xl font-bold text-ui-foreground">R TO Folio</h1>
                <p className="text-ui-destructive">{error}</p>
            </div>
        )
    }

    return(
        <div className="flex flex-col items-center justify-center min-h-screen gap-6 p-4 bg-ui-background">
            <h1 className="text-4xl font-bold text-ui-foreground">R TO Folio</h1>
            
            <div className="flex flex-col items-center gap-4 w-full max-w-md">
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileChange}
                    className="hidden"
                />
                
                <Button 
                    onClick={handleUploadClick}
                    className="w-full border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
                    variant="outline"
                >
                    <Upload className="mr-2 h-4 w-4" />
                    {selectedFile ? selectedFile.name : "Upload PDF Resume"}
                </Button>

                {selectedFile && (
                    <p className="text-sm text-ui-primary">
                        File selected: {selectedFile.name}
                    </p>
                )}
                
                <div>
                    <ColorPalette onColorsChange={setColors}/>
                </div>

                <Button 
                    onClick={handleClick}
                    className="bg-ui-primary text-ui-primary-foreground hover:bg-ui-primary/90"
                >
                    See Preview
                </Button>
            </div>
        </div>
    )
}

export default RtoFolio