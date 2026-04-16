/**
 * Format number to currency format (NPR - Nepali Rupees)
 */
export const formatCurrency = (value) => {
  return new Intl.NumberFormat('ne-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 2,
  }).format(value)
}

/**
 * Format number with commas
 */
export const formatNumber = (value, decimals = 2) => {
  return parseFloat(value).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
}

/**
 * Format percentage
 */
export const formatPercent = (value) => {
  return `${(value >= 0 ? '+' : '')}{formatNumber(value, 2)}%`
}

/**
 * Get color based on value (positive/negative)
 */
export const getPriceColor = (value) => {
  if (value > 0) return 'text-green-400'
  if (value < 0) return 'text-red-400'
  return 'text-gray-300'
}

/**
 * Get background color based on value
 */
export const getPriceBgColor = (value) => {
  if (value > 0) return 'bg-green-900/20'
  if (value < 0) return 'bg-red-900/20'
  return 'bg-gray-800'
}

/**
 * Format date
 */
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

/**
 * Format date and time
 */
export const formatDateTime = (date) => {
  return new Date(date).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Get recommendation color and icon
 */
export const getRecommendationStyle = (recommendation) => {
  const styles = {
    strong_buy: { color: 'text-green-400', bg: 'bg-green-900/20', label: '🚀 Strong Buy' },
    buy: { color: 'text-green-300', bg: 'bg-green-900/10', label: '📈 Buy' },
    watch: { color: 'text-yellow-400', bg: 'bg-yellow-900/10', label: '👀 Watch' },
    sell: { color: 'text-red-300', bg: 'bg-red-900/10', label: '📉 Sell' },
    strong_sell: { color: 'text-red-400', bg: 'bg-red-900/20', label: '⛔ Strong Sell' },
  }
  return styles[recommendation] || styles.watch
}

/**
 * Get alert type emoji and color
 */
export const getAlertTypeStyle = (type) => {
  const styles = {
    sell_target: { emoji: '🎯', color: 'text-green-400', label: 'Sell Target' },
    buy_dip: { emoji: '💰', color: 'text-blue-400', label: 'Buy Dip' },
    stop_loss: { emoji: '⛔', color: 'text-red-400', label: 'Stop Loss' },
    rsi_signal: { emoji: '📊', color: 'text-yellow-400', label: 'RSI Signal' },
    ma_crossover: { emoji: '📈', color: 'text-purple-400', label: 'MA Crossover' },
  }
  return styles[type] || { emoji: '📢', color: 'text-gray-400', label: 'Alert' }
}
