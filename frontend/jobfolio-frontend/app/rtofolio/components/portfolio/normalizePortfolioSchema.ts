import type { PortfolioSchema, Theme } from "@/types/portfolio";

function normalizeFont(font: unknown): "sans" | "mono" | undefined {
  if (typeof font !== "string" || !font.trim()) return undefined;
  const f = font.toLowerCase();
  if (f.includes("mono")) return "mono";
  return "sans";
}

export function normalizeTheme(theme: unknown): Theme {
  const t = (theme ?? {}) as Record<string, any>;

  return {
    ...t,
    width: t.width ?? t.width,
    maxWidth: t.maxWidth ?? t.max_width,
    margin: t.margin ?? t.margin,
    display: t.display ?? t.display,
    flexDirection: t.flexDirection ?? t.flex_direction,
    alignItems: t.alignItems ?? t.align_items,
    colorPalette: Array.isArray(t.colorPalette) ? t.colorPalette : (Array.isArray(t.color_palette) ? t.color_palette : undefined),
    color_palette: Array.isArray(t.color_palette) ? t.color_palette : (Array.isArray(t.colorPalette) ? t.colorPalette : undefined),
    font: normalizeFont(t.font) ?? t.font,
  };
}

export function normalizePortfolioSchema(schema: unknown): PortfolioSchema {
  const s = (schema ?? {}) as Record<string, any>;

  return {
    ...s,
    schemaVersion: s.schemaVersion ?? s.schema_version ?? s.schema_version,
    theme: normalizeTheme(s.theme),
    sections: s.sections ?? [],
  };
}

