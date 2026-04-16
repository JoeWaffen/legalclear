import { useState } from 'react';
import { Link } from 'react-router-dom';
import { AlertOctagon, CheckCircle2, AlertTriangle, FileText, Settings, ShieldAlert, FileCheck, MessageSquare, Menu, Home, Upload, BarChart2, Bell } from 'lucide-react';

export default function AnalysisDashboard() {
  const [activeTab, setActiveTab] = useState('summary');
  const [healthScore, setHealthScore] = useState(72);

  return (
    <div className="min-h-screen bg-background flex flex-col md:flex-row">
      
      {/* Sidebar - Zinc 900 */}
      <div className="w-full md:w-20 lg:w-64 bg-zinc-900 border-r border-white/5 flex flex-col">
        <div className="h-16 flex items-center justify-center lg:justify-start lg:px-6 border-b border-white/5">
          <span className="font-display font-bold text-xl text-white hidden lg:block">LegalClear</span>
          <ScaleIcon className="w-8 h-8 text-blue-500 lg:hidden" />
        </div>
        <div className="flex-1 py-6 flex flex-col gap-2 px-3">
          <SidebarLink icon={<Home />} label="Home" to="/" />
          <SidebarLink icon={<Upload />} label="Upload" to="/upload" />
          <SidebarLink icon={<BarChart2 />} label="Dashboard" active to="/dashboard" />
          <SidebarLink icon={<Settings />} label="Settings" to="#" />
        </div>
      </div>

      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Header - Glassmorphism */}
        <header className="h-16 flex items-center justify-between px-6 bg-background/50 backdrop-blur-md border-b border-white/10 shrink-0 z-10 relative">
          <div className="flex items-center gap-4">
            <div className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold tracking-wider border border-blue-500/20 uppercase hidden sm:block">
              Residential Lease Agreement
            </div>
          </div>
          <div className="flex flex-row items-center gap-4">
            <button className="text-gray-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-medium text-sm">
              JD
            </div>
          </div>
        </header>

        {/* Scrollable Main Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 relative">
          
          <div className="mb-8 pr-12">
            <h1 className="text-4xl md:text-5xl font-display font-bold mb-3 tracking-tight">123 Main St. Lease.pdf</h1>
            <p className="text-gray-400 flex items-center gap-2">
              Analyzed today <span className="w-1 h-1 rounded-full bg-gray-600"></span> High Complexity
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            
            {/* Nav Tabs */}
            <div className="lg:col-span-1 space-y-2">
              <TabButton active={activeTab === 'summary'} onClick={() => setActiveTab('summary')} icon={<FileText />} label="Summary & Rights" />
              <TabButton active={activeTab === 'risk'} onClick={() => setActiveTab('risk')} icon={<ShieldAlert />} label="Risk Scanner" alertCount={3} />
              <TabButton active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} icon={<MessageSquare />} label="Ask AI Question" />
            </div>

            {/* Content Cards */}
            <div className="lg:col-span-3">
              <div className="bg-zinc-900/50 backdrop-blur-sm border border-white/5 hover:border-blue-500/50 transition-colors duration-500 min-h-[500px] rounded-2xl p-6 md:p-8 relative overflow-hidden shadow-2xl">
                {activeTab === 'summary' && <SummaryView />}
                {activeTab === 'risk' && <RiskView score={healthScore} />}
                {activeTab === 'chat' && <ChatView />}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ScaleIcon(props) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path>
    </svg>
  );
}

function SidebarLink({ icon, label, active, to }) {
  return (
    <Link to={to} className={`flex items-center gap-3 w-full p-3 rounded-xl transition-all ${active ? 'bg-blue-600/10 text-blue-500' : 'text-gray-500 hover:bg-white/5 hover:text-gray-300'}`}>
      <div className={`w-6 h-6 flex justify-center items-center ${active ? 'opacity-100' : 'opacity-60'}`}>
        {icon}
      </div>
      <span className="font-medium hidden lg:block">{label}</span>
    </Link>
  );
}

function TabButton({ active, onClick, icon, label, alertCount }) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all font-medium text-left
        ${active ? 'bg-gradient-to-tr from-blue-600 to-indigo-500 text-white shadow-lg shadow-blue-500/25' : 'bg-zinc-900/30 text-gray-400 hover:bg-zinc-800 hover:text-white border border-transparent'}
      `}
    >
      <div className="flex items-center gap-3">
        <div className={`w-5 h-5 ${active ? 'opacity-100' : 'opacity-60'}`}>
          {icon}
        </div>
        {label}
      </div>
      {alertCount && (
        <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${active ? 'bg-white text-blue-600' : 'bg-red-500/20 text-red-500'}`}>
          {alertCount}
        </span>
      )}
    </button>
  );
}

