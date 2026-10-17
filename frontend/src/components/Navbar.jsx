import React from 'react';
import { Scale, FileText, Cpu, ShieldAlert, BookOpen, UploadCloud } from 'lucide-react';

export default function Navbar({ activePage, setActivePage, hasActiveReport }) {
  const navItems = [
    { id: 'home', label: 'Home', icon: Scale },
    { id: 'upload', label: 'Upload Contract', icon: UploadCloud },
    { id: 'analysis', label: 'NLP Lab & Workbench', icon: Cpu },
    { id: 'report', label: 'Risk Report', icon: ShieldAlert, highlight: hasActiveReport },
    { id: 'about', label: 'Methodology & ML Benchmarks', icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => setActivePage('home')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <Scale className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-blue-400 bg-clip-text text-transparent">
                  LexiRisk AI
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full">
                  Indian SMB Edition
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">NLP Contract Risk Intelligence</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all duration-150 relative ${
                    isActive
                      ? 'bg-blue-600/10 text-blue-400 border border-blue-500/30 shadow-sm shadow-blue-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                  {item.highlight && !isActive && (
                    <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse ml-1" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Quick CTA button */}
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setActivePage('upload')}
              className="hidden sm:flex items-center space-x-2 px-4 py-2 text-xs font-bold rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-600/20 hover:from-blue-500 hover:to-indigo-500 active:scale-95 transition-all"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Scan Contract</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
