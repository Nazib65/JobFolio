"use client"

import { useState } from "react"
import { PortfolioSchema } from "@/types/portfolio"
import PortfolioRenderer from "./PortfolioRenderer"
import { Monitor, Tablet, Smartphone, X } from "lucide-react"
import { DeviceSizeProvider } from "./DeviceSizeContext"

type DeviceSize = "desktop" | "tablet" | "phone"

interface FullscreenPreviewModalProps {
    portfolioSchema: PortfolioSchema
    isOpen: boolean
    onClose: () => void
}

const deviceSizes = {
    desktop: { width: "100%", maxWidth: "100%", label: "Desktop" },
    tablet: { width: "820px", maxWidth: "820px", label: "Tablet" },
    phone: { width: "420px", maxWidth: "420px", label: "Phone" },
}

const FullscreenPreviewModal = ({
    portfolioSchema,
    isOpen,
    onClose,
}: FullscreenPreviewModalProps) => {
    const [deviceSize, setDeviceSize] = useState<DeviceSize>("desktop")

    if (!isOpen) return null

    const currentSize = deviceSizes[deviceSize]

    return (
        <div className="fixed inset-0 z-50 bg-ui-background">
            {/* Header with controls */}
            <div className="relative z-[60] flex items-center justify-between border-b border-ui-border bg-ui-background px-4 py-3">
                <div className="flex items-center gap-2">
                    <h2 className="text-sm font-semibold text-ui-foreground">Preview</h2>
                    <span className="text-xs text-ui-muted-foreground">
                        {currentSize.label}
                    </span>
                </div>

                {/* Device size buttons */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setDeviceSize("desktop")}
                        className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                            deviceSize === "desktop"
                                ? "bg-ui-primary text-ui-primary-foreground"
                                : "bg-ui-secondary text-ui-secondary-foreground hover:bg-ui-secondary/80"
                        }`}
                        title="Desktop View"
                    >
                        <Monitor size={16} />
                        <span className="hidden sm:inline">Desktop</span>
                    </button>
                    <button
                        onClick={() => setDeviceSize("tablet")}
                        className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                            deviceSize === "tablet"
                                ? "bg-ui-primary text-ui-primary-foreground"
                                : "bg-ui-secondary text-ui-secondary-foreground hover:bg-ui-secondary/80"
                        }`}
                        title="Tablet View"
                    >
                        <Tablet size={16} />
                        <span className="hidden sm:inline">Tablet</span>
                    </button>
                    <button
                        onClick={() => setDeviceSize("phone")}
                        className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                            deviceSize === "phone"
                                ? "bg-ui-primary text-ui-primary-foreground"
                                : "bg-ui-secondary text-ui-secondary-foreground hover:bg-ui-secondary/80"
                        }`}
                        title="Phone View"
                    >
                        <Smartphone size={16} />
                        <span className="hidden sm:inline">Phone</span>
                    </button>
                </div>

                {/* Close button */}
                <button
                    onClick={onClose}
                    className="relative z-[61] rounded-md p-2 text-ui-foreground hover:bg-ui-secondary"
                    title="Close Preview"
                >
                    <X size={20} />
                </button>
            </div>

            {/* Preview content */}
            <div className="flex h-[calc(100vh-57px)] items-start justify-center overflow-auto bg-ui-muted/30 p-4">
                <div
                    className="transition-all duration-300 ease-in-out"
                    style={{
                        width: currentSize.width,
                        maxWidth: currentSize.maxWidth,
                    }}
                >
                    <div className="bg-background shadow-2xl">
                        <DeviceSizeProvider value={deviceSize}>
                            <PortfolioRenderer portfolioSchema={portfolioSchema} />
                        </DeviceSizeProvider>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FullscreenPreviewModal
