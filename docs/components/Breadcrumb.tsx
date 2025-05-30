'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight } from 'lucide-react';

export function Breadcrumb() {
  const pathname = usePathname();
  
  if (pathname === '/') {
    return null;
  }
  
  const segments = pathname.split('/').filter(Boolean);
  
  const breadcrumbItems = segments.map((segment, index) => {
    const href = `/${segments.slice(0, index + 1).join('/')}`;
    const label = segment
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
    
    return { href, label };
  });
  
  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
      <Link href="/" className="hover:text-foreground transition-colors">
        Home
      </Link>
      {breadcrumbItems.map((item, index) => (
        <div key={item.href} className="flex items-center gap-2">
          <ChevronRight className="h-4 w-4" />
          {index === breadcrumbItems.length - 1 ? (
            <span className="text-foreground font-medium">{item.label}</span>
          ) : (
            <Link href={item.href} className="hover:text-foreground transition-colors">
              {item.label}
            </Link>
          )}
        </div>
      ))}
    </div>
  );
}