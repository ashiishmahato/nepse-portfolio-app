import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { LoadingSpinner, EmptyState, PortfolioItemRow } from '../components/common'
import { portfolioAPI, stocksAPI } from '../services/api'
import { formatCurrency, formatNumber } from '../utils/formatting'
import { Plus, RefreshCw, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

const AddPortfolioModal = ({ isOpen, onClose, stocks, onAdded }) => {
  const [formData, setFormData] = useState({
    stock_symbol: '',
    buy_price: '',
    quantity: '',
    target_profit_percentage: 15,
    stop_loss_percentage: '',
    purchase_date: '',
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  
  const handleChange = (e) => {
    const { name, value } = e.target
    if (name === 'quantity') {
      setFormData(prev => ({
        ...prev,
        [name]: parseInt(value) || ''
      }))
    } else if (name === 'purchase_date') {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: parseFloat(value) || value
      }))
    }
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
        purchase_date: formData.purchase_date && formData.purchase_date.trim() ? formData.purchase_date : null,
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
        purchase_date: '',
        notes: '',
      })
      
      // Close modal first
      onClose()
      
      // Then reload data with better error handling
      setTimeout(() => {
        console.log('Calling onAdded to reload data...')
        onAdded().catch(err => {
          console.error('Error in onAdded callback:', err)
          toast.error('Error reloading portfolio')
        })
      }, 300)
      
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
                placeholder="Leave empty for no stop loss"
                step="0.1"
                min="0"
                max="100"
                className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
              />
              <p className="text-xs text-gray-500 mt-1">Enter 0 or leave empty to skip stop loss</p>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Purchase Date</label>
            <input
              type="date"
              name="purchase_date"
              value={formData.purchase_date}
              onChange={handleChange}
              max={new Date().toISOString().split('T')[0]}
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 text-white"
              style={{ colorScheme: 'dark' }}
            />
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

