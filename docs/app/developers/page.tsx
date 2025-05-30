import Link from 'next/link';

export default function DevelopersPage() {
  return (
    <div className="prose prose-neutral dark:prose-invert max-w-none">
      <h1 className="text-4xl font-bold mb-6 mt-8 text-foreground">🛠️ Developer Documentation</h1>
      
      <p className="text-lg text-muted-foreground mb-8">
        Welcome to the developer documentation for the Latency Recorder project. This section provides detailed technical information for contributors working on different aspects of the project.
      </p>

      <div className="grid gap-6 md:grid-cols-2 mt-8">
        <Link href="/developers/hardware" className="no-underline">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer h-full">
            <h2 className="text-2xl font-semibold mb-3">🔧 Hardware Development</h2>
            <p className="text-muted-foreground mb-4">
              Work with the Arduino-based hardware and Rust firmware that powers the latency recorder.
            </p>
            <div className="space-y-2 text-sm">
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Firmware:</strong> Rust embedded development for ATmega328P</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Hardware:</strong> Circuit design with TLV2462 op-amp</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Tools:</strong> cargo, avrdude, Arduino IDE</span>
              </p>
            </div>
          </div>
        </Link>

        <Link href="/developers/firmware" className="no-underline">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer h-full">
            <h2 className="text-2xl font-semibold mb-3">💻 GUI Development</h2>
            <p className="text-muted-foreground mb-4">
              Build and enhance the cross-platform Flutter application for device control and data visualization.
            </p>
            <div className="space-y-2 text-sm">
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Framework:</strong> Flutter/Dart for desktop platforms</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Features:</strong> Serial communication, real-time recording</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Platforms:</strong> macOS, Linux, Windows</span>
              </p>
            </div>
          </div>
        </Link>

        <Link href="/developers/data-analytics" className="no-underline">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer h-full">
            <h2 className="text-2xl font-semibold mb-3">📊 Data Analytics</h2>
            <p className="text-muted-foreground mb-4">
              Analyze and visualize timing data to extract meaningful insights from experiments.
            </p>
            <div className="space-y-2 text-sm">
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Analysis:</strong> Python scripts for data processing</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Formats:</strong> CSV data with timestamps and ADC readings</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Visualization:</strong> matplotlib, statistical analysis</span>
              </p>
            </div>
          </div>
        </Link>

        <a href="https://github.com/JasperVanDenBosch/latency-recorder" target="_blank" rel="noopener noreferrer" className="no-underline">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer h-full">
            <h2 className="text-2xl font-semibold mb-3">🌐 Repository & Contribution</h2>
            <p className="text-muted-foreground mb-4">
              Access the source code, submit issues, and contribute to the project on GitHub.
            </p>
            <div className="space-y-2 text-sm">
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>License:</strong> Open source project</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Community:</strong> Join our Discord for discussions</span>
              </p>
              <p className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Contributing:</strong> PRs welcome!</span>
              </p>
            </div>
          </div>
        </a>
      </div>

      <div className="mt-12 space-y-6">
        <div className="p-6 bg-muted/50 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">🚀 Quick Start</h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">For Hardware Developers</h3>
              <pre className="bg-zinc-800 text-zinc-300 p-4 rounded-lg overflow-x-auto">
                <code>{`# Install Rust and AVR target
rustup target add avr-unknown-gnu-atmega328

# Build firmware
cd firmware/recorder
cargo build --release

# Flash to Arduino
avrdude -p atmega328p -c arduino -P /dev/tty.usbserial-* -b 115200 -U flash:w:target/avr-atmega328p/release/recorder.elf:e`}</code>
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">For GUI Developers</h3>
              <pre className="bg-zinc-800 text-zinc-300 p-4 rounded-lg overflow-x-auto">
                <code>{`# Install Flutter dependencies
cd gui
flutter pub get

# Run the application
flutter run -d macos  # or linux, windows

# Build for release
flutter build macos --release`}</code>
              </pre>
            </div>
          </div>
        </div>

        <div className="p-6 bg-muted/50 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">📚 Documentation Generation</h2>
          <p className="mb-4">
            Generate comprehensive API documentation for all components:
          </p>
          <pre className="bg-zinc-800 text-zinc-300 p-4 rounded-lg overflow-x-auto">
            <code>{`# Generate all documentation
./generate-docs.sh

# View generated docs
cd docs && npm run dev`}</code>
          </pre>
        </div>

        <div className="p-6 bg-muted/50 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">🤝 Join the Community</h2>
          <p className="mb-4">
            Connect with other developers and researchers working with the Latency Recorder:
          </p>
          <div className="flex gap-4">
            <a href="https://discord.gg/47mBnvJM" className="text-primary hover:underline">Discord Community</a>
            <span className="text-muted-foreground">•</span>
            <a href="https://github.com/JasperVanDenBosch/latency-recorder/issues" className="text-primary hover:underline">GitHub Issues</a>
          </div>
        </div>
      </div>
    </div>
  );
}