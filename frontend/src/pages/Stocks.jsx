import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { StockPriceCard, LoadingSpinner, EmptyState } from '../components/common'
import { stocksAPI } from '../services/api'
import { Search } from 'lucide-react'
import toast from 'react-hot-toast'

export const Stocks = () => {
  const [stocks, setStocks] = useState([])
  const [filteredStocks, setFilteredStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('score')
  
  useEffect(() => {
    loadStocks()
    // Refresh every 60 seconds
    const interval = setInterval(loadStocks, 60000)
    return () => clearInterval(interval)
  }, [])
  
  useEffect(() => {
    filterAndSort()
  }, [stocks, searchQuery, sortBy])
  
  const loadStocks = async () => {
    try {
      setLoading(true)
      const res = await stocksAPI.listAll()
      setStocks(res.data)
    } catch (error) {
      console.error('Error loading stocks:', error)
      toast.error('Failed to load stocks')
    } finally {
      setLoading(false)
    }
  }
  
  const filterAndSort = () => {
    let filtered = stocks.filter(stock =>
      stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchQuery.toLowerCase())
    )
    
    // Sort
    if (sortBy === 'score') {
      filtered.sort((a, b) => b.analysis_score - a.analysis_score)
    } else if (sortBy === 'price_high') {
      filtered.sort((a, b) => b.current_price - a.current_price)
    } else if (sortBy === 'price_low') {
      filtered.sort((a, b) => a.current_price - b.current_price)
    } else if (sortBy === 'rsi') {
      filtered.sort((a, b) => (b.rsi || 0) - (a.rsi || 0))
    }
    
    setFilteredStocks(filtered)
  }
  
  if (loading) return <Layout><LoadingSpinner /></Layout>
  
  return (
    <Layout>
      <Header
        title="Stock Market"
        subtitle="NEPSE stocks with technical analysis"
      />
      
      {/* Search and Filter */}
      <div className="glass rounded-lg p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search stocks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 pl-10"
            />
          </div>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-white/10 border border-white/20 rounded px-3 py-2"
          >
            <option value="score">Sort by Score (High to Low)</option>
            <option value="price_high">Sort by Price (High to Low)</option>
            <option value="price_low">Sort by Price (Low to High)</option>
            <option value="rsi">Sort by RSI</option>
          </select>
        </div>
      </div>
      
      {/* Stocks Grid */}
      {filteredStocks.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredStocks.map(stock => (
            <StockPriceCard
              key={stock.symbol}
              stock={stock}
              onClick={() => console.log('View details:', stock.symbol)}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="No Stocks Found"
          description={searchQuery ? 'Try a different search term' : 'No stocks available'}
        />
      )}
    </Layout>
  )
}
