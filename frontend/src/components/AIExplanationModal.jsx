import React, { useState } from 'react';
import { X, Scale, AlertOctagon, CheckCircle2, Copy, Check, Sparkles, Building, ArrowRight } from 'lucide-react';

export default function AIExplanationModal({ clause, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!clause) return null;

  const handleCopyCounter = () => {
    navigator.clipboard.writeText(clause.recommended_counter_clause || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isHigh = clause.risk_level === 'High';
  const isMedium = clause.risk_level === 'Medium';
  const badgeStyle = isHigh ? 'bg-red-500/10 text-red-400 border-red-500/30' : (isMedium ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">AI Clause Legal Risk & Mitigation</h3>
              <p className="text-xs text-slate-400">Clause #{clause.clause_id} • {clause.category}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${badgeStyle}`}>
              {clause.risk_level} Risk ({clause.risk_score}/100)
            </span>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="p-6 space-y-6 overflow-y-auto">
          
          {/* Original Clause Text */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Original Contract Clause</label>
            <div className="p-3.5 bg-slate-950 rounded-xl border border-slate-800 text-sm text-slate-200 font-serif leading-relaxed italic">
              "{clause.clause_text}"
            </div>
          </div>

          {/* Heuristic Trigger Flags */}
          {clause.heuristic_flags && clause.heuristic_flags.length > 0 && (
            <div className="p-3 bg-red-950/30 border border-red-900/50 rounded-xl flex items-start space-x-2.5">
              <AlertOctagon className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-xs font-bold text-red-300 block mb-0.5">Critical Risk Factor:</span>
                <span className="text-xs text-red-200">{clause.heuristic_flags.join(" • ")}</span>
              </div>
            </div>
          )}

          {/* Indian Statutory Grounding */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-indigo-400">
              <Scale className="w-4 h-4" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Indian Legal Statute & Grounding</h4>
            </div>
            <div className="p-4 bg-indigo-950/20 border border-indigo-900/40 rounded-xl space-y-2">
              <div className="text-xs font-bold text-indigo-200">
                {clause.statute}
              </div>
              <div className="text-xs text-slate-300 leading-relaxed">
                {clause.legal_principle}
              </div>
            </div>
          </div>

          {/* SMB Impact Analysis */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-amber-400">
              <Building className="w-4 h-4" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Operational & Financial Impact on SMB</h4>
            </div>
            <div className="p-3.5 bg-amber-950/20 border border-amber-900/40 rounded-xl text-xs text-slate-300 leading-relaxed">
              {clause.sme_impact}
            </div>
          </div>

          {/* Recommended Counter-Clause */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <h4 className="text-xs font-bold uppercase tracking-wider">Recommended Renegotiation Counter-Clause</h4>
              </div>
              <button
                onClick={handleCopyCounter}
                className="flex items-center space-x-1.5 px-2.5 py-1 text-xs font-semibold rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/20 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied!' : 'Copy Template'}</span>
              </button>
            </div>
            <div className="p-4 bg-emerald-950/20 border border-emerald-900/40 rounded-xl text-xs text-emerald-200 font-mono leading-relaxed select-all">
              {clause.recommended_counter_clause}
            </div>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 border-t border-slate-800 bg-slate-950/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-bold rounded-lg bg-slate-800 text-slate-200 hover:bg-slate-700 transition-colors"
          >
            Close Analysis
          </button>
        </div>

      </div>
    </div>
  );
}
