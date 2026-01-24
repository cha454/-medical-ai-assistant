/**
 * Panneau de Debug Visuel
 * Affiche les logs directement sur la page
 */

// Créer le panneau de debug
function createDebugPanel() {
    const panel = document.createElement('div');
    panel.id = 'debug-panel';
    panel.style.cssText = `
        position: fixed;
        top: 80px;
        right: 10px;
        width: 350px;
        max-height: 250px;
        background: rgba(0, 0, 0, 0.95);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 12px;
        color: #fff;
        font-family: monospace;
        font-size: 11px;
        overflow-y: auto;
        z-index: 10000;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    `;

    const title = document.createElement('div');
    title.style.cssText = `
        font-weight: bold;
        margin-bottom: 8px;
        color: #3b82f6;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    title.innerHTML = `
        <span>🔍 Debug Vocal</span>
        <button onclick="clearDebugPanel()" style="
            background: #ef4444;
            border: none;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 10px;
        ">Effacer</button>
    `;

    const logs = document.createElement('div');
    logs.id = 'debug-logs';
    logs.style.cssText = `
        max-height: 250px;
        overflow-y: auto;
    `;

    panel.appendChild(title);
    panel.appendChild(logs);
    document.body.appendChild(panel);

    console.log('✅ Panneau de debug créé');
}

// Ajouter un log au panneau
function addDebugLog(message, type = 'info') {
    const logs = document.getElementById('debug-logs');
    if (!logs) return;

    const logEntry = document.createElement('div');
    logEntry.style.cssText = `
        padding: 4px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    `;

    let color = '#fff';
    if (type === 'success') color = '#22c55e';
    if (type === 'error') color = '#ef4444';
    if (type === 'warning') color = '#fbbf24';
    if (type === 'info') color = '#3b82f6';

    const time = new Date().toLocaleTimeString();
    logEntry.innerHTML = `<span style="color: #666">${time}</span> <span style="color: ${color}">${message}</span>`;

    logs.appendChild(logEntry);
    logs.scrollTop = logs.scrollHeight;

    // Limiter à 50 logs
    if (logs.children.length > 50) {
        logs.removeChild(logs.firstChild);
    }
}

// Effacer les logs
function clearDebugPanel() {
    const logs = document.getElementById('debug-logs');
    if (logs) {
        logs.innerHTML = '';
        addDebugLog('Logs effacés', 'info');
    }
}

// Intercepter console.log
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;

console.log = function (...args) {
    originalLog.apply(console, args);
    const message = args.join(' ');
    if (message.includes('🎤') || message.includes('📝') || message.includes('✅') ||
        message.includes('❌') || message.includes('📤') || message.includes('🔊') ||
        message.includes('📬') || message.includes('🌐')) {
        addDebugLog(message, 'info');
    }
};

console.error = function (...args) {
    originalError.apply(console, args);
    const message = args.join(' ');
    addDebugLog('❌ ' + message, 'error');
};

console.warn = function (...args) {
    originalWarn.apply(console, args);
    const message = args.join(' ');
    addDebugLog('⚠️ ' + message, 'warning');
};

// Créer le panneau au chargement
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createDebugPanel);
} else {
    createDebugPanel();
}

// Message de bienvenue
setTimeout(() => {
    addDebugLog('🔍 Panneau de debug activé', 'success');
    addDebugLog('Cliquez sur 🎤 et parlez pour voir les logs', 'info');
}, 1000);
