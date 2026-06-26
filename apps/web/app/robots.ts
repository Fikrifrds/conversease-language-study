import type { MetadataRoute } from "next";
import { SITE_URL } from "@conversease/shared";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? SITE_URL;

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      // Everything behind auth or part of the app shell — keep it out of the
      // index. Individual pages also set their own noindex as a backstop.
      disallow: [
        "/admin",
        "/dashboard",
        "/settings",
        "/billing",
        "/progress",
        "/conversation-coach",
        "/conversation-partner",
        "/review",
        "/level-tests",
        "/onboarding",
        "/verify-email",
        "/reset-password",
        "/forgot-password"
      ]
    },
    sitemap: `${siteUrl}/sitemap.xml`,
    host: siteUrl
  };
}
