import React from 'react'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'
import { getPriceColor, formatNumber } from '../utils/formatting'

/**
 * Price Change Badge Component
 */
export const PriceChangeBadge = ({ value, showIcon = true }) => {
  const isPositive = value > 0
  const color = getPriceColor(value)
  
  return (
    <span className={`inline-flex items-center gap-1 ${color}`}>
      {showIcon && (isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />)}
      {isPositive ? '+' : ''}{formatNumber(value, 2)}%
    </span>
  )
}

/**
 * Stock Price Card Component
 */
export const StockPriceCard = ({ stock, onClick }) => {
  const change = stock.analysis_score || 0
  
  return (
    <div
      onClick={onClick}
      className="glass rounded-lg p-4 cursor-pointer hover:bg-white/10 hover:border-white/20"
    >
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="font-bold text-lg">{stock.symbol}</h3>
          <p className="text-sm text-gray-400">{stock.name}</p>
        </div>
        <span className="text-xs bg-primary/20 text-primary px-2 py-1 rounded">
          {stock.sector}
        </span>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between items-end">
          <span className="text-2xl font-bold">Rs. {formatNumber(stock.current_price)}</span>
          <div className="text-right">
            <div className="text-sm text-gray-400">Analysis Score</div>
            <div className="text-lg font-bold gradient-text">{formatNumber(change, 1)}/4</div>
          </div>
        </div>
        
        <div className="flex justify-between items-center pt-2 border-t border-white/10">
          <span className="text-xs text-gray-400">Recommendation</span>
          <span className="text-sm font-semibold text-green-400">
            {stock.analysis_recommendation}
          </span>
        </div>
      </div>
    </div>
  )
}

/**
 * Alert Badge Component
 */
export const AlertBadge = ({ alert }) => {
  const alertColors = {
    sell_target: 'bg-green-900/20 text-green-300 border-green-500/30',
    buy_dip: 'bg-blue-900/20 text-blue-300 border-blue-500/30',
    stop_loss: 'bg-red-900/20 text-red-300 border-red-500/30',
    rsi_signal: 'bg-yellow-900/20 text-yellow-300 border-yellow-500/30',
  }
  
  const alertEmojis = {
    sell_target: '🎯',
    buy_dip: '💰',
    stop_loss: '⛔',
    rsi_signal: '📊',
  }
  
  return (
    <div className={`border rounded-lg p-3 ${alertColors[alert.alert_type] || 'glass'}`}>
      <div className="flex items-start gap-2">
        <span className="text-lg">{alertEmojis[alert.alert_type] || '📢'}</span>
        <div className="flex-1">
          <h4 className="font-semibold">{alert.title}</h4>
          <p className="text-sm opacity-80">{alert.description}</p>
          <div className="text-xs opacity-60 mt-1">
            Price: Rs. {formatNumber(alert.current_price)} | Trigger: Rs. {formatNumber(alert.trigger_price)}
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * Loading Spinner Component
 */
export const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center py-8">
      <div className="animate-spin rounded-full h-8 w-8 border border-primary border-t-transparent"></div>
    </div>
  )
}

/**
 * Empty State Component
 */
export const EmptyState = ({ icon: Icon, title, description, action }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      {Icon && <Icon size={48} className="text-gray-500 mb-4" />}
      <h3 className="text-lg font-semibold text-gray-300 mb-2">{title}</h3>
      <p className="text-gray-400 mb-6">{description}</p>
      {action}
    </div>
  )
}

/**
 * Stat Card Component
 */
export const StatCard = ({ label, value, unit = '', icon: Icon, color = 'primary' }) => {
  const colorMap = {
    primary: 'text-primary',
    success: 'text-green-400',
    danger: 'text-red-400',
    warning: 'text-yellow-400',
  }
  
  return (
    <div className="glass rounded-lg p-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">{label}</p>
          <p className="text-2xl font-bold">
            {value}
            {unit && <span className="text-sm text-gray-400 ml-1">{unit}</span>}
          </p>
        </div>
        {Icon && <Icon size={32} className={`${colorMap[color]} opacity-50`} />}
      </div>
    </div>
  )
}

/**
 * Portfolio Item Row Component
 */
export const PortfolioItemRow = ({ item, onUpdate, onRemove, onDelete }) => {
  const profitLoss = item.profit_loss || 0
  const profitLossColor = profitLoss >= 0 ? 'text-green-400' : 'text-red-400'
  
  return (
    <div className="glass rounded-lg p-4 mb-3">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h4 className="font-bold">{item.stock_symbol}</h4>
          <p className="text-sm text-gray-400">
            {item.quantity} @ Rs. {formatNumber(item.buy_price)}
          </p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold">Rs. {formatNumber(item.current_value)}</p>
          <p className={`text-sm ${profitLossColor}`}>
            {profitLoss >= 0 ? '+' : ''}{formatNumber(profitLoss, 2)} ({formatNumber(item.profit_loss_percentage, 2)}%)
          </p>
        </div>
      </div>
      
      <div className="flex gap-2">
        <div className="flex-1 text-sm">
          <p className="text-gray-400">Target: {item.target_profit_percentage}%</p>
          {item.stop_loss_percentage && (
            <p className="text-gray-400">Stop Loss: {item.stop_loss_percentage}%</p>
          )}
        </div>
        <div className="flex gap-2">
          <button
            onClick={onUpdate}
            className="px-3 py-1 bg-primary/20 hover:bg-primary/30 rounded text-sm"
          >
            Edit
          </button>
          <button
            onClick={onRemove}
            className="px-3 py-1 bg-yellow-900/20 hover:bg-yellow-900/30 rounded text-sm text-yellow-300"
          >
            Sell
          </button>
          <button
            onClick={onDelete}
            className="px-3 py-1 bg-red-900/20 hover:bg-red-900/30 rounded text-sm text-red-400"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}
