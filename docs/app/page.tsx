import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { getMarkdownBySlug } from '@/lib/markdown';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Getting Started - ElectroTime',
  description: 'Open-source Arduino-based device for measuring stimulus presentation latency in neuroscience experiments',
};

// ISR: Revalidate every hour
export const revalidate = 3600;

export default function HomePage() {
  const content = getMarkdownBySlug('repo');

  if (!content) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Content Not Found</h1>
        <p className="text-muted-foreground">
          The repository documentation could not be loaded.
        </p>
      </div>
    );
  }

  return <MarkdownRenderer content={content.content} />;
}