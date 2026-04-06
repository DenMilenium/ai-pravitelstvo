#!/usr/bin/env python3
"""
🔗 Integration-Agent
Integration Specialist

Интегрирует различные сервисы, API и системы.
Создаёт middleware, API gateway, webhooks.
"""

import argparse
from pathlib import Path
from typing import Dict


class IntegrationAgent:
    """
    🔗 Integration-Agent
    
    Специализация: Service Integration
    Задачи: API интеграции, Webhooks, Middleware
    """
    
    NAME = "🔗 Integration-Agent"
    ROLE = "Integration Specialist"
    EXPERTISE = ["API Integration", "Webhooks", "Middleware", "ETL", "API Gateway"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["api-gateway.js"] = self._generate_api_gateway()
        files["webhook-handler.js"] = self._generate_webhook_handler()
        files["integration-patterns.md"] = self._generate_patterns()
        files["service-connector.js"] = self._generate_service_connector()
        
        return files
    
    def _generate_api_gateway(self) -> str:
        return """const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const cors = require('cors');
const jwt = require('jsonwebtoken');

class APIGateway {
  constructor() {
    this.app = express();
    this.services = new Map();
    this.setupMiddleware();
  }
  
  setupMiddleware() {
    // Security
    this.app.use(helmet());
    this.app.use(cors({
      origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
      credentials: true
    }));
    
    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // limit each IP to 100 requests per windowMs
      message: { error: 'Too many requests, please try again later.' }
    });
    this.app.use(limiter);
    
    // Body parsing
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true }));
    
    // Request logging
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }
  
  // Register a service
  registerService(name, config) {
    this.services.set(name, config);
    
    const proxyOptions = {
      target: config.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/${name}`]: config.path || '/'
      },
      onError: (err, req, res) => {
        console.error(`Proxy error for ${name}:`, err.message);
        res.status(502).json({ error: 'Service unavailable' });
      },
      onProxyReq: (proxyReq, req, res) => {
        // Add authentication header if needed
        if (config.apiKey) {
          proxyReq.setHeader('X-API-Key', config.apiKey);
        }
        // Forward user context
        if (req.user) {
          proxyReq.setHeader('X-User-ID', req.user.id);
          proxyReq.setHeader('X-User-Role', req.user.role);
        }
      }
    };
    
    this.app.use(`/api/${name}`, this.authMiddleware(config.auth), createProxyMiddleware(proxyOptions));
    console.log(`✅ Service registered: ${name} -> ${config.url}`);
  }
  
  // Authentication middleware
  authMiddleware(required = true) {
    return (req, res, next) => {
      const authHeader = req.headers.authorization;
      
      if (!authHeader) {
        if (required) {
          return res.status(401).json({ error: 'Authorization required' });
        }
        return next();
      }
      
      try {
        const token = authHeader.replace('Bearer ', '');
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
      } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
      }
    };
  }
  
  // Circuit breaker pattern
  circuitBreaker(serviceName, fallback) {
    let failures = 0;
    const threshold = 5;
    const timeout = 60000; // 1 minute
    let nextAttempt = Date.now();
    
    return async (req, res, next) => {
      if (Date.now() < nextAttempt) {
        return res.status(503).json({ 
          error: 'Service temporarily unavailable',
          fallback: fallback 
        });
      }
      
      try {
        next();
        failures = 0;
      } catch (error) {
        failures++;
        if (failures >= threshold) {
          nextAttempt = Date.now() + timeout;
        }
        throw error;
      }
    };
  }
  
  // Health check endpoint
  setupHealthCheck() {
    this.app.get('/health', async (req, res) => {
      const checks = {};
      
      for (const [name, config] of this.services) {
        try {
          const response = await fetch(`${config.url}/health`, { timeout: 5000 });
          checks[name] = response.ok ? 'healthy' : 'unhealthy';
        } catch {
          checks[name] = 'unreachable';
        }
      }
      
      const allHealthy = Object.values(checks).every(s => s === 'healthy');
      
      res.status(allHealthy ? 200 : 503).json({
        status: allHealthy ? 'healthy' : 'degraded',
        services: checks,
        timestamp: new Date().toISOString()
      });
    });
  }
  
  start(port = 3000) {
    this.setupHealthCheck();
    
    this.app.listen(port, () => {
      console.log(`🚀 API Gateway running on port ${port}`);
      console.log(`📋 Registered services: ${Array.from(this.services.keys()).join(', ')}`);
    });
  }
}

// Usage
const gateway = new APIGateway();

gateway.registerService('users', {
  url: 'http://user-service:3001',
  auth: true
});

gateway.registerService('orders', {
  url: 'http://order-service:3002',
  auth: true
});

gateway.registerService('products', {
  url: 'http://product-service:3003',
  auth: false
});

gateway.start(3000);

module.exports = APIGateway;
"""
    
    def _generate_webhook_handler(self) -> str:
        return """const crypto = require('crypto');
const EventEmitter = require('events');

class WebhookManager extends EventEmitter {
  constructor() {
    super();
    this.handlers = new Map();
    this.secrets = new Map();
  }
  
  // Register webhook handler
  register(provider, config) {
    this.handlers.set(provider, config.handler);
    if (config.secret) {
      this.secrets.set(provider, config.secret);
    }
    console.log(`✅ Webhook registered: ${provider}`);
  }
  
  // Verify webhook signature
  verifySignature(provider, payload, signature) {
    const secret = this.secrets.get(provider);
    if (!secret) return true; // No secret configured
    
    const computed = crypto
      .createHmac('sha256', secret)
      .update(payload, 'utf8')
      .digest('hex');
    
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(computed)
    );
  }
  
  // Handle incoming webhook
  async handle(provider, req, res) {
    const handler = this.handlers.get(provider);
    
    if (!handler) {
      return res.status(404).json({ error: 'Unknown provider' });
    }
    
    // Verify signature
    const signature = req.headers['x-webhook-signature'] || 
                      req.headers['stripe-signature'] ||
                      req.headers['x-hub-signature-256'];
    
    if (signature && !this.verifySignature(provider, req.body, signature)) {
      return res.status(401).json({ error: 'Invalid signature' });
    }
    
    try {
      // Parse payload
      const payload = typeof req.body === 'string' 
        ? JSON.parse(req.body) 
        : req.body;
      
      // Emit event for processing
      const eventType = payload.event || payload.type || 'unknown';
      this.emit(`${provider}:${eventType}`, payload);
      
      // Call handler
      await handler(payload, req, res);
      
      // Acknowledge receipt
      res.status(200).json({ received: true });
    } catch (error) {
      console.error(`Webhook error for ${provider}:`, error);
      res.status(500).json({ error: 'Processing failed' });
    }
  }
}

// Pre-configured handlers
const handlers = {
  stripe: async (payload, req, res) => {
    switch (payload.type) {
      case 'payment_intent.succeeded':
        console.log('Payment succeeded:', payload.data.object.id);
        // Update order status, send confirmation email
        break;
      case 'customer.subscription.created':
        console.log('Subscription created:', payload.data.object.id);
        // Activate subscription
        break;
    }
  },
  
  github: async (payload, req, res) => {
    switch (payload.event) {
      case 'push':
        console.log('Push to:', payload.repository.full_name);
        // Trigger CI/CD pipeline
        break;
      case 'pull_request':
        console.log('PR:', payload.action, payload.pull_request.title);
        // Run checks
        break;
    }
  },
  
  slack: async (payload, req, res) => {
    if (payload.type === 'url_verification') {
      return res.json({ challenge: payload.challenge });
    }
    // Handle Slack events
  }
};

// Usage
const webhooks = new WebhookManager();

webhooks.register('stripe', {
  handler: handlers.stripe,
  secret: process.env.STRIPE_WEBHOOK_SECRET
});

webhooks.register('github', {
  handler: handlers.github,
  secret: process.env.GITHUB_WEBHOOK_SECRET
});

// Express routes
app.post('/webhooks/:provider', (req, res) => {
  webhooks.handle(req.params.provider, req, res);
});

module.exports = { WebhookManager, handlers };
"""
    
    def _generate_service_connector(self) -> str:
        return """class ServiceConnector {
  constructor(baseURL, options = {}) {
    this.baseURL = baseURL;
    this.options = {
      timeout: 10000,
      retries: 3,
      ...options
    };
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.options.timeout);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }
  
  // Retry wrapper
  async requestWithRetry(endpoint, options = {}) {
    let lastError;
    
    for (let i = 0; i < this.options.retries; i++) {
      try {
        return await this.request(endpoint, options);
      } catch (error) {
        lastError = error;
        const delay = Math.pow(2, i) * 1000; // Exponential backoff
        await new Promise(r => setTimeout(r, delay));
      }
    }
    
    throw lastError;
  }
  
  // REST methods
  async get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = query ? `${endpoint}?${query}` : endpoint;
    return this.requestWithRetry(url, { method: 'GET' });
  }
  
  async post(endpoint, data) {
    return this.requestWithRetry(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
  
  async put(endpoint, data) {
    return this.requestWithRetry(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }
  
  async delete(endpoint) {
    return this.requestWithRetry(endpoint, { method: 'DELETE' });
  }
}

// Pre-configured connectors
const connectors = {
  slack: new ServiceConnector('https://slack.com/api', {
    headers: { 'Authorization': `Bearer ${process.env.SLACK_TOKEN}` }
  }),
  
  notion: new ServiceConnector('https://api.notion.com/v1', {
    headers: {
      'Authorization': `Bearer ${process.env.NOTION_TOKEN}`,
      'Notion-Version': '2022-06-28'
    }
  }),
  
  airtable: new ServiceConnector('https://api.airtable.com/v0', {
    headers: { 'Authorization': `Bearer ${process.env.AIRTABLE_TOKEN}` }
  }),
  
  shopify: new ServiceConnector(`https://${process.env.SHOPIFY_STORE}.myshopify.com/admin/api/2024-01`, {
    headers: {
      'X-Shopify-Access-Token': process.env.SHOPIFY_TOKEN
    }
  })
};

module.exports = { ServiceConnector, connectors };
"""
    
    def _generate_patterns(self) -> str:
        return """# Integration Patterns

## 1. API Gateway Pattern
```
Client -> API Gateway -> [Service A, Service B, Service C]
```
- Single entry point
- Authentication centralized
- Rate limiting
- Request routing

## 2. Circuit Breaker Pattern
```
Client -> Circuit Breaker -> Service
                ↓
           Fallback
```
- Fail fast
- Prevent cascade failures
- Automatic recovery

## 3. Webhook Pattern
```
Service A -(event)-> Webhook Handler -> Service B
```
- Event-driven
- Asynchronous
- Loose coupling

## 4. Message Queue Pattern
```
Producer -> Queue -> Consumer(s)
```
- Async processing
- Load leveling
- Retry logic

## 5. ETL Pattern
```
Extract -> Transform -> Load
```
- Data synchronization
- Format conversion
- Batch processing

## 6. Adapter Pattern
```
Client -> Adapter -> External Service
```
- Interface compatibility
- Protocol translation
- Data transformation
"""


def main():
    parser = argparse.ArgumentParser(description="🔗 Integration-Agent — Integration")
    parser.add_argument("request", nargs="?", help="Что интегрировать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = IntegrationAgent()
    
    if args.request:
        print(f"🔗 {agent.NAME} создаёт интеграцию: {args.request}")
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
        print(f"🔗 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
