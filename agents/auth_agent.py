#!/usr/bin/env python3
"""
🔐 Auth-Agent
Authentication Specialist агент

Создаёт:
- JWT аутентификацию
- OAuth2 интеграции
- SSO решения
- Auth0/Firebase Auth
"""

import argparse
from pathlib import Path
from typing import Dict


class AuthAgent:
    """
    🔐 Auth-Agent
    
    Специализация: Authentication & Authorization
    Технологии: JWT, OAuth2, SSO, RBAC
    """
    
    NAME = "🔐 Auth-Agent"
    ROLE = "Auth Specialist"
    EXPERTISE = ["JWT", "OAuth2", "SSO", "RBAC", "Auth0", "Firebase Auth"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["auth-service.js"] = """const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class AuthService {
  constructor() {
    this.JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
    this.JWT_EXPIRES_IN = '7d';
    this.REFRESH_TOKEN_EXPIRES_IN = '30d';
    this.users = new Map(); // In production: use database
    this.refreshTokens = new Set();
  }
  
  // Register new user
  async register(email, password, userData = {}) {
    // Check if user exists
    if (this.users.has(email)) {
      throw new Error('User already exists');
    }
    
    // Hash password
    const saltRounds = 12;
    const passwordHash = await bcrypt.hash(password, saltRounds);
    
    // Create user
    const user = {
      id: crypto.randomUUID(),
      email,
      passwordHash,
      role: 'user',
      isEmailVerified: false,
      createdAt: new Date(),
      ...userData
    };
    
    this.users.set(email, user);
    
    // Generate tokens
    const tokens = this.generateTokens(user);
    
    return {
      user: this.sanitizeUser(user),
      ...tokens
    };
  }
  
  // Login user
  async login(email, password) {
    const user = this.users.get(email);
    
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    // Verify password
    const isValid = await bcrypt.compare(password, user.passwordHash);
    
    if (!isValid) {
      throw new Error('Invalid credentials');
    }
    
    // Update last login
    user.lastLogin = new Date();
    
    // Generate tokens
    const tokens = this.generateTokens(user);
    
    return {
      user: this.sanitizeUser(user),
      ...tokens
    };
  }
  
  // Generate JWT tokens
  generateTokens(user) {
    const payload = {
      sub: user.id,
      email: user.email,
      role: user.role
    };
    
    const accessToken = jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN,
      issuer: 'your-app',
      audience: 'your-app-users'
    });
    
    const refreshToken = crypto.randomBytes(40).toString('hex');
    this.refreshTokens.add(refreshToken);
    
    return {
      accessToken,
      refreshToken,
      expiresIn: 7 * 24 * 60 * 60 // 7 days in seconds
    };
  }
  
  // Refresh access token
  async refreshAccessToken(refreshToken) {
    if (!this.refreshTokens.has(refreshToken)) {
      throw new Error('Invalid refresh token');
    }
    
    // Decode token to get user info (in production: verify from DB)
    const decoded = jwt.decode(refreshToken);
    const user = Array.from(this.users.values()).find(u => u.id === decoded?.sub);
    
    if (!user) {
      throw new Error('User not found');
    }
    
    // Generate new tokens
    const tokens = this.generateTokens(user);
    
    // Remove old refresh token
    this.refreshTokens.delete(refreshToken);
    
    return tokens;
  }
  
  // Verify JWT token
  verifyToken(token) {
    try {
      return jwt.verify(token, this.JWT_SECRET);
    } catch (error) {
      throw new Error('Invalid token');
    }
  }
  
  // Middleware for Express
  middleware(requiredRole = null) {
    return (req, res, next) => {
      try {
        const authHeader = req.headers.authorization;
        
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
          return res.status(401).json({ error: 'No token provided' });
        }
        
        const token = authHeader.substring(7);
        const decoded = this.verifyToken(token);
        
        // Check role if required
        if (requiredRole && decoded.role !== requiredRole && decoded.role !== 'admin') {
          return res.status(403).json({ error: 'Insufficient permissions' });
        }
        
        req.user = decoded;
        next();
      } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
      }
    };
  }
  
  // Logout
  async logout(refreshToken) {
    this.refreshTokens.delete(refreshToken);
  }
  
  // Password reset
  async requestPasswordReset(email) {
    const user = this.users.get(email);
    
    if (!user) {
      // Don't reveal if user exists
      return { message: 'If email exists, reset link sent' };
    }
    
    const resetToken = crypto.randomBytes(32).toString('hex');
    user.resetToken = resetToken;
    user.resetTokenExpires = new Date(Date.now() + 3600000); // 1 hour
    
    // Send email with reset link (implement email service)
    return { 
      message: 'Password reset link sent',
      resetToken // In production: send via email only
    };
  }
  
  // Sanitize user object (remove sensitive data)
  sanitizeUser(user) {
    const { passwordHash, resetToken, ...safe } = user;
    return safe;
  }
}

module.exports = new AuthService();
"""
        
        files["rbac-roles.js"] = """// Role-Based Access Control (RBAC)

const ROLES = {
  SUPER_ADMIN: {
    level: 100,
    permissions: ['*'] // All permissions
  },
  ADMIN: {
    level: 80,
    permissions: [
      'users:read', 'users:write', 'users:delete',
      'content:read', 'content:write', 'content:delete',
      'settings:read', 'settings:write',
      'reports:read'
    ]
  },
  MODERATOR: {
    level: 60,
    permissions: [
      'users:read',
      'content:read', 'content:write', 'content:moderate',
      'reports:read'
    ]
  },
  USER: {
    level: 40,
    permissions: [
      'users:read:own',
      'content:read',
      'content:write:own',
      'content:delete:own'
    ]
  },
  GUEST: {
    level: 20,
    permissions: [
      'content:read:public'
    ]
  }
};

class RBAC {
  constructor() {
    this.roles = ROLES;
  }
  
  // Check if role has permission
  hasPermission(role, permission) {
    const roleConfig = this.roles[role];
    
    if (!roleConfig) return false;
    
    // Super admin has all permissions
    if (roleConfig.permissions.includes('*')) return true;
    
    // Check exact permission
    if (roleConfig.permissions.includes(permission)) return true;
    
    // Check wildcard permissions
    const [resource, action] = permission.split(':');
    return roleConfig.permissions.some(p => {
      const [pResource, pAction] = p.split(':');
      return (
        (pResource === resource || pResource === '*') &&
        (pAction === action || pAction === '*')
      );
    });
  }
  
  // Check if user can access resource
  canAccess(userRole, targetRole) {
    const userLevel = this.roles[userRole]?.level || 0;
    const targetLevel = this.roles[targetRole]?.level || 0;
    return userLevel >= targetLevel;
  }
  
  // Get all permissions for role
  getPermissions(role) {
    return this.roles[role]?.permissions || [];
  }
  
  // Middleware factory
  requirePermission(permission) {
    return (req, res, next) => {
      const userRole = req.user?.role || 'GUEST';
      
      if (!this.hasPermission(userRole, permission)) {
        return res.status(403).json({
          error: 'Forbidden',
          message: `Required permission: ${permission}`
        });
      }
      
      next();
    };
  }
  
  // Require multiple permissions (AND)
  requireAllPermissions(permissions) {
    return (req, res, next) => {
      const userRole = req.user?.role || 'GUEST';
      
      const missing = permissions.filter(
        p => !this.hasPermission(userRole, p)
      );
      
      if (missing.length > 0) {
        return res.status(403).json({
          error: 'Forbidden',
          message: `Missing permissions: ${missing.join(', ')}`
        });
      }
      
      next();
    };
  }
}

module.exports = { RBAC, ROLES };
"""
        
        files["oauth-config.js"] = """// OAuth2 Configuration

const OAUTH_PROVIDERS = {
  google: {
    name: 'Google',
    authorizationURL: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenURL: 'https://oauth2.googleapis.com/token',
    userInfoURL: 'https://www.googleapis.com/oauth2/v2/userinfo',
    scopes: ['openid', 'email', 'profile']
  },
  github: {
    name: 'GitHub',
    authorizationURL: 'https://github.com/login/oauth/authorize',
    tokenURL: 'https://github.com/login/oauth/access_token',
    userInfoURL: 'https://api.github.com/user',
    scopes: ['user:email', 'read:user']
  },
  discord: {
    name: 'Discord',
    authorizationURL: 'https://discord.com/api/oauth2/authorize',
    tokenURL: 'https://discord.com/api/oauth2/token',
    userInfoURL: 'https://discord.com/api/users/@me',
    scopes: ['identify', 'email']
  }
};

class OAuthService {
  constructor() {
    this.providers = OAUTH_PROVIDERS;
  }
  
  // Generate authorization URL
  getAuthorizationURL(provider, state, redirectUri) {
    const config = this.providers[provider];
    
    if (!config) {
      throw new Error(`Unknown provider: ${provider}`);
    }
    
    const params = new URLSearchParams({
      client_id: process.env[`${provider.toUpperCase()}_CLIENT_ID`],
      redirect_uri: redirectUri,
      response_type: 'code',
      scope: config.scopes.join(' '),
      state
    });
    
    return `${config.authorizationURL}?${params.toString()}`;
  }
  
  // Exchange code for tokens
  async exchangeCode(provider, code, redirectUri) {
    const config = this.providers[provider];
    
    const response = await fetch(config.tokenURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      },
      body: new URLSearchParams({
        client_id: process.env[`${provider.toUpperCase()}_CLIENT_ID`],
        client_secret: process.env[`${provider.toUpperCase()}_CLIENT_SECRET`],
        code,
        redirect_uri: redirectUri,
        grant_type: 'authorization_code'
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to exchange code');
    }
    
    return response.json();
  }
  
  // Get user info from provider
  async getUserInfo(provider, accessToken) {
    const config = this.providers[provider];
    
    const response = await fetch(config.userInfoURL, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to get user info');
    }
    
    return response.json();
  }
}

module.exports = { OAuthService, OAUTH_PROVIDERS };
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🔐 Auth-Agent — Authentication")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = AuthAgent()
    
    if args.request:
        print(f"🔐 {agent.NAME} создаёт: {args.request}")
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
        print(f"🔐 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
