'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Components } from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const components: Components = {
    code({ node, inline, className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '');
      const language = match ? match[1] : '';
      
      return !inline && match ? (
        <SyntaxHighlighter
          style={vscDarkPlus}
          language={language}
          PreTag="div"
          className="rounded-lg my-4 text-sm"
          customStyle={{
            margin: 0,
            padding: '1rem',
            backgroundColor: '#1e1e1e',
            color: '#d4d4d4'
          }}
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      ) : (
        <code className="bg-zinc-800 text-zinc-300 px-1 py-0.5 rounded text-sm font-mono" {...props}>
          {children}
        </code>
      );
    },
    h1: ({ children }) => (
      <h1 className="text-4xl font-bold mb-6 mt-8 text-foreground">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-3xl font-semibold mb-4 mt-6 text-foreground">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-2xl font-semibold mb-3 mt-4 text-foreground">{children}</h3>
    ),
    h4: ({ children }) => (
      <h4 className="text-xl font-semibold mb-2 mt-3 text-foreground">{children}</h4>
    ),
    p: ({ children }) => (
      <p className="mb-4 leading-7 text-muted-foreground">{children}</p>
    ),
    ul: ({ children }) => (
      <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>
    ),
    li: ({ children }) => (
      <li className="mb-1">{children}</li>
    ),
    blockquote: ({ children }) => (
      <blockquote className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 my-4 not-italic">
        {children}
      </blockquote>
    ),
    table: ({ children }) => (
      <div className="overflow-x-auto mb-4">
        <table className="w-full border-collapse">{children}</table>
      </div>
    ),
    thead: ({ children }) => (
      <thead>{children}</thead>
    ),
    tbody: ({ children }) => (
      <tbody>{children}</tbody>
    ),
    tr: ({ children }) => (
      <tr>{children}</tr>
    ),
    th: ({ children }) => (
      <th className="border border-border px-4 py-2 bg-muted text-left font-semibold">
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td className="border border-border px-4 py-2">{children}</td>
    ),
    a: ({ href, children }) => (
      <a
        href={href}
        className="text-primary hover:text-primary/80 underline underline-offset-4"
        target={href?.startsWith('http') ? '_blank' : undefined}
        rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
      >
        {children}
      </a>
    ),
    img: ({ src, alt }) => (
      <img
        src={src}
        alt={alt || ''}
        className="max-w-full h-auto rounded-lg shadow-md my-4"
      />
    ),
    hr: () => (
      <hr className="my-8 border-t border-border" />
    ),
  };

  return (
    <div className="markdown-content max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}