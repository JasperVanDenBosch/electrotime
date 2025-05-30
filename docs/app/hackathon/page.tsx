import { Metadata } from "next";
import fs from "fs";
import path from "path";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";

export const metadata: Metadata = {
  title: "Hackathon Resources - ElectroTime",
  description: "Documentation and resources for the Timing Matters Hackathon",
};

export default function HackathonIndexPage() {
  const contentPath = path.join(
    process.cwd(),
    "content",
    "hackathon",
    "overview.md"
  );
  let content = "";

  try {
    content = fs.readFileSync(contentPath, "utf8");
  } catch (error) {
    content = "# Hackathon Overview\n\nContent not found.";
  }

  return <MarkdownRenderer content={content} />;
}
