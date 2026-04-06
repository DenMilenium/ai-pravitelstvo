#!/usr/bin/env python3
"""
🚀 FullStack-Agent
FullStack Developer агент

Создаёт:
- Next.js приложения
- MERN стек
- Fullstack проекты
"""

import argparse
from pathlib import Path
from typing import Dict


class FullStackAgent:
    """
    🚀 FullStack-Agent
    
    Специализация: Fullstack разработка
    Стек: Next.js, React, Node.js, MongoDB
    """
    
    NAME = "🚀 FullStack-Agent"
    ROLE = "FullStack Developer"
    EXPERTISE = ["Next.js", "React", "Node.js", "MongoDB", "MERN", "TypeScript"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["package.json"] = """{
  "name": "fullstack-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "mongoose": "^8.0.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "next-auth": "^4.24.0",
    "tailwindcss": "^3.3.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/bcryptjs": "^2.4.6",
    "@types/jsonwebtoken": "^9.0.5",
    "typescript": "^5.3.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "14.0.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
"""
        
        files["app/layout.tsx"] = """import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/components/AuthProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FullStack App',
  description: 'Created by FullStack-Agent',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
"""
        
        files["app/page.tsx"] = """export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold text-white text-center mb-8">
          🚀 FullStack App
        </h1>
        
        <p className="text-xl text-white/90 text-center max-w-2xl mx-auto">
          Built with Next.js 14, React, TypeScript, and MongoDB
        </p>
        
        <div className="mt-12 flex justify-center gap-4">
          <a
            href="/dashboard"
            className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-white/90 transition"
          >
            Get Started
          </a>
        </div>
      </div>
    </main>
  )
}
"""
        
        files["app/api/users/route.ts"] = """import { NextRequest, NextResponse } from 'next/server'
import { connectDB } from '@/lib/db'
import { User } from '@/models/User'

export async function GET() {
  try {
    await connectDB()
    const users = await User.find({}).select('-password')
    return NextResponse.json({ users })
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch users' }, { status: 500 })
  }
}

export async function POST(req: NextRequest) {
  try {
    await connectDB()
    const body = await req.json()
    
    const user = await User.create(body)
    return NextResponse.json({ user }, { status: 201 })
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create user' }, { status: 500 })
  }
}
"""
        
        files["lib/db.ts"] = """import mongoose from 'mongoose'

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/fullstack'

export async function connectDB() {
  try {
    if (mongoose.connection.readyState >= 1) return
    
    await mongoose.connect(MONGODB_URI)
    console.log('✅ MongoDB connected')
  } catch (error) {
    console.error('❌ MongoDB connection error:', error)
    throw error
  }
}
"""
        
        files["models/User.ts"] = """import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user',
  },
}, {
  timestamps: true,
})

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 12)
  next()
})

export const User = mongoose.models.User || mongoose.model('User', userSchema)
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🚀 FullStack-Agent — Next.js/MERN")
    parser.add_argument("request", nargs="?", help="Что разработать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = FullStackAgent()
    
    if args.request:
        print(f"🚀 {agent.NAME} создаёт: {args.request}")
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
        print(f"🚀 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
