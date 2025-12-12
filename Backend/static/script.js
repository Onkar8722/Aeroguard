// Global variables
let alerts = [];
let matchCount = 0;
let isStreaming = false;
let selectedCamera = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ========== INITIALIZATION ==========
async function initializeApp() {
    console.log('Initializing AERO application...');
    
    // Load cameras
    await loadCameras();
    
    // Check system status
    await checkSystemStatus();
    
    // Setup event listeners
    setupEventListeners();
    
    console.log('Application initialized');
}

// ========== EVENT LISTENERS ==========
function setupEventListeners() {
    // Upload form
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', handleUpload);
    
    // Drag and drop
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => e.preventDefault());
    uploadArea.addEventListener('drop', handleDrop);
    
    // Threshold slider
    const threshold = document.getElementById('threshold');
    threshold.addEventListener('input', (e) => {
        document.getElementById('thresholdValue').textContent = e.target.value + '%';
    });
}

// ========== CAMERA FUNCTIONS ==========
async function loadCameras() {
    try {
        const response = await fetch('/api/cameras');
        const data = await response.json();
        
        const cameras = data.cameras || [];
        console.log('Available cameras:', cameras);
        
        // Update stat
        document.getElementById('activeCameras').textContent = cameras.length;
        
        // Populate dropdown
        const cameraSelect = document.getElementById('cameraSelect');
        cameras.forEach(cam => {
            const option = document.createElement('option');
            option.value = cam;
            option.textContent = cam.toUpperCase();
            cameraSelect.appendChild(option);
        });
        
        // Auto-select first camera
        if (cameras.length > 0) {
            cameraSelect.value = cameras[0];
            switchCamera(cameras[0]);
        }
    } catch (error) {
        console.error('Error loading cameras:', error);
        addAlert('Error loading cameras', 'error');
    }
}

function switchCamera(camId) {
    if (!camId) {
        document.getElementById('feedStatus').textContent = 'Select a camera to start streaming...';
        return;
    }
    
    selectedCamera = camId;
    const cameraFeed = document.getElementById('cameraFeed');
    cameraFeed.src = `/api/stream/${camId}`;
    cameraFeed.style.display = 'block';
    document.getElementById('feedStatus').style.display = 'none';
    isStreaming = true;
}

function startSurveillance() {
    if (selectedCamera) {
        switchCamera(selectedCamera);
        addAlert('Surveillance started', 'success');
    } else {
        addAlert('Please select a camera first', 'error');
    }
}

function stopSurveillance() {
    const cameraFeed = document.getElementById('cameraFeed');
    cameraFeed.src = '';
    cameraFeed.style.display = 'none';
    document.getElementById('feedStatus').style.display = 'block';
    isStreaming = false;
    addAlert('Surveillance stopped', 'success');
}

// ========== FILE UPLOAD ==========
function handleDrop(e) {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById('fileInput').files = files;
    }
}

async function handleUpload(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        addAlert('Please select an image', 'error');
        return;
    }
    
    if (!file.type.startsWith('image/')) {
        addAlert('Please select a valid image file', 'error');
        return;
    }
    
    // Show loading state
    const uploadStatus = document.getElementById('uploadStatus');
    uploadStatus.textContent = 'Analyzing image...';
    uploadStatus.className = 'upload-status';
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/upload_suspicious', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const matches = result.matches || [];
            matchCount += matches.length;
            document.getElementById('matchCount').textContent = matchCount;
            
            if (matches.length > 0) {
                addAlert(`Found ${matches.length} face match(es)!`, 'success');
                showMatchesModal(matches);
            } else {
                addAlert('No matches found in database', 'warning');
            }
            
            uploadStatus.textContent = `Analysis complete: ${matches.length} matches`;
            uploadStatus.className = 'upload-status success';
        } else {
            addAlert(result.error || 'Upload failed', 'error');
            uploadStatus.className = 'upload-status error';
            uploadStatus.textContent = 'Upload failed';
        }
        
        // Clear input
        fileInput.value = '';
        
    } catch (error) {
        console.error('Upload error:', error);
        addAlert('Error uploading image', 'error');
        uploadStatus.className = 'upload-status error';
        uploadStatus.textContent = 'Error uploading image';
    }
}

// ========== ALERTS ==========
function addAlert(message, type = 'info') {
    const alertsList = document.getElementById('alertsList');
    
    // Remove "no alerts" message
    const noAlerts = alertsList.querySelector('.no-alerts');
    if (noAlerts) noAlerts.remove();
    
    const alert = document.createElement('div');
    alert.className = `alert-item ${type === 'error' ? 'warning' : ''}`;
    
    const now = new Date();
    const time = now.toLocaleTimeString();
    
    alert.innerHTML = `
        <div class="alert-message">${message}</div>
        <div class="alert-time">${time}</div>
    `;
    
    alertsList.insertBefore(alert, alertsList.firstChild);
    
    // Update alert count
    document.getElementById('alertCount').textContent = alertsList.children.length;
    
    // Keep only last 10 alerts
    const items = alertsList.querySelectorAll('.alert-item');
    if (items.length > 10) {
        items[items.length - 1].remove();
    }
    
    // Auto-remove after 5 seconds for info alerts
    if (type === 'info') {
        setTimeout(() => alert.remove(), 5000);
    }
}

// ========== MODAL ==========
function showMatchesModal(matches) {
    const modal = document.getElementById('matchesModal');
    const matchesList = document.getElementById('matchesList');
    
    matchesList.innerHTML = '';
    matches.forEach((match, index) => {
        const matchDiv = document.createElement('div');
        matchDiv.className = 'match-item';
        
        const confidence = Math.round((1 - match.distance) * 100);
        
        matchDiv.innerHTML = `
            <h3>Match #${index + 1}</h3>
            <div class="match-info">
                <p><strong>URN:</strong> ${match.urn}</p>
                <p><strong>Confidence:</strong> ${confidence}%</p>
                <p><strong>Distance:</strong> ${match.distance.toFixed(3)}</p>
            </div>
        `;
        
        matchesList.appendChild(matchDiv);
    });
    
    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('matchesModal').classList.add('hidden');
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('matchesModal');
    if (e.target === modal) {
        closeModal();
    }
});

// ========== SYSTEM STATUS ==========
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'running') {
            updateStatusBadge('ONLINE', false);
            addAlert('System online and ready', 'info');
        }
    } catch (error) {
        console.error('Status check error:', error);
        updateStatusBadge('OFFLINE', true);
    }
}

function updateStatusBadge(status, offline = false) {
    const badge = document.getElementById('systemStatus');
    badge.textContent = status;
    if (offline) {
        badge.classList.add('offline');
    } else {
        badge.classList.remove('offline');
    }
}

// Periodically check system status
setInterval(checkSystemStatus, 30000);
