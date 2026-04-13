import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './i18n';

export default function App() {
  const { t, i18n } = useTranslation();

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === 'en' ? 'es' : 'en');
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-surface overflow-x-hidden">
        {/* Navigation Bar */}
        <header className="bg-navy text-white py-4 px-6 shadow-md flex justify-between items-center">
          <div className="text-2xl font-bold tracking-wide">
            <Link to="/">LegalClear.</Link>
          </div>
          <div className="flex space-x-6 items-center font-medium">
            <Link to="/results/demo" className="hover:text-teal transition-colors">Results Demo</Link>
            <Link to="/subscribe" className="hover:text-teal transition-colors">Pricing</Link>
            <button 
              onClick={toggleLanguage}
              className="bg-teal px-4 py-2 rounded-full shadow hover:bg-opacity-80 transition-all font-semibold text-sm"
            >
              {i18n.language === 'en' ? 'ESPAÑOL' : 'ENGLISH'}
            </button>
          </div>
        </header>

        {/* Main Content Area Routing */}
        <main className="flex-grow flex flex-col w-full px-4 sm:px-6 lg:px-8 py-10 max-w-7xl mx-auto">
          <Suspense fallback={<div className="animate-pulse flex space-x-4">Loading application...</div>}>
            <Routes>
              <Route path="/" element={<UploadPage t={t} />} />
              <Route path="/processing/:sessionId" element={<ProcessingPage t={t} />} />
              <Route path="/results/:documentId" element={<ResultsPage t={t} />} />
              <Route path="/subscribe" element={<SubscriptionPage t={t} />} />
            </Routes>
          </Suspense>
        </main>

        <footer className="footer bg-white border-t border-border_color p-6 text-center text-sm text-gray-500 mt-10">
          <p>© 2026 LegalClear. Not a law firm. {t('welcome')}</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

/* Stubs for the 4 primary Routes pending deeper implementation */
function UploadPage({ t }) {
  return (
    <div className="w-full max-w-3xl mx-auto mt-10 bg-white shadow-xl rounded-2xl p-8 border border-border_color">
       <h1 className="text-4xl font-extrabold text-navy text-center mb-4 leading-tight">{t('welcome')}</h1>
       
       <div className="flex flex-col items-center justify-center border-2 border-dashed border-teal rounded-xl p-12 bg-surface hover:bg-teal hover:bg-opacity-10 transition-colors cursor-pointer group">
         <svg className="w-16 h-16 text-teal mb-4 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
         <h3 className="text-xl font-bold text-navy">{t('drag_drop')}</h3>
         <p className="text-gray-500 mt-2">{t('paste_text')}</p>
       </div>
    </div>
  );
}

function ProcessingPage({ t }) {
  return <div className="text-center pt-24"><div className="text-2xl font-bold animate-pulse text-teal">{t('processing')}</div></div>;
}

function ResultsPage({ t }) {
  return <div className="bg-white shadow p-8 rounded-xl border border-red_flag"><h1 className="text-2xl font-bold text-navy">{t('risk_report')} Tab Architecture Pending Implementation</h1></div>;
}

function SubscriptionPage({ t }) {
  return <div className="bg-white shadow p-8 rounded-xl border border-teal text-center"><h1 className="text-4xl font-bold text-navy mb-4">Pricing</h1><button className="bg-navy text-white px-8 py-3 rounded text-xl font-bold transform hover:scale-105 transition-transform">{t('unlock')}</button></div>;
}