function RadialProgress({ percentage }) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;
  
  let colorClass = "text-green-500";
  if (percentage < 80) colorClass = "text-yellow-500";
  if (percentage < 60) colorClass = "text-red-500";

  return (
    <div className="relative w-32 h-32 flex items-center justify-center">
      <svg className="w-full h-full transform -rotate-90">
        {/* Background track */}
        <circle cx="64" cy="64" r="45" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-zinc-800" />
        {/* Progress bar */}
        <circle 
          cx="64" cy="64" r="45" stroke="currentColor" strokeWidth="8" fill="transparent" 
          className={`${colorClass} transition-all duration-1000 ease-out`}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-display font-bold">{percentage}</span>
        <span className="text-[10px] text-gray-400 uppercase tracking-widest font-bold">Health</span>
      </div>
    </div>
  );
}

function SummaryView() {
  return (
    <div className="space-y-8 animate-slide-up">
      <div>
        <h2 className="text-2xl font-bold mb-4 font-display">Plain Language Summary</h2>
        <p className="text-gray-300 text-lg leading-relaxed">
          This is a standard residential lease agreement between you (the Tenant) and ABC Management (the Landlord) for the property at 123 Main St. You are agreeing to pay <strong className="text-white">$2,000 per month</strong> for a period of 12 months starting on May 1st, 2026. You are responsible for all utilities except water and trash collection.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-zinc-800/30 border border-green-500/20 rounded-xl p-6 hover:border-green-500/40 transition-colors">
          <h3 className="text-lg font-bold text-green-400 flex items-center gap-2 mb-4 font-display">
            <CheckCircle2 className="w-5 h-5" /> Your Key Rights
          </h3>
          <ul className="space-y-3 text-gray-300">
            <li className="flex items-start gap-2"><span className="text-green-500 mt-1">•</span> Right to peaceful enjoyment of the property.</li>
            <li className="flex items-start gap-2"><span className="text-green-500 mt-1">•</span> Landlord must provide 24 hours notice before entering.</li>
            <li className="flex items-start gap-2"><span className="text-green-500 mt-1">•</span> Right to a functional heating and plumbing system.</li>
          </ul>
        </div>
        
        <div className="bg-zinc-800/30 border border-blue-500/20 rounded-xl p-6 hover:border-blue-500/40 transition-colors">
          <h3 className="text-lg font-bold text-blue-400 flex items-center gap-2 mb-4 font-display">
            <FileCheck className="w-5 h-5" /> Important Obligations
          </h3>
          <ul className="space-y-3 text-gray-300">
            <li className="flex items-start gap-2"><span className="text-blue-500 mt-1">•</span> Rent is due on the 1st, late after the 5th.</li>
            <li className="flex items-start gap-2"><span className="text-blue-500 mt-1">•</span> No pets allowed without written consent.</li>
            <li className="flex items-start gap-2"><span className="text-blue-500 mt-1">•</span> Must notify landlord of maintenance issues within 48h.</li>
          </ul>
        </div>
      </div>
      
      <div className="pt-4 flex justify-end">
         <button className="btn-primary" onClick={() => alert("Downloading PDF Report...")}>Generate PDF Report</button>
      </div>
    </div>
  );
}

function RiskView({ score }) {
  return (
    <div className="space-y-6 animate-slide-up">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-6">
        <div className="flex-1">
          <h2 className="text-3xl font-display font-bold mb-2">Risk Scanner</h2>
          <p className="text-gray-400">Our AI has flagged clauses that are heavily one-sided or highly unusual.</p>
        </div>
        
        {/* Gamified Radical Progress Bar */}
        <div className="flex items-center gap-4 bg-zinc-800/40 p-4 rounded-2xl border border-white/5">
          <RadialProgress percentage={score} />
          <div className="flex flex-col gap-1">
             <div className="text-sm font-medium text-gray-300">3 Risks Found</div>
             <div className="text-xs text-gray-500">Requires review before signing</div>
             <button onClick={() => alert("Opening advanced Risk Details modal...")} className="text-xs text-blue-400 font-bold uppercase tracking-wider mt-2 hover:text-blue-300 text-left">View Details</button>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <RiskItem 
          level="red" 
          title="Uncapped Rent Acceleration" 
          quote="Upon default, landlord may accelerate and demand the entire remaining balance of the lease immediately."
          explanation="If you are late on rent once, the landlord could legally demand the rest of the year's rent all at once. This is highly aggressive."
          action="Negotiate to strike this clause or limit the penalty to late fees."
        />

        <RiskItem 
          level="red" 
          title="Personal Guarantee Implied" 
          quote="Tenant guarantees performance unconditionally regardless of LLC or corporate shielding."
          explanation="Even if you sign this for an LLC, they can come after your personal bank accounts and house if the LLC breaks the lease."
          action="Refuse to sign a personal guarantee if this is purely a commercial/LLC transaction."
        />

        <RiskItem 
          level="yellow" 
          title="Auto-Renewal Notice Window" 
          quote="Lease automatically renews for one year unless written notice is given 90 days prior to end."
          explanation="90 days is an unusually long notice period. Most leases only require 30 to 60 days."
          action="Set an aggressive calendar reminder, or ask to change it to 30 days."
        />
      </div>
    </div>
  );
}

