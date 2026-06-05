import Image from "next/image";
import Link from "next/link";

type BrandMarkProps = {
  href?: string;
  tone?: "dark" | "light";
  size?: "sm" | "md";
};

export function BrandMark({ href = "/", tone = "dark", size = "md" }: BrandMarkProps) {
  const iconSize = size === "sm" ? 32 : 36;
  const textClass = tone === "light" ? "text-white" : "text-ink";

  const content = (
    <>
      <span className="grid place-items-center rounded-lg drop-shadow-sm">
        <Image src="/conversease-logo.png" alt="" width={iconSize} height={iconSize} priority={size === "md"} />
      </span>
      <span className={`font-semibold ${textClass}`}>Conversease</span>
    </>
  );

  if (!href) {
    return <div className="flex items-center gap-2">{content}</div>;
  }

  return (
    <Link href={href} className="focus-ring flex items-center gap-2 rounded-lg">
      {content}
    </Link>
  );
}
