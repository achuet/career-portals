/**
 * Jobseeker Company Directory - App Engine
 * Dynamic Markdown Table Fetcher, Parser, Filter & UI Controller
 */

(function () {
  'use strict';

  // State
  let state = {
    allCompanies: [],
    filteredCompanies: [],
    activeCategoryFile: 'companies/pharma.md',
    activeCity: 'ALL',
    activeType: 'ALL',
    searchQuery: '',
    showFavsOnly: false,
    viewMode: localStorage.getItem('companyhub_view') || 'grid',
    favorites: new Set(JSON.parse(localStorage.getItem('companyhub_favs') || '[]'))
  };

  // DOM Elements
  const elements = {
    gridContainer: document.getElementById('grid-container'),
    tableContainer: document.getElementById('table-container'),
    tableBody: document.getElementById('table-body'),
    loadingSpinner: document.getElementById('loading-spinner'),
    emptyState: document.getElementById('empty-state'),
    searchInput: document.getElementById('search-input'),
    clearSearchBtn: document.getElementById('clear-search'),
    typeSelect: document.getElementById('type-select'),
    cityPills: document.getElementById('city-pills'),
    favOnlyCheckbox: document.getElementById('fav-only-checkbox'),
    viewGridBtn: document.getElementById('view-grid'),
    viewTableBtn: document.getElementById('view-table'),
    sectorTabs: document.getElementById('sector-tabs'),
    themeToggleBtn: document.getElementById('theme-toggle'),
    resultsCountText: document.getElementById('results-count-text'),
    favCountText: document.getElementById('fav-count-text'),
    kpiCompanies: document.getElementById('kpi-companies'),
    kpiCities: document.getElementById('kpi-cities'),
    kpiSectors: document.getElementById('kpi-sectors'),
    kpiSaved: document.getElementById('kpi-saved'),
    
    // Modals
    addModal: document.getElementById('add-modal'),
    addCompanyBtn: document.getElementById('add-company-btn'),
    closeAddModal: document.getElementById('close-add-modal'),
    exportModal: document.getElementById('export-modal'),
    exportBtn: document.getElementById('export-btn'),
    closeExportModal: document.getElementById('close-export-modal'),
    
    // Add Form
    addForm: document.getElementById('add-company-form'),
    compNameInput: document.getElementById('comp-name'),
    compWebsiteInput: document.getElementById('comp-website'),
    compCareersInput: document.getElementById('comp-careers'),
    compLocationsInput: document.getElementById('comp-locations'),
    compTypeInput: document.getElementById('comp-type'),
    compFocusInput: document.getElementById('comp-focus'),
    markdownOutput: document.getElementById('markdown-output'),
    copyMdBtn: document.getElementById('copy-md-btn'),
    openGhEditBtn: document.getElementById('open-gh-edit'),

    // Export Options
    exportCount: document.getElementById('export-count'),
    exportJsonBtn: document.getElementById('export-json'),
    exportCsvBtn: document.getElementById('export-csv'),
    exportMdBtn: document.getElementById('export-md'),
    resetFiltersBtn: document.getElementById('reset-filters-btn')
  };

  // Initialize Application
  function init() {
    setupTheme();
    setupEventListeners();
    updateViewModeUI();
    loadCategoryData(state.activeCategoryFile);
    updateFavCountUI();
  }

  // Setup Theme Mode
  function setupTheme() {
    const savedTheme = localStorage.getItem('companyhub_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  }

  function updateThemeIcon(theme) {
    const icon = elements.themeToggleBtn.querySelector('i');
    if (theme === 'dark') {
      icon.className = 'fa-solid fa-sun';
    } else {
      icon.className = 'fa-solid fa-moon';
    }
  }

  // Load and Parse Category Markdown File
  async function loadCategoryData(filePath) {
    showLoading(true);
    try {
      const response = await fetch(filePath);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const text = await response.text();
      state.allCompanies = parseMarkdownTable(text);
      
      buildDynamicFilters();
      applyFilters();
      updateKPIDashboard();
      
      // Update GH edit button target link
      elements.openGhEditBtn.href = `https://github.com/achuet/career-portals/blob/main/${filePath}`;
    } catch (err) {
      console.error('Error loading markdown file:', err);
      state.allCompanies = [];
      applyFilters();
    } finally {
      showLoading(false);
    }
  }

  // Markdown Table Parser
  function parseMarkdownTable(mdText) {
    const lines = mdText.split(/\r?\n/);
    const companies = [];
    let isTable = false;

    for (let line of lines) {
      line = line.trim();
      // Check for table header row
      if (line.startsWith('|') && line.includes('ID') && line.includes('Company Name')) {
        isTable = true;
        continue;
      }
      // Skip separator row (|---|---|...)
      if (line.startsWith('|') && line.includes('---|')) {
        continue;
      }
      // Parse table data row
      if (isTable && line.startsWith('|') && line.endsWith('|')) {
        const cells = line.split('|').map(c => c.trim()).slice(1, -1);
        if (cells.length >= 6) {
          const id = cells[0];
          const name = cells[1].replace(/\*\*/g, '').trim();
          
          // Extract URLs from Markdown syntax [Text](URL)
          const websiteUrl = extractUrlFromMdLink(cells[2]) || `https://www.google.com/search?q=${encodeURIComponent(name)}`;
          const careerUrl = extractUrlFromMdLink(cells[3]) || `https://www.google.com/search?q=${encodeURIComponent(name + ' careers')}`;
          
          const rawLocs = cells[4];
          const locations = rawLocs.split(',').map(s => s.trim()).filter(Boolean);
          
          const type = cells[5].replace(/`/g, '').trim();
          const focus = cells[6] || 'Pharmaceuticals & Healthcare';

          companies.push({
            id,
            name,
            websiteUrl,
            careerUrl,
            locations,
            rawLocations: rawLocs,
            type,
            focus
          });
        }
      }
    }

    return companies;
  }

  function extractUrlFromMdLink(mdCell) {
    const match = mdCell.match(/\[.*?\]\((.*?)\)/);
    return match ? match[1] : null;
  }

  // Build Dynamic City & Type Filters
  function buildDynamicFilters() {
    // Collect unique cities
    const citySet = new Set();
    state.allCompanies.forEach(c => {
      c.locations.forEach(loc => citySet.add(loc));
    });

    const sortedCities = Array.from(citySet).sort();

    // Render City Pills
    let pillsHTML = `<button class="city-pill ${state.activeCity === 'ALL' ? 'active' : ''}" data-city="ALL">All Cities</button>`;
    sortedCities.forEach(city => {
      pillsHTML += `<button class="city-pill ${state.activeCity === city ? 'active' : ''}" data-city="${city}">${city}</button>`;
    });
    elements.cityPills.innerHTML = pillsHTML;

    // Collect unique Types
    const typeSet = new Set();
    state.allCompanies.forEach(c => typeSet.add(c.type));
    const sortedTypes = Array.from(typeSet).sort();

    let typeOpts = `<option value="ALL">All Types / Categories</option>`;
    sortedTypes.forEach(t => {
      typeOpts += `<option value="${t}" ${state.activeType === t ? 'selected' : ''}>${t}</option>`;
    });
    elements.typeSelect.innerHTML = typeOpts;
  }

  // Apply Filter & Search Logic
  function applyFilters() {
    let result = state.allCompanies;

    // 1. Search Query
    if (state.searchQuery.trim() !== '') {
      const q = state.searchQuery.toLowerCase();
      result = result.filter(c => 
        c.name.toLowerCase().includes(q) ||
        c.rawLocations.toLowerCase().includes(q) ||
        c.type.toLowerCase().includes(q) ||
        c.focus.toLowerCase().includes(q)
      );
    }

    // 2. City Filter
    if (state.activeCity !== 'ALL') {
      result = result.filter(c => c.locations.includes(state.activeCity));
    }

    // 3. Type Filter
    if (state.activeType !== 'ALL') {
      result = result.filter(c => c.type === state.activeType);
    }

    // 4. Favorites Only
    if (state.showFavsOnly) {
      result = result.filter(c => state.favorites.has(c.name));
    }

    state.filteredCompanies = result;
    renderResults();
  }

  // Render Results UI
  function renderResults() {
    elements.resultsCountText.textContent = `Showing ${state.filteredCompanies.length} of ${state.allCompanies.length} companies`;
    elements.exportCount.textContent = state.filteredCompanies.length;

    if (state.filteredCompanies.length === 0) {
      elements.gridContainer.style.display = 'none';
      elements.tableContainer.style.display = 'none';
      elements.emptyState.style.display = 'block';
      return;
    }

    elements.emptyState.style.display = 'none';

    if (state.viewMode === 'grid') {
      elements.tableContainer.style.display = 'none';
      elements.gridContainer.style.display = 'grid';
      renderGrid();
    } else {
      elements.gridContainer.style.display = 'none';
      elements.tableContainer.style.display = 'block';
      renderTable();
    }
  }

  // Render Cards Grid
  function renderGrid() {
    elements.gridContainer.innerHTML = state.filteredCompanies.map(c => {
      const isFav = state.favorites.has(c.name);
      const linkedInUrl = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(c.name)}`;

      return `
        <div class="company-card">
          <div>
            <div class="card-top">
              <div class="company-name-group">
                <span class="company-id">#${c.id}</span>
                <h3 class="company-name">${escapeHTML(c.name)}</h3>
              </div>
              <button class="fav-btn ${isFav ? 'active' : ''}" data-name="${escapeHTML(c.name)}" title="Save Favorite">
                <i class="${isFav ? 'fa-solid' : 'fa-regular'} fa-star"></i>
              </button>
            </div>
            <span class="type-badge">${escapeHTML(c.type)}</span>
            <div class="card-body">
              <div class="location-list">
                <i class="fa-solid fa-location-dot"></i>
                <span>${escapeHTML(c.rawLocations)}</span>
              </div>
              <p class="focus-text">${escapeHTML(c.focus)}</p>
            </div>
          </div>
          <div class="card-footer">
            <a href="${c.careerUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-careers">
              <i class="fa-solid fa-briefcase"></i> Careers
            </a>
            <a href="${c.websiteUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-website" title="Website">
              <i class="fa-solid fa-globe"></i>
            </a>
            <a href="${linkedInUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-website" title="LinkedIn Jobs">
              <i class="fa-brands fa-linkedin"></i>
            </a>
          </div>
        </div>
      `;
    }).join('');
  }

  // Render List Table
  function renderTable() {
    elements.tableBody.innerHTML = state.filteredCompanies.map(c => {
      const isFav = state.favorites.has(c.name);
      const linkedInUrl = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(c.name)}`;

      return `
        <tr>
          <td>
            <button class="fav-btn ${isFav ? 'active' : ''}" data-name="${escapeHTML(c.name)}">
              <i class="${isFav ? 'fa-solid' : 'fa-regular'} fa-star"></i>
            </button>
          </td>
          <td><strong>#${c.id}</strong></td>
          <td><strong>${escapeHTML(c.name)}</strong></td>
          <td><span class="type-badge">${escapeHTML(c.type)}</span></td>
          <td><i class="fa-solid fa-location-dot" style="color:var(--accent-emerald)"></i> ${escapeHTML(c.rawLocations)}</td>
          <td>${escapeHTML(c.focus)}</td>
          <td>
            <div class="table-actions">
              <a href="${c.careerUrl}" target="_blank" class="btn btn-careers" style="font-size:0.75rem;">
                <i class="fa-solid fa-briefcase"></i> Careers
              </a>
              <a href="${c.websiteUrl}" target="_blank" class="btn btn-website" style="font-size:0.75rem;" title="Website">
                <i class="fa-solid fa-globe"></i>
              </a>
              <a href="${linkedInUrl}" target="_blank" class="btn btn-website" style="font-size:0.75rem;" title="LinkedIn">
                <i class="fa-brands fa-linkedin"></i>
              </a>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  // Update KPI Stats Dashboard
  function updateKPIDashboard() {
    elements.kpiCompanies.textContent = state.allCompanies.length;
    
    // Unique cities count
    const citySet = new Set();
    state.allCompanies.forEach(c => c.locations.forEach(loc => citySet.add(loc)));
    elements.kpiCities.textContent = citySet.size;

    elements.kpiSaved.textContent = state.favorites.size;
  }

  function updateFavCountUI() {
    elements.favCountText.textContent = state.favorites.size;
    elements.kpiSaved.textContent = state.favorites.size;
  }

  // Event Listeners Setup
  function setupEventListeners() {
    // Theme Toggle
    elements.themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('companyhub_theme', nextTheme);
      updateThemeIcon(nextTheme);
    });

    // Sector Tab Change
    elements.sectorTabs.addEventListener('click', (e) => {
      const tab = e.target.closest('.tab-btn');
      if (!tab) return;

      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      tab.classList.add('active');

      const file = tab.getAttribute('data-file');
      state.activeCategoryFile = file;
      state.activeCity = 'ALL';
      state.activeType = 'ALL';
      state.searchQuery = '';
      elements.searchInput.value = '';
      elements.clearSearchBtn.style.display = 'none';

      loadCategoryData(file);
    });

    // Search Input
    elements.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      elements.clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
      applyFilters();
    });

    elements.clearSearchBtn.addEventListener('click', () => {
      state.searchQuery = '';
      elements.searchInput.value = '';
      elements.clearSearchBtn.style.display = 'none';
      applyFilters();
    });

    // Type Select Filter
    elements.typeSelect.addEventListener('change', (e) => {
      state.activeType = e.target.value;
      applyFilters();
    });

    // City Pills Filter
    elements.cityPills.addEventListener('click', (e) => {
      if (!e.target.classList.contains('city-pill')) return;
      document.querySelectorAll('.city-pill').forEach(p => p.classList.remove('active'));
      e.target.classList.add('active');
      state.activeCity = e.target.getAttribute('data-city');
      applyFilters();
    });

    // Favorites Checkbox
    elements.favOnlyCheckbox.addEventListener('change', (e) => {
      state.showFavsOnly = e.target.checked;
      applyFilters();
    });

    // Favorite Toggle (Delegated on Grid and Table)
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.fav-btn');
      if (!btn) return;
      const compName = btn.getAttribute('data-name');
      if (!compName) return;

      if (state.favorites.has(compName)) {
        state.favorites.delete(compName);
      } else {
        state.favorites.add(compName);
      }

      localStorage.setItem('companyhub_favs', JSON.stringify(Array.from(state.favorites)));
      updateFavCountUI();
      applyFilters();
    });

    // View Mode Toggle
    elements.viewGridBtn.addEventListener('click', () => {
      state.viewMode = 'grid';
      localStorage.setItem('companyhub_view', 'grid');
      updateViewModeUI();
      renderResults();
    });

    elements.viewTableBtn.addEventListener('click', () => {
      state.viewMode = 'table';
      localStorage.setItem('companyhub_view', 'table');
      updateViewModeUI();
      renderResults();
    });

    // Reset Filters
    elements.resetFiltersBtn.addEventListener('click', () => {
      state.searchQuery = '';
      state.activeCity = 'ALL';
      state.activeType = 'ALL';
      state.showFavsOnly = false;
      elements.searchInput.value = '';
      elements.favOnlyCheckbox.checked = false;
      elements.clearSearchBtn.style.display = 'none';
      buildDynamicFilters();
      applyFilters();
    });

    // Modal Handlers
    elements.addCompanyBtn.addEventListener('click', () => {
      elements.addModal.style.display = 'flex';
      updateMarkdownPreview();
    });
    elements.closeAddModal.addEventListener('click', () => {
      elements.addModal.style.display = 'none';
    });

    elements.exportBtn.addEventListener('click', () => {
      elements.exportModal.style.display = 'flex';
    });
    elements.closeExportModal.addEventListener('click', () => {
      elements.exportModal.style.display = 'none';
    });

    // Form Live Markdown Generator
    const addInputs = [
      elements.compNameInput, elements.compWebsiteInput, 
      elements.compCareersInput, elements.compLocationsInput, 
      elements.compTypeInput, elements.compFocusInput
    ];
    addInputs.forEach(input => input.addEventListener('input', updateMarkdownPreview));

    // Copy Markdown Button
    elements.copyMdBtn.addEventListener('click', () => {
      const mdText = elements.markdownOutput.textContent;
      navigator.clipboard.writeText(mdText).then(() => {
        const origText = elements.copyMdBtn.innerHTML;
        elements.copyMdBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
        setTimeout(() => elements.copyMdBtn.innerHTML = origText, 2000);
      });
    });

    // Export Options
    elements.exportJsonBtn.addEventListener('click', exportAsJson);
    elements.exportCsvBtn.addEventListener('click', exportAsCsv);
    elements.exportMdBtn.addEventListener('click', exportAsMarkdown);
  }

  function updateViewModeUI() {
    if (state.viewMode === 'grid') {
      elements.viewGridBtn.classList.add('active');
      elements.viewTableBtn.classList.remove('active');
    } else {
      elements.viewTableBtn.classList.add('active');
      elements.viewGridBtn.classList.remove('active');
    }
  }

  function updateMarkdownPreview() {
    const nextId = state.allCompanies.length + 1;
    const name = elements.compNameInput.value.trim() || 'Company Name';
    const website = elements.compWebsiteInput.value.trim() || 'https://example.com';
    const careers = elements.compCareersInput.value.trim() || 'https://example.com/careers';
    const locations = elements.compLocationsInput.value.trim() || 'City';
    const type = elements.compTypeInput.value.trim() || 'Category';
    const focus = elements.compFocusInput.value.trim() || 'Description';

    const mdRow = `| ${nextId} | **${name}** | [Website](${website}) | [Careers Portal](${careers}) | ${locations} | \`${type}\` | ${focus} |`;
    elements.markdownOutput.textContent = mdRow;
  }

  // Export Implementations
  function exportAsJson() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state.filteredCompanies, null, 2));
    downloadFile(dataStr, "companies_export.json");
  }

  function exportAsCsv() {
    let csv = "ID,Company Name,Website,Careers Portal,Locations,Type,Focus\n";
    state.filteredCompanies.forEach(c => {
      csv += `"${c.id}","${c.name}","${c.websiteUrl}","${c.careerUrl}","${c.rawLocations}","${c.type}","${c.focus.replace(/"/g, '""')}"\n`;
    });
    const dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    downloadFile(dataStr, "companies_export.csv");
  }

  function exportAsMarkdown() {
    let md = "| ID | Company Name | Official Website | Careers Portal | India Locations | Type | Key Focus |\n|---|---|---|---|---|---|---|\n";
    state.filteredCompanies.forEach(c => {
      md += `| ${c.id} | **${c.name}** | [Website](${c.websiteUrl}) | [Careers Portal](${c.careerUrl}) | ${c.rawLocations} | \`${c.type}\` | ${c.focus} |\n`;
    });
    const dataStr = "data:text/markdown;charset=utf-8," + encodeURIComponent(md);
    downloadFile(dataStr, "companies_export.md");
  }

  function downloadFile(dataStr, filename) {
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", filename);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  }

  function showLoading(show) {
    elements.loadingSpinner.style.display = show ? 'block' : 'none';
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  // Start app on DOMReady
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
