import React, { useState } from 'react';
import {
  ShieldAlert, Download, FileText, Sparkles, Building2,
  Calendar, IndianRupee, Clock, UserCheck, AlertOctagon,
  Layers, ArrowUpRight, CheckCircle2, ChevronRight, UploadCloud
} from 'lucide-react';
import RiskGauge from '../components/RiskGauge';
import EntityBadge from '../components/EntityBadge';
import ClauseTable from '../components/ClauseTable';
import { CategoryRadarChart, RiskDistributionPieChart, CategoryBarChart } from '../components/Charts';
import { downloadPDFReport } from '../services/api';

export default function RiskReportPage({ activeReport, setActivePage }) {
  const [downloading, setDownloading] = useState(false);

  if (!activeReport) {
    return (
      <div className="max-w-xl mx-auto py-20 text-center space-y-4">
        <div className="w-16 h-16 rounded-3xl bg-slate-900 border border-slate-800 text-slate-500 flex items-center justify-center mx-auto">
          <FileText className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-white">No Contract Analysis Active</h2>
        <p className="text-xs text-slate-400">
          Upload a contract or load one of the authentic sample agreements to generate a comprehensive risk audit report.
        </p>
        <button
          onClick={() => setActivePage('upload')}
          className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl text-xs font-bold bg-blue-600 text-white hover:bg-blue-500 transition-all"
        >
          <UploadCloud className="w-4 h-4" />
          <span>Upload or Choose Sample Contract</span>
        </button>
      </div>
    );
  }

  const handleDownloadPDF = async () => {
    try {
      setDownloading(true);
      await downloadPDFReport(activeReport);
    } catch (err) {
      alert('Error downloading PDF: ' + err.message);
    } finally {
      setDownloading(false);
    }
  };

  const entities = activeReport.entities || {};

  return (
    <div className="space-y-8 py-6">
      
      {/* Top Banner / Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 bg-slate-900 border border-slate-800 rounded-3xl shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 border border-blue-500/20">
              {activeReport.contract_type || 'Commercial Agreement'}
            </span>
            <span className="text-xs text-slate-500">•</span>
            <span className="text-xs text-slate-400 font-mono">
              {activeReport.clause_counts?.total || 0} Clauses Evaluated
            </span>
          </div>
          <h1 className="text-2xl font-extrabold text-white">
            {activeReport.contract_title}
          </h1>
          <p className="text-xs text-slate-400">
            {activeReport.risk_summary_text}
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => setActivePage('analysis')}
            className="flex items-center space-x-1.5 px-4 py-2.5 text-xs font-bold rounded-xl bg-slate-800 text-slate-200 border border-slate-700 hover:bg-slate-700 transition-all"
          >
            <Sparkles className="w-4 h-4 text-blue-400" />
            <span>Open in NLP Lab</span>
          </button>

          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="flex items-center space-x-2 px-5 py-2.5 text-xs font-bold rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-600/30 hover:opacity-95 disabled:opacity-50 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>{downloading ? 'Compiling PDF...' : 'Download PDF Audit Report'}</span>
          </button>
        </div>
      </div>

      {/* Summary Row: Risk Score + Red Flags + Extracted Entities */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Risk Score Gauge Card */}
        <div className="lg:col-span-1">
          <RiskGauge
            score={activeReport.overall_risk_score}
            grade={activeReport.overall_risk_grade}
            badge={activeReport.overall_risk_badge}
          />
        </div>

        {/* Critical Red Flags Box */}
        <div className="lg:col-span-2 p-5 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center space-x-2">
                <AlertOctagon className="w-4 h-4 text-red-400" />
                <span>Critical Red Flags for SMB Review</span>
              </h3>
              <span className="text-[11px] text-slate-400">
                {activeReport.clause_counts?.high_risk || 0} High Risk Traps
              </span>
            </div>

            <div className="space-y-2 max-h-56 overflow-y-auto">
              {activeReport.red_flags?.length > 0 ? (
                activeReport.red_flags.map((rf, idx) => (
                  <div key={idx} className="p-3 bg-red-950/20 border border-red-900/40 rounded-xl space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-red-300">Clause #{rf.clause_id}: {rf.category}</span>
                      <span className="px-2 py-0.5 bg-red-500/20 text-red-200 rounded text-[10px] font-bold uppercase">
                        High Risk
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 font-serif italic">"{rf.snippet}"</p>
                    <p className="text-[11px] text-red-400 font-semibold">{rf.summary}</p>
                  </div>
                ))
              ) : (
                <div className="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl text-xs text-emerald-300 flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>No extreme statutory red flags detected in this agreement.</span>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center">
            <div className="p-2 bg-slate-950 rounded-xl border border-slate-800">
              <span className="text-lg font-bold text-red-400 font-mono">
                {activeReport.clause_counts?.high_risk || 0}
              </span>
              <p className="text-[10px] text-slate-400 uppercase font-semibold">High Severity</p>
            </div>
            <div className="p-2 bg-slate-950 rounded-xl border border-slate-800">
              <span className="text-lg font-bold text-amber-400 font-mono">
                {activeReport.clause_counts?.medium_risk || 0}
              </span>
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Medium Warning</p>
            </div>
            <div className="p-2 bg-slate-950 rounded-xl border border-slate-800">
              <span className="text-lg font-bold text-emerald-400 font-mono">
                {activeReport.clause_counts?.low_risk || 0}
              </span>
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Standard Safe</p>
            </div>
          </div>
        </div>

      </div>

      {/* Extracted Metadata (NER) Section */}
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-3xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <FileText className="w-4 h-4 text-blue-400" />
            <span>Extracted Contract Intelligence & Entities (NER)</span>
          </h3>
          <span className="text-xs text-slate-400">Automated Named Entity Recognition</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
              Parties / Organizations
            </span>
            <div className="flex flex-wrap gap-1.5">
              {entities.organizations?.length > 0 ? (
                entities.organizations.map((org, idx) => (
                  <EntityBadge key={idx} type="organizations" value={org} />
                ))
              ) : (
                <span className="text-xs text-slate-500">None identified</span>
              )}
            </div>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">
              Financial Terms & Amounts
            </span>
            <div className="flex flex-wrap gap-1.5">
              {entities.money_amounts?.length > 0 ? (
                entities.money_amounts.map((m, idx) => (
                  <EntityBadge key={idx} type="money_amounts" value={m} />
                ))
              ) : (
                <span className="text-xs text-slate-500">None identified</span>
              )}
            </div>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-purple-400 uppercase tracking-wider block">
              Durations & Notice Windows
            </span>
            <div className="flex flex-wrap gap-1.5">
              {entities.contract_durations?.length > 0 ? (
                entities.contract_durations.map((dur, idx) => (
                  <EntityBadge key={idx} type="contract_durations" value={dur} />
                ))
              ) : (
                <span className="text-xs text-slate-500">None identified</span>
              )}
            </div>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">
              Key Dates
            </span>
            <div className="flex flex-wrap gap-1.5">
              {entities.dates?.length > 0 ? (
                entities.dates.map((d, idx) => (
                  <EntityBadge key={idx} type="dates" value={d} />
                ))
              ) : (
                <span className="text-xs text-slate-500">None identified</span>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Visual Analytics / Recharts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Category Radar Chart */}
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-2 lg:col-span-1">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Risk Profile Radar (8 Categories)
          </h3>
          <CategoryRadarChart data={activeReport.category_breakdown || []} />
        </div>

        {/* Risk Distribution Donut */}
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-2 lg:col-span-1">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Clause Risk Distribution
          </h3>
          <RiskDistributionPieChart counts={activeReport.clause_counts || {}} />
        </div>

        {/* Category Bar Chart */}
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-2 lg:col-span-1">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Category Severity Scores
          </h3>
          <CategoryBarChart data={activeReport.category_breakdown || []} />
        </div>

      </div>

      {/* Clause Detection Table */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center space-x-2">
              <Layers className="w-5 h-5 text-blue-400" />
              <span>Full Clause Detection & Risk Evaluation Table</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Click any clause to inspect the plain-English AI legal reasoning, Indian statutory grounding, and counter-clause template.
            </p>
          </div>
        </div>

        <ClauseTable clauses={activeReport.clauses || []} />
      </div>

    </div>
  );
}
