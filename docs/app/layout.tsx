import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Sidebar } from '@/components/Sidebar';
import { MobileSidebar } from '@/components/MobileSidebar';
import { Logo } from '@/components/Logo';
import { Breadcrumb } from '@/components/Breadcrumb';
import { ScrollToTop } from '@/components/ScrollToTop';
import { getNavigation } from '@/lib/markdown';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  metadataBase: new URL('https://electrotime.org'),
  title: 'ElectroTime Documentation - Open Source Latency Recorder',
  description: 'Open-source Arduino-based device for microsecond-precision measurement of stimulus presentation latency in neuroscience and psychology experiments',
  keywords: ['latency recorder', 'arduino', 'neuroscience', 'psychology', 'timing', 'open source', 'stimulus presentation'],
  authors: [{ name: 'Jasper Van Den Bosch' }],
  openGraph: {
    title: 'ElectroTime - Latency Recorder Documentation',
    description: 'Microsecond-precision timing measurements for research',
    type: 'website',
    url: 'https://electrotime.org',
    images: ['/electrotime.svg'],
  },
  twitter: {
    card: 'summary',
    title: 'ElectroTime - Latency Recorder',
    description: 'Open-source timing measurement device for research',
  },
  robots: {
    index: false,
    follow: false,
    nocache: true,
    googleBot: {
      index: false,
      follow: false,
      noimageindex: true,
    },
  },
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
              <div className="flex-1 overflow-auto !mb-4" id="main-content">
                <ScrollToTop />
                <div className="container max-w-[75dvw] max-sm:h-[85dvh] h-[80dvh] mx-auto px-4 md:px-8 pt-0 max-md:pb-8 max-md:pt-0 min-md:pb-4">
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