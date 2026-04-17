import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { LoadingSpinner, EmptyState, PortfolioItemRow } from '../components/common'
import { portfolioAPI, stocksAPI } from '../services/api'
import { formatCurrency, formatNumber } from '../utils/formatting'
import { Plus, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

const AddPortfolioModal = ({ isOpen, onClose, stocks, onAdded }) => {
  const [formData, setFormData] = useState({
    stock_symbol: '',
    buy_price: '',
    quantity: '',
    target_profit_percentage: 15,
    stop_loss_percentage: '',
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'quantity' ? parseInt(value) || '' : parseFloat(value) || value
    }))
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.stock_symbol || !formData.buy_price || !formData.quantity) {
      toast.error('Please fill all required fields')
      return
    }
    
    try {
      setLoading(true)
      
      // Log the data being sent for debugging
      console.log('Submitting portfolio data:', formData)
      
      // Ensure numeric fields are proper numbers
      const submitData = {
        stock_symbol: formData.stock_symbol,
        buy_price: parseFloat(formData.buy_price),
        quantity: parseInt(formData.quantity),
        target_profit_percentage: parseFloat(formData.target_profit_percentage) || 15,
        stop_loss_percentage: formData.stop_loss_percentage ? parseFloat(formData.stop_loss_percentage) : null,
        notes: formData.notes || '',
      }
      
      console.log('Formatted data to send:', submitData)
      
      const response = await portfolioAPI.addStock(submitData)
      console.log('Response from server:', response.data)
      
      toast.success('Stock added to portfolio!')
      setFormData({
        stock_symbol: '',
        buy_price: '',
        quantity: '',
        target_profit_percentage: 15,
        stop_loss_percentage: '',
        notes: '',
      })
      onAdded()
      onClose()
    } catch (error) {
      console.error('Error adding stock:', error)
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to add stock'
      console.error('Error details:', errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }
  
  if (!isOpen) return null
  
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass rounded-lg max-w-md w-full p-6">
        <h2 className="text-2xl font-bold mb-4">Add to Portfolio</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Stock Symbol *</label>
            {stocks.length === 0 ? (
              <div className="w-full bg-slate-800 text-yellow-400 border border-white/20 rounded px-3 py-2 text-sm">
                Loading stocks... If this takes too long, please refresh the page.
              </div>
            ) : (
              <select
                name="stock_symbol"
                value={formData.stock_symbol}
                onChange={handleChange}
                className="w-full bg-slate-800 text-white border border-white/20 rounded px-3 py-2 cursor-pointer"
                required
              >
                <option value="">Select a stock</option>
                {stocks.map(stock => (
                  <option key={stock.symbol} value={stock.symbol} className="bg-slate-800 text-white">
                    {stock.symbol} - {stock.name}
                  </option>
                ))}
              </select>
            )}
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Buy Price *</label>
              <input
                type="number"
                name="buy_price"
                value={formData.buy_price}
                onChange={handleChange}
                placeholder="1000"
                step="0.01"
                className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Quantity *</label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                placeholder="10"
                className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
                required
              />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Target Profit %</label>
              <input
                type="number"
                name="target_profit_percentage"
                value={formData.target_profit_percentage}
                onChange={handleChange}
                placeholder="15"
                step="0.1"
                className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Stop Loss %</label>
              <input
                type="number"
                name="stop_loss_percentage"
                value={formData.stop_loss_percentage}
                onChange={handleChange}
                placeholder="10"
                step="0.1"
                className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Notes</label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Add any notes about this investment..."
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 resize-none h-20"
            />
          </div>
          
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading || stocks.length === 0}
              className="flex-1 bg-primary hover:bg-primary/80 rounded px-4 py-2 font-medium disabled:opacity-50"
            >
              {loading ? 'Adding...' : stocks.length === 0 ? 'Loading Stocks...' : 'Add to Portfolio'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-white/10 hover:bg-white/20 rounded px-4 py-2 font-medium"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export const Portfolio = () => {
  const [portfolioItems, setPortfolioItems] = useState([])
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  
  useEffect(() => {
    loadData()
  }, [])
  
  const loadData = async () => {
    try {
      setLoading(true)
      console.log('Loading portfolio and stocks...')
      const [portfolioRes, stocksRes] = await Promise.all([
        portfolioAPI.getList(),
        stocksAPI.listAll(),
      ])
      console.log('Portfolio items:', portfolioRes.data)
      console.log('Stocks loaded:', stocksRes.data?.length || 0, 'stocks')
      setPortfolioItems(portfolioRes.data)
      setStocks(stocksRes.data)
      
      if (!stocksRes.data || stocksRes.data.length === 0) {
        console.warn('No stocks found! Backend may not have initialized properly.')
      }
    } catch (error) {
      console.error('Error loading data:', error)
      toast.error('Failed to load portfolio')
    } finally {
      setLoading(false)
    }
  }
  
  const handleRemove = async (id) => {
    if (!window.confirm('Are you sure you want to sell this position?')) return
    
    try {
      await portfolioAPI.remove(id)
      toast.success('Position sold')
      loadData()
    } catch (error) {
      toast.error('Failed to remove from portfolio')
    }
  }
  
  if (loading) return <Layout><LoadingSpinner /></Layout>
  
  const totalInvested = portfolioItems.reduce((sum, item) => sum + item.total_invested, 0)
  const totalValue = portfolioItems.reduce((sum, item) => sum + item.current_value, 0)
  const totalProfitLoss = totalValue - totalInvested
  
  return (
    <Layout>
      <Header
        title="Portfolio"
        subtitle="Your stock holdings and performance"
        action={
          <div className="flex gap-2">
            <button
              onClick={loadData}
              className="flex items-center gap-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg font-medium"
            >
              <RefreshCw size={20} />
              Refresh
            </button>
            <button
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-2 bg-primary hover:bg-primary/80 px-4 py-2 rounded-lg font-medium"
            >
              <Plus size={20} />
              Add Stock
            </button>
          </div>
        }
      />
      
      <AddPortfolioModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        stocks={stocks}
        onAdded={loadData}
      />
      
      {portfolioItems.length > 0 ? (
        <>
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="glass rounded-lg p-4">
              <p className="text-sm text-gray-400 mb-1">Total Invested</p>
              <p className="text-2xl font-bold">{formatCurrency(totalInvested)}</p>
            </div>
            <div className="glass rounded-lg p-4">
              <p className="text-sm text-gray-400 mb-1">Current Value</p>
              <p className="text-2xl font-bold">{formatCurrency(totalValue)}</p>
            </div>
            <div className="glass rounded-lg p-4">
              <p className="text-sm text-gray-400 mb-1">Profit/Loss</p>
              <p className={`text-2xl font-bold ${totalProfitLoss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {totalProfitLoss >= 0 ? '+' : ''}{formatCurrency(totalProfitLoss)}
              </p>
            </div>
          </div>
          
          {/* Portfolio Items */}
          <div>
            {portfolioItems.map(item => (
              <PortfolioItemRow
                key={item.id}
                item={item}
                onUpdate={() => console.log('Update:', item.id)}
                onRemove={() => handleRemove(item.id)}
              />
            ))}
          </div>
        </>
      ) : (
        <EmptyState
          title="No Holdings"
          description="You don't have any stocks in your portfolio yet"
          action={
            <button
              onClick={() => setModalOpen(true)}
              className="bg-primary hover:bg-primary/80 px-6 py-2 rounded-lg font-medium"
            >
              Add Your First Stock
            </button>
          }
        />
      )}
    </Layout>
  )
}
