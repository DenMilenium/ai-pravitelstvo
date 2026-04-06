#!/usr/bin/env python3
"""
⚛️ Electron-Agent
Desktop агент на Electron + React

Создаёт:
- Electron приложения
- Main/Renderer процессы
- IPC коммуникацию
- Нативные модули
"""

import argparse
from pathlib import Path
from typing import Dict


class ElectronAgent:
    """
    ⚛️ Electron-Agent
    
    Специализация: Desktop на JavaScript
    Стек: Electron, React, Node.js
    """
    
    NAME = "⚛️ Electron-Agent"
    ROLE = "Electron Developer"
    EXPERTISE = ["Electron", "React", "Node.js", "IPC", "Desktop JS"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["package.json"] = """{
  "name": "electron-app",
  "version": "1.0.0",
  "description": "Electron Application",
  "main": "src/main.js",
  "scripts": {
    "start": "electron .",
    "dev": "concurrently \"npm run dev:vite\" \"wait-on http://localhost:5173 && electron .\"",
    "dev:vite": "vite",
    "build": "vite build",
    "dist": "electron-builder"
  },
  "dependencies": {
    "electron": "^28.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "concurrently": "^8.2.0",
    "electron-builder": "^24.9.0",
    "vite": "^5.0.0",
    "wait-on": "^7.2.0"
  },
  "build": {
    "appId": "com.example.electronapp",
    "productName": "Electron App",
    "directories": {
      "output": "dist-electron"
    },
    "files": [
      "src/**/*",
      "dist/**/*"
    ],
    "mac": {
      "target": "dmg"
    },
    "win": {
      "target": "nsis"
    },
    "linux": {
      "target": "AppImage"
    }
  }
}
"""
        
        files["src/main.js"] = """const { app, BrowserWindow, ipcMain, dialog, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hiddenInset',
    show: false
  });

  // Load app
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Create menu
  createMenu();
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Open',
          accelerator: 'CmdOrCtrl+O',
          click: async () => {
            const result = await dialog.showOpenDialog(mainWindow, {
              properties: ['openFile']
            });
            if (!result.canceled) {
              mainWindow.webContents.send('file-opened', result.filePaths[0]);
            }
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => app.quit()
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// IPC Handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('show-message-box', async (event, options) => {
  const result = await dialog.showMessageBox(mainWindow, options);
  return result;
});

ipcMain.handle('get-system-info', () => {
  return {
    platform: process.platform,
    arch: process.arch,
    version: process.version,
    electronVersion: process.versions.electron
  };
});

// App events
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
"""
        
        files["src/preload.js"] = """const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // App info
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
  
  // Dialogs
  showMessageBox: (options) => ipcRenderer.invoke('show-message-box', options),
  
  // File operations
  onFileOpened: (callback) => ipcRenderer.on('file-opened', callback),
  
  // Platform
  platform: process.platform
});
"""
        
        files["src/renderer/App.jsx"] = """import { useState, useEffect } from 'react';

function App() {
  const [systemInfo, setSystemInfo] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Get system info on mount
    window.electronAPI.getSystemInfo().then(setSystemInfo);

    // Listen for file open events
    window.electronAPI.onFileOpened((event, filePath) => {
      setMessage(`Opened: ${filePath}`);
    });
  }, []);

  const showMessage = async () => {
    const result = await window.electronAPI.showMessageBox({
      type: 'info',
      title: 'Message',
      message: 'Hello from Electron!',
      buttons: ['OK', 'Cancel']
    });
    setMessage(`Button clicked: ${result.response}`);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚛️ Electron + React</h1>
      </header>
      
      <main className="app-main">
        {systemInfo && (
          <div className="info-card">
            <h3>System Info</h3>
            <p>Platform: {systemInfo.platform}</p>
            <p>Arch: {systemInfo.arch}</p>
            <p>Electron: {systemInfo.electronVersion}</p>
          </div>
        )}
        
        <button onClick={showMessage}>Show Message</button>
        
        {message && <p className="message">{message}</p>}
      </main>
    </div>
  );
}

export default App;
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="⚛️ Electron-Agent — Desktop JS")
    parser.add_argument("request", nargs="?", help="Что разработать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = ElectronAgent()
    
    if args.request:
        print(f"⚛️ {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"⚛️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
