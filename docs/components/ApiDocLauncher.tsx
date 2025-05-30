'use client';

import { ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ApiDocLauncherProps {
  docsPath: string;
  title: string;
  description: string;
}

export function ApiDocLauncher({ docsPath, title, description }: ApiDocLauncherProps) {
  const handleOpen = () => {
    window.open(docsPath, '_blank');
  };

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center space-y-6 max-w-md">
        <h1 className="text-3xl font-bold">{title}</h1>
        <p className="text-muted-foreground text-lg">{description}</p>
        <Button 
          onClick={handleOpen}
          size="lg"
          className="gap-2"
        >
          <ExternalLink className="h-5 w-5" />
          Open Documentation
        </Button>
        <p className="text-sm text-muted-foreground">
          Documentation will open in a new tab for the best viewing experience.
        </p>
      </div>
    </div>
  );
}