#!/usr/bin/env python3
"""
🍎 Cocoa-Agent
macOS Native App Specialist

Нативные приложения для macOS на Swift и AppKit.
"""

import argparse
from pathlib import Path
from typing import Dict


class CocoaAgent:
    """
    🍎 Cocoa-Agent
    
    Специализация: macOS Native Development
    Задачи: AppKit, SwiftUI, macOS apps
    """
    
    NAME = "🍎 Cocoa-Agent"
    ROLE = "macOS Developer"
    EXPERTISE = ["Swift", "AppKit", "Cocoa", "macOS", "Xcode"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "AppDelegate.swift": self._generate_app_delegate(),
            "ViewController.swift": self._generate_viewcontroller(),
            "Main.storyboard": self._generate_storyboard(),
            "ContentView.swift": self._generate_swiftui_view(),
            "Info.plist": self._generate_info_plist()
        }
    
    def _generate_app_delegate(self) -> str:
        return '''import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {

    @IBOutlet var window: NSWindow!

    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Initialize app
        setupWindow()
        setupMenu()
    }

    func applicationWillTerminate(_ aNotification: Notification) {
        // Clean up
    }

    func applicationSupportsSecureRestorableState(_ app: NSApplication) -> Bool {
        return true
    }

    private func setupWindow() {
        window.title = "My macOS App"
        window.minSize = NSSize(width: 800, height: 600)
        
        // Center window
        window.center()
    }

    private func setupMenu() {
        // Additional menu setup if needed
    }
}
'''
    
    def _generate_viewcontroller(self) -> str:
        return '''import Cocoa

class ViewController: NSViewController {

    @IBOutlet weak var tableView: NSTableView!
    @IBOutlet weak var searchField: NSSearchField!
    
    var data: [String] = []
    var filteredData: [String] = []

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        loadData()
    }

    private func setupUI() {
        // Configure table view
        tableView.delegate = self
        tableView.dataSource = self
        
        // Configure search field
        searchField.target = self
        searchField.action = #selector(performSearch)
    }

    private func loadData() {
        data = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        filteredData = data
        tableView.reloadData()
    }

    @objc private func performSearch() {
        let query = searchField.stringValue.lowercased()
        
        if query.isEmpty {
            filteredData = data
        } else {
            filteredData = data.filter { $0.lowercased().contains(query) }
        }
        
        tableView.reloadData()
    }
}

// MARK: - NSTableViewDataSource
extension ViewController: NSTableViewDataSource {
    func numberOfRows(in tableView: NSTableView) -> Int {
        return filteredData.count
    }
}

// MARK: - NSTableViewDelegate
extension ViewController: NSTableViewDelegate {
    func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
        let cell = tableView.makeView(withIdentifier: NSUserInterfaceItemIdentifier("Cell"), owner: nil) as? NSTableCellView
        cell?.textField?.stringValue = filteredData[row]
        return cell
    }
}
'''
    
    def _generate_swiftui_view(self) -> str:
        return '''import SwiftUI

struct ContentView: View {
    @State private var items: [Item] = []
    @State private var searchText = ""
    @State private var selectedItem: Item?
    
    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.name.localizedCaseInsensitiveContains(searchText) }
    }
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(filteredItems, selection: $selectedItem) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .searchable(text: $searchText)
            .navigationTitle("My App")
            .toolbar {
                ToolbarItem {
                    Button(action: addItem) {
                        Label("Add", systemImage: "plus")
                    }
                }
            }
        } detail: {
            // Detail
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                Text("Select an item")
                    .foregroundStyle(.secondary)
            }
        }
    }
    
    private func addItem() {
        let newItem = Item(name: "New Item \(items.count + 1)")
        items.append(newItem)
    }
}

struct Item: Identifiable, Hashable {
    let id = UUID()
    var name: String
}

struct ItemRow: View {
    let item: Item
    
    var body: some View {
        HStack {
            Image(systemName: "doc")
            Text(item.name)
            Spacer()
        }
    }
}

struct ItemDetailView: View {
    let item: Item
    
    var body: some View {
        VStack {
            Image(systemName: "doc.text")
                .font(.system(size: 64))
            Text(item.name)
                .font(.title)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

#Preview {
    ContentView()
}
'''
    
    def _generate_storyboard(self) -> str:
        return '''<?xml version="1.0" encoding="UTF-8"?>
<document type="com.apple.InterfaceBuilder3.Cocoa.Storyboard.XIB" version="3.0"
    toolsVersion="22505" targetRuntime="MacOSX.Cocoa" propertyAccessControl="none">
    <scenes>
        <!--Application-->
        <scene sceneID="JPo-4y-FX3">
            <objects>
                <application id="hnw-xV-0zn" sceneMemberID="viewController">
                    <connections>
                        <outlet property="delegate" destination="Voe-Tx-rLC" id="PrD-fU-P6m"/>
                    </connections>
                </application>
                <customObject id="Voe-Tx-rLC" customClass="AppDelegate" customModule="MyApp"
                    customModuleProvider="target"/>
            </objects>
            <point key="canvasLocation" x="75" y="0.0"/>
        </scene>
        
        <!--Window Controller-->
        <scene sceneID="R2V-Bp-nqG">
            <objects>
                <windowController id="jGA-lt-P6n" sceneMemberID="viewController">
                    <window key="window" title="My macOS App" allowsToolTipsWhenApplicationIsInactive="NO"
                        autorecalculatesKeyViewLoop="NO" releasedWhenClosed="NO" visibleAtLaunch="NO"
                        animationBehavior="default" id="IQv-IB-i5M">
                        <windowStyleMask key="styleMask" titled="YES" closable="YES" miniaturizable="YES"
                            resizable="YES"/>
                        <windowPositionMask key="initialPositionMask" leftStrut="YES"
                            rightStrut="YES" topStrut="YES" bottomStrut="YES"/>
                        <rect key="contentRect" x="196" y="240" width="800" height="600"/>
                    </window>
                    <connections>
                        <segue destination="XfG-lQ-9wD" kind="relationship" relationship="window.shadowedContentViewController" id="cq2-FE-BQF"/>
                    </connections>
                </windowController>
            </objects>
            <point key="canvasLocation" x="75" y="250"/>
        </scene>
    </scenes>
</document>
'''
    
    def _generate_info_plist(self) -> str:
        return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>$(DEVELOPMENT_LANGUAGE)</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIconFile</key>
    <string></string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>$(MACOSX_DEPLOYMENT_TARGET)</string>
    <key>NSMainStoryboardFile</key>
    <string>Main</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
'''


def main():
    parser = argparse.ArgumentParser(description="🍎 Cocoa-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = CocoaAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🍎 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
