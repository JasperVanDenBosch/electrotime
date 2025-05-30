import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'API Documentation - ElectroTime',
  description: 'Complete API reference for the Latency Recorder project',
};

export default function ApiDocsPage() {
  return (
    <div className="prose prose-neutral dark:prose-invert max-w-none">
      <h1 className="text-4xl font-bold mb-6 mt-8 text-foreground">📚 API Documentation</h1>
      
      <p className="text-lg text-muted-foreground mb-8">
        Complete API reference documentation for all components of the Latency Recorder project.
      </p>

      <div className="grid gap-6 md:grid-cols-2 mt-8">
        <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-3">🦀 Rust Firmware API</h2>
          <p className="text-muted-foreground mb-4">
            Low-level firmware documentation for the Arduino-based latency recorder.
          </p>
          <div className="space-y-3">
            <a 
              href="/docs-api/firmware/latreclib/" 
              target="_blank"
              className="block p-3 bg-muted rounded hover:bg-muted/80 transition-colors no-underline"
            >
              <h3 className="font-semibold text-foreground">latreclib</h3>
              <p className="text-sm text-muted-foreground">
                Core library with bit manipulation functions and hardware abstractions
              </p>
            </a>
          </div>
          <Link 
            href="/developers/hardware"
            className="inline-block mt-4 text-primary hover:underline"
          >
            View Hardware Development Guide →
          </Link>
        </div>

        <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-3">🎯 Flutter GUI API</h2>
          <p className="text-muted-foreground mb-4">
            Complete API reference for the cross-platform desktop application.
          </p>
          <div className="space-y-3">
            <a 
              href="/docs-api/gui/" 
              target="_blank"
              className="block p-3 bg-muted rounded hover:bg-muted/80 transition-colors no-underline"
            >
              <h3 className="font-semibold text-foreground">Full API Reference</h3>
              <p className="text-sm text-muted-foreground">
                All classes, widgets, and utilities with interactive search
              </p>
            </a>
          </div>
          <Link 
            href="/developers/firmware"
            className="inline-block mt-4 text-primary hover:underline"
          >
            View GUI Development Guide →
          </Link>
        </div>
      </div>

      <div className="mt-12 p-6 bg-muted/50 rounded-lg">
        <h2 className="text-2xl font-semibold mb-4">🔧 Generating Documentation</h2>
        <p className="mb-4">
          The API documentation is auto-generated from source code comments. To regenerate:
        </p>
        <pre className="bg-zinc-800 text-zinc-300 p-4 rounded-lg overflow-x-auto">
          <code>{`# From the project root
./generate-docs.sh

# Or manually:
# Rust docs
cd firmware/latreclib && cargo doc --no-deps

# Flutter docs
cd gui && dart doc`}</code>
        </pre>
      </div>

      <div className="mt-8 p-6 bg-muted/50 rounded-lg">
        <h2 className="text-2xl font-semibold mb-4">📝 Documentation Standards</h2>
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Rust Documentation</h3>
            <p className="text-muted-foreground">
              Use triple-slash comments (<code>///</code>) for public items. Include examples using 
              <code>```rust</code> code blocks within doc comments.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Flutter Documentation</h3>
            <p className="text-muted-foreground">
              Use triple-slash comments (<code>///</code>) for public APIs. Follow 
              <a href="https://dart.dev/guides/language/effective-dart/documentation" className="text-primary hover:underline ml-1" target="_blank">
                Effective Dart
              </a> 
              &nbsp;documentation guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}