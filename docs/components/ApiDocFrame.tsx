'use client';

import { useEffect, useRef, useState } from 'react';
import { ExternalLink, RotateCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ApiDocFrameProps {
  basePath: string;
  title: string;
}

export function ApiDocFrame({ basePath, title }: ApiDocFrameProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [currentUrl, setCurrentUrl] = useState(basePath);
  const [iframeKey, setIframeKey] = useState(0);

  useEffect(() => {
    const handleIframeLoad = () => {
      const iframe = iframeRef.current;
      if (!iframe || !iframe.contentWindow) return;

      try {
        // Inject a script to handle link clicks
        const script = iframe.contentDocument?.createElement('script');
        if (script && iframe.contentDocument) {
          script.textContent = `
            // Override link clicks to stay within the iframe
            document.addEventListener('click', function(e) {
              const link = e.target.closest('a');
              if (link && link.href && !link.href.includes('#')) {
                e.preventDefault();
                // Update the iframe src from parent
                window.parent.postMessage({
                  type: 'navigate',
                  url: link.href
                }, '*');
              }
            });
          `;
          iframe.contentDocument.body.appendChild(script);
        }
      } catch (e) {
        // Cross-origin restriction, fallback to default behavior
        console.log('Could not inject navigation handler:', e);
      }
    };

    const iframe = iframeRef.current;
    if (iframe) {
      iframe.addEventListener('load', handleIframeLoad);
      return () => iframe.removeEventListener('load', handleIframeLoad);
    }
  }, [iframeKey]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === 'navigate') {
        // Convert absolute URL to relative path
        const url = new URL(event.data.url);
        const relativePath = url.pathname;
        
        // Update iframe src to the new path
        setCurrentUrl(relativePath);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const handleRefresh = () => {
    setIframeKey(prev => prev + 1);
  };

  const handleOpenExternal = () => {
    window.open(currentUrl, '_blank');
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-2 border-b bg-muted/50">
        <div className="flex items-center gap-2">
          <h2 className="text-sm font-medium">{title}</h2>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleRefresh}
            title="Refresh"
          >
            <RotateCw className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenExternal}
            title="Open in new tab"
          >
            <ExternalLink className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <iframe
        ref={iframeRef}
        key={iframeKey}
        src={currentUrl}
        className="flex-1 w-full border-0"
        title={title}
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  );
}