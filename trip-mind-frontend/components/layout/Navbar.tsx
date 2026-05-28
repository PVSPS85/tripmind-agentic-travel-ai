import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full bg-surface/80 backdrop-blur-md border-b border-border">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo / Brand */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-8 h-8 rounded-full bg-primary-soft flex items-center justify-center text-primary font-display font-bold text-sm transition-transform group-hover:scale-105">
              TM
            </div>
            <span className="font-display font-bold text-xl tracking-tight text-foreground">
              TripMind AI
            </span>
          </Link>

          {/* Nav Actions */}
          <div className="flex items-center space-x-6">
            <Link href="/plan" className="text-sm font-medium text-muted hover:text-foreground transition-colors">
              New Trip
            </Link>
          </div>

        </div>
      </div>
    </nav>
  );
}