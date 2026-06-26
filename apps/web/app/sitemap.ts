import type { MetadataRoute } from "next";
import { SITE_URL } from "@conversease/shared";
import { courses, lessonCatalog } from "@/lib/data";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? SITE_URL;

// Only public, English-track URLs belong in the sitemap. App pages live behind
// auth and Arabic content stays out while that track is coming-soon.
export default function sitemap(): MetadataRoute.Sitemap {
  const staticPaths = ["", "/courses", "/pricing", "/login", "/register"];

  const staticEntries = staticPaths.map((path) => ({
    url: `${siteUrl}${path}`,
    changeFrequency: "weekly" as const,
    priority: path === "" ? 1 : 0.7
  }));

  const courseEntries = courses
    .filter((course) => course.language === "english")
    .map((course) => ({
      url: `${siteUrl}/courses/${course.slug}`,
      changeFrequency: "monthly" as const,
      priority: 0.7
    }));

  const lessonEntries = lessonCatalog
    .filter((lesson) => lesson.language === "english")
    .map((lesson) => ({
      url: `${siteUrl}/lessons/${lesson.slug}`,
      changeFrequency: "monthly" as const,
      priority: 0.6
    }));

  return [...staticEntries, ...courseEntries, ...lessonEntries];
}
