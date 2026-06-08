"use client";

import { useEffect } from "react";
import { markStudyDay } from "@/lib/weekly-streak";

export function StudyDayMarker() {
  useEffect(() => {
    markStudyDay();
  }, []);

  return null;
}

