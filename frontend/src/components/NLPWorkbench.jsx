import React, { useState } from 'react';
import {
  Scissors, Type, Filter, Cpu, Layers, Tag,
  Binary, FileSpreadsheet, Search, Sparkles, BookOpen, GitCompare
} from 'lucide-react';
import EntityBadge from './EntityBadge';
import { runNLPExperiment } from '../services/api';

export default function NLPWorkbench({ initialText = '', initialAnalysis = null }) {
  const [activeTab, setActiveTab] = useState('preprocessing');
  const [customText, setCustomText] = useState(
    initialText ||
    "This Agreement shall automatically renew for successive terms of 3 (three) years each unless Apex Tech Solutions Pvt Ltd provides written notice within 180 days prior to the Effective Date 15th October 2024. The Service Provider shall indemnify Customer for a penalty sum of INR 5,00,000."
  );
  const [nlpData, setNlpData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [queryWord, setQueryWord] = useState('indemnify');
  const [wsdWord, setWsdWord] = useState('consideration');

  // Trigger custom experiment
  const handleRunExperiment = async () => {
    try {
      setLoading(true);
      const res = await runNLPExperiment(customText, 'all', queryWord);
      setNlpData(res);
    } catch (err) {
      alert('Error running NLP experiment: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Run on mount if no initial data
  React.useEffect(() => {
    handleRunExperiment();
  }, []);

  const tabs = [
    { id: 'preprocessing', label: '1. Preprocessing & Stemming', icon: Scissors },
    { id: 'syntax', label: '2. POS Tagging & Chunking', icon: Layers },
    { id: 'ner', label: '3. Named Entity Recognition (NER)', icon: Tag },
    { id: 'vectors', label: '4. BoW, TF-IDF & N-Grams', icon: Binary },
    { id: 'semantics', label: '5. Word2Vec, WordNet & WSD', icon: Sparkles }
  ];

  return (
    <div className="space-y-6">
      
      {/* NLP Workbench Header & Custom Text Editor */}
      <div className="p-6 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Cpu className="w-5 h-5 text-blue-400" />
              <span>Interactive NLP Laboratory & Feature Explorer</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Live inspection of all 13 NLP algorithms applied to contract clauses. Edit text below to test dynamically.
            </p>
          </div>
          
          <button
            onClick={handleRunExperiment}
            disabled={loading}
            className="flex items-center space-x-2 px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white hover:bg-blue-500 active:scale-95 disabled:opacity-50 transition-all self-start sm:self-auto"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Processing Pipeline...' : 'Re-Run NLP Pipeline'}</span>
          </button>
        </div>

        <div>
          <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
            Test Contract Snippet
          </label>
          <textarea
            rows={3}
            value={customText}
            onChange={(e) => setCustomText(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs text-slate-200 font-mono focus:outline-none focus:border-blue-500 transition-colors resize-y"
            placeholder="Paste any legal clause or contract excerpt to analyze..."
          />
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {tabs.map((t) => {
          const Icon = t.icon;
          const isActive = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Preprocessing & Morphology */}
      {activeTab === 'preprocessing' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Tokenization */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Type className="w-4 h-4 text-blue-400" />
              <span>1. Sentence & Word Tokenization</span>
            </h3>
            
            {nlpData?.tokenization && (
              <div className="space-y-3">
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1">
                  <span className="text-[11px] font-bold text-slate-400">
                    Sentence Tokenizer ({nlpData.tokenization.sentence_count} Sentences Detected):
                  </span>
                  <div className="space-y-1 mt-1">
                    {nlpData.tokenization.sentences.map((s, idx) => (
                      <div key={idx} className="text-xs text-slate-300 font-serif bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                        <span className="font-mono text-blue-400 mr-2 font-bold">[{idx + 1}]</span>
                        {s}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                  <span className="text-[11px] font-bold text-slate-400">
                    Word Tokens ({nlpData.tokenization.word_count} Tokens):
                  </span>
                  <div className="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto">
                    {nlpData.tokenization.words.map((w, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-slate-800 border border-slate-700 text-slate-300 rounded font-mono text-[11px]">
                        {w}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Stop Words Filtering */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Filter className="w-4 h-4 text-amber-400" />
              <span>2. Stop Word Removal (Legal Preserved Negations)</span>
            </h3>
            
            {nlpData?.stopwords && (
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs text-slate-400 px-1">
                  <span>Original: <strong className="text-white">{nlpData.stopwords.original_count}</strong></span>
                  <span>Filtered: <strong className="text-emerald-400">{nlpData.stopwords.filtered_count}</strong></span>
                  <span>Removed: <strong className="text-amber-400">{nlpData.stopwords.removed_stopwords.length}</strong></span>
                </div>

                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-[11px] font-bold text-amber-400">Removed Stopwords:</span>
                  <div className="flex flex-wrap gap-1 max-h-32 overflow-y-auto">
                    {nlpData.stopwords.removed_stopwords.map((sw, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-amber-950/40 text-amber-300 border border-amber-800/40 rounded text-[10px] font-mono">
                        {sw}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-[11px] font-bold text-emerald-400">Retained Informative Legal Tokens:</span>
                  <div className="flex flex-wrap gap-1 max-h-32 overflow-y-auto">
                    {nlpData.stopwords.filtered_tokens.map((ft, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-emerald-950/40 text-emerald-300 border border-emerald-800/40 rounded text-[10px] font-mono">
                        {ft}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Stemmer Comparison: Porter vs Lancaster */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4 md:col-span-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <GitCompare className="w-4 h-4 text-purple-400" />
                <span>3 & 4. Morphological Analysis: Porter Stemmer vs. Lancaster Stemmer Comparison</span>
              </h3>
              <span className="text-xs text-slate-400">
                Lancaster employs heavier rule-based truncation compared to Porter.
              </span>
            </div>

            {nlpData?.stemming?.comparison && (
              <div className="overflow-x-auto max-h-80 border border-slate-800 rounded-xl">
                <table className="w-full text-left text-xs">
                  <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold border-b border-slate-800">
                    <tr>
                      <th className="p-3">Original Legal Word</th>
                      <th className="p-3">Porter Stem</th>
                      <th className="p-3">Lancaster Stem</th>
                      <th className="p-3">Stemming Variance</th>
                      <th className="p-3">Reduction Behavior</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono">
                    {nlpData.stemming.comparison.map((item, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/40">
                        <td className="p-2.5 font-bold text-slate-200">{item.word}</td>
                        <td className="p-2.5 text-blue-400">{item.porter_stem}</td>
                        <td className="p-2.5 text-purple-400">{item.lancaster_stem}</td>
                        <td className="p-2.5">
                          {item.is_different ? (
                            <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded text-[10px]">
                              Morphological Divergence
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded text-[10px]">
                              Identical Stem
                            </span>
                          )}
                        </td>
                        <td className="p-2.5 text-slate-400 text-[11px]">{item.reduction_type}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Lemmatization */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4 md:col-span-2">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <BookOpen className="w-4 h-4 text-emerald-400" />
              <span>5. WordNet POS-Aware Lemmatization</span>
            </h3>

            {nlpData?.lemmatization && (
              <div className="flex flex-wrap gap-2 max-h-60 overflow-y-auto">
                {nlpData.lemmatization.map((item, idx) => (
                  <div key={idx} className="flex items-center space-x-2 px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs">
                    <span className="font-bold text-slate-200 font-mono">{item.word}</span>
                    <span className="text-slate-500 font-mono text-[10px]">({item.pos_tag})</span>
                    <span className="text-slate-600">➔</span>
                    <span className="font-bold text-emerald-400 font-mono">{item.lemma}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}

      {/* Tab 2: Syntactic Structure & Grammar */}
      {activeTab === 'syntax' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* POS Tagging */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <Tag className="w-4 h-4 text-indigo-400" />
                <span>6. Part-of-Speech (POS) Tagging (Penn Treebank)</span>
              </h3>
            </div>

            {nlpData?.pos_tagging && (
              <div className="space-y-4">
                
                {/* Modal Obligations Alert */}
                {nlpData.pos_tagging.modal_obligations?.length > 0 && (
                  <div className="p-3 bg-indigo-950/30 border border-indigo-800/40 rounded-xl">
                    <span className="text-xs font-bold text-indigo-300 block mb-1">
                      Detected Modal Verbs (Legal Obligations/Mandates):
                    </span>
                    <div className="flex gap-1.5">
                      {nlpData.pos_tagging.modal_obligations.map((m, idx) => (
                        <span key={idx} className="px-2.5 py-0.5 bg-indigo-500/20 text-indigo-200 border border-indigo-500/40 rounded font-mono text-xs font-bold uppercase">
                          {m}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tagged tokens list */}
                <div className="max-h-72 overflow-y-auto space-y-1.5 p-3 bg-slate-950 rounded-xl border border-slate-800">
                  {nlpData.pos_tagging.tagged_tokens.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between text-xs py-1 border-b border-slate-900">
                      <span className="font-mono font-bold text-slate-200">{item.word}</span>
                      <div className="flex items-center space-x-2">
                        <span className="px-1.5 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 rounded font-mono text-[10px] font-bold">
                          {item.tag}
                        </span>
                        <span className="text-[11px] text-slate-400 truncate max-w-[180px]">{item.description}</span>
                      </div>
                    </div>
                  ))}
                </div>

              </div>
            )}
          </div>

          {/* Regexp Chunking */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Layers className="w-4 h-4 text-blue-400" />
              <span>7. Syntactic Chunking (NP, VP, PP Regexp Parser)</span>
            </h3>

            {nlpData?.chunking && (
              <div className="space-y-4">
                
                {/* Legal Obligations Chunks */}
                {nlpData.chunking.chunks.legal_obligations?.length > 0 && (
                  <div className="p-3 bg-red-950/30 border border-red-900/40 rounded-xl space-y-1">
                    <span className="text-xs font-bold text-red-300 block">Legal Obligation Chunks:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {nlpData.chunking.chunks.legal_obligations.map((chunk, idx) => (
                        <span key={idx} className="px-2.5 py-1 bg-red-500/10 text-red-300 border border-red-500/30 rounded font-mono text-xs">
                          {chunk}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Noun Phrases */}
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-[11px] font-bold text-blue-400">Noun Phrases (NP):</span>
                  <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto">
                    {nlpData.chunking.chunks.noun_phrases.map((chunk, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-blue-950/40 text-blue-300 border border-blue-800/40 rounded font-mono text-[11px]">
                        {chunk}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Prepositional Phrases */}
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-[11px] font-bold text-purple-400">Prepositional Phrases (PP):</span>
                  <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto">
                    {nlpData.chunking.chunks.prepositional_phrases.map((chunk, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-purple-950/40 text-purple-300 border border-purple-800/40 rounded font-mono text-[11px]">
                        {chunk}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Bracketed Parse Tree */}
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1">
                  <span className="text-[11px] font-bold text-slate-400">Chunk Parse Tree:</span>
                  <pre className="text-[10px] text-slate-400 font-mono overflow-x-auto whitespace-pre-wrap max-h-28">
                    {nlpData.chunking.tree_representation}
                  </pre>
                </div>

              </div>
            )}
          </div>

        </div>
      )}

      {/* Tab 3: Named Entity Recognition */}
      {activeTab === 'ner' && (
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl space-y-6">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Tag className="w-4 h-4 text-emerald-400" />
              <span>8. Named Entity Recognition (NER) & Legal Metadata Extraction</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Extracts Organizations, Key Dates, Financial Terms / Amounts, Durations, and Person Names.
            </p>
          </div>

          {nlpData?.ner && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              
              {/* Organizations */}
              <div className="p-4 bg-slate-950 border border-indigo-900/30 rounded-xl space-y-2">
                <div className="flex items-center space-x-2 text-indigo-400">
                  <span className="text-xs font-bold uppercase">1. Organization Names</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {nlpData.ner.organizations?.length > 0 ? (
                    nlpData.ner.organizations.map((org, idx) => (
                      <EntityBadge key={idx} type="organizations" value={org} />
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">None detected</span>
                  )}
                </div>
              </div>

              {/* Dates */}
              <div className="p-4 bg-slate-950 border border-emerald-900/30 rounded-xl space-y-2">
                <div className="flex items-center space-x-2 text-emerald-400">
                  <span className="text-xs font-bold uppercase">2. Key Dates</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {nlpData.ner.dates?.length > 0 ? (
                    nlpData.ner.dates.map((d, idx) => (
                      <EntityBadge key={idx} type="dates" value={d} />
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">None detected</span>
                  )}
                </div>
              </div>

              {/* Money Amounts */}
              <div className="p-4 bg-slate-950 border border-amber-900/30 rounded-xl space-y-2">
                <div className="flex items-center space-x-2 text-amber-400">
                  <span className="text-xs font-bold uppercase">3. Financial Exposure / Amounts</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {nlpData.ner.money_amounts?.length > 0 ? (
                    nlpData.ner.money_amounts.map((m, idx) => (
                      <EntityBadge key={idx} type="money_amounts" value={m} />
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">None detected</span>
                  )}
                </div>
              </div>

              {/* Contract Durations */}
              <div className="p-4 bg-slate-950 border border-purple-900/30 rounded-xl space-y-2">
                <div className="flex items-center space-x-2 text-purple-400">
                  <span className="text-xs font-bold uppercase">4. Contract Durations & Notice Windows</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {nlpData.ner.contract_durations?.length > 0 ? (
                    nlpData.ner.contract_durations.map((dur, idx) => (
                      <EntityBadge key={idx} type="contract_durations" value={dur} />
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">None detected</span>
                  )}
                </div>
              </div>

              {/* Person Names */}
              <div className="p-4 bg-slate-950 border border-blue-900/30 rounded-xl space-y-2">
                <div className="flex items-center space-x-2 text-blue-400">
                  <span className="text-xs font-bold uppercase">5. Signatories & Person Names</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {nlpData.ner.person_names?.length > 0 ? (
                    nlpData.ner.person_names.map((p, idx) => (
                      <EntityBadge key={idx} type="person_names" value={p} />
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">None detected</span>
                  )}
                </div>
              </div>

            </div>
          )}
        </div>
      )}

      {/* Tab 4: Vectors, BoW & N-Grams */}
      {activeTab === 'vectors' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Bag of Words */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Binary className="w-4 h-4 text-blue-400" />
              <span>9. Bag of Words (CountVectorizer Matrix)</span>
            </h3>

            {nlpData?.bow && (
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs text-slate-400 px-1">
                  <span>Vocabulary Size: <strong className="text-white">{nlpData.bow.total_vocab_size}</strong></span>
                  <span>Active Non-Zero Features: <strong className="text-blue-400">{nlpData.bow.active_features_count}</strong></span>
                </div>

                <div className="overflow-y-auto max-h-60 border border-slate-800 rounded-xl p-2 bg-slate-950 font-mono text-xs">
                  <div className="grid grid-cols-2 gap-2">
                    {nlpData.bow.word_frequencies.map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between p-1.5 bg-slate-900 rounded border border-slate-800">
                        <span className="text-slate-300 font-bold">{item.word}</span>
                        <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded text-[10px] font-bold">
                          {item.count}x
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* N-Gram Analysis */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <FileSpreadsheet className="w-4 h-4 text-amber-400" />
              <span>10. N-Gram Analysis (1-grams, 2-grams, 3-grams)</span>
            </h3>

            {nlpData?.ngrams && (
              <div className="space-y-4">
                
                {/* Bigrams */}
                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-amber-400">Top Bigrams (2-grams):</span>
                  <div className="flex flex-wrap gap-1.5">
                    {nlpData.ngrams.bigrams?.map((bg, idx) => (
                      <span key={idx} className="px-2.5 py-1 bg-amber-950/30 text-amber-300 border border-amber-800/40 rounded-lg text-xs font-mono">
                        {bg.ngram} <strong className="text-white ml-1">({bg.frequency})</strong>
                      </span>
                    ))}
                  </div>
                </div>

                {/* Trigrams */}
                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-purple-400">Top Trigrams (3-grams):</span>
                  <div className="flex flex-wrap gap-1.5">
                    {nlpData.ngrams.trigrams?.map((tg, idx) => (
                      <span key={idx} className="px-2.5 py-1 bg-purple-950/30 text-purple-300 border border-purple-800/40 rounded-lg text-xs font-mono">
                        {tg.ngram} <strong className="text-white ml-1">({tg.frequency})</strong>
                      </span>
                    ))}
                  </div>
                </div>

              </div>
            )}
          </div>

        </div>
      )}

      {/* Tab 5: Semantic Space: Word2Vec, WordNet, WSD */}
      {activeTab === 'semantics' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* WordNet Synonym Expansion */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <BookOpen className="w-4 h-4 text-emerald-400" />
                <span>11. WordNet Synonyms</span>
              </h3>
            </div>

            <div className="flex space-x-2">
              <input
                type="text"
                value={queryWord}
                onChange={(e) => setQueryWord(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200 font-mono"
                placeholder="Query word..."
              />
              <button
                onClick={handleRunExperiment}
                className="px-3 py-1 bg-emerald-600 text-white rounded-lg text-xs font-bold"
              >
                Find
              </button>
            </div>

            {nlpData?.wordnet_expansion && (
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
                <div className="text-slate-300">
                  <strong className="text-emerald-400">Definition:</strong> {nlpData.wordnet_expansion.primary_definition}
                </div>
                <div className="space-y-1">
                  <strong className="text-slate-400 block text-[11px]">Synonym Set:</strong>
                  <div className="flex flex-wrap gap-1">
                    {nlpData.wordnet_expansion.synonyms?.map((syn, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-emerald-950/40 text-emerald-300 border border-emerald-800/40 rounded font-mono text-[10px]">
                        {syn}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Word2Vec Embeddings */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Binary className="w-4 h-4 text-blue-400" />
              <span>12. Word2Vec Semantic Space</span>
            </h3>

            {nlpData?.word2vec && (
              <div className="space-y-3">
                <div className="text-xs text-slate-400">
                  100-dim Skip-Gram embedding similarity to <strong className="text-blue-400">"{nlpData.word2vec.queried_word}"</strong>:
                </div>

                <div className="space-y-1.5 max-h-60 overflow-y-auto">
                  {nlpData.word2vec.similar_terms?.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                      <span className="font-mono text-slate-200 font-bold">{item.word}</span>
                      <span className="font-mono text-blue-400 font-bold">
                        {(item.similarity * 100).toFixed(1)}% Sim
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Word Sense Disambiguation */}
          <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <span>13. Word Sense Disambiguation (Lesk)</span>
            </h3>

            {nlpData?.wsd && (
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
                <div>
                  <span className="text-[11px] font-bold text-slate-400 block">Ambiguous Term:</span>
                  <span className="text-sm font-bold text-purple-300 font-mono">{nlpData.wsd.target_word}</span>
                </div>

                <div className="p-2.5 bg-purple-950/20 border border-purple-900/40 rounded-lg space-y-1">
                  <span className="text-[10px] font-bold text-purple-400 block">Selected Sense via Context Overlap:</span>
                  <span className="font-mono text-xs text-white font-bold">{nlpData.wsd.chosen_sense}</span>
                  <p className="text-[11px] text-slate-300 italic">{nlpData.wsd.definition}</p>
                </div>
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}
