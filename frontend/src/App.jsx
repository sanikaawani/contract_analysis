import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import AnalysisPage from './pages/AnalysisPage';
import RiskReportPage from './pages/RiskReportPage';
import AboutPage from './pages/AboutPage';
import { fetchSampleContracts, analyzeContractText } from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [activeReport, setActiveReport] = useState(null);
  const [initializing, setInitializing] = useState(true);

  // Pre-load default sample analysis so user immediately sees a live report on first click
  useEffect(() => {
    fetchSampleContracts()
      .then(async (samples) => {
        if (samples && samples.length > 0) {
          try {
            const defaultAnalysis = await analyzeContractText(
              samples[0].text,
              samples[0].title,
              samples[0].contract_type
            );
            setActiveReport(defaultAnalysis);
          } catch (e) {
            console.error("Default analysis init error:", e);
          }
        }
      })
      .catch(err => console.error("Initial samples fetch error:", err))
      .finally(() => setInitializing(false));
  }, []);

  const handleAnalysisComplete = (reportData) => {
    setActiveReport(reportData);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-blue-600 selection:text-white">
      {/* Top Navigation */}
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        hasActiveReport={!!activeReport}
      />

      {/* Main Page Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activePage === 'home' && (
          <HomePage setActivePage={setActivePage} />
        )}

        {activePage === 'upload' && (
          <UploadPage
            onAnalysisComplete={handleAnalysisComplete}
            setActivePage={setActivePage}
          />
        )}

        {activePage === 'analysis' && (
          <AnalysisPage activeReport={activeReport} />
        )}

        {activePage === 'report' && (
          <RiskReportPage
            activeReport={activeReport}
            setActivePage={setActivePage}
          />
        )}

        {activePage === 'about' && (
          <AboutPage />
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
