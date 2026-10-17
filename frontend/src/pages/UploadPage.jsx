import React, { useState, useEffect } from 'react';
import {
  UploadCloud, FileText, Sparkles, Check, AlertCircle,
  FileCode, Layers, ArrowRight, RefreshCw, FileUp
} from 'lucide-react';
import { analyzeContractFile, analyzeContractText, fetchSampleContracts } from '../services/api';

export default function UploadPage({ onAnalysisComplete, setActivePage }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [contractText, setContractText] = useState('');
  const [contractTitle, setContractTitle] = useState('Master Service Agreement');
  const [contractType, setContractType] = useState('Service Agreement');
  const [sampleContracts, setSampleContracts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch preloaded sample contracts
  useEffect(() => {
    fetchSampleContracts()
      .then(data => {
        setSampleContracts(data);
        if (data.length > 0 && !contractText) {
          // Default load the first sample
          setContractText(data[0].text);
          setContractTitle(data[0].title);
          setContractType(data[0].contract_type);
        }
      })
      .catch(err => console.error("Error loading samples:", err));
  }, []);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      setContractTitle(file.name.replace(/\.[^/.]+$/, ""));
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setContractTitle(file.name.replace(/\.[^/.]+$/, ""));
    }
  };

  const loadSample = (sample) => {
    setSelectedFile(null);
    setContractText(sample.text);
    setContractTitle(sample.title);
    setContractType(sample.contract_type);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      let result;
      if (selectedFile) {
        result = await analyzeContractFile(selectedFile, contractTitle, contractType);
      } else if (contractText.trim()) {
        result = await analyzeContractText(contractText, contractTitle, contractType);
      } else {
        throw new Error("Please upload a file or paste contract text to proceed.");
      }

      onAnalysisComplete(result);
      setActivePage('report');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 py-6">
      
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-white">
          Upload & Audit Commercial Contract
        </h1>
        <p className="text-xs text-slate-400 max-w-xl mx-auto">
          Upload any legal contract (.pdf, .docx, .txt) or test with authentic preloaded Indian commercial agreements.
        </p>
      </div>

      {/* 1-Click Sample Contracts Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>1-Click Test: Preloaded Indian Agreements</span>
          </span>
          <span className="text-[11px] text-slate-500 font-medium">Select to auto-populate</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2.5">
          {sampleContracts.map((sample, idx) => {
            const isSelected = !selectedFile && contractType === sample.contract_type;
            return (
              <button
                key={idx}
                type="button"
                onClick={() => loadSample(sample)}
                className={`p-3 rounded-xl text-left border text-xs transition-all flex flex-col justify-between space-y-2 ${
                  isSelected
                    ? 'bg-blue-600/20 border-blue-500 text-white shadow-md shadow-blue-500/10'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
              >
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-blue-400 uppercase tracking-wider block">
                    Sample {idx + 1}
                  </span>
                  <div className="font-bold text-xs truncate text-slate-200">
                    {sample.contract_type}
                  </div>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">
                  {sample.filename}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Upload Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Metadata Controls: Title & Contract Type */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-5 bg-slate-900/80 border border-slate-800 rounded-2xl">
          <div>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
              Contract Title / Document Identifier
            </label>
            <input
              type="text"
              value={contractTitle}
              onChange={(e) => setContractTitle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="e.g. Master Service Agreement 2024"
              required
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
              Target Contract Type
            </label>
            <select
              value={contractType}
              onChange={(e) => setContractType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="Service Agreement">1. Service Agreement (MSA)</option>
              <option value="Vendor Agreement">2. Vendor Agreement</option>
              <option value="Employment Agreement">3. Employment Agreement</option>
              <option value="Non-Disclosure Agreement (NDA)">4. Non-Disclosure Agreement (NDA)</option>
              <option value="Supply Agreement">5. Commercial Supply Agreement</option>
              <option value="Auto-Detect">Auto-Detect / General Contract</option>
            </select>
          </div>
        </div>

        {/* Drag and Drop Zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`p-8 border-2 border-dashed rounded-2xl text-center transition-all flex flex-col items-center justify-center space-y-3 cursor-pointer ${
            dragActive
              ? 'border-blue-500 bg-blue-500/10'
              : selectedFile
              ? 'border-emerald-500/50 bg-emerald-500/5'
              : 'border-slate-800 bg-slate-900/50 hover:border-slate-700'
          }`}
          onClick={() => document.getElementById('file-upload-input').click()}
        >
          <input
            id="file-upload-input"
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="w-12 h-12 rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20 flex items-center justify-center">
            {selectedFile ? <FileText className="w-6 h-6 text-emerald-400" /> : <UploadCloud className="w-6 h-6" />}
          </div>

          {selectedFile ? (
            <div className="space-y-1">
              <span className="text-xs font-bold text-emerald-400 block font-mono">
                Selected File: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
              </span>
              <p className="text-[11px] text-slate-400">Click or drop another file to replace</p>
            </div>
          ) : (
            <div className="space-y-1">
              <p className="text-xs font-bold text-slate-200">
                Drag and drop your contract here, or <span className="text-blue-400 underline">browse computer</span>
              </p>
              <p className="text-[11px] text-slate-500">
                Supports PDF, Microsoft Word (.docx), and plain text (.txt) files
              </p>
            </div>
          )}
        </div>

        {/* Text Area (Fallback & Direct Editor) */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Or Edit / Paste Raw Contract Text Directly
            </label>
            {selectedFile && (
              <button
                type="button"
                onClick={() => setSelectedFile(null)}
                className="text-[11px] text-amber-400 hover:underline"
              >
                Clear file and switch to text editor
              </button>
            )}
          </div>

          <textarea
            rows={10}
            value={contractText}
            onChange={(e) => {
              setSelectedFile(null);
              setContractText(e.target.value);
            }}
            disabled={!!selectedFile}
            className={`w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 text-xs text-slate-200 font-mono focus:outline-none focus:border-blue-500 transition-colors leading-relaxed ${
              selectedFile ? 'opacity-40 cursor-not-allowed' : ''
            }`}
            placeholder="Contract text will appear here when loaded or pasted..."
          />
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-4 bg-red-950/40 border border-red-900/60 rounded-xl flex items-center space-x-3 text-red-300 text-xs">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center space-x-2 px-8 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 text-white shadow-xl shadow-blue-600/30 hover:opacity-95 active:scale-95 disabled:opacity-50 transition-all"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Executing NLP Pipelines & ML Models...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Execute Complete Contract Risk Analysis</span>
                <ArrowRight className="w-4 h-4 ml-1" />
              </>
            )}
          </button>
        </div>

      </form>

    </div>
  );
}
