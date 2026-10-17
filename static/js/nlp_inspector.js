/**
 * Interactive NLP Inspector Logic (13 Techniques Playground)
 */

const NLP_SNIPPETS = {
  indemnity: "The Service Provider agrees to indemnify, defend, and hold harmless the Client from any and all claims, losses, damages, liabilities, costs, and expenses without any monetary cap or limitation of liability whatsoever under the laws of India.",
  renewal: "This Agreement shall automatically renew for successive terms of two (2) years each unless the Client provides written notice of non-renewal at least ninety (90) days prior to the expiration date. In the event of non-renewal, Vendor shall pay an exit penalty of INR 1,50,000.",
  noncompete: "The Consultant and its employees agree not to engage in any competing business, provide similar services, or solicit any client in Maharashtra for a period of three (3) years post-termination under Section 27 of the Indian Contract Act 1872.",
  polysemy: "In consideration of the mutual covenants contained herein and the payment of INR 5,00,000, the parties have executed this instrument on the Effective Date."
};

document.addEventListener('DOMContentLoaded', () => {
  setupNlpLab();
});

function setupNlpLab() {
  const runBtn = document.getElementById('run-nlp-btn');
  const inputTextArea = document.getElementById('nlp-input-text');

  // Check if text was passed from analysis dashboard
  const passedText = sessionStorage.getItem('nlp_lab_input_text');
  if (passedText) {
    inputTextArea.value = passedText;
    sessionStorage.removeItem('nlp_lab_input_text');
  } else if (!inputTextArea.value.trim()) {
    inputTextArea.value = NLP_SNIPPETS.indemnity;
  }

  runBtn.addEventListener('click', runNlpInspection);

  // Initial execution
  runNlpInspection();
}

function loadNlpSnippet(type) {
  const text = NLP_SNIPPETS[type] || NLP_SNIPPETS.indemnity;
  document.getElementById('nlp-input-text').value = text;
  
  if (type === 'polysemy') {
    document.getElementById('nlp-target-keyword').value = 'consideration';
  } else if (type === 'renewal') {
    document.getElementById('nlp-target-keyword').value = 'renew';
  } else if (type === 'noncompete') {
    document.getElementById('nlp-target-keyword').value = 'compete';
  } else {
    document.getElementById('nlp-target-keyword').value = 'indemnify';
  }

  runNlpInspection();
}

function switchNlpTab(tabId) {
  // Update Buttons
  const buttons = document.querySelectorAll('#nlp-tabs-nav .nav-tab-btn');
  buttons.forEach(btn => {
    btn.classList.remove('active', 'bg-blue-600', 'text-white');
    if (btn.dataset.tab === tabId) {
      btn.classList.add('active', 'bg-blue-600', 'text-white');
    }
  });

  // Update Panes
  const panes = document.querySelectorAll('.nlp-tab-pane');
  panes.forEach(pane => pane.classList.add('hidden'));

  const activePane = document.getElementById(`tab-${tabId}`);
  if (activePane) {
    activePane.classList.remove('hidden');
  }
}

async function runNlpInspection() {
  const text = document.getElementById('nlp-input-text').value.trim();
  const keyword = document.getElementById('nlp-target-keyword').value.trim() || 'terminate';
  const runBtn = document.getElementById('run-nlp-btn');

  if (!text) {
    showToast('Please enter text to inspect.', 'warning');
    return;
  }

  runBtn.disabled = true;
  runBtn.innerHTML = `<div class="loader-spinner w-3.5 h-3.5 border-2"></div> Processing 13 NLP Techniques...`;

  try {
    const res = await fetch('/api/nlp-inspect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, keyword })
    });

    const data = await res.json();

    if (data.success && data.nlp_data) {
      renderNlpData(data.nlp_data);
      showToast('All 13 NLP techniques processed!', 'success');
    } else {
      showToast(data.error || 'Inspection failed', 'error');
    }
  } catch (e) {
    showToast(`Error: ${e.message}`, 'error');
  } finally {
    runBtn.disabled = false;
    runBtn.innerHTML = `<i data-feather="cpu" class="w-3.5 h-3.5"></i> Inspect All 13 NLP Techniques`;
    feather.replace();
  }
}

