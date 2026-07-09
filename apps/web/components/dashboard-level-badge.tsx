"use client";

import { useEffect, useState } from "react";
import { getLearningProgress } from "@/lib/learning-api";

const LEVEL_LABELS: Record<string, string> = {
  A1: "A1 Beginner",
  A2: "A2 Elementary",
  B1: "B1 Intermediate",
  B2: "B2 Upper Intermediate",
  C1: "C1 Advanced",
};

export function DashboardLevelBadge() {
  const [label, setLabel] = useState("A1 Beginner");

  useEffect(() => {
    let ignore = false;

    async function load() {
      try {
        const summary = await getLearningProgress();
        if (!ignore && summary?.course?.levelCode) {
          setLabel(LEVEL_LABELS[summary.course.levelCode] ?? `${summary.course.levelCode}`);
        }
      } catch {
        // keep default
      }
    }

    load();
    return () => {
      ignore = true;
    };
  }, []);

  return (
    <p className="text-sm font-semibold uppercase text-leaf">{label}</p>
  );
}
