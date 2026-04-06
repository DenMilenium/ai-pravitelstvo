#!/usr/bin/env python3
"""
⚓ K8s-Agent
Kubernetes Specialist агент

Создаёт:
- Kubernetes manifests
- Helm charts
- Ingress configs
- Service meshes
"""

import argparse
from pathlib import Path
from typing import Dict


class K8sAgent:
    """
    ⚓ K8s-Agent
    
    Специализация: Kubernetes
    Экспертиза: K8s manifests, Helm, Ingress, Services
    """
    
    NAME = "⚓ K8s-Agent"
    ROLE = "Kubernetes Specialist"
    EXPERTISE = ["Kubernetes", "Helm", "Ingress", "Services", "ConfigMaps"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["deployment.yaml"] = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: web
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
        version: v1
    spec:
      containers:
      - name: web
        image: nginx:latest
        ports:
        - containerPort: 80
          protocol: TCP
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: app-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web
              topologyKey: kubernetes.io/hostname
"""
        
        files["service.yaml"] = """apiVersion: v1
kind: Service
metadata:
  name: app-service
  labels:
    app: web
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  sessionAffinity: None
---
apiVersion: v1
kind: Service
metadata:
  name: app-headless
  labels:
    app: web
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
"""
        
        files["ingress.yaml"] = """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
"""
        
        files["configmap.yaml"] = """apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    app.name=MyApp
    app.version=1.0.0
    app.environment=production
  logging.properties: |
    level=INFO
    format=json
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # echo -n 'your-secret' | base64
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0Bsb2NhbGhvc3Q6NTQzMi9teWRi
  api-key: c2VjcmV0LWtleS0xMjM=
"""
        
        files["hpa.yaml"] = """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="⚓ K8s-Agent — Kubernetes")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = K8sAgent()
    
    if args.request:
        print(f"⚓ {agent.NAME} создаёт: {args.request}")
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
        print(f"⚓ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
