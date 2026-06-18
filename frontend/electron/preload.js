const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    printInvoice: () => ipcRenderer.invoke('print-invoice'),
    getAppVersion: () => ipcRenderer.invoke('get-app-version'),
    platform: process.platform,
});