const EditPortfolioModal = ({ isOpen, onClose, item, onUpdated }) => {
  const [formData, setFormData] = useState({
    target_profit_percentage: 15,
    stop_loss_percentage: '',
    purchase_date: '',
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  
  // Update form data when item changes
  useEffect(() => {
    if (item) {
      setFormData({
        target_profit_percentage: item.target_profit_percentage || 15,
        stop_loss_percentage: item.stop_loss_percentage || '',
        purchase_date: item.purchase_date ? item.purchase_date.split('T')[0] : '',
        notes: item.notes || '',
      })
    }
  }, [item, isOpen])
  
  const handleChange = (e) => {
    const { name, value } = e.target
    if (name === 'purchase_date') {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: parseFloat(value) || value
      }))
    }
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      await portfolioAPI.update(item.id, {
        target_profit_percentage: parseFloat(formData.target_profit_percentage),
        stop_loss_percentage: formData.stop_loss_percentage ? parseFloat(formData.stop_loss_percentage) : null,
        purchase_date: formData.purchase_date || null,
        notes: formData.notes,
      })
      toast.success('Portfolio updated!')
      onClose()
      onUpdated()
    } catch (error) {
      console.error('Error updating portfolio:', error)
      toast.error(error.response?.data?.detail || 'Failed to update portfolio')
    } finally {
      setLoading(false)
    }
  }
  
  if (!isOpen) return null
  
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass rounded-lg max-w-md w-full p-6">
        <h2 className="text-2xl font-bold mb-4">Edit {item?.stock_symbol}</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Target Profit %</label>
            <input
              type="number"
              name="target_profit_percentage"
              value={formData.target_profit_percentage}
              onChange={handleChange}
              step="0.1"
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Stop Loss %</label>
            <input
              type="number"
              name="stop_loss_percentage"
              value={formData.stop_loss_percentage}
              onChange={handleChange}
              placeholder="Leave empty for no stop loss"
              step="0.1"
              min="0"
              max="100"
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2"
            />
            <p className="text-xs text-gray-500 mt-1">Enter 0 or leave empty to skip stop loss</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Purchase Date</label>
            <input
              type="date"
              name="purchase_date"
              value={formData.purchase_date}
              onChange={handleChange}
              max={new Date().toISOString().split('T')[0]}
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 text-white"
              style={{ colorScheme: 'dark' }}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Notes</label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Add notes..."
              className="w-full bg-white/10 border border-white/20 rounded px-3 py-2 resize-none h-20"
            />
          </div>
          
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-primary hover:bg-primary/80 rounded px-4 py-2 font-medium disabled:opacity-50"
            >
              {loading ? 'Updating...' : 'Update'}
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
  const [error, setError] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [editModalOpen, setEditModalOpen] = useState(false)
  
  useEffect(() => {
    loadData()
  }, [])
  
  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      console.log('📂 Loading portfolio and stocks...')
      
      const [portfolioRes, stocksRes] = await Promise.all([
        portfolioAPI.getList().catch(err => {
          console.error('❌ Error fetching portfolio:', err)
          throw err
        }),
        stocksAPI.listAll().catch(err => {
          console.error('❌ Error fetching stocks:', err)
          throw err
        }),
      ])
      
      console.log('✅ Portfolio items:', portfolioRes.data)
      console.log('✅ Stocks loaded:', stocksRes.data?.length || 0, 'stocks')
      
      // Ensure data is an array
      const portfolioData = Array.isArray(portfolioRes.data) ? portfolioRes.data : []
      const stocksData = Array.isArray(stocksRes.data) ? stocksRes.data : []
      
      console.log(`📊 Setting state - Portfolio: ${portfolioData.length} items, Stocks: ${stocksData.length} items`)
      
      setPortfolioItems(portfolioData)
      setStocks(stocksData)
      
      if (!stocksData || stocksData.length === 0) {
        console.warn('⚠️ No stocks found! Backend may not have initialized properly.')
        setError('No stocks available. Please refresh the page.')
      }
    } catch (error) {
      console.error('❌ Error loading data:', error)
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to load portfolio'
      setError(errorMsg)
      toast.error(errorMsg)
    } finally {
      setLoading(false)
      console.log('✅ Loading complete')
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
  
  const handleEdit = (item) => {
    setEditingItem(item)
    setEditModalOpen(true)
  }
  
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this position? This action cannot be undone.')) return
    
    try {
      await portfolioAPI.remove(id)
      toast.success('Position deleted')
      loadData()
    } catch (error) {
      toast.error('Failed to delete from portfolio')
    }
  }
  
  // Show loading state
  if (loading) {
    console.log('🔄 Showing loading spinner')
    return <Layout><LoadingSpinner /></Layout>
  }
  
  // Show error state only if stocks aren't available AND there's an error
  if (error && stocks.length === 0 && portfolioItems.length === 0) {
    console.log('❌ Showing error state')
    return (
      <Layout>
        <Header
          title="📈 Portfolio"
          subtitle="Your stock holdings and performance"
          action={
            <button
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-2 bg-primary hover:bg-primary/80 px-4 py-2 rounded-lg font-medium"
            >
              <Plus size={20} />
              Add Stock
            </button>
          }
        />
        <div className="text-center py-10">
          <AlertCircle size={48} className="mx-auto mb-4 text-red-400" />
          <p className="text-red-400 mb-2 font-bold">⚠️ {error}</p>
          <button
            onClick={loadData}
            className="mt-4 bg-primary hover:bg-primary/80 px-6 py-2 rounded-lg font-medium"
          >
            🔄 Try Again
          </button>
        </div>
      </Layout>
    )
  }
  
  const totalInvested = portfolioItems?.reduce((sum, item) => sum + (item?.total_invested || 0), 0) || 0
  const totalValue = portfolioItems?.reduce((sum, item) => sum + (item?.current_value || 0), 0) || 0
  const totalProfitLoss = totalValue - totalInvested
  
  console.log('📊 Rendering main portfolio view:', { portfolioItemsCount: portfolioItems?.length, stocksCount: stocks?.length })
  
  return (
    <Layout>
      <Header
        title="📈 Portfolio"
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
      
      <EditPortfolioModal
        isOpen={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        item={editingItem}
        onUpdated={loadData}
      />
      
      {portfolioItems && portfolioItems.length > 0 ? (
        <>
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="glass rounded-lg p-4 border border-white/10">
              <p className="text-sm text-gray-400 mb-1">💰 Total Invested</p>
              <p className="text-2xl font-bold text-cyan-400">{formatCurrency(totalInvested)}</p>
            </div>
            <div className="glass rounded-lg p-4 border border-white/10">
              <p className="text-sm text-gray-400 mb-1">📊 Current Value</p>
              <p className="text-2xl font-bold text-cyan-400">{formatCurrency(totalValue)}</p>
            </div>
            <div className="glass rounded-lg p-4 border border-white/10">
              <p className="text-sm text-gray-400 mb-1">📈 Profit/Loss</p>
              <p className={`text-2xl font-bold ${totalProfitLoss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {totalProfitLoss >= 0 ? '+' : ''}{formatCurrency(totalProfitLoss)}
              </p>
            </div>
          </div>
          
          {/* Portfolio Items */}
          <div className="space-y-3">
            {portfolioItems.map((item) => {
              if (!item) {
                console.warn('⚠️ Null portfolio item')
                return null
              }
              return (
                <PortfolioItemRow
                  key={item.id}
                  item={item}
                  onUpdate={() => handleEdit(item)}
                  onRemove={() => handleRemove(item.id)}
                  onDelete={() => handleDelete(item.id)}
                />
              )
            })}
          </div>
        </>
      ) : (
        <EmptyState
          title="📭 No Holdings Yet"
          description="Start building your portfolio by adding your first stock"
          action={
            <button
              onClick={() => setModalOpen(true)}
              className="bg-primary hover:bg-primary/80 px-6 py-2 rounded-lg font-medium"
            >
              ➕ Add Your First Stock
            </button>
          }
        />
      )}
    </Layout>
  )
}
