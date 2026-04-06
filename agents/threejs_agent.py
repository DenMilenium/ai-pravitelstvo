#!/usr/bin/env python3
"""
🎯 ThreeJS-Agent
3D Web Developer агент

Создаёт:
- Three.js 3D сцены
- WebGL приложения
- 3D интерактивы
"""

import argparse
from pathlib import Path
from typing import Dict


class ThreeJSAgent:
    """
    🎯 ThreeJS-Agent
    
    Специализация: 3D Web Development
    Стек: Three.js, WebGL, GLSL
    """
    
    NAME = "🎯 ThreeJS-Agent"
    ROLE = "3D Web Developer"
    EXPERTISE = ["Three.js", "WebGL", "3D Graphics", "GLSL", "Animations"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["scene.js"] = """import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

class Scene3D {
  constructor(container) {
    this.container = container;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.objects = [];
    
    this.init();
  }
  
  init() {
    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x1a1a2e);
    
    // Camera
    this.camera = new THREE.PerspectiveCamera(
      75,
      this.container.clientWidth / this.container.clientHeight,
      0.1,
      1000
    );
    this.camera.position.z = 5;
    
    // Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.container.appendChild(this.renderer.domElement);
    
    // Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    
    // Lights
    this.addLights();
    
    // Objects
    this.addObjects();
    
    // Event listeners
    window.addEventListener('resize', this.onResize.bind(this));
    
    // Start animation
    this.animate();
  }
  
  addLights() {
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);
    
    // Directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    directionalLight.castShadow = true;
    this.scene.add(directionalLight);
    
    // Point light
    const pointLight = new THREE.PointLight(0x00ffff, 1, 100);
    pointLight.position.set(0, 2, 0);
    this.scene.add(pointLight);
  }
  
  addObjects() {
    // Cube
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a90d9,
      metalness: 0.5,
      roughness: 0.5
    });
    const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    cube.position.set(-2, 0, 0);
    cube.castShadow = true;
    cube.receiveShadow = true;
    this.scene.add(cube);
    this.objects.push(cube);
    
    // Sphere
    const sphereGeometry = new THREE.SphereGeometry(0.7, 32, 32);
    const sphereMaterial = new THREE.MeshStandardMaterial({
      color: 0xe74c3c,
      metalness: 0.3,
      roughness: 0.4
    });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.set(0, 0, 0);
    sphere.castShadow = true;
    this.scene.add(sphere);
    this.objects.push(sphere);
    
    // Torus
    const torusGeometry = new THREE.TorusGeometry(0.6, 0.2, 16, 100);
    const torusMaterial = new THREE.MeshStandardMaterial({
      color: 0x2ecc71,
      metalness: 0.6,
      roughness: 0.2
    });
    const torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.position.set(2, 0, 0);
    this.scene.add(torus);
    this.objects.push(torus);
    
    // Floor
    const floorGeometry = new THREE.PlaneGeometry(20, 20);
    const floorMaterial = new THREE.MeshStandardMaterial({
      color: 0x16213e,
      roughness: 0.8
    });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -2;
    floor.receiveShadow = true;
    this.scene.add(floor);
  }
  
  animate() {
    requestAnimationFrame(this.animate.bind(this));
    
    // Rotate objects
    this.objects.forEach((obj, index) => {
      obj.rotation.x += 0.01 * (index + 1);
      obj.rotation.y += 0.01 * (index + 1);
    });
    
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  onResize() {
    this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
  }
  
  destroy() {
    window.removeEventListener('resize', this.onResize.bind(this));
    this.container.removeChild(this.renderer.domElement);
    this.renderer.dispose();
  }
}

export default Scene3D;
"""
        
        files["main.js"] = """import Scene3D from './scene.js';

// Initialize 3D scene
const container = document.getElementById('canvas-container');
const scene = new Scene3D(container);

// Add interactivity
document.getElementById('reset-btn').addEventListener('click', () => {
  scene.camera.position.set(0, 0, 5);
  scene.camera.lookAt(0, 0, 0);
  scene.controls.reset();
});

// Export for global access
window.scene3D = scene;
"""
        
        files["index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>3D Scene - Three.js</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: Arial, sans-serif;
      background: #1a1a2e;
      color: white;
      overflow: hidden;
    }
    #canvas-container {
      width: 100vw;
      height: 100vh;
    }
    #controls {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
    }
    button {
      padding: 10px 20px;
      background: #4a90d9;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover {
      background: #357abd;
    }
  </style>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <button id="reset-btn">Reset Camera</button>
  </div>
  <script type="module" src="main.js"></script>
</body>
</html>
"""
        
        files["package.json"] = """{
  "name": "3d-scene",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "three": "^0.160.0"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🎯 ThreeJS-Agent — 3D Web")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = ThreeJSAgent()
    
    if args.request:
        print(f"🎯 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
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
        print(f"🎯 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
