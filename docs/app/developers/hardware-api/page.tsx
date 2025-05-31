'use client';

import { Button } from '@/components/ui/button';
import { 
  Globe, 
  Terminal,
  Cpu,
  BookOpen,
  CheckCircle,
  Info,
  AlertCircle,
  Package2,
  Download
} from 'lucide-react';

export default function HardwareApiPage() {
  return (
    <div className="w-full max-w-4xl mx-auto py-8 px-4">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="p-4 bg-orange-100 dark:bg-orange-900 rounded-full">
              <Cpu className="h-12 w-12 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
          <h1 className="text-4xl font-bold">Rust Firmware API Documentation</h1>
          <p className="text-xl text-muted-foreground">
            Complete API reference for firmware crates: latreclib, recorder, and simulator
          </p>
        </div>

        {/* Info Box */}
        <div className="bg-amber-50 dark:bg-amber-950 border border-amber-200 dark:border-amber-800 rounded-lg p-6 space-y-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400 mt-0.5" />
            <div className="space-y-2">
              <h3 className="font-semibold">Important: Download Required for Full Functionality</h3>
              <p className="text-sm text-muted-foreground">
                While the Rust documentation can be viewed online, some features like search and cross-crate 
                references work better when downloaded and viewed locally. We recommend downloading for the 
                best experience.
              </p>
            </div>
          </div>
        </div>

        {/* Access Section */}
        <div className="border rounded-lg p-8 space-y-6 bg-card">
          <div className="text-center space-y-6">
            <div>
              <h2 className="text-2xl font-semibold">Access Documentation</h2>
              <p className="text-muted-foreground mt-2">
                Choose how you'd like to view the Rust firmware API documentation
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                variant="outline"
                className="gap-2"
                onClick={() => window.open('/docs-api/firmware/index.html', '_blank')}
              >
                <Globe className="h-5 w-5" />
                View Online (Limited)
              </Button>
              
              <Button 
                size="lg" 
                className="gap-2"
                onClick={() => window.location.href = '/rust-firmware-docs.zip'}
              >
                <Download className="h-5 w-5" />
                Download Documentation (ZIP)
              </Button>
            </div>
            
            <p className="text-sm text-muted-foreground">
              ZIP size: ~2MB • Contains documentation for available crates
            </p>
          </div>
        </div>

        {/* Crates Overview */}
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold">Available Crates</h2>
          
          <div className="grid gap-4">
            {/* latreclib */}
            <div className="border rounded-lg p-6 space-y-3 bg-card">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h3 className="font-semibold flex items-center gap-2">
                    <Package2 className="h-5 w-5 text-green-600 dark:text-green-400" />
                    latreclib
                    <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 px-2 py-1 rounded">
                      Available
                    </span>
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Core library providing helper functions and abstractions for the latency recorder hardware
                  </p>
                </div>
              </div>
              <div className="text-sm space-y-2">
                <p className="font-medium">Key Features:</p>
                <ul className="space-y-1 ml-4">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Timing utilities for microsecond precision</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>ADC (Analog-to-Digital Converter) abstractions</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Serial communication helpers</span>
                  </li>
                </ul>
              </div>
              <Button 
                variant="outline"
                size="sm"
                className="gap-2"
                onClick={() => window.open('/docs-api/firmware/latreclib/index.html', '_blank')}
              >
                <BookOpen className="h-4 w-4" />
                View Documentation
              </Button>
            </div>

            {/* recorder */}
            <div className="border rounded-lg p-6 space-y-3 bg-card opacity-75">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h3 className="font-semibold flex items-center gap-2">
                    <Package2 className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
                    recorder
                    <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 px-2 py-1 rounded">
                      AVR Target Required
                    </span>
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Main firmware application that runs on the Arduino hardware
                  </p>
                </div>
              </div>
              <div className="text-sm space-y-2">
                <p className="font-medium">Key Features:</p>
                <ul className="space-y-1 ml-4">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Real-time latency measurement</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Serial communication with GUI</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Hardware interrupt handling</span>
                  </li>
                </ul>
              </div>
              <div className="flex items-start gap-2 text-sm text-yellow-600 dark:text-yellow-400">
                <AlertCircle className="h-4 w-4 mt-0.5" />
                <span>Documentation requires AVR toolchain installation</span>
              </div>
            </div>

            {/* simulator */}
            <div className="border rounded-lg p-6 space-y-3 bg-card opacity-75">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h3 className="font-semibold flex items-center gap-2">
                    <Package2 className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
                    simulator
                    <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 px-2 py-1 rounded">
                      AVR Target Required
                    </span>
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Hardware simulator for testing firmware logic without physical Arduino
                  </p>
                </div>
              </div>
              <div className="text-sm space-y-2">
                <p className="font-medium">Key Features:</p>
                <ul className="space-y-1 ml-4">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Simulated hardware environment</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Testing without physical device</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
                    <span>Development and debugging support</span>
                  </li>
                </ul>
              </div>
              <div className="flex items-start gap-2 text-sm text-yellow-600 dark:text-yellow-400">
                <AlertCircle className="h-4 w-4 mt-0.5" />
                <span>Documentation requires AVR toolchain installation</span>
              </div>
            </div>
          </div>
        </div>

        {/* Generate Documentation */}
        <div className="border rounded-lg p-6 space-y-4 bg-muted/30">
          <h3 className="font-semibold flex items-center gap-2">
            <Terminal className="h-5 w-5" />
            Generate Complete Documentation
          </h3>
          <p className="text-sm text-muted-foreground">
            To generate documentation for all crates (including AVR targets):
          </p>
          <pre className="bg-card p-4 rounded-lg overflow-x-auto text-sm">
            <code>{`# Install AVR toolchain (macOS)
brew tap osx-cross/avr
brew install avr-gcc avrdude

# Install Rust AVR target
rustup target add avr-unknown-gnu-atmega328

# Generate all documentation
cd firmware
cargo doc --all --no-deps`}</code>
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
              <span>Complete type signatures and trait bounds</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Module hierarchy navigation</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Source code links</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Search functionality</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Trait implementations</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400 mt-0.5" />
              <span>Cross-crate references</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}