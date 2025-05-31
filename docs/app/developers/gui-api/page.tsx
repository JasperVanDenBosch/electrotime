'use client';

import { Button } from '@/components/ui/button';
import { 
  Download, 
  FolderOpen, 
  Globe, 
  Terminal,
  Package,
  BookOpen,
  CheckCircle,
  Info,
  AlertCircle,
  FileArchive
} from 'lucide-react';

export default function GuiApiPage() {
  const handleDownload = async () => {
    // Create a zip file of the Flutter docs
    const response = await fetch('/api/download-flutter-docs');
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'flutter-dart-api-docs.zip';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  return (
    <div className="w-full max-w-4xl mx-auto py-8 px-4">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="p-4 bg-blue-100 dark:bg-blue-900 rounded-full">
              <Package className="h-12 w-12 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <h1 className="text-4xl font-bold">Flutter/Dart API Documentation</h1>
          <p className="text-xl text-muted-foreground">
            Complete API reference for the Latency Recorder GUI application
          </p>
        </div>

        {/* Info Box */}
        <div className="bg-amber-50 dark:bg-amber-950 border border-amber-200 dark:border-amber-800 rounded-lg p-6 space-y-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400 mt-0.5" />
            <div className="space-y-2">
              <h3 className="font-semibold">Important: Download Required</h3>
              <p className="text-sm text-muted-foreground">
                The Flutter/Dart documentation uses advanced features like search and cross-references 
                that <strong>do not work when served from GitHub Pages</strong>. You must download 
                the documentation and open it locally on your computer for it to function properly.
              </p>
            </div>
          </div>
        </div>

        {/* Download Section */}
        <div className="border rounded-lg p-8 space-y-6 bg-card">
          <div className="text-center space-y-4">
            <h2 className="text-2xl font-semibold">Download Documentation</h2>
            <p className="text-muted-foreground">
              Download the complete Flutter/Dart API documentation package
            </p>
            
            <Button 
              size="lg" 
              className="gap-2"
              onClick={() => window.location.href = '/flutter-dart-docs.zip'}
              disabled={false} // Will be enabled when zip is available
            >
              <Download className="h-5 w-5" />
              Download Documentation (ZIP)
            </Button>
            
            <p className="text-sm text-muted-foreground">
              Size: ~5MB • Contains all API documentation and search index
            </p>
          </div>
        </div>

        {/* Instructions */}
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold">How to Use the Documentation</h2>
          
          <div className="grid gap-6">
            {/* Step 1 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                  1
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold flex items-center gap-2">
                  <Download className="h-4 w-4" />
                  Download the Documentation
                </h3>
                <p className="text-sm text-muted-foreground">
                  Click the "Download Documentation (ZIP)" button above to download the complete 
                  Flutter/Dart API documentation package to your computer.
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                  2
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold flex items-center gap-2">
                  <FileArchive className="h-4 w-4" />
                  Extract the ZIP File
                </h3>
                <p className="text-sm text-muted-foreground">
                  Extract the downloaded ZIP file to a folder on your computer. This will create a 
                  <code className="px-1 py-0.5 bg-muted rounded text-xs">flutter-dart-docs</code> folder 
                  containing all the documentation files.
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                  3
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold flex items-center gap-2">
                  <FolderOpen className="h-4 w-4" />
                  Open index.html
                </h3>
                <p className="text-sm text-muted-foreground">
                  Navigate to the extracted folder and double-click on <code className="px-1 py-0.5 bg-muted rounded text-xs">index.html</code> 
                  to open the documentation in your web browser. All features including search will now work properly.
                </p>
              </div>
            </div>

            {/* Step 4 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold">
                  4
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold">Navigate Libraries</h3>
                <p className="text-sm text-muted-foreground">
                  Once opened locally, use the sidebar to browse through the different libraries:
                </p>
                <ul className="text-sm text-muted-foreground space-y-1 ml-4">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>about</strong> - About page functionality</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>device</strong> - Device connection and control</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>home</strong> - Main application interface</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>main</strong> - Application entry point</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>ports</strong> - Serial port management</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <span><strong>recordbutton</strong> - Recording UI components</span>
                  </li>
                </ul>
              </div>
            </div>

          </div>
        </div>

        {/* Alternative Access */}
        <div className="border rounded-lg p-6 space-y-4 bg-muted/30">
          <h3 className="font-semibold flex items-center gap-2">
            <Terminal className="h-5 w-5" />
            Generate Fresh Documentation
          </h3>
          <p className="text-sm text-muted-foreground">
            To generate the latest documentation from source:
          </p>
          <pre className="bg-card p-4 rounded-lg overflow-x-auto text-sm">
            <code>{`cd gui
dart doc
# Documentation will be generated in doc/api/`}</code>
          </pre>
        </div>

        {/* Features */}
        <div className="border rounded-lg p-6 space-y-4">
          <h3 className="font-semibold flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            Documentation Features
          </h3>
          <div className="grid sm:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Full API reference for all classes and methods</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Interactive search functionality</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Cross-referenced navigation</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Source code links</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Inheritance hierarchies</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Light/dark theme support</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}