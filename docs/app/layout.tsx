import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Sidebar } from '@/components/Sidebar';
import { MobileSidebar } from '@/components/MobileSidebar';
import { Logo } from '@/components/Logo';
import { Breadcrumb } from '@/components/Breadcrumb';
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
        <div className="flex flex-col h-[100dvh]">
          <div className="w-full bg-background border-b">
            <div className="container mx-auto px-8 py-4 flex justify-center relative">
              <MobileSidebar navigation={navigation} />
              <Logo />
            </div>
          </div>
          <div className="flex flex-1 overflow-hidden">
            <div className="hidden md:block">
              <Sidebar navigation={navigation} />
            </div>
            <main className="flex-1 flex flex-col bg-background">
              <div className="sticky top-0 z-10 bg-background border-b">
                <div className="container max-w-5xl mx-auto px-4 md:px-8 py-4">
                  <Breadcrumb />
                </div>
              </div>
              <div className="flex-1 overflow-auto">
                <div className="container max-w-5xl mx-auto px-4 md:px-8 py-8">
                  {children}
                </div>
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}