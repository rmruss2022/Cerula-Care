import { useMemo } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { HealthScreening } from '../types'
import { format, parseISO } from 'date-fns'

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

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'improving':
        return 'text-[#28a745]'
      case 'worsening':
        return 'text-[#dc3545]'
      case 'stable':
        return 'text-[#6c757d]'
      default:
        return 'text-[#6c757d]'
    }
  }

  return (
    <div className="mb-8">
      <div className="flex gap-8 mb-6 p-4 bg-[#f8f9fa] rounded md:flex-col md:gap-4">
        <div className="flex flex-col gap-1">
          <span className="text-sm text-[#6c757d]">Average Score:</span>
          <span className="text-xl font-semibold text-[#2c3e50]">{averageScore.toFixed(1)}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-sm text-[#6c757d]">Trend:</span>
          <span className={`text-xl font-semibold ${getTrendColor(trend)}`}>{trend}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-sm text-[#6c757d]">Total Screenings:</span>
          <span className="text-xl font-semibold text-[#2c3e50]">{screenings.length}</span>
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
      <div className="mt-4 p-4 bg-[#e7f3ff] border-l-4 border-[#007bff] rounded">
        <p className="m-0 text-sm text-[#495057]">
          <strong>Score Interpretation:</strong> Lower scores indicate improvement. Scores range from 0-10, with
          higher scores indicating more severe symptoms.
        </p>
      </div>
    </div>
  )
}

export default HealthScreeningChart
