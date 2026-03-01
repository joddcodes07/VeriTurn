import './style.css'

// Global state for full table data storage
let currentTableData = [];

// Basic Router to handle views
class Router {
    constructor() {
        this.currentView = 'landing';
        this.views = {
            landing: document.getElementById('view-landing'),
            upload: document.getElementById('view-upload'),
            dashboard: document.getElementById('view-dashboard'),
        };
        this.state = { platformName: '' };
    }

    navigate(viewName) {
        if (!this.views[viewName]) return;
        Object.values(this.views).forEach(view => view.classList.remove('active'));
        this.views[viewName].classList.add('active');
        this.currentView = viewName;
        this.onViewChange(viewName);
    }

    onViewChange(viewName) {
        const navActions = document.getElementById('nav-actions');
        const mainNav = document.getElementById('main-nav');

        if (viewName === 'landing') {
            navActions.innerHTML = `<button class="btn btn-primary" onclick="window.router.navigate('upload')">Start Analysis</button>`;
        } else if (viewName === 'upload') {
            navActions.innerHTML = `<button class="btn" style="background: transparent; border: 1px solid var(--color-divider); color: var(--color-text);" onclick="window.router.navigate('landing')">Back</button>`;
        } else if (viewName === 'dashboard') {
            navActions.innerHTML = `<span style="margin-right: 16px; font-weight: 500;">Welcome, ${this.state.platformName || 'User'}</span><button class="btn btn-primary" onclick="window.router.navigate('upload')">New Analysis</button>`;
            mainNav.querySelector('.logo h2').innerText = `${this.state.platformName || 'Platform'} - Fraud Intelligence Dashboard`;
        }
    }
}

window.router = new Router();
window.router.navigate('landing');

export function setup() {
    console.log('VeriTurn App Initialized - AI CONNECTED');
    setupUploadForm();
}

function setupUploadForm() {
    const form = document.getElementById('upload-form');
    const dropzone = document.getElementById('csv-dropzone');
    const fileInput = document.getElementById('csv-file');
    const btnText = document.querySelector('#btn-generate .btn-text');
    const loader = document.querySelector('#btn-generate .loader');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

    ['dragenter', 'dragover'].forEach(eventName => dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false));
    ['dragleave', 'drop'].forEach(eventName => dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false));

    fileInput.addEventListener('change', function (e) {
        if (this.files && this.files.length > 0) {
            document.querySelector('.dropzone-text').textContent = this.files[0].name;
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const platformName = document.getElementById('platform-name').value;
        window.router.state.platformName = platformName;
        const file = fileInput.files[0];
        if (!file) { alert("Please select a CSV file!"); return; }

        btnText.textContent = 'Analyzing with AI Engine...';
        loader.classList.remove('hidden');

        const formData = new FormData();
        formData.append("file", file);

        try {
            // UPDATED: Ensuring the path exactly matches your working Render primary URL
            const response = await fetch("https://veriturn.onrender.com/upload", { 
                method: "POST", 
                body: formData 
            });
            
            if (!response.ok) throw new Error("Backend processing failed.");
            const result = await response.json();
            
            btnText.textContent = 'Generate AI Dashboard';
            loader.classList.add('hidden');
            window.router.navigate('dashboard');
            
            initializeDashboard(result);
        } catch (error) {
            console.error("Upload Error:", error);
            alert("Failed to connect to VeriTurn Cloud. Please check your internet connection and verify the backend is running.");
            btnText.textContent = 'Generate AI Dashboard';
            loader.classList.add('hidden');
        }
    });
}

function initializeDashboard(backendData) {
    if (backendData.charts) renderCharts(backendData.charts);
    
    if (backendData.table_data) {
        currentTableData = backendData.table_data;
        renderTable();
    }
    
    if (backendData.metrics) {
        const formatMoney = (num) => '₹' + num.toLocaleString('en-IN', { 
            minimumFractionDigits: 0, 
            maximumFractionDigits: 0 
        });
        
        document.getElementById('kpi-total').innerText = backendData.metrics.total_analyzed.toLocaleString('en-IN');
        document.getElementById('kpi-flagged').innerText = backendData.metrics.flagged_count.toLocaleString('en-IN');
        document.getElementById('kpi-loss').innerText = formatMoney(backendData.metrics.est_loss);
        document.getElementById('kpi-prevented').innerText = formatMoney(backendData.metrics.preventable_loss);
    }
}

function renderCharts(charts) {
    // FIXED: Synchronized with your working primary Render URL to fix broken images
    const baseUrl = "https://veriturn.onrender.com/"; 
    const timestamp = Date.now();
    const scatterContainer = document.getElementById('scatterChart');
    const barContainer = document.getElementById('barChart');

    if (scatterContainer && charts.cluster_scatter) {
        // Cache busting with timestamp ensures the latest graph is always pulled
        scatterContainer.innerHTML = `<img src="${baseUrl}${charts.cluster_scatter}?t=${timestamp}" style="width:100%; height:100%; object-fit:contain; border-radius:8px;" alt="Anomaly Clusters" />`;
    }
    if (barContainer && charts.risk_level) {
        barContainer.innerHTML = `<img src="${baseUrl}${charts.risk_level}?t=${timestamp}" style="width:100%; height:100%; object-fit:contain; border-radius:8px;" alt="Risk Distribution" />`;
    }
}

function renderTable() {
    const tbody = document.getElementById('table-body');
    const paginationControls = document.getElementById('table-pagination-controls');
    if (!tbody || !currentTableData.length) return;

    tbody.innerHTML = currentTableData.map(row => `
    <tr>
      <td style="font-weight: 500;">${row.id}</td>
      <td>${row.price}</td>
      <td>${row.window}</td>
      <td>
        <div style="display: flex; align-items: center; gap: 8px;">
          <div style="flex: 1; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden;">
            <div style="width: ${row.score}%; height: 100%; background: ${row.score > 80 ? 'var(--color-risk)' : 'var(--color-accent)'};"></div>
          </div>
          <span style="font-size: 0.85rem; font-weight: 600;">${row.score}</span>
        </div>
      </td>
      <td><span class="status-badge status-risk">${row.status}</span></td>
      <td class="reasoning-cell" style="font-size: 0.85rem; line-height: 1.4;">${row.reason}</td>
      <td>
        <button class="btn btn-small" 
                onclick="window.openReviewModal('${row.id}', ${row.score}, '${row.reason}', '${row.usp_policy}')" 
                style="color: var(--color-accent); border-color: var(--color-accent);">
            Review
        </button>
      </td>
    </tr>
  `).join('');

    if (paginationControls) {
        paginationControls.style.display = 'none';
    }
}

window.openReviewModal = function(id, score, reason, policyText) {
    const modal = document.getElementById('review-modal');
    if (!modal) return;

    document.getElementById('modal-user-id').innerText = `Analysis for ${id}`;
    document.getElementById('modal-risk-score').innerText = `${score}%`;
    document.getElementById('modal-risk-fill').style.width = `${score}%`;
    document.getElementById('modal-reasoning').innerText = reason;
    
    const policyEl = document.getElementById('modal-policy-text');
    if (policyEl) {
        policyEl.innerText = policyText;
    }
    
    const tag = score > 85 ? "Critical Anomaly" : "Suspicious Pattern";
    document.getElementById('modal-tag').innerText = tag;

    modal.classList.remove('hidden');
}

window.closeModal = function() {
    const modal = document.getElementById('review-modal');
    if (modal) modal.classList.add('hidden');
}

setup();