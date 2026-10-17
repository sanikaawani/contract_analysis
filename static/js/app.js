/**
 * Main Frontend Application Logic for Legal Contract Risk Analyzer
 */

document.addEventListener('DOMContentLoaded', () => {
  setupFileUpload();
  setupAnalyzeAction();
  setupPdfDownload();
});

// Current active analysis state
let currentAnalysisData = null;

function setupFileUpload() {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');

  if (!dropZone || !fileInput) return;

  // Drag-and-drop events
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    }, false);
  });

  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelected(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });
}

async function handleFileSelected(file) {
  const fileNameDisplay = document.getElementById('file-name-display');
  const fileInfo = document.getElementById('file-info');
  const textArea = document.getElementById('contract-text');

  if (!file) return;

  showToast(`Uploading and extracting: ${file.name}...`, 'info');

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    if (data.success && data.metadata) {
      const meta = data.metadata;
      textArea.value = meta.cleaned_text || meta.raw_text;
      fileNameDisplay.innerText = `${meta.filename} (${meta.word_count.toLocaleString()} words)`;
      fileInfo.classList.remove('hidden');

      // Auto-update word count
      const words = textArea.value.trim().split(/\s+/).length;
      document.getElementById('word-count-badge').innerText = `${words.toLocaleString()} words`;

      showToast(`Document extracted successfully! (${words} words)`, 'success');
    } else {
      showToast(data.error || 'Failed to extract text from file', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

function setupAnalyzeAction() {
  const analyzeBtn = document.getElementById('analyze-btn');
  if (!analyzeBtn) return;

  analyzeBtn.addEventListener('click', async () => {
    const textArea = document.getElementById('contract-text');
    const contractType = document.getElementById('contract-type-select').value;
    const modelType = document.getElementById('model-select').value;
    const text = textArea.value.trim();

    if (!text) {
      showToast('Please paste contract text or upload a document first.', 'warning');
      return;
    }

    showToast('Running NLP preprocessing and ML risk classification...', 'info');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `<div class="loader-spinner w-4 h-4 border-2"></div> Analyzing...`;

    try {
      const fileNameEl = document.getElementById('file-name-display');
      const filename = fileNameEl && !fileNameEl.parentElement.classList.contains('hidden')
        ? fileNameEl.innerText.split(' ')[0]
        : 'contract_document.txt';

      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          contract_type: contractType,
          model_type: modelType,
          filename: filename
        })
      });

      const data = await res.json();

      if (data.success) {
        sessionStorage.setItem('current_analysis_data', JSON.stringify(data));
        showToast('Analysis complete! Redirecting to Dashboard...', 'success');
        setTimeout(() => {
          window.location.href = '/analysis';
        }, 600);
      } else {
        showToast(data.error || 'Analysis failed', 'error');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = `<i data-feather="zap" class="w-4 h-4"></i> Run NLP Risk Analysis`;
        feather.replace();
      }
    } catch (e) {
      showToast(`Network error: ${e.message}`, 'error');
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `<i data-feather="zap" class="w-4 h-4"></i> Run NLP Risk Analysis`;
      feather.replace();
    }
  });
}

