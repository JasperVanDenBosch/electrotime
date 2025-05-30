import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Sidebar } from '@/components/Sidebar';
import { Navbar } from '@/components/Navbar';
import { getNavigation } from '@/lib/markdown';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ElectroTime Documentation',
  description: 'Open-source Arduino-based device for measuring stimulus presentation latency',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const navigation = getNavigation();

  return (
    <html lang="en" className="dark">
      <body className={inter.className} suppressHydrationWarning>
        <div className="flex flex-col h-screen">
          <div className="w-full bg-background border-b">
            <div className="container mx-auto px-8 py-4 flex justify-center">
              <img 
                src="/electrotime/electrotime.svg" 
                alt="ElectroTime" 
                className="h-12 w-auto"
              />
            </div>
          </div>
          <Navbar />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar navigation={navigation} />
            <main className="flex-1 overflow-auto bg-background">
              <div className="container max-w-5xl mx-auto px-8 py-8">
                {children}
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}