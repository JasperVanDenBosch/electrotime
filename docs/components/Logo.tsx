'use client';

import { useEffect, useState } from 'react';

export function Logo() {
  const [isDark, setIsDark] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Check if theme is dark
    const checkTheme = () => {
      setIsDark(document.documentElement.classList.contains('dark'));
    };

    checkTheme();

    // Watch for theme changes
    const observer = new MutationObserver(checkTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  // Determine base path based on actual location
  const getBasePath = () => {
    if (!mounted) return '';
    if (typeof window !== 'undefined' && window.location.pathname.startsWith('/latency-recorder')) {
      return '/latency-recorder';
    }
    return '';
  };

  const basePath = getBasePath();

  return (
    <img 
      src={isDark ? `${basePath}/electrotime-dark.svg` : `${basePath}/electrotime.svg`} 
      alt="ElectroTime" 
      className="h-12 md:h-20 w-auto"
    />
  );
}