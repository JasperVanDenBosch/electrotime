'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

export function ScrollToTop() {
  const pathname = usePathname();

  useEffect(() => {
    // Scroll to top when pathname changes
    const scrollContainer = document.getElementById('main-content');
    if (scrollContainer) {
      scrollContainer.scrollTop = 0;
    }
    // Also scroll the window to top for mobile
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}