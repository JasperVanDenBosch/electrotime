import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { getMarkdownBySlug, getAllMarkdownDocuments } from '@/lib/markdown';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  const documents = getAllMarkdownDocuments();
  return documents
    .filter(doc => doc.category === 'hackathon' && doc.slug !== 'hackathon/overview')
    .map((doc) => ({
      slug: doc.slug.replace('hackathon/', ''),
    }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const doc = getMarkdownBySlug(`hackathon/${slug}`);
  
  if (!doc) {
    return {
      title: 'Page Not Found',
    };
  }

  return {
    title: `${doc.title} - ElectroTime`,
    description: doc.description || `Documentation for ${doc.title}`,
  };
}

// ISR: Revalidate every hour
export const revalidate = 3600;

export default async function HackathonPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const content = getMarkdownBySlug(`hackathon/${slug}`);

  if (!content) {
    notFound();
  }

  return <MarkdownRenderer content={content.content} />;
}