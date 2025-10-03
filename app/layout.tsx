import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FiapFlix - Sistema de Recomendação de Filmes',
  description: 'Sistema inteligente de recomendação de filmes baseado em IA e clusterização',
  keywords: 'filmes, recomendação, IA, machine learning, clusterização',
  authors: [{ name: 'FIAP - Front End & Mobile Development' }],
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <div className="min-h-screen bg-netflix-black">
          {children}
        </div>
      </body>
    </html>
  )
}
