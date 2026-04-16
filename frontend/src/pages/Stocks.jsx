import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { LoadingSpinner, EmptyState } from '../components/common'
import { stocksAPI } from '../services/api'
import { Search, TrendingUp, TrendingDown, Eye } from 'lucide-react'
import toast from 'react-hot-toast'
import { formatNumber } from '../utils/formatting'

export const Stocks = () => {
  const [stocks, setStocks] = useState([])
  const [filteredStocks, setFilteredStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('score')
  const [viewType, setViewType] = useState('table') // 'table' or 'grid'
  
  useEffect(() => {
    loadStocks()
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

  // Market Statistics
  const avgPrice = stocks.length > 0 ? (stocks.reduce((sum, s) => sum + s.current_price, 0) / stocks.length).toFixed(2) : 0
  const topGainers = [...stocks].sort((a, b) => (b.rsi || 0) - (a.rsi || 0)).slice(0, 5)
  const topLosers = [...stocks].sort((a, b) => (a.rsi || 0) - (b.rsi || 0)).slice(0, 5)
  
  if (loading) return <Layout><LoadingSpinner /></Layout>
  
  return (
    <Layout>
      <Header
        title="📊 Stock Market"
        subtitle="Real-time NEPSE market data with technical analysis"
      />
      
      {/* Market Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="glass rounded-lg p-4 border border-white/10">
          <p className="text-gray-400 text-sm">Total Stocks</p>
          <p className="text-3xl font-bold text-primary">{stocks.length}</p>
        </div>
        <div className="glass rounded-lg p-4 border border-white/10">
          <p className="text-gray-400 text-sm">Average Price</p>
          <p className="text-3xl font-bold text-cyan-400">Rs. {avgPrice}</p>
        </div>
        <div className="glass rounded-lg p-4 border border-green-500/30 bg-green-900/10">
          <p className="text-green-400 text-sm">Top Gainers</p>
          <p className="text-2xl font-bold">{topGainers.length > 0 ? topGainers[0].symbol : '-'}</p>
        </div>
        <div className="glass rounded-lg p-4 border border-red-500/30 bg-red-900/10">
          <p className="text-red-400 text-sm">Top Losers</p>
          <p className="text-2xl font-bold">{topLosers.length > 0 ? topLosers[0].symbol : '-'}</p>
        </div>
      </div>

      {/* Controls */}
      <div className="glass rounded-lg p-4 mb-6 border border-white/10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search stocks by symbol or name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 pl-10 focus:outline-none focus:border-primary/50"
            />
          </div>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-white/10 border border-white/20 rounded px-3 py-2 focus:outline-none focus:border-primary/50"
          >
            <option value="score">📊 Sort by Score</option>
            <option value="price_high">⬆️ Price (High to Low)</option>
            <option value="price_low">⬇️ Price (Low to High)</option>
            <option value="rsi">📈 Sort by RSI</option>
          </select>

          <div className="flex gap-2">
            <button
              onClick={() => setViewType('table')}
              className={`flex-1 px-4 py-2 rounded font-semibold transition-all ${
                viewType === 'table' 
                  ? 'bg-primary text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              📋 Table
            </button>
            <button
              onClick={() => setViewType('grid')}
              className={`flex-1 px-4 py-2 rounded font-semibold transition-all ${
                viewType === 'grid' 
                  ? 'bg-primary text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              📊 Grid
            </button>
          </div>
        </div>
      </div>

      {/* Stocks Table View */}
      {viewType === 'table' && filteredStocks.length > 0 && (
        <div className="glass rounded-lg overflow-hidden border border-white/10">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-white/5 border-b border-white/10 sticky top-0">
                <tr>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">#</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Symbol</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Company</th>
                  <th className="px-4 py-3 text-right text-gray-400 font-semibold">Price</th>
                  <th className="px-4 py-3 text-center text-gray-400 font-semibold">RSI</th>
                  <th className="px-4 py-3 text-center text-gray-400 font-semibold">MA50/200</th>
                  <th className="px-4 py-3 text-center text-gray-400 font-semibold">Score</th>
                  <th className="px-4 py-3 text-left text-gray-400 font-semibold">Recommendation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredStocks.map((stock, idx) => {
                  const rsiColor = stock.rsi > 70 ? 'text-red-400' : stock.rsi < 30 ? 'text-green-400' : 'text-gray-300'
                  const recColor = stock.analysis_recommendation === 'buy' ? 'text-green-400' : 
                                   stock.analysis_recommendation === 'sell' ? 'text-red-400' : 'text-yellow-400'
                  
                  return (
                    <tr key={stock.symbol} className="hover:bg-white/5 transition-colors">
                      <td className="px-4 py-3 text-gray-400">{idx + 1}</td>
                      <td className="px-4 py-3 font-bold text-primary">{stock.symbol}</td>
                      <td className="px-4 py-3 text-gray-300">{stock.name.substring(0, 20)}</td>
                      <td className="px-4 py-3 text-right font-bold text-cyan-400">Rs. {formatNumber(stock.current_price, 2)}</td>
                      <td className={`px-4 py-3 text-center font-semibold ${rsiColor}`}>
                        {stock.rsi ? formatNumber(stock.rsi, 1) : '-'}
                      </td>
                      <td className="px-4 py-3 text-center text-gray-300 text-xs">
                        <div>{stock.ma_50 ? formatNumber(stock.ma_50, 0) : '-'}</div>
                        <div className="text-gray-500">{stock.ma_200 ? formatNumber(stock.ma_200, 0) : '-'}</div>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="bg-primary/20 text-primary px-2 py-1 rounded text-xs font-bold">
                          {formatNumber(stock.analysis_score, 1)}/4
                        </span>
                      </td>
                      <td className={`px-4 py-3 font-semibold ${recColor}`}>
                        {stock.analysis_recommendation?.toUpperCase() || '-'}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Stocks Grid View */}
      {viewType === 'grid' && filteredStocks.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredStocks.map((stock) => {
            const rsiColor = stock.rsi > 70 ? 'bg-red-900/20 border-red-500/30' : 
                            stock.rsi < 30 ? 'bg-green-900/20 border-green-500/30' : 
                            'bg-white/5 border-white/10'
            
            return (
              <div key={stock.symbol} className={`glass rounded-lg p-4 border transition-all hover:scale-105 cursor-pointer ${rsiColor}`}>
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <p className="font-bold text-lg text-primary">{stock.symbol}</p>
                    <p className="text-xs text-gray-400">{stock.name.substring(0, 15)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-cyan-400">Rs.{formatNumber(stock.current_price, 0)}</p>
                  </div>
                </div>

                <div className="space-y-2 mb-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">RSI:</span>
                    <span className={stock.rsi > 70 ? 'text-red-400' : stock.rsi < 30 ? 'text-green-400' : 'text-gray-300'}>
                      {stock.rsi ? formatNumber(stock.rsi, 1) : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Score:</span>
                    <span className="text-primary font-bold">{formatNumber(stock.analysis_score, 1)}/4</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Volume:</span>
                    <span className="text-gray-300">{stock.volume_trend || '-'}</span>
                  </div>
                </div>

                <div className="flex gap-2 pt-3 border-t border-white/10">
                  <span className={`flex-1 text-center py-1 rounded text-xs font-bold ${
                    stock.analysis_recommendation === 'buy' ? 'bg-green-900/30 text-green-400' :
                    stock.analysis_recommendation === 'sell' ? 'bg-red-900/30 text-red-400' :
                    'bg-yellow-900/30 text-yellow-400'
                  }`}>
                    {stock.analysis_recommendation?.toUpperCase() || 'HOLD'}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {filteredStocks.length === 0 && (
        <EmptyState
          title="No Stocks Found"
          description={searchQuery ? 'Try a different search term' : 'No stocks available'}
        />
      )}

      {/* Top Gainers and Losers */}
      {!searchQuery && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          {/* Top Gainers */}
          <div className="glass rounded-lg p-6 border border-green-500/30 bg-green-900/10">
            <h3 className="text-xl font-bold text-green-400 mb-4 flex items-center gap-2">
              <TrendingUp size={20} />
              Top Performers
            </h3>
            <div className="space-y-2">
              {topGainers.map((stock, idx) => (
                <div key={stock.symbol} className="flex items-center justify-between p-2 bg-white/5 rounded">
                  <div>
                    <p className="font-bold">{idx + 1}. {stock.symbol}</p>
                    <p className="text-xs text-gray-400">{stock.name.substring(0, 25)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-green-400 font-bold">Rs. {formatNumber(stock.current_price, 2)}</p>
                    {stock.rsi && <p className="text-xs text-gray-400">RSI: {formatNumber(stock.rsi, 1)}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Top Losers */}
          <div className="glass rounded-lg p-6 border border-red-500/30 bg-red-900/10">
            <h3 className="text-xl font-bold text-red-400 mb-4 flex items-center gap-2">
              <TrendingDown size={20} />
              Potential Opportunities
            </h3>
            <div className="space-y-2">
              {topLosers.map((stock, idx) => (
                <div key={stock.symbol} className="flex items-center justify-between p-2 bg-white/5 rounded">
                  <div>
                    <p className="font-bold">{idx + 1}. {stock.symbol}</p>
                    <p className="text-xs text-gray-400">{stock.name.substring(0, 25)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-red-400 font-bold">Rs. {formatNumber(stock.current_price, 2)}</p>
                    {stock.rsi && <p className="text-xs text-gray-400">RSI: {formatNumber(stock.rsi, 1)}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}
