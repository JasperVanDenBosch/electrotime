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
    <div className="flex items-center gap-1 md:gap-2 text-xs md:text-sm text-muted-foreground overflow-x-auto">
      <Link href="/" className="hover:text-foreground transition-colors whitespace-nowrap">
        Home
      </Link>
      {breadcrumbItems.map((item, index) => (
        <div key={item.href} className="flex items-center gap-1 md:gap-2">
          <ChevronRight className="h-3 w-3 md:h-4 md:w-4 flex-shrink-0" />
          {index === breadcrumbItems.length - 1 ? (
            <span className="text-foreground font-medium whitespace-nowrap">{item.label}</span>
          ) : (
            <Link href={item.href} className="hover:text-foreground transition-colors whitespace-nowrap">
              {item.label}
            </Link>
          )}
        </div>
      ))}
    </div>
  );
}