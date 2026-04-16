import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { BarChart3, Briefcase, TrendingUp, Bell, Menu, X } from 'lucide-react'
import { useState } from 'react'

export const Navigation = () => {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  const isActive = (path) => location.pathname === path
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/portfolio', label: 'Portfolio', icon: Briefcase },
    { path: '/stocks', label: 'Stocks', icon: TrendingUp },
    { path: '/alerts', label: 'Alerts', icon: Bell },
  ]
  
  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        className="md:hidden fixed top-4 right-4 z-50 p-2 rounded-lg glass"
      >
        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>
      
      {/* Navigation Bar */}
      <nav className={`glass border-b border-white/10 sticky top-0 z-40 ${mobileMenuOpen ? 'block' : 'block'}`}>
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="grid grid-cols-4 gap-2 md:flex md:gap-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex flex-col md:flex-row md:items-center md:gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive(path)
                    ? 'bg-primary/30 text-primary border border-primary/50'
                    : 'text-gray-300 hover:bg-white/5'
                }`}
              >
                <Icon size={20} />
                <span className="text-xs md:text-sm">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </nav>
    </>
  )
}

export const Header = ({ title, subtitle, action }) => {
  return (
    <div className="flex items-start justify-between mb-6">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold mb-1">{title}</h1>
        {subtitle && <p className="text-gray-400">{subtitle}</p>}
      </div>
      {action}
    </div>
  )
}

export const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
