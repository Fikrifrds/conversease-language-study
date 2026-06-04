"use client";

import { useEffect, useState } from "react";
import { Mic } from "lucide-react";
import { ActionButton } from "@/components/action-button";
import { getAuthSession, onAuthSessionChanged } from "@/lib/auth-api";

export function LandingCoachCta() {
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    function sync() {
      setAuthed(Boolean(getAuthSession()));
    }

    sync();
    return onAuthSessionChanged(sync);
  }, []);

  return (
    <ActionButton href={authed ? "/conversation-coach" : "/register"} icon={Mic} tone="glass">
      {authed ? "Mulai Conversation Coach" : "Coba Conversation Coach"}
    </ActionButton>
  );
}
