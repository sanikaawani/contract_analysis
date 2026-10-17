import React from 'react';
import { Scale, BookOpen, ShieldCheck, Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-800 py-10 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Scale className="w-5 h-5 text-blue-500" />
              <span className="font-bold text-base text-white">LexiRisk AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Final Year NLP Engineering Project: AI-Based Contract Risk Analysis and Clause Detection System for Small and Medium-Sized Businesses using Natural Language Processing.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Core NLP Pipeline</h4>
            <ul className="text-xs text-slate-400 space-y-1.5 font-mono">
              <li>Tokenization & Stemming (Porter/Lancaster)</li>
              <li>Penn POS Tagging & Regexp Chunking</li>
              <li>Named Entity Recognition (NER)</li>
              <li>BoW, TF-IDF & Word2Vec Embeddings</li>
              <li>Word Sense Disambiguation (Lesk)</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Indian Statutory Scope</h4>
            <ul className="text-xs text-slate-400 space-y-1.5">
              <li>Indian Contract Act, 1872 (Sec 27, 28, 73, 74)</li>
              <li>MSMED Act, 2006 (Delayed Payments Sec 15-16)</li>
              <li>Arbitration & Conciliation Act, 1996</li>
              <li>Specific Relief Act, 1963</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Contract Types</h4>
            <ul className="text-xs text-slate-400 space-y-1.5">
              <li>1. Master Service Agreement (MSA)</li>
              <li>2. Vendor Procurement Agreement</li>
              <li>3. Employment Agreement & Bond Clauses</li>
              <li>4. Non-Disclosure Agreement (NDA)</li>
              <li>5. Commercial Supply Agreement</li>
            </ul>
          </div>

        </div>

        <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2025 LexiRisk AI. Academic NLP & Legal-Tech Research Project.</p>
          <p className="mt-2 sm:mt-0 flex items-center space-x-1">
            <ShieldCheck className="w-4 h-4 text-blue-400" />
            <span>Built for SMB Legal Empowerment & Contract Transparency</span>
          </p>
        </div>
      </div>
    </footer>
  );
}
