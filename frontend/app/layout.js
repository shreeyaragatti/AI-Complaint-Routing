import './globals.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

function Navbar() {
  const pathname = usePathname();

  const isActive = (path) => {
    if (path === '/' && pathname === '/') return true;
    if (path !== '/' && pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <i className="fas fa-robot"></i>
        <span>AI Complaint Router</span>
      </div>
      <div className="nav-links">
        <Link href="/" className={isActive('/') ? 'active' : ''}>
          <i className="fas fa-home"></i> Home
        </Link>
        <Link href="/submit" className={isActive('/submit') ? 'active' : ''}>
          <i className="fas fa-plus-circle"></i> Submit Complaint
        </Link>
        <Link href="/dashboard" className={isActive('/dashboard') ? 'active' : ''}>
          <i className="fas fa-chart-bar"></i> Dashboard
        </Link>
      </div>
    </nav>
  );
}

export const metadata = {
  title: 'AI Complaint Router',
  description: 'AI-Powered Complaint Prioritization & Smart Routing',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        {children}
        <footer>
          <p>AI Complaint Prioritization & Smart Routing System</p>
        </footer>
      </body>
    </html>
  );
}
