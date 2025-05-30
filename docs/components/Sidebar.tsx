'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { ChevronRight, Home, Rocket, FileText, Code, Cpu, BarChart3, Smartphone, Globe, Sparkles, CodeSquare, Github, Moon, Sun, BookOpen } from 'lucide-react';
import { useState, useEffect } from 'react';
import { NavItem } from '@/lib/markdown';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';

interface SidebarProps {
  navigation: NavItem[];
}

export function Sidebar({ navigation }: SidebarProps) {
  const pathname = usePathname();
  const [expandedSections, setExpandedSections] = useState<string[]>(['Hackathon', 'Developers']);
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }
  }, []);

  // Auto-expand sections that contain the active page
  useEffect(() => {
    const sectionsToExpand: string[] = [];
    navigation.forEach(item => {
      if (item.children) {
        const hasActiveChild = item.children.some(child => 
          pathname === child.href || pathname.startsWith(child.href + '/')
        );
        if (hasActiveChild) {
          sectionsToExpand.push(item.title);
        }
      }
    });
    
    setExpandedSections(prev => {
      const newSections = Array.from(new Set([...prev, ...sectionsToExpand]));
      return newSections;
    });
  }, [pathname, navigation]);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

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
    const isActive = pathname === item.href || 
                    (item.href !== '/' && pathname.startsWith(item.href + '/'));
    const isChildActive = item.children?.some(child => 
      pathname === child.href || pathname.startsWith(child.href + '/')
    );

    return (
      <div key={item.href}>
        <div
          className={cn(
            "flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200",
            level > 0 && "ml-4",
            isActive && "bg-muted text-foreground",
            !isActive && !isChildActive && "hover:bg-muted hover:text-foreground",
            isChildActive && !hasChildren && "text-primary"
          )}
        >
          {hasChildren ? (
            <button
              onClick={() => toggleSection(item.title)}
              className={cn(
                "flex items-center gap-2 w-full text-left",
                isChildActive && "text-primary font-semibold"
              )}
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
      'API Documentation': <BookOpen className="h-4 w-4" />,
      'Hackathon': <Rocket className="h-4 w-4" />,
      'Developers': <CodeSquare className="h-4 w-4" />,
      'Hardware': <Cpu className="h-4 w-4" />,
      'Hardware API': <Cpu className="h-4 w-4" />,
      'GUI': <Smartphone className="h-4 w-4" />,
      'GUI API': <Smartphone className="h-4 w-4" />,
      'Firmware': <Code className="h-4 w-4" />,
      'Data Analysis': <BarChart3 className="h-4 w-4" />,
      'Data Analytics': <BarChart3 className="h-4 w-4" />,
      'User Interface': <Smartphone className="h-4 w-4" />,
      'Website Documentation': <Globe className="h-4 w-4" />,
      'Miscellaneous Ideas & Fun Projects': <Sparkles className="h-4 w-4" />,
      'Repository': <FileText className="h-4 w-4" />,
      'Syrinx Static Site Generator': <Code className="h-4 w-4" />,
    };
    return iconMap[title] || <FileText className="h-4 w-4" />;
  };

  return (
    <aside className="w-64 h-full bg-muted/10 border-r flex flex-col">
      <ScrollArea className="flex-1 py-6 px-4">
        <nav className="space-y-1">
          {navigation.map(item => renderNavItem(item))}
        </nav>
      </ScrollArea>
      
      <div className="mt-auto p-4 space-y-2">
        <Separator className="mb-2" />
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start"
          asChild
        >
          <a
            href="https://github.com/JasperVanDenBosch/latency-recorder"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2"
          >
            <Github className="h-4 w-4" />
            <span>GitHub Repository</span>
          </a>
        </Button>
        
        <Button
          variant="ghost"
          size="sm"
          onClick={toggleTheme}
          className="w-full justify-start"
        >
          {theme === 'dark' ? (
            <Sun className="h-4 w-4 mr-2" />
          ) : (
            <Moon className="h-4 w-4 mr-2" />
          )}
          <span>{theme === 'dark' ? 'Light' : 'Dark'} Mode</span>
        </Button>
      </div>
    </aside>
  );
}