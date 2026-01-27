import { Button } from "@/components/ui/button"
import { Palette } from "lucide-react"
import { useState } from "react"

interface ColorPaletteProps {
    onColorsChange?: (colors: string[]) => void
}

export const ColorPalette = ({ onColorsChange }: ColorPaletteProps) => {

    const [colors, setColors] = useState<string[]>([])

    const generateColors = async () => {
        const newColors = Array.from({ length: 3 }, () => {
            return '#' + Math.floor(Math.random() * 16777215).toString(16)
        });
        setColors(newColors)
        console.log("Generated colors:", newColors)
        // Pass the new colors to the parent component
        if (onColorsChange) {
            onColorsChange(newColors)
        }
    }

    return (
        <div className="flex items-center justify-center gap-2">
            <div className="grid grid-cols-3 gap-2 mt-4">
                {colors.map((color: string, index: number) => (
                    <div key={index} className="w-24 h-24 rounded-2xl p-2" style={{ backgroundColor: color }}>
                        <p className="text-xs text-white text-center">{color}</p>
                    </div>
                ))}
            </div>
            <Button variant="outline" onClick={generateColors}>
                <Palette className="w-4 h-4" />
            </Button>
        </div>
    );
};

export default ColorPalette;