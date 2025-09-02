// Global variables
let entries = [];
let moodChart = null;
let trendChart = null;
let currentEmotionData = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupDarkMode();
    setupEmotionAnalysis();
    setupAuth();
    loadEntries();
    loadStats();
});

// Navigation functionality
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const targetId = this.getAttribute('href').substring(1);
            showSection(targetId);
        });
    });
}

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// Simple auth using localStorage
function setupAuth() {
    const storedUser = JSON.parse(localStorage.getItem('mj_user') || 'null');
    const welcomeBanner = document.getElementById('welcomeBanner');
    const welcomeText = document.getElementById('welcomeText');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginForm = document.getElementById('loginForm');

    function renderAuth(user) {
        if (user) {
            welcomeText.textContent = `Welcome, ${user.name}!`;
            welcomeBanner.style.display = 'flex';
        } else {
            welcomeBanner.style.display = 'none';
        }
    }

    if (storedUser) {
        renderAuth(storedUser);
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('loginName').value.trim();
            const email = document.getElementById('loginEmail').value.trim();
            if (!name || !email) {
                showError('Please provide both name and email.');
                return;
            }
            const user = { name, email };
            localStorage.setItem('mj_user', JSON.stringify(user));
            renderAuth(user);
            showSection('new-entry');
            showSuccess(`Welcome, ${name}!`);
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('mj_user');
            renderAuth(null);
            showSection('login');
            showSuccess('Logged out successfully.');
        });
    }
}

// Dark mode functionality
function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Load saved preference
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'true') {
        body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    });
}

// Emotion analysis functionality
function setupEmotionAnalysis() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const saveBtn = document.getElementById('saveBtn');
    const journalForm = document.getElementById('journalForm');
    
    analyzeBtn.addEventListener('click', function() {
        const content = document.getElementById('content').value.trim();
        if (!content) {
            showError('Please enter some text to analyze.');
            return;
        }
        
        analyzeEmotion(content);
    });
    
    journalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!currentEmotionData) {
            showError('Please analyze your emotion first.');
            return;
        }
        
        saveEntry();
    });
}

async function analyzeEmotion(content) {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const emotionResult = document.getElementById('emotionResult');
    const emotionLabel = document.getElementById('emotionLabel');
    const emotionScore = document.getElementById('emotionScore');
    const emotionDescription = document.getElementById('emotionDescription');
    
    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    emotionResult.style.display = 'block';
    emotionLabel.textContent = 'Analyzing...';
    emotionScore.textContent = '0%';
    emotionDescription.textContent = 'Processing your text...';
    
    try {
        const response = await fetch('/api/ai/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentEmotionData = data;
            
            // Update emotion display
            const emotion = data.emotion_label || 'neutral';
            const score = Math.round((data.sentiment_score || 0.5) * 100);
            const emotionDisplay = emotion.charAt(0).toUpperCase() + emotion.slice(1);
            
            emotionLabel.textContent = emotionDisplay;
            emotionScore.textContent = `${score}%`;
            
            // Set emotion description
            const descriptions = {
                'positive': 'You seem to be in a positive mood! Keep up the great energy.',
                'neutral': 'You appear to be feeling balanced and calm today.',
                'negative': 'It looks like you might be having a challenging day. Remember, it\'s okay to feel this way.'
            };
            
            emotionDescription.textContent = descriptions[emotion] || 'Your emotion has been analyzed successfully.';
            
            // Enable save button
            document.getElementById('saveBtn').disabled = false;
            
            showSuccess('Emotion analyzed successfully!');
            
        } else {
            throw new Error('Failed to analyze emotion');
        }
        
    } catch (error) {
        console.error('Error analyzing emotion:', error);
        showError('Failed to analyze emotion. Please try again.');
        
        // Reset emotion result
        emotionResult.style.display = 'none';
        currentEmotionData = null;
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-brain"></i> Analyze Emotion';
    }
}

async function saveEntry() {
    const content = document.getElementById('content').value.trim();
    const saveBtn = document.getElementById('saveBtn');
    
    if (!content || !currentEmotionData) {
        showError('Please enter content and analyze emotion first.');
        return;
    }
    
    // Show loading state
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    
    try {
        const response = await fetch('/api/entries', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
                emotion_label: currentEmotionData.emotion_label,
                sentiment_score: currentEmotionData.sentiment_score,
                ai_provider: currentEmotionData.ai_provider || 'huggingface',
                detailed_analysis: currentEmotionData.detailed_analysis
            })
        });
        
        if (response.ok) {
            const newEntry = await response.json();
            entries.unshift(newEntry);
            
            // Clear form
            document.getElementById('content').value = '';
            document.getElementById('emotionResult').style.display = 'none';
            currentEmotionData = null;
            saveBtn.disabled = true;
            
            // Update displays
            updateEntriesList();
            loadStats();
            
            showSuccess('Entry saved successfully!');
            
        } else {
            throw new Error('Failed to save entry');
        }
        
    } catch (error) {
        console.error('Error saving entry:', error);
        showError('Failed to save entry. Please try again.');
    } finally {
        // Reset button state
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Save Entry';
    }
}

// Load and display entries
async function loadEntries() {
    try {
        const response = await fetch('/api/entries');
        if (response.ok) {
            entries = await response.json();
            updateEntriesList();
        }
    } catch (error) {
        console.error('Error loading entries:', error);
        showError('Failed to load entries.');
    }
}

