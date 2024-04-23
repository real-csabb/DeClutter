const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  startFlask();
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Open the DevTools.
  mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
const startFlask = () => {
  PythonShell.run('api.py', {
    scriptPath: '/Users/csabb/unc_asheville/csci_480_capstone/Secret_DeClutterGPT/src/NLP',
    pythonPath: '/Users/csabb/unc_asheville/csci_480_capstone/Secret_DeClutterGPT/src/NLP/venv/bin/python3' // Specify the path to your Python executable
  }).then(messages => {
    console.log(messages);
    console.log('finished');
  });
};

// Make the dialog work or something idk anymore
ipcMain.handle('choose-files', async (event, options) => {
  return dialog.showOpenDialog(options);
});
//const showOpenDialog = options => dialog.showOpenDialog(options);

// // Organize library code
// const organizeLibrary = () => {
//   fetch('http://127.0.0.1:3000/categories').then(
//       response => response.json()
//   ).then(
//       responseText => console.log(responseText)
//   );
// };
