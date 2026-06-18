const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

const isDev = !app.isPackaged;

function getBackendPath() {
    if (isDev) {
        return null; // In dev, backend runs separately
    }
    // In production, the bundled Python executable is in resources
    return path.join(process.resourcesPath, 'backend', 'backend.exe');
}

function startBackend() {
    const backendPath = getBackendPath();
    if (!backendPath) {
        console.log('[Electron] Dev mode: backend should be running separately on port 8000');
        return;
    }

    console.log('[Electron] Starting backend:', backendPath);
    backendProcess = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        stdio: ['pipe', 'pipe', 'pipe'],
    });

    backendProcess.stdout.on('data', (data) => {
        console.log(`[Backend] ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
        console.error(`[Backend Error] ${data}`);
    });

    backendProcess.on('close', (code) => {
        console.log(`[Backend] Process exited with code ${code}`);
    });
}

function waitForBackend(url, retries = 30, delay = 500) {
    return new Promise((resolve, reject) => {
        const http = require('http');
        let attempts = 0;

        function tryConnect() {
            attempts++;
            http.get(url, (res) => {
                resolve();
            }).on('error', () => {
                if (attempts < retries) {
                    setTimeout(tryConnect, delay);
                } else {
                    reject(new Error('Backend did not start in time'));
                }
            });
        }

        tryConnect();
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1024,
        minHeight: 700,
        title: 'Techware BillSoft v2.0',
        icon: path.join(__dirname, 'icon.png'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
        show: false,
        backgroundColor: '#f8fafc',
    });

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    if (isDev) {
        mainWindow.loadURL('http://localhost:5173');
        mainWindow.webContents.openDevTools({ mode: 'detach' });
    } else {
        mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// IPC handlers
ipcMain.handle('print-invoice', async () => {
    if (mainWindow) {
        mainWindow.webContents.print({
            silent: false,
            printBackground: true,
            margins: { marginType: 'printableArea' },
        });
    }
});

ipcMain.handle('get-app-version', () => {
    return app.getVersion();
});

app.whenReady().then(async () => {
    startBackend();

    if (!isDev) {
        try {
            await waitForBackend('http://127.0.0.1:8000/health');
            console.log('[Electron] Backend is ready');
        } catch (err) {
            console.error('[Electron] Backend failed to start:', err.message);
        }
    }

    createWindow();
});

app.on('window-all-closed', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
    app.quit();
});

app.on('before-quit', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
