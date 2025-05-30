interface ApiLinkCardProps {
  href: string;
  title: string;
  description: string;
  icon?: string;
}

export function ApiLinkCard({ href, title, description, icon = '📖' }: ApiLinkCardProps) {
  return (
    <div className="bg-zinc-900 p-4 rounded-lg my-4 border border-zinc-800">
      <a 
        href={href} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-400 hover:text-blue-300 font-bold text-lg flex items-center gap-2 mb-2"
      >
        <span>{icon}</span>
        {title}
      </a>
      <p className="text-zinc-400 text-sm m-0">
        {description}
      </p>
    </div>
  );
}

export function ApiCardGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
      {children}
    </div>
  );
}