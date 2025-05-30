import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Hackathon Resources - Latency Recorder',
  description: 'Documentation and resources for the Timing Matters Hackathon',
};

export default function HackathonIndexPage() {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold mb-4">Hackathon Resources</h1>
      <p className="text-lg text-muted-foreground">
        Select a topic from the sidebar to get started.
      </p>
    </div>
  );
}