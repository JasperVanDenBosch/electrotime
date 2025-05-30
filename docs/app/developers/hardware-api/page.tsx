'use client';

import { useState } from 'react';
import { ApiDocFrame } from '@/components/ApiDocFrame';
import { ApiDocLauncher } from '@/components/ApiDocLauncher';
import { Button } from '@/components/ui/button';
import { ExternalLink, FileText } from 'lucide-react';

export default function HardwareApiPage() {
  const [viewMode, setViewMode] = useState<'inline' | 'external'>('inline');

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex items-center justify-between p-4 border-b">
        <h1 className="text-2xl font-bold">Rust Firmware API Reference</h1>
        <div className="flex gap-2">
          <Button
            variant={viewMode === 'inline' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('inline')}
          >
            <FileText className="h-4 w-4 mr-2" />
            View Inline
          </Button>
          <Button
            variant={viewMode === 'external' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('external')}
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            Open External
          </Button>
        </div>
      </div>
      
      <div className="flex-1">
        {viewMode === 'inline' ? (
          <ApiDocFrame
            basePath="/docs-api/firmware/latreclib/index.html"
            title="Rust Firmware API Documentation"
          />
        ) : (
          <ApiDocLauncher
            docsPath="/docs-api/firmware/latreclib/index.html"
            title="Rust Firmware API Documentation"
            description="Core library documentation with helper functions for bit manipulation and hardware abstraction."
          />
        )}
      </div>
    </div>
  );
}