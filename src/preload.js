// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRenderer } = require('electron');

// Enable electron remote to be accessible from within application

contextBridge.exposeInMainWorld('ipc', {
    chooseFiles: options => ipcRenderer.invoke('choose-files', options)
});
