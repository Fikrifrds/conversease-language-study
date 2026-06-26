import type { Metadata } from "next";

// Metadata for pages that should never appear in search results — anything
// behind auth (dashboard, settings, billing, the learning app itself) or
// transient auth flows. Keeps a human title but tells crawlers to skip it.
export function noindexMetadata(title: string): Metadata {
  return {
    title,
    robots: {
      index: false,
      follow: false
    }
  };
}
