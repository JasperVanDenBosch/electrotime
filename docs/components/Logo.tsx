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

  return (
    <img 
      src={isDark ? "/electrotime/electrotime-dark.svg" : "/electrotime/electrotime.svg"} 
      alt="ElectroTime" 
      className="h-12 w-auto"
    />
  );
}