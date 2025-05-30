import { ApiRedirect } from '@/components/ApiRedirect';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'GUI API Reference - ElectroTime',
  description: 'Flutter/Dart API documentation for the latency recorder GUI',
};

export default function GuiApiPage() {
  return <ApiRedirect path="/api/gui/" />;
}