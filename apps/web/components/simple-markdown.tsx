import type { ReactNode } from "react";

type Block =
  | { type: "heading"; level: 1 | 2 | 3; text: string }
  | { type: "paragraph"; text: string }
  | { type: "ul"; items: string[] }
  | { type: "ol"; items: string[] }
  | { type: "code"; text: string };

function renderInline(text: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**") && part.length > 4) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return <span key={index}>{part}</span>;
  });
}

function parseMarkdown(markdown: string): Block[] {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const blocks: Block[] = [];
  let i = 0;

  function isBlank(line: string) {
    return line.trim() === "";
  }

  while (i < lines.length) {
    const raw = lines[i] ?? "";
    const line = raw.trimEnd();

    if (isBlank(line)) {
      i += 1;
      continue;
    }

    if (line.startsWith("```")) {
      const buffer: string[] = [];
      i += 1;
      while (i < lines.length && !(lines[i] ?? "").trim().startsWith("```")) {
        buffer.push(lines[i] ?? "");
        i += 1;
      }
      i += 1;
      blocks.push({ type: "code", text: buffer.join("\n").trimEnd() });
      continue;
    }

    const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);
    if (headingMatch) {
      const level = headingMatch[1].length as 1 | 2 | 3;
      blocks.push({ type: "heading", level, text: headingMatch[2].trim() });
      i += 1;
      continue;
    }

    const ulMatch = line.match(/^-+\s+(.*)$/);
    if (ulMatch) {
      const items: string[] = [];
      while (i < lines.length) {
        const current = (lines[i] ?? "").trimEnd();
        const match = current.match(/^-+\s+(.*)$/);
        if (!match) {
          break;
        }
        items.push(match[1].trim());
        i += 1;
      }
      blocks.push({ type: "ul", items });
      continue;
    }

    const olMatch = line.match(/^\d+\.\s+(.*)$/);
    if (olMatch) {
      const items: string[] = [];
      while (i < lines.length) {
        const current = (lines[i] ?? "").trimEnd();
        const match = current.match(/^\d+\.\s+(.*)$/);
        if (!match) {
          break;
        }
        items.push(match[1].trim());
        i += 1;
      }
      blocks.push({ type: "ol", items });
      continue;
    }

    const paragraphLines: string[] = [line.trim()];
    i += 1;
    while (i < lines.length) {
      const next = (lines[i] ?? "").trimEnd();
      if (isBlank(next)) {
        break;
      }
      if (next.trim().startsWith("```")) {
        break;
      }
      if (/^(#{1,3})\s+/.test(next.trim())) {
        break;
      }
      if (/^-+\s+/.test(next.trim())) {
        break;
      }
      if (/^\d+\.\s+/.test(next.trim())) {
        break;
      }
      paragraphLines.push(next.trim());
      i += 1;
    }
    blocks.push({ type: "paragraph", text: paragraphLines.join(" ") });
  }

  return blocks;
}

export function SimpleMarkdown({ markdown, dropLeadingHeading = false }: { markdown: string; dropLeadingHeading?: boolean }) {
  const blocks = parseMarkdown(markdown);
  if (dropLeadingHeading && blocks[0]?.type === "heading") {
    blocks.shift();
  }
  return (
    <div className="space-y-3 text-ink/75">
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          const classes = block.level === 1 ? "mt-2 text-lg font-semibold text-ink" : block.level === 2 ? "mt-2 text-base font-semibold text-ink" : "text-sm font-semibold uppercase tracking-wide text-ink/70";
          const Tag = block.level === 1 ? "h3" : block.level === 2 ? "h4" : "h5";
          return (
            <Tag key={index} className={classes}>
              {renderInline(block.text)}
            </Tag>
          );
        }

        if (block.type === "paragraph") {
          return (
            <p key={index} className="leading-7">
              {renderInline(block.text)}
            </p>
          );
        }

        if (block.type === "ul") {
          return (
            <ul key={index} className="list-disc space-y-1 pl-5 leading-7">
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex}>{renderInline(item)}</li>
              ))}
            </ul>
          );
        }

        if (block.type === "ol") {
          return (
            <ol key={index} className="list-decimal space-y-1 pl-5 leading-7">
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex}>{renderInline(item)}</li>
              ))}
            </ol>
          );
        }

        return (
          <pre key={index} className="overflow-x-auto rounded-lg bg-paper p-4 text-sm text-ink">
            <code>{block.text}</code>
          </pre>
        );
      })}
    </div>
  );
}

