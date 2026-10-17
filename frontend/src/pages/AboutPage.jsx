import React, { useState, useEffect } from 'react';
import {
  BookOpen, Cpu, Scale, CheckCircle2, BarChart3,
  Layers, Binary, FileSpreadsheet, ShieldAlert, Award
} from 'lucide-react';
import { fetchModelMetrics } from '../services/api';

export default function AboutPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModelMetrics()
      .then(data => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading metrics:", err);
        setLoading(false);
      });
  }, []);

  const nlpDescriptions = [
    {
      num: 1,
      title: "Sentence & Word Tokenization",
      formula: "T = \\{s_1, s_2, ..., s_n\\}, \\quad w_i \\in s_j",
      desc: "Segments raw contractual text into individual clause sentences using punkt/regex boundary detection, followed by lexical word tokenization preserving legal numbering and currency symbols."
    },
    {
      num: 2,
      title: "Stop Word Removal & Legal Negation Guard",
      formula: "W_{clean} = \\{w \\in W \\mid w \\notin Stopwords \\lor w \\in LegalPreserved\\}",
      desc: "Filters out high-frequency non-informative English tokens while strictly preserving legally critical negation modifiers such as 'not', 'without', 'unless', 'except', and 'against'."
    },
    {
      num: 3,
      title: "Porter Stemmer",
      formula: "f_{Porter}: w \\to Stem_{standard}",
      desc: "Applies Martin Porter's 5-phase algorithmic rule engine to strip morphological suffixes (e.g. 'indemnification' -> 'indemnifi', 'terminates' -> 'termin')."
    },
    {
      num: 4,
      title: "Lancaster Stemmer",
      formula: "f_{Lancaster}: w \\to Stem_{aggressive}",
      desc: "Applies Paice/Husk's aggressive iterative truncation rules. Side-by-side benchmarking highlights morphological divergence between Porter and Lancaster."
    },
    {
      num: 5,
      title: "WordNet POS-Aware Lemmatization",
      formula: "Lemma(w, POS) = \\arg\\min_{base} (w \\mid Synset(POS))",
      desc: "Maps Penn Treebank POS tags into WordNet syntactic categories (Noun, Verb, Adjective, Adverb) to accurately restore base dictionary roots (e.g. 'breached' -> 'breach')."
    },
    {
      num: 6,
      title: "Part-of-Speech (POS) Tagging & Modal Mandates",
      formula: "P(T \\mid W) = \\prod P(t_i \\mid t_{i-1}) P(w_i \\mid t_i)",
      desc: "Assigns 36 Penn Treebank tags. Isolates Modal Auxiliaries (MD: 'shall', 'must', 'may') which dictate statutory contractual duties and liabilities."
    },
    {
      num: 7,
      title: "Regexp Syntactic Chunking",
      formula: "NP \\to \\langle DT \\rangle? \\langle JJ.* \\rangle^* \\langle NN.* \\rangle^+, \\quad VP \\to \\langle MD \\rangle? \\langle VB.* \\rangle",
      desc: "Constructs shallow syntactic parse trees identifying Noun Phrases (NP), Verb Phrases (VP), Prepositional Phrases (PP), and mandatory Legal Obligations."
    },
    {
      num: 8,
      title: "Named Entity Recognition (NER)",
      formula: "NER(W) \\to \\{ (e_i, Type_i) \\mid Type \\in \\{ORG, DATE, MONEY, DURATION, PERSON\\} \\}",
      desc: "Custom regex and MaxEnt statistical NER models extract contracting Corporate Entities, Effective Dates, Financial Exposure in INR/₹, Durations, and Signatories."
    },
    {
      num: 9,
      title: "Bag of Words (BoW)",
      formula: "v_{BoW}(d) = [tf(w_1, d), tf(w_2, d), ..., tf(w_{|V|}, d)]",
      desc: "Constructs term-frequency vocabulary vectors representing clause occurrences across a 1,000-dimensional legal dictionary."
    },
    {
      num: 10,
      title: "N-Gram Distribution (1, 2, 3-Grams)",
      formula: "N\\text{-}Gram(k) = (w_i, w_{i+1}, ..., w_{i+k-1})",
      desc: "Captures multi-word legal collocations such as 'liquidated damages', 'hold harmless', and 'perpetually and indefinitely'."
    },
    {
      num: 11,
      title: "WordNet Synonym & Taxonomical Expansion",
      formula: "Synsets(w) \\cup Hypernyms(w)",
      desc: "Expands domain legal search terms with ontological synsets, gloss definitions, and hypernym trees for comprehensive semantic matching."
    },
    {
      num: 12,
      title: "Continuous Word2Vec Embeddings",
      formula: "\\mathcal{L}_{SG} = \\sum_{t=1}^T \\sum_{-c \\le j \\le c, j \\ne 0} \\log P(w_{t+j} \\mid w_t)",
      desc: "Skip-gram continuous neural word vectors trained on contract corpora. Produces 100-dimensional dense semantic representations enabling nearest neighbor search."
    },
    {
      num: 13,
      title: "Word Sense Disambiguation (Lesk Algorithm)",
      formula: "\\hat{s} = \\arg\\max_{s \\in Senses(w)} |Gloss(s) \\cap Context(w)|",
      desc: "Disambiguates polysemous legal terms (e.g. 'consideration' = legal contract value vs mental thought; 'damages' = financial compensation vs physical harm)."
    }
  ];

  return (
    <div className="space-y-12 py-6 max-w-6xl mx-auto">
      
      {/* Title & Overview */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Final Year Project Documentation & Academic Methodology</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          AI-Based Contract Risk Analysis and Clause Detection System
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Comprehensive review of the NLP pipeline, theoretical mathematical formulations, machine learning comparative benchmarks, and Indian statutory grounding under the Indian Contract Act 1872.
        </p>
      </div>

      {/* Dataset & Scope Card */}
      <div className="p-8 bg-slate-900/90 border border-slate-800 rounded-3xl space-y-4 shadow-xl">
        <h2 className="text-lg font-bold text-white flex items-center space-x-2">
          <Award className="w-5 h-5 text-indigo-400" />
          <span>Primary Dataset & Indian Legal Scope</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-1.5">
            <span className="font-bold text-slate-300 block">Dataset Source</span>
            <p className="text-slate-400">
              Legal Indian Contract Clauses Dataset annotated across 5 commercial contract types and 8 statutory risk categories with Low/Medium/High severity tags.
            </p>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-1.5">
            <span className="font-bold text-slate-300 block">5 Contract Verticals</span>
            <p className="text-slate-400">
              Master Service Agreement (MSA), Vendor Procurement, Executive Employment, Non-Disclosure (NDA), and Commercial Supply.
            </p>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 space-y-1.5">
            <span className="font-bold text-slate-300 block">Statutory Grounding</span>
            <p className="text-slate-400">
              Indian Contract Act 1872 (Sec 27 Non-compete void, Sec 73-74 Penalties), MSMED Act 2006 (Sec 15 45-day payment limit), and Arbitration Act 1996.
            </p>
          </div>
        </div>
      </div>

      {/* Machine Learning Model Performance Benchmarks */}
      <div className="p-8 bg-slate-900 border border-slate-800 rounded-3xl space-y-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              <span>Machine Learning Model Evaluation & Comparative Benchmarks</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Stratified 4-Fold Cross Validation comparing traditional NLP + ML algorithms across Feature Spaces (BoW vs TF-IDF vs Word2Vec).
            </p>
          </div>
          {metrics && (
            <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-mono font-bold">
              Production Accuracy: {metrics.best_category_model_metrics?.test_accuracy}%
            </span>
          )}
        </div>

        {/* Benchmarking Table */}
        <div className="overflow-x-auto border border-slate-800 rounded-2xl">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 font-bold border-b border-slate-800">
              <tr>
                <th className="p-3.5">Model & Feature Representation</th>
                <th className="p-3.5 text-center">Mean Accuracy</th>
                <th className="p-3.5 text-center">Mean Precision</th>
                <th className="p-3.5 text-center">Mean Recall</th>
                <th className="p-3.5 text-center">Weighted F1-Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {metrics?.feature_comparison_category?.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="p-3 font-bold text-slate-200">{row.model_feature_combination}</td>
                  <td className="p-3 text-center text-slate-300">{row.mean_accuracy}%</td>
                  <td className="p-3 text-center text-slate-300">{row.mean_precision}%</td>
                  <td className="p-3 text-center text-slate-300">{row.mean_recall}%</td>
                  <td className="p-3 text-center text-emerald-400 font-bold">{row.mean_f1_score}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 13 NLP Techniques Breakdown */}
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Cpu className="w-6 h-6 text-blue-400" />
            <span>Detailed Documentation of all 13 NLP Techniques</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Mathematical foundations and role within the automated contract risk engine.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {nlpDescriptions.map((item) => (
            <div key={item.num} className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-2 hover:border-slate-700 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-blue-400">
                  Technique #{item.num}
                </span>
                <span className="font-mono text-[10px] text-slate-500 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                  NLP Pipeline
                </span>
              </div>
              <h3 className="text-sm font-bold text-white">{item.title}</h3>
              <div className="p-2 bg-slate-950 rounded-lg border border-slate-800 text-[11px] font-mono text-indigo-300 overflow-x-auto">
                {item.formula}
              </div>
              <p className="text-xs text-slate-400 leading-relaxed pt-1">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
