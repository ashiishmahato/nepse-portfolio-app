import React, { useState, useEffect } from 'react'

export const MarketStatus = () => {
  const [marketStatus, setMarketStatus] = useState({
    isOpen: false,
    timeRemaining: '',
    nepaliTime: '',
    ukTime: '',
    statusColor: 'red',
    countdownDisplay: '00:00:00',
    progress: 0
  })

  useEffect(() => {
    const updateMarketStatus = () => {
      // Get current time in UTC
      const now = new Date()

      // Convert to Nepali Time (UTC+5:45)
      const utcTime = new Date(now.toLocaleString('en-US', { timeZone: 'UTC' }))
      const nepaliTime = new Date(utcTime.getTime() + (5 * 60 + 45) * 60 * 1000)

      // Get UK Time
      const ukTime = new Date(now.toLocaleString('en-US', { timeZone: 'Europe/London' }))

      // Extract time components for Nepali Time
      const nepaliHours = nepaliTime.getHours()
      const nepaliMinutes = nepaliTime.getMinutes()
      const nepaliSeconds = nepaliTime.getSeconds()
      const nepaliDay = nepaliTime.getDay()

      // Extract time components for UK Time
      const ukHours = ukTime.getHours()
      const ukMinutes = ukTime.getMinutes()
      const ukSeconds = ukTime.getSeconds()

      // Format times
      const formatTime = (h, m, s) => {
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
      }

      const nepaliTimeStr = formatTime(nepaliHours, nepaliMinutes, nepaliSeconds)
      const ukTimeStr = formatTime(ukHours, ukMinutes, ukSeconds)

      // NEPSE Market Hours: 11:30 AM to 3:30 PM NST (Monday=1 to Friday=5)
      const totalMinutes = nepaliHours * 60 + nepaliMinutes
      const marketOpenTime = 11 * 60 + 30 // 11:30 AM = 690 minutes
      const marketCloseTime = 15 * 60 + 30 // 3:30 PM = 930 minutes

      let isOpen = false
      let timeRemaining = ''
      let statusColor = 'red'
      let countdownDisplay = ''
      let progress = 0

      // Check if market is open (Monday=1 to Friday=5)
      if (nepaliDay >= 1 && nepaliDay <= 5) {
        if (totalMinutes >= marketOpenTime && totalMinutes < marketCloseTime) {
          // Market is OPEN
          isOpen = true
          statusColor = 'green'
          const remainingMinutes = marketCloseTime - totalMinutes
          const closingHours = Math.floor(remainingMinutes / 60)
          const closingMins = remainingMinutes % 60
          countdownDisplay = `${String(closingHours).padStart(2, '0')}:${String(closingMins).padStart(2, '0')}:00`
          timeRemaining = `Market Closes In`
          progress = ((totalMinutes - marketOpenTime) / (marketCloseTime - marketOpenTime)) * 100
        } else if (totalMinutes < marketOpenTime) {
          // Market opens later today
          statusColor = 'yellow'
          const openingMinutes = marketOpenTime - totalMinutes
          const openingHours = Math.floor(openingMinutes / 60)
          const openingMins = openingMinutes % 60
          countdownDisplay = `${String(openingHours).padStart(2, '0')}:${String(openingMins).padStart(2, '0')}:00`
          timeRemaining = `Market Opens In`
          progress = 0
        } else {
          // Market closed for the day
          statusColor = 'red'
          countdownDisplay = '--:--:--'
          timeRemaining = 'Market Closed'
          progress = 100
        }
      } else {
        // Weekend
        statusColor = 'red'
        countdownDisplay = '--:--:--'
        timeRemaining = 'Market Closed (Weekend)'
        progress = 100
      }

      setMarketStatus({
        isOpen,
        timeRemaining,
        nepaliTime: nepaliTimeStr,
        ukTime: ukTimeStr,
        statusColor,
        countdownDisplay,
        progress
      })
    }

    // Update immediately
    updateMarketStatus()

    // Update every second
    const interval = setInterval(updateMarketStatus, 1000)
    return () => clearInterval(interval)
  }, [])

  const statusBgColor = {
    green: 'bg-gradient-to-r from-green-900/30 to-green-800/20 border border-green-500/50',
    yellow: 'bg-gradient-to-r from-yellow-900/30 to-yellow-800/20 border border-yellow-500/50',
    red: 'bg-gradient-to-r from-red-900/30 to-red-800/20 border border-red-500/50'
  }

  const statusTextColor = {
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    red: 'text-red-400'
  }

  const indicatorColor = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500'
  }

  const progressBarColor = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500'
  }

  return (
    <div className={`glass rounded-lg p-6 ${statusBgColor[marketStatus.statusColor]}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-xl">📈 NEPSE Market</h3>
        <div className="flex items-center gap-2">
          <div className={`w-4 h-4 rounded-full ${indicatorColor[marketStatus.statusColor]} animate-pulse`}></div>
          <span className={`font-bold text-lg ${statusTextColor[marketStatus.statusColor]}`}>
            {marketStatus.isOpen ? '🟢 OPEN' : '🔴 CLOSED'}
          </span>
        </div>
      </div>

      {/* Large Countdown Timer */}
      <div className="bg-black/30 rounded-lg p-6 mb-4 border border-white/10 text-center">
        <p className={`text-sm font-semibold mb-2 ${statusTextColor[marketStatus.statusColor]}`}>
          {marketStatus.timeRemaining}
        </p>
        <p className="font-mono text-5xl font-bold gradient-text tracking-wider">
          {marketStatus.countdownDisplay}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full rounded-full ${progressBarColor[marketStatus.statusColor]} transition-all duration-1000`}
            style={{ width: `${marketStatus.progress}%` }}
          ></div>
        </div>
      </div>

      {/* Times Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-white/5 rounded-lg p-3 border border-white/10">
          <p className="text-xs text-gray-400 font-semibold mb-1">🇳🇵 NEPALI TIME (NST)</p>
          <p className="font-mono text-2xl font-bold text-cyan-400">
            {marketStatus.nepaliTime}
          </p>
        </div>
        <div className="bg-white/5 rounded-lg p-3 border border-white/10">
          <p className="text-xs text-gray-400 font-semibold mb-1">🇬🇧 UK TIME (GMT/BST)</p>
          <p className="font-mono text-2xl font-bold text-blue-400">
            {marketStatus.ukTime}
          </p>
        </div>
      </div>

      {/* Market Info */}
      <div className="bg-white/5 rounded-lg p-3 text-sm">
        <div className="space-y-1 text-gray-300">
          <p>⏰ <span className="font-semibold">Market Hours:</span> 11:30 AM - 3:30 PM NST</p>
          <p>📅 <span className="font-semibold">Trading Days:</span> Monday - Friday</p>
        </div>
      </div>
    </div>
  )
}
