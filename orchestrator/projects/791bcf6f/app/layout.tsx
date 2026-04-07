import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata: Metadata = {
  title: 'Судебный департамент при Верховном суде РФ',
  description: 'Официальный сайт Судебного департамента при Верховном суде Российской Федерации',
  keywords: 'судебный департамент, верховный суд, правосудие, суды рф, электронное правосудие',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
