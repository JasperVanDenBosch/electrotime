import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { getMarkdownBySlug, getAllMarkdownSlugs } from '@/lib/markdown';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  const slugs = getAllMarkdownSlugs();
  return slugs
    .filter(slug => slug !== 'overview')
    .map((slug) => ({
      slug,
    }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const doc = getMarkdownBySlug(slug);
  
  if (!doc) {
    return {
      title: 'Page Not Found',
    };
  }

  return {
    title: `${doc.title} - Latency Recorder`,
    description: doc.description || `Documentation for ${doc.title}`,
  };
}

// ISR: Revalidate every hour
export const revalidate = 3600;

export default async function HackathonPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const content = getMarkdownBySlug(slug);

  if (!content) {
    notFound();
  }

  return <MarkdownRenderer content={content.content} />;
}