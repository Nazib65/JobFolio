"use client";

import { useLayoutEffect } from "react";

export default function ThemeApplier({
  palette,
  font,
}: {
  palette?: string;
  font?: "sans" | "mono";
}) {
  useLayoutEffect(() => {
    const root = document.documentElement;

    // palette
    if (palette) {
      root.dataset.palette = palette;
    } else {
      delete root.dataset.palette;
    }

    // font (you already have --font-sans/--font-mono wired)
    root.classList.remove("font-sans", "font-mono");
    root.classList.add(font === "mono" ? "font-mono" : "font-sans");
  }, [palette, font]);

  return null;
}
