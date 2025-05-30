export default function DevelopersPage() {
  return (
    <div className="prose prose-neutral dark:prose-invert max-w-none">
      <h1 className="text-4xl font-bold mb-6 mt-8 text-foreground">🛠️ Developer Documentation</h1>
      
      <p className="text-lg text-muted-foreground mb-8">
        Welcome to the developer documentation for the Latency Recorder project. This section provides detailed technical information for contributors working on different aspects of the project.
      </p>

      <div className="grid gap-6 md:grid-cols-3 mt-8">
        <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-3">🔧 Hardware</h2>
          <p className="text-muted-foreground">
            Circuit design, component selection, PCB layout, and manufacturing guidelines for the Latency Recorder hardware.
          </p>
        </div>

        <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-3">💻 Firmware</h2>
          <p className="text-muted-foreground">
            Rust embedded development, AVR HAL library usage, serial protocols, and performance optimization for the Arduino firmware.
          </p>
        </div>

        <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-3">📊 Data Analytics</h2>
          <p className="text-muted-foreground">
            Data format specifications, analysis pipelines, statistical methods, and visualization techniques for latency data.
          </p>
        </div>
      </div>

      <div className="mt-12 p-6 bg-muted/50 rounded-lg">
        <h2 className="text-2xl font-semibold mb-4">Getting Started</h2>
        <p className="mb-4">
          Choose your area of expertise from the sections above to access detailed documentation, setup guides, and best practices.
        </p>
        <p>
          All developer documentation is actively being expanded. If you have specific questions or would like to contribute documentation, please join our <a href="https://discord.gg/47mBnvJM" className="text-primary hover:underline">Discord community</a> or open an issue on <a href="https://github.com/JasperVanDenBosch/latency-recorder" className="text-primary hover:underline">GitHub</a>.
        </p>
      </div>
    </div>
  );
}