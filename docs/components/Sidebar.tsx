'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { ChevronRight, Home, Rocket, FileText, Code, Cpu, BarChart3, Smartphone, Globe, Sparkles } from 'lucide-react';
import { useState } from 'react';
import { NavItem } from '@/lib/markdown';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';

interface SidebarProps {
  navigation: NavItem[];
}

export function Sidebar({ navigation }: SidebarProps) {
  const pathname = usePathname();
  const [expandedSections, setExpandedSections] = useState<string[]>(['Hackathon']);

  const toggleSection = (title: string) => {
    setExpandedSections(prev =>
      prev.includes(title)
        ? prev.filter(t => t !== title)
        : [...prev, title]
    );
  };

  const renderNavItem = (item: NavItem, level = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedSections.includes(item.title);
    const isActive = pathname === item.href;
    const isParentActive = item.children?.some(child => pathname === child.href);

    return (
      <div key={item.href}>
        <div
          className={cn(
            "flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200",
            level > 0 && "ml-4",
            isActive && "bg-primary/10 text-primary border-l-2 border-primary",
            !isActive && "hover:bg-muted hover:text-foreground",
            isParentActive && "text-primary"
          )}
        >
          {hasChildren ? (
            <button
              onClick={() => toggleSection(item.title)}
              className="flex items-center gap-2 w-full text-left"
            >
              <ChevronRight
                className={cn(
                  "h-4 w-4 transition-transform",
                  isExpanded && "rotate-90"
                )}
              />
              {getIcon(item.title)}
              <span>{item.title}</span>
            </button>
          ) : (
            <Link href={item.href} className="flex items-center gap-2 w-full">
              {level === 0 && getIcon(item.title)}
              {level > 0 && <span className="ml-6" />}
              <span>{item.title}</span>
            </Link>
          )}
        </div>
        {hasChildren && isExpanded && (
          <div className="mt-1">
            {item.children!.map(child => renderNavItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  const getIcon = (title: string) => {
    const iconMap: { [key: string]: JSX.Element } = {
      'Getting Started': <Home className="h-4 w-4" />,
      'Hackathon': <Rocket className="h-4 w-4" />,
      'Hardware': <Cpu className="h-4 w-4" />,
      'Firmware': <Code className="h-4 w-4" />,
      'Data Analysis': <BarChart3 className="h-4 w-4" />,
      'User Interface': <Smartphone className="h-4 w-4" />,
      'Website': <Globe className="h-4 w-4" />,
      'Miscellaneous Ideas & Fun Projects': <Sparkles className="h-4 w-4" />,
    };
    return iconMap[title] || <FileText className="h-4 w-4" />;
  };

  return (
    <aside className="w-64 h-full bg-muted/10 border-r">
      <ScrollArea className="h-full py-6 px-4">
        <nav className="space-y-1">
          {navigation.map(item => renderNavItem(item))}
        </nav>
      </ScrollArea>
    </aside>
  );
}