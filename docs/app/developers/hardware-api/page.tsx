import { ApiRedirect } from '@/components/ApiRedirect';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Hardware API Reference - ElectroTime',
  description: 'Rust API documentation for the latency recorder firmware',
};

export default function HardwareApiPage() {
  return <ApiRedirect path="/api/firmware/latreclib/" />;
}