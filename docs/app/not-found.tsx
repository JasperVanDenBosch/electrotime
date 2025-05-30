import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-lg text-muted-foreground mb-8">
        The page you are looking for doesn't exist.
      </p>
      <Link
        href="/"
        className="inline-block px-6 py-3 bg-primary text-primary-foreground rounded-md hover:opacity-90 transition-opacity"
      >
        Go Back Home
      </Link>
    </div>
  );
}