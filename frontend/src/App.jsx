import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { Dashboard } from './pages/Dashboard'
import { Portfolio } from './pages/Portfolio'
import { Stocks } from './pages/Stocks'
import { Alerts } from './pages/Alerts'
import { stocksAPI } from './services/api'
import './index.css'

function App() {
  useEffect(() => {
    document.title = 'Smart NEPSE Investor'
    // Initialize stocks on app load
    initializeStocks()
  }, [])
  
  const initializeStocks = async () => {
    try {
      console.log('Initializing stocks...')
      const response = await stocksAPI.initialize()
      console.log('Stocks initialized:', response.data)
    } catch (err) {
      console.error('Failed to initialize stocks:', err)
      // Continue anyway - the backend has fallback to mock data
    }
  }
  
  return (
    <>
      <Toaster position="top-right" />
      <Router>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/stocks" element={<Stocks />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
