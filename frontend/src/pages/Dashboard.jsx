import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { StatCard, LoadingSpinner, EmptyState, AlertBadge } from '../components/common'
import { MarketStatus } from '../components/MarketStatus'
import { portfolioAPI, alertsAPI } from '../services/api'
import { formatCurrency, formatNumber, formatDateTime } from '../utils/formatting'
import { TrendingUp, AlertCircle, Briefcase } from 'lucide-react'
import toast from 'react-hot-toast'

export const Dashboard = () => {
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    loadDashboard()
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboard, 30000)
    return () => clearInterval(interval)
  }, [])
  
  const loadDashboard = async () => {
    try {
      const dashboardRes = await portfolioAPI.getDashboard()
      setDashboard(dashboardRes.data)
    } catch (error) {
      console.error('Error loading dashboard:', error)
      toast.error('Failed to load dashboard')
    } finally {
      setLoading(false)
    }
  }
  
  if (loading) return <Layout><LoadingSpinner /></Layout>
  if (!dashboard) return <Layout><EmptyState title="No Data" description="Unable to load dashboard" /></Layout>
  
  const totalReturn = dashboard.total_profit_loss_percentage || 0
  const totalReturnColor = totalReturn >= 0 ? 'text-green-400' : 'text-red-400'
  
  return (
    <Layout>
      <Header
        title="Dashboard"
        subtitle="Your NEPSE investment overview"
      />
      
      {/* Market Status */}
      <div className="mb-8">
        <MarketStatus />
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Total Invested"
          value={formatCurrency(dashboard.total_invested)}
          icon={Briefcase}
          color="primary"
        />
        <StatCard
          label="Current Value"
          value={formatCurrency(dashboard.total_current_value)}
          icon={TrendingUp}
          color="primary"
        />
        <StatCard
          label="Profit/Loss"
          value={formatCurrency(dashboard.total_profit_loss)}
          unit=""
          color={dashboard.total_profit_loss >= 0 ? 'success' : 'danger'}
          icon={null}
        />
        <StatCard
          label="Return %"
          value={formatNumber(totalReturn, 2) + '%'}
          color={dashboard.total_profit_loss >= 0 ? 'success' : 'danger'}
          icon={null}
        />
      </div>
      
      {/* Portfolio and Alerts Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Portfolio Summary */}
        <div className="lg:col-span-2 glass rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">Portfolio Holdings</h2>
          
          {dashboard.portfolio_items && dashboard.portfolio_items.length > 0 ? (
            <div className="space-y-2">
              {dashboard.portfolio_items.slice(0, 5).map((item) => {
                const profitColor = item.profit_loss >= 0 ? 'text-green-400' : 'text-red-400'
                return (
                  <div key={item.id} className="flex items-center justify-between p-3 bg-white/5 rounded">
                    <div className="flex-1">
                      <p className="font-semibold">{item.stock_symbol}</p>
                      <p className="text-sm text-gray-400">{item.quantity} shares @ Rs. {formatNumber(item.buy_price)}</p>
                    </div>
                    <div className="text-right">
                      <p className={`font-bold ${profitColor}`}>
                        {item.profit_loss >= 0 ? '+' : ''}{formatNumber(item.profit_loss_percentage, 2)}%
                      </p>
                      <p className="text-sm text-gray-400">Rs. {formatNumber(item.current_value)}</p>
                    </div>
                  </div>
                )
              })}
              {dashboard.portfolio_items.length > 5 && (
                <p className="text-center text-sm text-gray-400 pt-2">
                  +{dashboard.portfolio_items.length - 5} more holdings
                </p>
              )}
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">No portfolio holdings yet</p>
          )}
        </div>
        
        {/* Alert Summary */}
        <div className="glass rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <AlertCircle size={20} />
            Active Alerts
          </h2>
          
          <div className="text-3xl font-bold gradient-text mb-4">
            {dashboard.active_alerts_count}
          </div>
          
          {dashboard.recent_alerts && dashboard.recent_alerts.length > 0 ? (
            <div className="space-y-2">
              {dashboard.recent_alerts.slice(0, 3).map((alert) => (
                <div key={alert.id} className="p-2 bg-white/5 rounded text-sm">
                  <p className="font-semibold text-yellow-400">{alert.alert_type}</p>
                  <p className="text-gray-400">{alert.stock_symbol}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">No active alerts</p>
          )}
        </div>
      </div>
    </Layout>
  )
}
