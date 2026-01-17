"use client"

import React, { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Upload } from "lucide-react"

const RtoFolio = () => {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [markdown, setMarkdown] = useState<string | null>(null)
    const fileInputRef = useRef<HTMLInputElement>(null)
    const router = useRouter()

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

            const response = await fetch(`/api/v1/resume/`, {
                method: "POST",
                body: formData,
            })

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`)
            }

            const data = await response.json()
            console.log("Resume parsed:", data)
            setMarkdown(data.markdown)

            const generationResponse = await fetch(`/api/v1/generation/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    resume_markdown: data.markdown,
                }),
            })

            if (!generationResponse.ok) {
                throw new Error(`Generation failed: ${generationResponse.statusText}`)
            }

            const portfolioData = await generationResponse.json()
            console.log("Portfolio generated:", portfolioData)

            const uploadResponse = await fetch(`/api/v1/portfolio/`, {
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
        <div className="flex flex-col items-center justify-center min-h-screen gap-6 p-4">
            <h1 className="text-4xl font-bold">R TO Folio</h1>
            
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
                    className="w-full"
                    variant="outline"
                >
                    <Upload className="mr-2 h-4 w-4" />
                    {selectedFile ? selectedFile.name : "Upload PDF Resume"}
                </Button>

                {selectedFile && (
                    <p className="text-sm text-green-600">
                        File selected: {selectedFile.name}
                    </p>
                )}
                
                <div>
                    <p>
                        {markdown ? markdown : "No markdown generated"}
                    </p>
                </div>

                <Button onClick={handleClick}>
                    See Preview
                </Button>
            </div>
        </div>
    )
}

export default RtoFolio