function updateEntriesList() {
    const entriesList = document.getElementById('entriesList');
    if (!entriesList) return;
    
    if (entries.length === 0) {
        entriesList.innerHTML = '<div class="loading">No entries yet. Start journaling to see your mood patterns!</div>';
        return;
    }

    entriesList.innerHTML = entries.map(entry => {
        // Convert sentiment score to percentage
        const scorePercentage = Math.round((entry.sentiment_score || 0.5) * 100);
        
        // Get emotion with better formatting
        const emotion = entry.emotion_label || 'neutral';
        const emotionDisplay = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        
        // Get emotion color class
        const emotionClass = `emotion-${emotion}`;
        
        // Use the correct timestamp field
        const timestamp = entry.timestamp || entry.created_at;
        
        return `
            <div class="entry-item">
                <div class="entry-header">
                    <div class="entry-meta">
                        <span class="emotion-badge ${emotionClass}">
                            ${emotionDisplay}: ${scorePercentage}%
                        </span>
                        <span class="ai-provider-badge">${entry.ai_provider || 'huggingface'}</span>
                        <span class="entry-timestamp">${formatDate(timestamp)}</span>
                    </div>
                    <button class="btn btn-danger" onclick="deleteEntry(${entry.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="entry-content">${entry.content}</div>
                ${entry.detailed_analysis ? `<div class="entry-analysis">${entry.detailed_analysis}</div>` : ''}
            </div>
        `;
    }).join('');
}

// Load and display statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        if (response.ok) {
            const stats = await response.json();
            updateStatsDisplay(stats);
            updateCharts(stats);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function updateStatsDisplay(stats) {
    const statsGrid = document.getElementById('statsGrid');
    if (!statsGrid) return;
    
    // Ensure we have emotion counts, default to empty object if not
    const emotionCounts = stats.emotion_counts || {};
    
    statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-number">${stats.total_entries || 0}</div>
            <div class="stat-label">Total Entries</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${emotionCounts.positive || 0}</div>
            <div class="stat-label">Happy Days</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${emotionCounts.neutral || 0}</div>
            <div class="stat-label">Neutral Days</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${emotionCounts.negative || 0}</div>
            <div class="stat-label">Sad Days</div>
        </div>
    `;
}

function updateCharts(stats) {
    if (stats) {
        updateMoodChart(stats.emotion_counts);
        updateTrendChart(stats.trend_data);
    }
}

function updateMoodChart(emotionCounts) {
    const ctx = document.getElementById('moodChart');
    if (!ctx) return;
    
    if (moodChart) {
        moodChart.destroy();
    }

    const colors = {
        positive: '#28a745',
        neutral: '#6c757d',
        negative: '#dc3545'
    };

    moodChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(emotionCounts).map(emotion => 
                emotion.charAt(0).toUpperCase() + emotion.slice(1)
            ),
            datasets: [{
                data: Object.values(emotionCounts),
                backgroundColor: Object.keys(emotionCounts).map(emotion => colors[emotion]),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateTrendChart(trendData) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;
    
    if (trendChart) {
        trendChart.destroy();
    }

    trendChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: trendData.map(item => item.date),
            datasets: [{
                label: 'Mood Score',
                data: trendData.map(item => item.score),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Delete entry functionality
async function deleteEntry(entryId) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }

    try {
        const response = await fetch(`/api/entries/${entryId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            entries = entries.filter(entry => entry.id !== entryId);
            updateEntriesList();
            loadStats();
            showSuccess('Entry deleted successfully!');
        } else {
            throw new Error('Failed to delete entry');
        }
    } catch (error) {
        console.error('Error deleting entry:', error);
        showError('Failed to delete entry.');
    }
}

// Payment modal functionality
function showPaymentModal(plan) {
    const planNames = {
        'basic': 'Basic Plan ($5.99/month)',
        'premium': 'Premium Plan ($12.99/month)',
        'pro': 'Pro Plan ($24.99/month)'
    };
    
    const planAmount = getPlanAmount(plan);
    
    if (confirm(`Would you like to subscribe to ${planNames[plan]}?`)) {
        initiatePayment(plan, planAmount);
    }
}

function getPlanAmount(plan) {
    const amounts = {
        'basic': 5.99,
        'premium': 12.99,
        'pro': 24.99
    };
    return amounts[plan] || 5.99;
}

async function initiatePayment(plan, amount) {
    try {
        const response = await fetch('/api/payment/initiate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                plan_type: plan,
                amount: amount
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            showSuccess('Payment initiated! Redirecting to payment gateway...');
            
            // In a real app, you would redirect to the payment URL
            setTimeout(() => {
                alert('Payment simulation complete! In a real app, you would be redirected to IntaSend.');
            }, 2000);
            
        } else {
            throw new Error('Payment initiation failed');
        }
    } catch (error) {
        console.error('Payment error:', error);
        showError('Payment initiation failed. Please try again.');
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function showSuccess(message) {
    const successMessage = document.getElementById('successMessage');
    successMessage.textContent = message;
    successMessage.style.display = 'flex';
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 3000);
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

// Export functions for global access
window.deleteEntry = deleteEntry;
window.showPaymentModal = showPaymentModal;
