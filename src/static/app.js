// Mode switching
const modeBtns = document.querySelectorAll('.mode-btn');
const modeContents = document.querySelectorAll('.mode-content');

modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;

        // Update buttons
        modeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update content
        modeContents.forEach(content => content.classList.remove('active'));
        document.getElementById(`${mode}-mode`).classList.add('active');

        // Clear results
        hideResults();
    });
});

// Upload Mode
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const reviewBtn = document.getElementById('review-btn');
let selectedFile = null;

// Make Upload File button trigger file selection
modeBtns.forEach(btn => {
    if (btn.dataset.mode === 'upload') {
        btn.addEventListener('click', (e) => {
            if (btn.classList.contains('active')) {
                // If already active, trigger file selection
                fileInput.click();
            }
        });
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    fileInfo.innerHTML = `
        <span>📄 ${file.name}</span>
        <span style="color: var(--text-secondary);">${formatFileSize(file.size)}</span>
    `;
    fileInfo.classList.remove('hidden');
    reviewBtn.classList.remove('hidden');
}

reviewBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    showLoading('Agents are analyzing your code...');

    try {
        const response = await fetch('/api/review/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Analysis failed');
        }

        showResults(data.report, selectedFile.name);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

// GitHub Mode
const repoUrlInput = document.getElementById('repo-url');
const fetchBtn = document.getElementById('fetch-btn');
const fileList = document.getElementById('file-list');
const filesContainer = document.getElementById('files-container');
const analyzeBtn = document.getElementById('analyze-btn');
let repoFiles = [];

fetchBtn.addEventListener('click', async () => {
    const repoUrl = repoUrlInput.value.trim();

    if (!repoUrl) {
        showError('Please enter a repository URL');
        return;
    }

    showLoading('Fetching repository...');

    try {
        const response = await fetch(`/api/files/list?repo_url=${encodeURIComponent(repoUrl)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to fetch repository');
        }

        repoFiles = data.files;
        displayFiles(data.files);
        fileList.classList.remove('hidden');
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

function displayFiles(files) {
    if (files.length === 0) {
        filesContainer.innerHTML = '<p style="color: var(--text-secondary);">No Python files found</p>';
        return;
    }

    filesContainer.innerHTML = files.map((file, index) => `
        <div class="file-item">
            <input type="checkbox" id="file-${index}" ${index < 5 ? 'checked' : ''}>
            <label for="file-${index}">
                <span>${file.path}</span>
                <span class="file-size">${formatFileSize(file.size)}</span>
            </label>
        </div>
    `).join('');
}

analyzeBtn.addEventListener('click', async () => {
    const checkboxes = filesContainer.querySelectorAll('input[type="checkbox"]:checked');
    const selectedFiles = Array.from(checkboxes).map((cb, index) => {
        const fileIndex = parseInt(cb.id.replace('file-', ''));
        return repoFiles[fileIndex].path;
    });

    if (selectedFiles.length === 0) {
        showError('Please select at least one file');
        return;
    }

    const repoUrl = repoUrlInput.value.trim();
    showLoading(`Analyzing ${selectedFiles.length} file(s)...`);

    try {
        const formData = new FormData();
        formData.append('repo_url', repoUrl);
        formData.append('selected_files', selectedFiles.join(','));

        const response = await fetch('/api/review/github', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Analysis failed');
        }

        showResults(data.report, `GitHub Repository (${selectedFiles.length} files)`);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

// Results
const resultsSection = document.getElementById('results-section');
const resultsContent = document.getElementById('results-content');
const downloadBtn = document.getElementById('download-btn');
let currentReport = '';
let currentFilename = '';

function showResults(report, filename) {
    currentReport = report;
    currentFilename = filename;

    // Convert markdown to HTML (simple implementation)
    const html = markdownToHTML(report);
    resultsContent.innerHTML = html;
    resultsSection.classList.remove('hidden');

    // Hide file list when results are shown
    fileList.classList.add('hidden');

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function hideResults() {
    resultsSection.classList.add('hidden');
    currentReport = '';
    currentFilename = '';
}

downloadBtn.addEventListener('click', () => {
    const blob = new Blob([currentReport], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentFilename.replace('.py', '')}_review.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// Loading
const loadingOverlay = document.getElementById('loading-overlay');
const loadingText = document.getElementById('loading-text');
let loadingInterval = null;

const agents = [
    '🔍 Code Analyst Agent analyzing...',
    '🛡️ Security Expert Agent reviewing...',
    '⚡ Performance Optimizer Agent checking...',
    '📝 Documentation Specialist Agent inspecting...',
    '✅ Quality Assurance Agent validating...'
];

function showLoading(message) {
    let currentIndex = 0;
    loadingText.textContent = agents[0];
    loadingOverlay.classList.remove('hidden');

    // Rotate through agent messages
    loadingInterval = setInterval(() => {
        currentIndex = (currentIndex + 1) % agents.length;
        loadingText.textContent = agents[currentIndex];
    }, 3000); // Change every 3 seconds
}

function hideLoading() {
    if (loadingInterval) {
        clearInterval(loadingInterval);
        loadingInterval = null;
    }
    loadingOverlay.classList.add('hidden');
}

// Utilities
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function showError(message) {
    alert('Error: ' + message);
}

function markdownToHTML(markdown) {
    let html = markdown;

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Code blocks
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

    // Inline code
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Lists
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Line breaks
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');

    return html;
}
