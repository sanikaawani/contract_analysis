const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchSampleContracts() {
  const res = await fetch(`${API_BASE}/samples`);
  if (!res.ok) throw new Error('Failed to fetch sample contracts');
  return res.json();
}

export async function analyzeContractText(text, contractTitle = 'Uploaded Contract', contractType = 'Auto-Detect') {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      contract_title: contractTitle,
      contract_type: contractType
    })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to analyze contract');
  }
  return res.json();
}

export async function analyzeContractFile(file, contractTitle, contractType) {
  const formData = new FormData();
  formData.append('file', file);
  if (contractTitle) formData.append('contract_title', contractTitle);
  if (contractType) formData.append('contract_type', contractType);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to analyze contract file');
  }
  return res.json();
}

export async function runNLPExperiment(text, technique = 'all', queryWord = '') {
  const res = await fetch(`${API_BASE}/nlp-experiment`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      technique,
      query_word: queryWord
    })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to run NLP experiment');
  }
  return res.json();
}

export async function fetchModelMetrics() {
  const res = await fetch(`${API_BASE}/model-metrics`);
  if (!res.ok) throw new Error('Failed to fetch model metrics');
  return res.json();
}

export async function downloadPDFReport(analysisData) {
  const res = await fetch(`${API_BASE}/generate-pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(analysisData)
  });
  if (!res.ok) throw new Error('Failed to generate PDF report');
  
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `LexiRisk_Audit_Report_${(analysisData.contract_title || 'Report').replace(/\s+/g, '_')}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
