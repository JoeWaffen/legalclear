import { Link, useLocation } from 'react-router-dom';
import { Scale, FileText, LayoutDashboard, Menu } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed w-full z-50 bg-background/80 backdrop-blur-lg border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <Scale className="h-8 w-8 text-primary" />
            <span className="font-display font-bold text-2xl tracking-tight text-white">
              Legal<span className="text-primary">Clear</span>
            </span>
          </div>

          <div className="hidden md:flex space-x-8 items-center">
            <Link 
              to="/" 
              className={`text-sm font-medium transition-colors hover:text-white ${isActive('/') ? 'text-white' : 'text-gray-400'}`}
            >
              Home
            </Link>
            <Link 
              to="/upload" 
              className={`text-sm font-medium transition-colors hover:text-white flex items-center gap-1 ${isActive('/upload') ? 'text-white' : 'text-gray-400'}`}
            >
              <FileText className="w-4 h-4" />
              Upload
            </Link>
            <Link 
              to="/dashboard" 
              className={`text-sm font-medium transition-colors hover:text-white flex items-center gap-1 ${isActive('/dashboard') ? 'text-white' : 'text-gray-400'}`}
            >
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </Link>
            <Link
              to="/eligibility"
              className={`text-sm font-medium transition-colors hover:text-white flex items-center gap-1 ${isActive('/eligibility') ? 'text-white' : 'text-gray-400'}`}
            >
              <Scale className="w-4 h-4" />
              Eligibility
            </Link>
            <Link to="/upload" className="btn-primary text-sm py-2 px-4 shadow-primary/20">
              Get Started
            </Link>
          </div>

          <div className="md:hidden flex items-center">
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-300 hover:text-white p-2"
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
      
      {isMenuOpen && (
        <div className="md:hidden bg-background/95 border-b border-white/10 p-4 animate-fade-in">
          <div className="flex flex-col space-y-4">
            <Link to="/" onClick={() => setIsMenuOpen(false)} className="text-gray-300 hover:text-white">Home</Link>
            <Link to="/upload" onClick={() => setIsMenuOpen(false)} className="text-gray-300 hover:text-white">Upload Document</Link>
            <Link to="/dashboard" onClick={() => setIsMenuOpen(false)} className="text-gray-300 hover:text-white">Dashboard</Link>
            <Link to="/eligibility" onClick={() => setIsMenuOpen(false)} className="text-gray-300 hover:text-white">Eligibility</Link>
          </div>
        </div>
      )}
    </nav>
  );
}
