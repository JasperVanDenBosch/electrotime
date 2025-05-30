'use client';

import { useEffect } from 'react';

interface ApiRedirectProps {
  path: string;
}

export function ApiRedirect({ path }: ApiRedirectProps) {
  const newPath = path.replace('/api/', '/docs-api/');
  
  useEffect(() => {
    window.location.href = newPath;
  }, [newPath]);
  
  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">Redirecting to API Documentation...</h2>
        <p className="text-muted-foreground mb-4">
          If you are not redirected automatically, 
          <a href={newPath} className="text-primary hover:underline ml-1">
            click here
          </a>
        </p>
      </div>
    </div>
  );
}