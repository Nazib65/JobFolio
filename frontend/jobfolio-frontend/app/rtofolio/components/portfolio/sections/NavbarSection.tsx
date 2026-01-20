"use client"

import { useState, useEffect } from "react";
import { useDeviceSize } from "../DeviceSizeContext";

const NavbarSection = ({ section }: { section: any }) => {
    const contextDeviceSize = useDeviceSize();
    const layout = section?.layout || {};
    const desktopLayout = layout?.desktop || {};
    const mobileLayout = layout?.mobile || {};
    const props = section?.props || {};
    
    // State for mobile detection and menu toggle
    const [isMobile, setIsMobile] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    // Effect to handle window resize
    useEffect(() => {
        // If we have a context device size (from modal), use that
        if (contextDeviceSize !== null) {
            const shouldBeMobile = contextDeviceSize === "phone" || contextDeviceSize === "tablet";
            setIsMobile(shouldBeMobile);
            if (!shouldBeMobile) {
                setIsOpen(false); // Close menu when in desktop mode
            }
            return; // Skip window listener when context is provided
        }

        // Otherwise, use window width detection
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
            if (window.innerWidth >= 768) {
                setIsOpen(false); // Close menu when returning to desktop
            }
        };

        // Initial check
        handleResize();

        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [contextDeviceSize]);

    const ctaLabel = props.cta_label ?? props.ctaLabel ?? props.CTA;
    const ctaUrl = props.cta_url ?? props.ctaUrl;

    const activeLayout = isMobile ? mobileLayout : desktopLayout;
    const slots = desktopLayout?.slots || {};

    const maxWidth = activeLayout?.maxWidth ?? activeLayout?.max_width;
    const justifyContent = activeLayout?.justify ?? "space-between";
    const alignItems = activeLayout?.align ?? "center";
    const gap = activeLayout?.gap ?? "2rem";

    const navStyle: React.CSSProperties = {
        display: "flex",
        justifyContent,
        alignItems,
        gap,
        width: activeLayout?.width ?? "100%",
        maxWidth: maxWidth ?? undefined,
        margin: activeLayout?.margin ?? "0 auto",
        padding: "1rem 2rem",
    };

    const renderSlot = (slotName: string) => {
        switch (slotName.toLowerCase()) {
            case "logo":
                return props.logo ? (
                    <img src={props.logo} alt="Logo" className="h-10 w-10 object-contain" />
                ) : null;
            case "name":
                return props.name ? (
                    <span className="text-lg font-semibold">{props.name}</span>
                ) : null;
            case "links":
                return (props.links || []).length ? (
                    <div className="flex items-center gap-6">
                        {(props.links || []).map((link: any, idx: number) => (
                            <a
                                key={idx}
                                href={link.url || "#"}
                                className="text-sm text-foreground/80 hover:text-foreground"
                            >
                                {link.label || "Link"}
                            </a>
                        ))}
                    </div>
                ) : null;
            case "cta":
                return ctaLabel ? (
                    ctaUrl ? (
                        <a href={ctaUrl} target="_blank" rel="noreferrer">
                            <button className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground">
                                {ctaLabel}
                            </button>
                        </a>
                    ) : (
                        <button className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground">
                            {ctaLabel}
                        </button>
                    )
                ) : null;
            default:
                return null;
        }
    };

    const renderSlotGroup = (slotData: any) => {
        if (!slotData) return null;
        const items = Array.isArray(slotData) ? slotData : [slotData];
        return items.map((item: any, idx: number) => {
            const name = typeof item === "string" ? item : item?.name;
            if (!name) return null;
            return <div key={`${name}-${idx}`}>{renderSlot(name)}</div>;
        });
    };

    return (
        <nav
            className="relative z-50 w-full border-b border-border bg-background text-foreground"
            style={navStyle}
        >
            {/* Left slots */}
            <div className="flex items-center gap-4">
                {renderSlotGroup(slots?.left)}
            </div>

            {/* Desktop right slots */}
            {!isMobile && (
                <div className="flex items-center gap-6">
                    {renderSlotGroup(slots?.right)}
                </div>
            )}

            {/* Mobile View: Hamburger Button */}
            {isMobile && (
                <button 
                    onClick={() => setIsOpen(!isOpen)}
                    className="absolute right-4 top-4 z-51 rounded-md p-2 text-foreground hover:bg-muted"
                >
                    {/* Simple SVG Icon for Menu / Close */}
                    {isOpen ? (
                         <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                         </svg>
                    ) : (
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <line x1="3" y1="12" x2="21" y2="12"></line>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <line x1="3" y1="18" x2="21" y2="18"></line>
                        </svg>
                    )}
                </button>
            )}

            {/* Mobile Dropdown Menu */}
            {isMobile && isOpen && (
                <div className="absolute left-0 top-full w-full border-b border-border bg-background px-8 py-4 shadow">
                    {renderSlotGroup(slots?.right)}
                </div>
            )}
        </nav>
    )
}

export default NavbarSection;