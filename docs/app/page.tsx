import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { getMarkdownBySlug } from '@/lib/markdown';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Getting Started - Latency Recorder',
  description: 'Timing Matters Hackathon information and project overview',
};

// ISR: Revalidate every hour
export const revalidate = 3600;

export default function HomePage() {
  const content = getMarkdownBySlug('overview');

  if (!content) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Content Not Found</h1>
        <p className="text-muted-foreground">
          The overview content could not be loaded.
        </p>
      </div>
    );
  }

  return <MarkdownRenderer content={content.content} />;
}