import React, { useState } from 'react';
import { Search, Filter, Sparkles, AlertTriangle, ShieldCheck, ShieldAlert, ChevronRight } from 'lucide-react';
import AIExplanationModal from './AIExplanationModal';

export default function ClauseTable({ clauses = [] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedRisk, setSelectedRisk] = useState('All');
  const [activeClauseForModal, setActiveClauseForModal] = useState(null);

  const categories = ['All', ...new Set(clauses.map(c => c.category))];
  const riskLevels = ['All', 'High', 'Medium', 'Low'];

  const filteredClauses = clauses.filter(c => {
    const matchesSearch = c.clause_text.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          c.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || c.category === selectedCategory;
    const matchesRisk = selectedRisk === 'All' || c.risk_level === selectedRisk;
    return matchesSearch && matchesCategory && matchesRisk;
  });

  return (
    <div className="space-y-4">
      
      {/* Search and Filters Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between p-4 bg-slate-900/80 border border-slate-800 rounded-xl">
        
        {/* Search Input */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search clauses or categories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>

        {/* Category & Risk Filters */}
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>Category: {cat}</option>
            ))}
          </select>

          <select
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-slate-300 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {riskLevels.map(risk => (
              <option key={risk} value={risk}>Risk: {risk}</option>
            ))}
          </select>

        </div>

      </div>

      {/* Table Container */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/70 text-slate-400 font-bold uppercase tracking-wider">
                <th className="py-3.5 px-4 w-12 text-center">#</th>
                <th className="py-3.5 px-4 w-44">Clause Category</th>
                <th className="py-3.5 px-4">Clause Text & Language Triggers</th>
                <th className="py-3.5 px-4 w-28 text-center">Risk Level</th>
                <th className="py-3.5 px-4 w-24 text-center">Confidence</th>
                <th className="py-3.5 px-4 w-32 text-center">AI Guidance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredClauses.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-500 font-medium">
                    No clauses matched your filter criteria.
                  </td>
                </tr>
              ) : (
                filteredClauses.map((clause) => {
                  const isHigh = clause.risk_level === 'High';
                  const isMedium = clause.risk_level === 'Medium';
                  const badgeStyle = isHigh
                    ? 'bg-red-500/10 text-red-400 border-red-500/30'
                    : isMedium
                    ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
                  
                  return (
                    <tr 
                      key={clause.clause_id}
                      className="hover:bg-slate-800/40 transition-colors group cursor-pointer"
                      onClick={() => setActiveClauseForModal(clause)}
                    >
                      <td className="py-3 px-4 text-center font-mono text-slate-500 font-bold">
                        {clause.clause_id}
                      </td>

                      <td className="py-3 px-4">
                        <span className="font-semibold text-slate-200 block">
                          {clause.category}
                        </span>
                        {clause.modal_obligations && clause.modal_obligations.length > 0 && (
                          <span className="text-[10px] text-indigo-400 font-mono">
                            Obligation: {clause.modal_obligations.join(', ')}
                          </span>
                        )}
                      </td>

                      <td className="py-3 px-4 text-slate-300 font-serif leading-relaxed">
                        <div className="line-clamp-2 group-hover:line-clamp-none transition-all">
                          "{clause.clause_text}"
                        </div>
                        {clause.heuristic_flags && clause.heuristic_flags.length > 0 && (
                          <div className="mt-1 flex items-center space-x-1 text-[11px] text-red-400 font-sans">
                            <span className="font-bold">Trigger:</span>
                            <span>{clause.heuristic_flags[0]}</span>
                          </div>
                        )}
                      </td>

                      <td className="py-3 px-4 text-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${badgeStyle}`}>
                          {clause.risk_level}
                        </span>
                      </td>

                      <td className="py-3 px-4 text-center font-mono text-slate-400">
                        {Math.round(clause.confidence * 100)}%
                      </td>

                      <td className="py-3 px-4 text-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setActiveClauseForModal(clause);
                          }}
                          className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30 hover:bg-blue-500/20 active:scale-95 transition-all"
                        >
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>Explain</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Explanation Modal */}
      {activeClauseForModal && (
        <AIExplanationModal
          clause={activeClauseForModal}
          onClose={() => setActiveClauseForModal(null)}
        />
      )}

    </div>
  );
}
