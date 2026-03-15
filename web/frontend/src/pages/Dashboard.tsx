import { useQuery } from '@tanstack/react-query'
import {
  Layers,
  Bot,
  FileText,
  CheckCircle,
  TrendingUp
} from 'lucide-react'
import api from '@/lib/api'

interface DashboardSummary {
  initialized: boolean
  name: string
  current_phase: number
  phase_status: string
  progress_percentage: number
  total_artifacts: number
}

interface Metrics {
  artifacts: { total: number }
  agents: { total: number; active: number }
  gates: { passed: number; failed: number }
}

interface TimelinePhase {
  phase: number
  name: string
  owner: string
  status: string
}

interface TimelineResponse {
  timeline: TimelinePhase[]
}

interface Metrics {
  artifacts: { total: number }
  agents: { total: number; active: number }
  gates: { passed: number; failed: number }
}

interface TimelinePhase {
  phase: number
  name: string
  owner: string
  status: string
}

interface TimelineResponse {
  timeline: TimelinePhase[]
}

export default function Dashboard() {
  const { data: summary, isLoading: summaryLoading } = useQuery<DashboardSummary>({
    queryKey: ['dashboard', 'summary'],
    queryFn: () => api.get('/api/dashboard/summary').then(r => r.data),
  })

  const { data: metrics, isLoading: metricsLoading } = useQuery<Metrics>({
    queryKey: ['dashboard', 'metrics'],
    queryFn: () => api.get('/api/dashboard/metrics').then(r => r.data),
  })

  const { data: timeline } = useQuery<TimelineResponse>({
    queryKey: ['dashboard', 'timeline'],
    queryFn: () => api.get('/api/dashboard/timeline').then(r => r.data),
  })

  if (summaryLoading || metricsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  if (!summary?.initialized) {
    return (
      <div className="card text-center py-12">
        <Layers className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">No Project Initialized</h2>
        <p className="text-gray-500 mb-4">
          Run <code className="bg-gray-100 px-2 py-1 rounded">octalume init &lt;name&gt;</code> to create a project.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{summary.name}</h1>
        <p className="text-gray-500">Phase {summary.current_phase} - {summary.phase_status}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Progress</p>
              <p className="text-2xl font-bold text-gray-900">{summary.progress_percentage}%</p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-primary-500" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Artifacts</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.artifacts.total || 0}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-blue-500" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Agents</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.agents.active || 0}</p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Bot className="w-6 h-6 text-purple-500" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Gates Passed</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.gates.passed || 0}</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Phase Timeline */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Phase Timeline</h2>
        <div className="space-y-3">
          {timeline?.timeline?.map((phase: TimelinePhase) => (
            <div
              key={phase.phase}
              className="flex items-center gap-4 p-3 rounded-lg bg-gray-50"
            >
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold
                ${phase.status === 'completed' ? 'bg-green-500 text-white' : ''}
                ${phase.status === 'in_progress' ? 'bg-yellow-500 text-white' : ''}
                ${phase.status === 'blocked' ? 'bg-red-500 text-white' : ''}
                ${phase.status === 'not_started' ? 'bg-gray-200 text-gray-600' : ''}
              `}>
                {phase.phase}
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">{phase.name}</p>
                <p className="text-sm text-gray-500">{phase.owner}</p>
              </div>
              <span className={`
                px-2 py-1 rounded text-xs font-medium
                ${phase.status === 'completed' ? 'bg-green-100 text-green-700' : ''}
                ${phase.status === 'in_progress' ? 'bg-yellow-100 text-yellow-700' : ''}
                ${phase.status === 'blocked' ? 'bg-red-100 text-red-700' : ''}
                ${phase.status === 'not_started' ? 'bg-gray-100 text-gray-600' : ''}
              `}>
                {phase.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
