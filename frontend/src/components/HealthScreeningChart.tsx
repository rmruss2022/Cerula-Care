import { useMemo } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { HealthScreening } from '../types'
import { format, parseISO } from 'date-fns'
import './HealthScreeningChart.css'

interface HealthScreeningChartProps {
  screenings: HealthScreening[]
}

const HealthScreeningChart = ({ screenings }: HealthScreeningChartProps) => {
  const chartData = useMemo(() => {
    return screenings
      .slice()
      .sort((a, b) => new Date(a.screening_date).getTime() - new Date(b.screening_date).getTime())
      .map((screening) => ({
        date: format(parseISO(screening.screening_date), 'MMM dd, yyyy'),
        dateValue: screening.screening_date,
        score: screening.score,
      }))
  }, [screenings])

  const getScoreColor = (score: number) => {
    if (score >= 7) return '#dc3545' // High (red)
    if (score >= 4) return '#ffc107' // Medium (yellow)
    return '#28a745' // Low (green)
  }

  const averageScore = useMemo(() => {
    if (screenings.length === 0) return 0
    const sum = screenings.reduce((acc, s) => acc + s.score, 0)
    return sum / screenings.length
  }, [screenings])

  const trend = useMemo(() => {
    if (screenings.length < 2) return 'insufficient data'
    const sorted = [...screenings].sort(
      (a, b) => new Date(a.screening_date).getTime() - new Date(b.screening_date).getTime()
    )
    const first = sorted[0].score
    const last = sorted[sorted.length - 1].score
    const diff = last - first
    if (Math.abs(diff) < 0.5) return 'stable'
    return diff < 0 ? 'improving' : 'worsening'
  }, [screenings])

  return (
    <div className="health-screening-chart">
      <div className="chart-stats">
        <div className="stat-item">
          <span className="stat-label">Average Score:</span>
          <span className="stat-value">{averageScore.toFixed(1)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Trend:</span>
          <span className={`stat-value trend-${trend}`}>{trend}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Total Screenings:</span>
          <span className="stat-value">{screenings.length}</span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={80}
            interval={0}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            domain={[0, 10]}
            label={{ value: 'Score', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            formatter={(value: number) => [value.toFixed(1), 'Score']}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#007bff"
            strokeWidth={2}
            dot={{ r: 5, fill: '#007bff' }}
            name="Health Screening Score"
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="chart-legend-info">
        <p>
          <strong>Score Interpretation:</strong> Lower scores indicate improvement. Scores range from 0-10, with
          higher scores indicating more severe symptoms.
        </p>
      </div>
    </div>
  )
}

export default HealthScreeningChart
