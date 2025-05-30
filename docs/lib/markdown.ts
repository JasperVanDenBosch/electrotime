import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import toml from 'toml';

const contentDirectory = path.join(process.cwd(), 'content');

export interface MarkdownDocument {
  slug: string;
  title: string;
  description?: string;
  content: string;
  frontmatter: any;
  sequenceNumber?: number;
}

export interface NavItem {
  title: string;
  href: string;
  children?: NavItem[];
}

export function getAllMarkdownSlugs(): string[] {
  const files = fs.readdirSync(contentDirectory);
  return files
    .filter(file => file.endsWith('.md'))
    .map(file => file.replace('.md', ''));
}

export function getMarkdownBySlug(slug: string): MarkdownDocument | null {
  try {
    const fullPath = path.join(contentDirectory, `${slug}.md`);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    
    // Handle TOML frontmatter (delimited by +++)
    let data: any = {};
    let content = fileContents;
    
    const tomlMatch = fileContents.match(/^\+\+\+([\s\S]*?)\+\+\+/);
    if (tomlMatch) {
      try {
        data = toml.parse(tomlMatch[1]);
        content = fileContents.slice(tomlMatch[0].length).trim();
      } catch (e) {
        console.error('Error parsing TOML frontmatter:', e);
      }
    } else {
      // Fall back to YAML frontmatter
      const parsed = matter(fileContents);
      data = parsed.data;
      content = parsed.content;
    }
    
    // Extract title from frontmatter or first heading
    let title = data.title || slug.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    
    // If no title in frontmatter, try to extract from first heading
    if (!data.title) {
      const headingMatch = content.match(/^#\s+(.+)$/m);
      if (headingMatch) {
        title = headingMatch[1].replace(/[🔧💻📊🖥️🌐🎨]/g, '').trim();
      }
    }
    
    return {
      slug,
      title,
      description: data.description,
      content,
      frontmatter: data,
      sequenceNumber: data.SequenceNumber
    };
  } catch (error) {
    return null;
  }
}

export function getAllMarkdownDocuments(): MarkdownDocument[] {
  const slugs = getAllMarkdownSlugs();
  const documents = slugs
    .map(slug => getMarkdownBySlug(slug))
    .filter((doc): doc is MarkdownDocument => doc !== null);
  
  return documents;
}

export function getNavigation(): NavItem[] {
  const documents = getAllMarkdownDocuments();
  
  // Define the navigation structure
  const navigation: NavItem[] = [
    {
      title: 'Getting Started',
      href: '/',
    },
    {
      title: 'Hackathon',
      href: '/hackathon',
      children: documents
        .filter(doc => doc.slug !== 'overview' && !doc.slug.startsWith('developers-'))
        .sort((a, b) => {
          // Sort by sequence number if available, otherwise alphabetically
          if (a.sequenceNumber !== undefined && b.sequenceNumber !== undefined) {
            return a.sequenceNumber - b.sequenceNumber;
          }
          if (a.sequenceNumber !== undefined) return -1;
          if (b.sequenceNumber !== undefined) return 1;
          return a.title.localeCompare(b.title);
        })
        .map(doc => ({
          title: doc.title,
          href: `/hackathon/${doc.slug}`
        }))
    },
    {
      title: 'Developers',
      href: '/developers',
      children: [
        {
          title: 'Hardware',
          href: '/hackathon/developers-hardware'
        },
        {
          title: 'Firmware',
          href: '/hackathon/developers-firmware'
        },
        {
          title: 'Data Analytics',
          href: '/hackathon/developers-data-analytics'
        }
      ]
    }
  ];
  
  return navigation;
}