import { FileSearch, ShieldCheck, FileCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="min-h-screen pt-16 flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background blobs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full mix-blend-screen filter blur-3xl opacity-50 animate-blob"></div>
      <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-teal-500/20 rounded-full mix-blend-screen filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full animate-slide-up">
        <div className="text-center space-y-8">
          <div className="inline-flex items-center px-4 py-2 rounded-full glass-panel text-sm text-primary mb-4 border-primary/20">
            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse-slow"></span>
            AI-Powered Legal Clarity
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight max-w-4xl mx-auto leading-tight">
            Understand legal documents <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-teal-400">
              without a law degree.
            </span>
          </h1>
          
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-gray-400 leading-relaxed font-light">
            Upload any contract, lease, or court form. Our AI instantly explains what it means, highlights hidden risks, and guides you step-by-step.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
            <Link to="/upload" className="btn-primary flex items-center gap-2 text-lg px-8 py-4 w-full sm:w-auto justify-center shadow-primary/20">
              Upload Document
              <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </Link>
            <Link to="/dashboard" className="btn-secondary w-full sm:w-auto text-center text-lg px-8 py-4">
              View Sample Analysis
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24">
          <FeatureCard 
            icon={<FileSearch className="h-8 w-8 text-primary" />}
            title="Plain Language Summaries"
            description="We break down dense legalese into simple, actionable summaries so you know exactly what you are agreeing to."
          />
          <FeatureCard 
            icon={<ShieldCheck className="h-8 w-8 text-teal-400" />}
            title="Smart Risk Scanning"
            description="Automatically flags unusual or one-sided clauses with red and yellow warnings, protecting your interests."
          />
          <FeatureCard 
            icon={<FileCheck className="h-8 w-8 text-blue-400" />}
            title="Step-by-Step Form Guides"
            description="Need to file a small claims suit? We give you exact instructions on what to write in every box."
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="glass-card p-8 transition-transform hover:-translate-y-2 duration-300">
      <div className="h-14 w-14 rounded-xl bg-white/5 flex items-center justify-center mb-6 border border-white/10">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white mb-3">{title}</h3>
      <p className="text-gray-400 leading-relaxed">{description}</p>
    </div>
  );
}