function RiskItem({ level, title, quote, explanation, action }) {
  const isRed = level === 'red';
  const colorClass = isRed ? 'text-red-400' : 'text-yellow-400';
  const borderClass = isRed ? 'border-red-500/30' : 'border-yellow-500/30';
  const bgClass = isRed ? 'bg-red-500/5' : 'bg-yellow-500/5';
  const Icon = isRed ? AlertOctagon : AlertTriangle;

  return (
    <div className={`p-6 rounded-xl border ${borderClass} ${bgClass} relative overflow-hidden transition-all hover:bg-zinc-800/50`}>
      <div className={`absolute top-0 left-0 w-1 h-full ${isRed ? 'bg-red-500' : 'bg-yellow-500'}`}></div>
      <div className="flex items-start gap-4">
        <Icon className={`w-6 h-6 mt-1 flex-shrink-0 ${colorClass}`} />
        <div>
          <h3 className={`text-lg font-bold mb-2 ${colorClass}`}>{title}</h3>
          <p className="text-sm font-mono bg-black/40 text-gray-300 p-3 rounded border border-white/5 mb-4 border-l-4 border-l-zinc-600">
            "{quote}"
          </p>
          <p className="text-gray-300 mb-3"><strong className="text-white">Why it matters:</strong> {explanation}</p>
          <p className="text-gray-300"><strong className="text-white">What to do:</strong> {action}</p>
        </div>
      </div>
    </div>
  );
}

function ChatView() {
  const [messages, setMessages] = useState([
    { role: 'user', content: 'Can the landlord enter my apartment without telling me first?' },
    { role: 'ai', content: 'According to Section 4.b of your lease, the landlord must provide you with at least 24 hours written notice before entering the apartment, EXCEPT in the case of an emergency (like a fire or burst pipe). \n\nIf they enter without notice for non-emergencies, they are violating the lease.' }
  ]);
  const [inputVal, setInputVal] = useState('');
  
  const handleSend = () => {
    if(!inputVal.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: inputVal }]);
    setInputVal('');
    setTimeout(() => {
       setMessages(prev => [...prev, { role: 'ai', content: "Our AI is analyzing the document for context regarding your question. In a full production environment, this query acts as a real-time websocket stream from the FastAPI /process endpoint." }]);
    }, 800);
  };

  return (
    <div className="flex flex-col h-[500px] animate-slide-up">
      <div className="mb-6">
        <h2 className="text-3xl font-display font-bold mb-2">Ask LegalClear AI</h2>
        <p className="text-gray-400">Ask any specific question about the document text.</p>
      </div>

      <div className="flex-1 rounded-xl p-2 overflow-y-auto space-y-6 mb-4">
        {messages.map((msg, idx) => (
          msg.role === 'user' ? (
            <div key={idx} className="flex gap-4 justify-end items-end">
              <div className="bg-zinc-800 text-gray-200 p-4 rounded-2xl rounded-tr-sm max-w-[80%] border border-white/5 shadow-md">
                {msg.content}
              </div>
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white text-xs font-bold shrink-0 shadow-lg shadow-blue-500/20">
                JD
              </div>
            </div>
          ) : (
            <div key={idx} className="flex gap-4 items-end">
              <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0 border border-white/10">
                <ShieldAlert className="w-4 h-4 text-white" />
              </div>
              <div className="bg-gradient-to-tr from-blue-600/10 to-indigo-500/10 border border-blue-500/20 p-5 rounded-2xl rounded-tl-sm max-w-[85%] shadow-md">
                <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                  {msg.content}
                </p>
              </div>
            </div>
          )
        ))}
      </div>

      <div className="relative mt-2">
        <input 
          type="text" 
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question..." 
          className="w-full bg-zinc-900 border border-white/10 rounded-xl py-4 pl-5 pr-14 text-white outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all shadow-inner"
        />
        <button onClick={handleSend} className="btn-primary absolute right-2 top-2 p-2 rounded-lg h-[calc(100%-16px)] w-10 flex cursor-pointer items-center justify-center shadow-none hover:shadow-lg">
          <svg className="w-5 h-5 -ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </button>
      </div>
    </div>
  );
}