function renderAnalysisDashboard(data) {
  if (!data || !data.success) return;
  currentAnalysisData = data;

  const meta = data.metadata || {};
  const scoreInfo = data.risk_score || {};
  const clauses = data.clauses || [];
  const entities = data.entities || {};
  const recs = data.recommendations || [];

  // Update Top Metadata
  const docTypeBadge = document.getElementById('doc-type-badge');
  const docFilename = document.getElementById('doc-filename');
  const docMetaSubtitle = document.getElementById('doc-meta-subtitle');

  if (docTypeBadge) docTypeBadge.innerText = data.contract_type || 'Commercial Agreement';
  if (docFilename) docFilename.innerText = meta.filename || 'contract.txt';
  if (docMetaSubtitle) {
    docMetaSubtitle.innerHTML = `Document: <span class="font-mono text-slate-300">${meta.filename || 'contract.txt'}</span> | ${(meta.word_count || 0).toLocaleString()} words | ${clauses.length} detected clauses`;
  }

  // Update Score Gauge
  const scoreNum = document.getElementById('risk-score-num');
  const scoreCircle = document.getElementById('risk-score-circle');
  const riskBadge = document.getElementById('risk-level-badge');
  const riskSummaryText = document.getElementById('risk-summary-text');

  const overall = scoreInfo.overall_score || 0;
  const level = scoreInfo.risk_level || 'Low';

  if (scoreNum) scoreNum.innerText = overall;
  if (riskSummaryText) riskSummaryText.innerText = scoreInfo.recommendation_headline || '';

  if (scoreCircle && riskBadge) {
    scoreCircle.className = 'score-circle mb-3 bg-slate-900 border-4';
    riskBadge.className = 'px-3 py-1 rounded-full text-xs font-bold mb-2';

    if (level === 'High') {
      scoreCircle.classList.add('border-rose-500', 'text-rose-500');
      riskBadge.classList.add('badge-risk-high');
      riskBadge.innerText = 'HIGH RISK CONTRACT';
    } else if (level === 'Medium') {
      scoreCircle.classList.add('border-amber-500', 'text-amber-500');
      riskBadge.classList.add('badge-risk-med');
      riskBadge.innerText = 'MODERATE RISK CONTRACT';
    } else {
      scoreCircle.classList.add('border-emerald-500', 'text-emerald-500');
      riskBadge.classList.add('badge-risk-low');
      riskBadge.innerText = 'LOW RISK CONTRACT';
    }
  }

  // Update Counts
  document.getElementById('count-high').innerText = scoreInfo.high_count || 0;
  document.getElementById('pct-high').innerText = `${scoreInfo.risk_percentage_breakdown?.High || 0}% of total`;

  document.getElementById('count-med').innerText = scoreInfo.medium_count || 0;
  document.getElementById('pct-med').innerText = `${scoreInfo.risk_percentage_breakdown?.Medium || 0}% of total`;

  document.getElementById('count-low').innerText = scoreInfo.low_count || 0;
  document.getElementById('pct-low').innerText = `${scoreInfo.risk_percentage_breakdown?.Low || 0}% of total`;

  document.getElementById('total-clauses-count').innerText = `${clauses.length} Clauses Detected`;

  // Render Charts
  if (typeof renderRiskCharts === 'function') {
    renderRiskCharts(scoreInfo, clauses);
  }

  // Render Extracted Entities
  renderEntitySection('ner-orgs', entities.organizations, 'entity-org');
  renderEntitySection('ner-persons', entities.persons, 'entity-person');
  renderEntitySection('ner-dates', entities.dates, 'entity-date');
  renderEntitySection('ner-money', entities.money_amounts, 'entity-money');
  renderEntitySection('ner-durations', entities.durations, 'entity-dur');
  renderEntitySection('ner-acts', entities.governing_acts, 'entity-act');

  // Render Recommendations Checklist
  const recsContainer = document.getElementById('recommendations-container');
  if (recsContainer) {
    recsContainer.innerHTML = '';
    recs.forEach((rec, idx) => {
      const item = document.createElement('div');
      item.className = 'flex items-start gap-2.5 p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-200';
      item.innerHTML = `
        <div class="w-5 h-5 rounded bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">${idx + 1}</div>
        <div class="leading-relaxed">${rec}</div>
      `;
      recsContainer.appendChild(item);
    });
  }

  // Render Clauses List
  renderClausesList(clauses);

  // Setup NLP Lab Button redirect
  const nlpLabBtn = document.getElementById('open-nlp-lab-btn');
  if (nlpLabBtn) {
    nlpLabBtn.onclick = () => {
      const sampleText = clauses.length > 0 ? clauses[0].clause_text : meta.cleaned_text;
      sessionStorage.setItem('nlp_lab_input_text', sampleText);
      window.location.href = '/nlp-lab';
    };
  }
}

function renderEntitySection(elementId, items, cssClass) {
  const container = document.getElementById(elementId);
  if (!container) return;
  container.innerHTML = '';

  if (!items || items.length === 0) {
    container.innerHTML = '<span class="text-slate-400 text-[10px] italic">None detected</span>';
    return;
  }

  items.slice(0, 3).forEach(val => {
    const span = document.createElement('span');
    span.className = `entity-pill ${cssClass}`;
    span.innerText = val;
    container.appendChild(span);
  });
}