function renderNlpData(d) {
  // 1. Tokenization
  const t1 = d.technique_1_tokenization || {};
  document.getElementById('tok-sent-count').innerText = t1.total_sentences || 0;
  document.getElementById('tok-word-count').innerText = t1.total_words || 0;

  const sentList = document.getElementById('tok-sentences-list');
  sentList.innerHTML = '';
  (t1.sentences || []).forEach((s, idx) => {
    const item = document.createElement('div');
    item.className = 'p-2.5 rounded-lg bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-300 flex items-start gap-2';
    item.innerHTML = `<span class="text-blue-400 font-bold shrink-0">[S${idx + 1}]</span> <span>${s}</span>`;
    sentList.appendChild(item);
  });

  const wordCloud = document.getElementById('tok-words-cloud');
  wordCloud.innerHTML = '';
  (t1.words_sample || []).forEach(w => {
    const span = document.createElement('span');
    span.className = 'px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300 font-mono text-[11px]';
    span.innerText = w;
    wordCloud.appendChild(span);
  });

  // 2. Stopwords
  const t2 = d.technique_2_stopwords || {};
  document.getElementById('stop-retained-count').innerText = t2.total_retained_tokens || 0;

  const presTokens = document.getElementById('stop-preserved-tokens');
  presTokens.innerHTML = '';
  (t2.preserved_legal_tokens || []).forEach(w => {
    const span = document.createElement('span');
    span.className = 'px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono font-semibold text-xs';
    span.innerText = w;
    presTokens.appendChild(span);
  });

  const filtTokens = document.getElementById('stop-filtered-tokens');
  filtTokens.innerHTML = '';
  (t2.filtered_tokens_sample || []).forEach(w => {
    const span = document.createElement('span');
    span.className = 'px-2 py-0.5 rounded bg-slate-900 text-slate-300 font-mono text-[11px]';
    span.innerText = w;
    filtTokens.appendChild(span);
  });

  // 3-5. Normalization Comparison Table
  const tNorm = d.techniques_3_4_5_normalization || {};
  const normTbody = document.getElementById('norm-table-body');
  normTbody.innerHTML = '';
  (tNorm.comparison_table || []).forEach(row => {
    const tr = document.createElement('tr');
    const isDiff = row.stem_vs_lemma_difference;
    tr.innerHTML = `
      <td class="p-3 font-bold text-white">${row.original_word}</td>
      <td class="p-3 text-purple-400 font-mono">${row.pos_tag}</td>
      <td class="p-3 text-blue-400 font-mono">${row.porter_stem}</td>
      <td class="p-3 text-cyan-400 font-mono">${row.lancaster_stem}</td>
      <td class="p-3 text-emerald-400 font-mono font-bold">${row.wordnet_lemma}</td>
      <td class="p-3 text-right font-mono ${isDiff ? 'text-amber-400' : 'text-slate-400'}">
        ${isDiff ? '<span class="px-1.5 py-0.5 rounded bg-amber-950/40 border border-amber-800/40 text-[10px]">Stem != Lemma</span>' : '<span class="text-[10px]">Identical</span>'}
      </td>
    `;
    normTbody.appendChild(tr);
  });

  // 6. POS Tagging
  const t6 = d.technique_6_pos_tagging || {};
  const posContainer = document.getElementById('pos-tokens-container');
  posContainer.innerHTML = '';
  (t6.tagged_tokens || []).forEach(t => {
    const div = document.createElement('div');
    const isModal = t.is_modal;
    div.className = `px-2 py-1 rounded-lg border text-[11px] font-mono flex items-center gap-1.5 ${isModal ? 'bg-purple-950/40 border-purple-500 text-purple-200 font-bold' : 'bg-slate-900 border-slate-800 text-slate-300'}`;
    div.innerHTML = `<span>${t.word}</span> <span class="text-[9px] px-1 rounded bg-black/40 ${isModal ? 'text-purple-400' : 'text-slate-400'}">${t.tag}</span>`;
    posContainer.appendChild(div);
  });

  const posDistList = document.getElementById('pos-distribution-list');
  posDistList.innerHTML = '';
  for (const [tag, count] of Object.entries(t6.pos_distribution || {})) {
    const div = document.createElement('div');
    div.className = 'flex items-center justify-between text-slate-400';
    div.innerHTML = `<span>Tag: <b class="text-white">${tag}</b></span> <span>${count} tokens</span>`;
    posDistList.appendChild(div);
  }

  // 7. Chunking
  const t7 = d.technique_7_chunking || {};
  const npList = document.getElementById('chunk-np-list');
  npList.innerHTML = '';
  (t7.noun_phrases || []).forEach(np => {
    const span = document.createElement('span');
    span.className = 'px-2 py-1 rounded bg-blue-950/40 border border-blue-800/50 text-blue-300 font-mono text-[11px]';
    span.innerText = `[NP: ${np}]`;
    npList.appendChild(span);
  });

  const vpList = document.getElementById('chunk-vp-list');
  vpList.innerHTML = '';
  (t7.verb_phrases || []).forEach(vp => {
    const span = document.createElement('span');
    span.className = 'px-2 py-1 rounded bg-purple-950/40 border border-purple-800/50 text-purple-300 font-mono text-[11px]';
    span.innerText = `[VP: ${vp}]`;
    vpList.appendChild(span);
  });

  document.getElementById('chunk-tree-pre').innerText = t7.tree_str || '(No parse tree generated)';

  // 8. NER
  const t8 = d.technique_8_ner || {};
  const nerChipsContainer = document.getElementById('ner-chips-container');
  nerChipsContainer.innerHTML = '';

  const nerSections = [
    { title: 'Organizations', items: t8.organizations, cls: 'entity-org', icon: 'briefcase' },
    { title: 'Signatories', items: t8.persons, cls: 'entity-person', icon: 'user' },
    { title: 'Dates', items: t8.dates, cls: 'entity-date', icon: 'calendar' },
    { title: 'Money Sums', items: t8.money_amounts, cls: 'entity-money', icon: 'dollar-sign' },
    { title: 'Durations', items: t8.durations, cls: 'entity-dur', icon: 'clock' },
    { title: 'Governing Acts', items: t8.governing_acts, cls: 'entity-act', icon: 'book' }
  ];

  nerSections.forEach(sec => {
    const card = document.createElement('div');
    card.className = 'p-3.5 rounded-xl bg-slate-950 border border-slate-800';
    
    let itemsHtml = '';
    if (sec.items && sec.items.length > 0) {
      itemsHtml = sec.items.map(it => `<span class="entity-pill ${sec.cls}">${it}</span>`).join(' ');
    } else {
      itemsHtml = '<span class="text-slate-400 text-[10px] italic">None detected</span>';
    }

    card.innerHTML = `
      <div class="text-[10px] text-slate-400 font-semibold uppercase tracking-wider mb-2">${sec.title}</div>
      <div class="flex flex-wrap gap-1">${itemsHtml}</div>
    `;
    nerChipsContainer.appendChild(card);
  });

  // 9. Bag of Words
  const t9 = d.technique_9_bow || {};
  const bowTbody = document.getElementById('bow-table-body');
  bowTbody.innerHTML = '';
  const topFreqs = t9.top_word_frequencies || [];
  const maxCount = topFreqs.length > 0 ? topFreqs[0].count : 1;

  topFreqs.slice(0, 15).forEach((item, idx) => {
    const tr = document.createElement('tr');
    const pct = Math.round((item.count / maxCount) * 100);
    tr.innerHTML = `
      <td class="p-3 text-slate-400">#${idx + 1}</td>
      <td class="p-3 font-bold text-white">${item.word}</td>
      <td class="p-3 text-yellow-400 font-bold">${item.count}</td>
      <td class="p-3">
        <div class="w-full bg-slate-800 rounded-full h-2">
          <div class="bg-yellow-500 h-2 rounded-full" style="width: ${pct}%"></div>
        </div>
      </td>
    `;
    bowTbody.appendChild(tr);
  });

  // 10. N-Grams
  const t10 = d.technique_10_ngrams || {};
  const riskCollocs = document.getElementById('ngrams-risk-collocations');
  riskCollocs.innerHTML = '';
  (t10.detected_risk_collocations || []).forEach(rc => {
    const card = document.createElement('div');
    card.className = 'p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 text-xs flex items-center justify-between';
    card.innerHTML = `
      <div>
        <div class="font-bold text-rose-300 font-mono">"${rc.collocation}"</div>
        <div class="text-[10px] text-rose-400/80">${rc.risk_type}</div>
      </div>
      <span class="px-2 py-0.5 rounded bg-rose-900/40 text-rose-300 font-mono text-[10px]">${rc.occurrences}x</span>
    `;
    riskCollocs.appendChild(card);
  });

  renderNgramList('ngrams-unigrams', t10.unigrams);
  renderNgramList('ngrams-bigrams', t10.bigrams);
  renderNgramList('ngrams-trigrams', t10.trigrams);

  // 11. WordNet Synonyms
  const t11 = d.technique_11_wordnet_synonyms || {};
  document.getElementById('wn-query-word').innerText = t11.query_word || '';

  const synList = document.getElementById('wn-synonyms-list');
  synList.innerHTML = '';
  (t11.synonyms || []).forEach(s => {
    const span = document.createElement('span');
    span.className = 'px-2 py-1 rounded bg-blue-950/40 border border-blue-800/50 text-blue-300 font-mono text-[11px]';
    span.innerText = s;
    synList.appendChild(span);
  });

  const legalSynList = document.getElementById('wn-legal-synonyms');
  legalSynList.innerHTML = '';
  (t11.legal_domain_synonyms || []).forEach(ls => {
    const span = document.createElement('span');
    span.className = 'px-2 py-1 rounded bg-purple-950/40 border border-purple-800/50 text-purple-300 font-mono text-[11px]';
    span.innerText = ls;
    legalSynList.appendChild(span);
  });

  const defsList = document.getElementById('wn-definitions-list');
  defsList.innerHTML = '';
  (t11.synset_definitions || []).forEach(def => {
    const div = document.createElement('div');
    div.className = 'p-3 rounded-xl bg-slate-950 border border-slate-800 text-[11px]';
    div.innerHTML = `
      <div class="font-mono font-bold text-slate-200 mb-1">${def.synset_name} (${def.pos})</div>
      <p class="text-slate-400 mb-1 leading-relaxed">${def.definition}</p>
      ${def.examples && def.examples.length > 0 ? `<p class="text-slate-400 italic text-[10px]">Ex: "${def.examples[0]}"</p>` : ''}
    `;
    defsList.appendChild(div);
  });

  // 12. Word2Vec
  const t12 = d.technique_12_word2vec || {};
  const neighborsList = document.getElementById('w2v-neighbors-list');
  neighborsList.innerHTML = '';
  (t12.top_semantic_neighbors || []).forEach(n => {
    const div = document.createElement('div');
    div.className = 'p-2.5 rounded-lg bg-emerald-950/20 border border-emerald-900/40 flex items-center justify-between text-xs font-mono';
    div.innerHTML = `
      <span class="text-white font-bold">${n.word}</span>
      <span class="text-emerald-400">Cosine: ${(n.similarity_score * 100).toFixed(1)}%</span>
    `;
    neighborsList.appendChild(div);
  });

  if (t12.sample_vector_slice && t12.sample_vector_slice.length > 0) {
    document.getElementById('w2v-vector-slice').innerText = `[${t12.sample_vector_slice.map(v => v.toFixed(4)).join(', ')}, ...]`;
  }

  // 13. WSD Lesk
  const t13 = d.technique_13_wsd_lesk || {};
  document.getElementById('wsd-context-sentence').innerText = t13.context_sentence || '';
  document.getElementById('wsd-synset-name').innerText = `${t13.target_word} (${t13.disambiguated_synset})`;
  document.getElementById('wsd-definition').innerText = t13.definition || '';

  const contrastBox = document.getElementById('wsd-contrast-content');
  contrastBox.innerHTML = '';
  if (t13.legal_vs_lay_contrast) {
    const c = t13.legal_vs_lay_contrast;
    contrastBox.innerHTML = `
      <div><b class="text-purple-300">Legal Meaning:</b> ${c.legal_sense}</div>
      <div class="mt-2"><b class="text-slate-400">Colloquial/Lay Meaning:</b> ${c.lay_sense}</div>
      <div class="mt-2 text-emerald-400 font-semibold">Detected Context: ${t13.inferred_context_type || 'Legal'}</div>
    `;
  } else {
    contrastBox.innerHTML = '<span class="text-slate-400 italic">No statutory polysemy conflict detected.</span>';
  }

  feather.replace();
}

function renderNgramList(elementId, items) {
  const container = document.getElementById(elementId);
  if (!container) return;
  container.innerHTML = '';

  (items || []).slice(0, 6).forEach(it => {
    const div = document.createElement('div');
    div.className = 'flex items-center justify-between text-[11px] text-slate-300 py-1 border-b border-slate-900';
    div.innerHTML = `<span>${it.ngram}</span> <span class="text-blue-400">${it.frequency}x</span>`;
    container.appendChild(div);
  });
}
