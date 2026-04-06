#!/usr/bin/env python3
"""
🧩 Plugin-Agent
Plugin/Extension Developer агент

Создаёт:
- VS Code extensions
- Chrome extensions
- IDE plugins
"""

import argparse
from pathlib import Path
from typing import Dict


class PluginAgent:
    """
    🧩 Plugin-Agent
    
    Специализация: Plugin/Extension Development
    Платформы: VS Code, Chrome, JetBrains
    """
    
    NAME = "🧩 Plugin-Agent"
    ROLE = "Extension Developer"
    EXPERTISE = ["VS Code Extensions", "Chrome Extensions", "Plugins", "Add-ons"]
    
    def process_request(self, request: str, platform: str = "vscode") -> Dict[str, str]:
        files = {}
        
        if platform == "chrome":
            files = self._generate_chrome_extension(request)
        else:
            files = self._generate_vscode_extension(request)
        
        return files
    
    def _generate_vscode_extension(self, feature: str) -> Dict[str, str]:
        files = {}
        
        files["package.json"] = """{
  "name": "my-extension",
  "displayName": "My Extension",
  "description": "VS Code extension created by Plugin-Agent",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": [
    "Other"
  ],
  "activationEvents": [
    "onCommand:myextension.helloWorld"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "myextension.helloWorld",
        "title": "Hello World",
        "category": "My Extension"
      },
      {
        "command": "myextension.showInfo",
        "title": "Show Info",
        "category": "My Extension"
      }
    ],
    "menus": {
      "commandPalette": [
        {
          "command": "myextension.helloWorld",
          "when": "editorTextFocus"
        }
      ],
      "editor/context": [
        {
          "command": "myextension.helloWorld",
          "group": "navigation"
        }
      ]
    },
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myextension.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable/disable extension"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.80.0",
    "@types/node": "20.x",
    "typescript": "^5.0.0"
  }
}
"""
        
        files["extension.ts"] = """import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension is now active!');

    // Register Hello World command
    let disposable = vscode.commands.registerCommand('myextension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from My Extension!');
    });
    context.subscriptions.push(disposable);

    // Register Show Info command
    let showInfo = vscode.commands.registerCommand('myextension.showInfo', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            const selection = editor.selection;
            const text = document.getText(selection);
            
            vscode.window.showInformationMessage(`Selected text: ${text || 'None'}`);
        }
    });
    context.subscriptions.push(showInfo);

    // Register status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = "$(plug) My Extension";
    statusBarItem.tooltip = "My Extension is active";
    statusBarItem.command = 'myextension.helloWorld';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register hover provider
    const hoverProvider = vscode.languages.registerHoverProvider(
        { pattern: '**/*' },
        {
            provideHover(document, position) {
                const range = document.getWordRangeAtPosition(position);
                const word = document.getText(range);
                
                if (word.length > 0) {
                    return new vscode.Hover(`Word: **${word}**`);
                }
            }
        }
    );
    context.subscriptions.push(hoverProvider);
}

export function deactivate() {
    console.log('Extension deactivated');
}
"""
        
        files["tsconfig.json"] = """{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "lib": ["ES2020"],
    "outDir": "out",
    "rootDir": ".",
    "sourceMap": true,
    "strict": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
"""
        
        return files
    
    def _generate_chrome_extension(self, feature: str) -> Dict[str, str]:
        files = {}
        
        files["manifest.json"] = """{
  "manifest_version": 3,
  "name": "My Chrome Extension",
  "version": "1.0.0",
  "description": "Chrome extension created by Plugin-Agent",
  "permissions": [
    "storage",
    "activeTab",
    "scripting"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["content.css"]
    }
  ],
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
"""
        
        files["popup.html"] = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      width: 300px;
      padding: 10px;
      font-family: Arial, sans-serif;
    }
    button {
      width: 100%;
      padding: 10px;
      margin: 5px 0;
      cursor: pointer;
      background: #4285f4;
      color: white;
      border: none;
      border-radius: 4px;
    }
    button:hover {
      background: #3367d6;
    }
  </style>
</head>
<body>
  <h2>My Extension</h2>
  <button id="btn-action">Perform Action</button>
  <button id="btn-info">Get Info</button>
  <script src="popup.js"></script>
</body>
</html>
"""
        
        files["popup.js"] = """document.getElementById('btn-action').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: performAction
  });
});

document.getElementById('btn-info').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: getPageInfo
  });
});

function performAction() {
  alert('Action performed!');
}

function getPageInfo() {
  const info = {
    url: window.location.href,
    title: document.title,
    domain: window.location.hostname
  };
  console.log('Page info:', info);
  alert(`Title: ${info.title}\\nURL: ${info.url}`);
}
"""
        
        files["background.js"] = """chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
  
  // Set default settings
  chrome.storage.sync.set({
    enabled: true,
    theme: 'light'
  });
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getData') {
    chrome.storage.sync.get('data', (result) => {
      sendResponse(result.data);
    });
    return true; // Keep message channel open for async
  }
});
"""
        
        files["content.js"] = """console.log('Content script loaded');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'highlight') {
    highlightElements();
  }
});

function highlightElements() {
  const paragraphs = document.querySelectorAll('p');
  paragraphs.forEach(p => {
    p.style.backgroundColor = 'yellow';
  });
}

// Add custom styles
const style = document.createElement('style');
style.textContent = `
  .my-extension-highlight {
    background-color: #ffff00 !important;
  }
`;
document.head.appendChild(style);
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🧩 Plugin-Agent — Extensions")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--platform", "-p", default="vscode", choices=["vscode", "chrome"])
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = PluginAgent()
    
    if args.request:
        print(f"🧩 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request, args.platform)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🧩 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
