import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Harga",
  description:
    "Pilih paket Conversease: Free untuk mulai, Pro untuk membuka kurikulum lengkap, feedback detail, evaluasi level, dan laporan progress.",
  alternates: { canonical: "/pricing" }
};

export default function PricingLayout({ children }: { children: React.ReactNode }) {
  return children;
}
