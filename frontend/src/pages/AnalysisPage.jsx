import React from 'react';
import NLPWorkbench from '../components/NLPWorkbench';
import { Cpu } from 'lucide-react';

export default function AnalysisPage({ activeReport }) {
  const initialSnippet = activeReport?.raw_text || (
    activeReport?.clauses?.map(c => c.clause_text).slice(0, 3).join("\n\n") || ""
  );

  return (
    <div className="space-y-6 py-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Cpu className="w-6 h-6 text-blue-400" />
            <span>Deep NLP Experiments & Linguistic Analysis</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Practical implementation & visual exploration of all 13 NLP techniques: Tokenization, Stemmers, Lemmatizer, POS, Chunking, NER, BoW, N-Grams, WordNet, Word2Vec, and Lesk WSD.
          </p>
        </div>
      </div>

      <NLPWorkbench
        initialText={initialSnippet}
        initialAnalysis={activeReport}
      />
    </div>
  );
}
