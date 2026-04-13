import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './i18n';

import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import ResultsPage from './pages/ResultsPage';

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
              <Route path="/processing/:documentId" element={<ProcessingPage t={t} />} />
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

function SubscriptionPage({ t }) {
  return <div className="bg-white shadow p-8 rounded-xl border border-teal text-center"><h1 className="text-4xl font-bold text-navy mb-4">Pricing</h1><button className="bg-navy text-white px-8 py-3 rounded text-xl font-bold transform hover:scale-105 transition-transform">{t('unlock')}</button></div>;
}
