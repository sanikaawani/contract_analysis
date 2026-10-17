import React from 'react';
import {
  Scale, ShieldAlert, Cpu, FileText, ArrowRight, CheckCircle2,
  AlertTriangle, UploadCloud, Layers, Sparkles, Building, Database, Zap
} from 'lucide-react';

export default function HomePage({ setActivePage }) {
  const contractTypes = [
    {
      name: "1. Service Agreement (MSA)",
      desc: "Cloud, consulting, and software development engagements. Detects uncapped liabilities and evergreen lock-ins.",
      badge: "High Risk Traps"
    },
    {
      name: "2. Vendor Agreement",
      desc: "Procurement & IT supplies. Identifies payment withholding and Section 15 MSMED 45-day violations.",
      badge: "Cashflow Risks"
    },
    {
      name: "3. Employment Agreement",
      desc: "Executive hiring & engineering contracts. Flags void Section 27 non-competes and bond penalty sums.",
      badge: "Labor Laws"
    },
    {
      name: "4. Non-Disclosure Agreement (NDA)",
      desc: "Confidentiality & trade secrets. Catches perpetual indefinite terms and lack of standard exclusions.",
      badge: "IP Exposure"
    },
    {
      name: "5. Commercial Supply Agreement",
      desc: "Manufacturing and distribution agreements. Audits territorial exclusivity and 5%/day delay penalties.",
      badge: "Operational Risk"
    }
  ];

  const riskCategories = [
    { title: "Automatic Renewal", desc: "Evergreen clauses locking SMBs into multi-year recurring obligations." },
    { title: "Payment Terms", desc: "Violations of 45-day statutory MSMED payment ceilings and usurious interest." },
    { title: "Liability Clauses", desc: "Uncapped consequential damages exposing SMBs to existential financial ruin." },
    { title: "Penalty Clauses", desc: "Disproportionate liquidated damages violating Section 74 Indian Contract Act." },
    { title: "Termination Clauses", desc: "Unilateral termination for convenience without compensation for work done." },
    { title: "Confidentiality Clauses", desc: "Perpetual obligations without public domain or legal process carve-outs." },
    { title: "Non-Compete Clauses", desc: "Post-termination restraints rendered legally void under Section 27." },
    { title: "Restrictive Clauses", desc: "Expropriation of SMB preexisting background IP and extreme non-solicitation." }
  ];

  const nlpTechniques = [
    "Sentence & Word Tokenization",
    "Stop Word Filtering with Legal Negation Protection",
    "Porter vs Lancaster Stemmer Comparison",
    "WordNet POS-Aware Lemmatization",
    "Penn Treebank POS Tagging & Modal Mandate Extraction",
    "Syntactic Regexp Chunking (NP, VP, PP)",
    "Named Entity Recognition (Org, Dates, Money, Duration, Person)",
    "Bag of Words (CountVectorizer)",
    "N-Gram Analysis (1-grams, 2-grams, 3-grams)",
    "WordNet Synonym & Taxonomical Expansion",
    "Word2Vec Continuous Semantic Embeddings",
    "Word Sense Disambiguation (Lesk Algorithm)"
  ];

  return (
    <div className="space-y-16 py-8">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-slate-900 via-slate-900/90 to-slate-950 border border-slate-800 p-8 sm:p-12 shadow-2xl">
        <div className="absolute -top-32 -right-32 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Academic Final Year NLP & Legal-Tech Project</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            AI-Based Contract Risk Analysis & Clause Detection System for SMBs
          </h1>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
            Empowering Small and Medium-Sized Businesses (SMBs) with automated Natural Language Processing to detect predatory clauses, quantify contractual risks under the <strong className="text-white">Indian Contract Act 1872</strong>, and generate actionable renegotiation strategies.
          </p>

          <div className="flex flex-wrap gap-4 pt-2">
            <button
              onClick={() => setActivePage('upload')}
              className="flex items-center space-x-2 px-6 py-3 rounded-xl text-sm font-bold bg-blue-600 text-white hover:bg-blue-500 shadow-lg shadow-blue-600/30 active:scale-95 transition-all"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Scan Your Contract Now</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>

            <button
              onClick={() => setActivePage('analysis')}
              className="flex items-center space-x-2 px-6 py-3 rounded-xl text-sm font-bold bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 active:scale-95 transition-all"
            >
              <Cpu className="w-4 h-4 text-blue-400" />
              <span>Explore NLP Workbench</span>
            </button>
          </div>
        </div>
      </section>

      {/* Contract Types Supported */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl font-bold text-white">5 Primary Commercial Contract Types</h2>
          <p className="text-xs text-slate-400">
            Trained and tuned on authentic Indian commercial agreements, highlighting risks faced by vendors and SMB service providers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {contractTypes.map((c, idx) => (
            <div key={idx} className="p-5 bg-slate-900/80 border border-slate-800 rounded-2xl hover:border-slate-700 transition-all flex flex-col justify-between space-y-3 group hover:scale-[1.02]">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400 block mb-1">
                  {c.badge}
                </span>
                <h3 className="text-sm font-bold text-white group-hover:text-blue-300 transition-colors">
                  {c.name}
                </h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                  {c.desc}
                </p>
              </div>
              <button
                onClick={() => setActivePage('upload')}
                className="text-xs font-semibold text-blue-400 flex items-center space-x-1 hover:text-blue-300 pt-2"
              >
                <span>Load Sample</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* 8 Risk Categories */}
      <section className="p-8 bg-slate-900/60 border border-slate-800 rounded-3xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
              <ShieldAlert className="w-6 h-6 text-red-400" />
              <span>8 Core Clause Risk Categories</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Multi-class machine learning classifiers and legal heuristics evaluate every clause across these standard risk verticals.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {riskCategories.map((r, idx) => (
            <div key={idx} className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
              <div className="flex items-center space-x-2 text-slate-200">
                <span className="w-2 h-2 rounded-full bg-red-400" />
                <h4 className="text-xs font-bold">{r.title}</h4>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                {r.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* NLP Pipeline Overview */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl font-bold text-white flex items-center justify-center space-x-2">
            <Layers className="w-6 h-6 text-blue-400" />
            <span>Comprehensive NLP Experiments & Techniques</span>
          </h2>
          <p className="text-xs text-slate-400">
            Practically implemented, mathematically evaluated, and integrated into the real-time contract processing workflow.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {nlpTechniques.map((tech, idx) => (
            <div key={idx} className="p-3.5 bg-slate-900 border border-slate-800 rounded-xl flex items-start space-x-2.5">
              <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded font-mono text-[10px] font-bold shrink-0 mt-0.5">
                {idx + 1}
              </span>
              <span className="text-xs text-slate-300 font-medium">
                {tech}
              </span>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