function renderClausesList(clauses, filter = 'all') {
  const container = document.getElementById('clauses-list-container');
  if (!container) return;
  container.innerHTML = '';

  const filtered = filter === 'all' ? clauses : clauses.filter(c => c.risk_level === filter);

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="text-center py-8 text-slate-400 text-xs">
        No clauses matching the selected filter (<span class="font-bold">${filter}</span>).
      </div>
    `;
    return;
  }

  filtered.forEach(c => {
    const card = document.createElement('div');
    card.className = 'p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all cursor-pointer';
    card.onclick = () => openClauseModal(c);

    const levelBadgeClass = c.risk_level === 'High' ? 'badge-risk-high' : (c.risk_level === 'Medium' ? 'badge-risk-med' : 'badge-risk-low');
    const borderLeftClass = c.risk_level === 'High' ? 'border-l-4 border-l-rose-500' : (c.risk_level === 'Medium' ? 'border-l-4 border-l-amber-500' : 'border-l-4 border-l-emerald-500');

    card.className += ` ${borderLeftClass}`;

    card.innerHTML = `
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <div class="flex items-center gap-2">
          <span class="font-bold text-white text-xs">${c.clause_title || c.clause_number}</span>
          <span class="badge-tag text-[10px]">${c.clause_category}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] text-slate-400 font-mono">Score: ${c.risk_score}/100</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${levelBadgeClass}">${c.risk_level} Risk</span>
        </div>
      </div>
      
      <p class="text-slate-400 text-xs font-mono line-clamp-2 mb-2 leading-relaxed">
        "${c.clause_text}"
      </p>

      <div class="flex items-center justify-between text-[11px]">
        <span class="text-blue-400 font-medium line-clamp-1"><i data-feather="info" class="w-3 h-3 inline mr-1"></i>${c.explanation}</span>
        <span class="text-slate-400 shrink-0 hover:text-white flex items-center gap-1">Details <i data-feather="chevron-right" class="w-3 h-3"></i></span>
      </div>
    `;

    container.appendChild(card);
  });

  feather.replace();
}

function filterClauses(filter) {
  const buttons = document.querySelectorAll('#clause-filters .filter-btn');
  buttons.forEach(btn => btn.classList.remove('active', 'bg-blue-600', 'text-white'));

  event.target.classList.add('active', 'bg-blue-600', 'text-white');

  if (currentAnalysisData && currentAnalysisData.clauses) {
    renderClausesList(currentAnalysisData.clauses, filter);
  }
}

function openClauseModal(clause) {
  const modal = document.getElementById('clause-modal');
  if (!modal) return;

  document.getElementById('modal-title').innerText = `${clause.clause_title || clause.clause_number}`;
  document.getElementById('modal-category-badge').innerText = `${clause.clause_category} (Confidence: ${(clause.category_confidence * 100).toFixed(0)}%)`;
  document.getElementById('modal-text').innerText = clause.clause_text;
  document.getElementById('modal-explanation').innerText = clause.explanation;
  document.getElementById('modal-recommendation').innerText = clause.recommendation;

  modal.classList.remove('hidden');
  feather.replace();
}

function closeClauseModal() {
  const modal = document.getElementById('clause-modal');
  if (modal) modal.classList.add('hidden');
}

function setupPdfDownload() {
  const btn = document.getElementById('download-pdf-btn');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    if (!currentAnalysisData) {
      showToast('No active analysis data to generate report from.', 'warning');
      return;
    }

    showToast('Generating official PDF Risk Assessment Report...', 'info');
    btn.disabled = true;
    btn.innerHTML = `<div class="loader-spinner w-3.5 h-3.5 border-2"></div> Generating PDF...`;

    try {
      const res = await fetch('/api/report/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ analysis_data: currentAnalysisData })
      });

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Risk_Report_${currentAnalysisData.metadata?.filename || 'contract'}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showToast('PDF Report downloaded successfully!', 'success');
      } else {
        const err = await res.json();
        showToast(`PDF error: ${err.error}`, 'error');
      }
    } catch (e) {
      showToast(`Download failed: ${e.message}`, 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i data-feather="download" class="w-3.5 h-3.5"></i> Download PDF Report`;
      feather.replace();
    }
  });
}
