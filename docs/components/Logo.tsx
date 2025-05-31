'use client';

import { useEffect, useState } from 'react';

export function Logo() {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
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

  const basePath = process.env.NODE_ENV === 'production' ? '/latency-recorder' : '';

  return (
    <img 
      src={isDark ? `${basePath}/electrotime-dark.svg` : `${basePath}/electrotime.svg`} 
      alt="ElectroTime" 
      className="h-12 md:h-20 w-auto"
    />
  );
}