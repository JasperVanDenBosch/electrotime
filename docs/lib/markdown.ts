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
  category?: string;
}

export interface NavItem {
  title: string;
  href: string;
  children?: NavItem[];
}

function getAllMarkdownFiles(dir: string = contentDirectory, category: string = ''): { path: string; slug: string; category: string }[] {
  const files: { path: string; slug: string; category: string }[] = [];
  
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && !item.startsWith('.')) {
      // Recursively get files from subdirectories
      files.push(...getAllMarkdownFiles(fullPath, item));
    } else if (item.endsWith('.md')) {
      const relativePath = path.relative(contentDirectory, fullPath);
      const slug = relativePath.replace(/\.md$/, '').replace(/\\/g, '/');
      files.push({ path: fullPath, slug, category });
    }
  }
  
  return files;
}

export function getMarkdownBySlug(slug: string): MarkdownDocument | null {
  try {
    // Check if file exists directly
    let fullPath = path.join(contentDirectory, `${slug}.md`);
    
    // If not found, check in subdirectories
    if (!fs.existsSync(fullPath)) {
      const allFiles = getAllMarkdownFiles();
      const file = allFiles.find(f => f.slug === slug);
      if (file) {
        fullPath = file.path;
      } else {
        return null;
      }
    }
    
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
    let title = data.title || slug.split('/').pop()!.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    
    // If no title in frontmatter, try to extract from first heading
    if (!data.title) {
      const headingMatch = content.match(/^#\s+(.+)$/m);
      if (headingMatch) {
        title = headingMatch[1].replace(/[🔧💻📊🖥️🌐🎨]/g, '').trim();
      }
    }
    
    // Determine category from path
    const category = slug.includes('/') ? slug.split('/')[0] : '';
    
    return {
      slug,
      title,
      description: data.description,
      content,
      frontmatter: data,
      sequenceNumber: data.SequenceNumber,
      category
    };
  } catch (error) {
    console.error(`Error reading markdown file: ${slug}`, error);
    return null;
  }
}

export function getAllMarkdownDocuments(): MarkdownDocument[] {
  const files = getAllMarkdownFiles();
  const documents = files
    .map(file => getMarkdownBySlug(file.slug))
    .filter((doc): doc is MarkdownDocument => doc !== null);
  
  return documents;
}

export function getNavigation(): NavItem[] {
  const documents = getAllMarkdownDocuments();
  
  // Filter documents by category
  const hackathonDocs = documents
    .filter(doc => doc.category === 'hackathon' && doc.slug !== 'hackathon/overview')
    .sort((a, b) => {
      if (a.sequenceNumber !== undefined && b.sequenceNumber !== undefined) {
        return a.sequenceNumber - b.sequenceNumber;
      }
      if (a.sequenceNumber !== undefined) return -1;
      if (b.sequenceNumber !== undefined) return 1;
      return a.title.localeCompare(b.title);
    });
    
  const developerDocs = documents
    .filter(doc => doc.category === 'developers')
    .sort((a, b) => {
      if (a.sequenceNumber !== undefined && b.sequenceNumber !== undefined) {
        return a.sequenceNumber - b.sequenceNumber;
      }
      if (a.sequenceNumber !== undefined) return -1;
      if (b.sequenceNumber !== undefined) return 1;
      return a.title.localeCompare(b.title);
    });
  
  // Define the navigation structure
  const navigation: NavItem[] = [
    {
      title: 'Getting Started',
      href: '/',
    },
    {
      title: 'Developers',
      href: '/developers',
      children: [
        {
          title: 'Overview',
          href: '/developers'
        },
        ...developerDocs
          .filter(doc => !doc.slug.includes('-api'))
          .map(doc => {
            // Simplify titles for navigation
            let title = doc.title;
            if (title === 'GUI Development') title = 'GUI';
            if (title === 'Hardware Development') title = 'Hardware';
            
            return {
              title,
              href: `/developers/${doc.slug.replace('developers/', '')}`
            };
          }),
        {
          title: 'API Documentation',
          href: '/api-docs'
        }
      ]
    },
    {
      title: 'Hackathon',
      href: '/hackathon',
      children: [
        {
          title: 'Overview',
          href: '/hackathon'
        },
        ...hackathonDocs.map(doc => ({
          title: doc.title,
          href: `/hackathon/${doc.slug.replace('hackathon/', '')}`
        }))
      ]
    }
  ];
  
  return navigation;
}