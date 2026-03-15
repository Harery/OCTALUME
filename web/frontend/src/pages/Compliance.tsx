import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Shield, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react'
import api from '@/lib/api'
import { useState } from 'react'

interface Standard {
  id: string
  name: string
  description: string
}

interface ScanResult {
  scan_id: string
  timestamp: string
  summary: {
    overall_status: string
    total_findings: number
    critical_findings: number
  }
}

export default function Compliance() {
  const queryClient = useQueryClient()
  const [selectedStandards, setSelectedStandards] = useState<string[]>([])

  const { data: standards } = useQuery<Standard[]>({
    queryKey: ['compliance', 'standards'],
    queryFn: () => api.get('/api/compliance/standards').then(r => r.data.standards),
  })

  const { data: status } = useQuery({
    queryKey: ['compliance', 'status'],
    queryFn: () => api.get('/api/compliance/status').then(r => r.data),
  })

  const scanMutation = useMutation({
    mutationFn: (standards: string[]) =>
      api.post('/api/compliance/scan', null, { params: { standards: standards.join(',') } }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['compliance'] }),
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Compliance</h1>
        <button
          onClick={() => scanMutation.mutate(selectedStandards)}
          disabled={scanMutation.isPending || selectedStandards.length === 0}
          className="btn btn-primary"
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${scanMutation.isPending ? 'animate-spin' : ''}`} />
          Run Scan
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {standards?.map((standard) => {
          const isConfigured = status?.configured_standards?.includes(standard.id)
          const isSelected = selectedStandards.includes(standard.id)

          return (
            <div
              key={standard.id}
              onClick={() => {
                setSelectedStandards(prev =>
                  isSelected
                    ? prev.filter(s => s !== standard.id)
                    : [...prev, standard.id]
                )
              }}
              className={`
                card cursor-pointer transition-all
                ${isSelected ? 'ring-2 ring-primary-500' : ''}
              `}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`
                    w-10 h-10 rounded-lg flex items-center justify-center
                    ${isConfigured ? 'bg-primary-100' : 'bg-gray-100'}
                  `}>
                    <Shield className={`w-5 h-5 ${isConfigured ? 'text-primary-600' : 'text-gray-400'}`} />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{standard.name}</h3>
                    <p className="text-xs text-gray-500">{standard.id}</p>
                  </div>
                </div>
                {isConfigured && (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                )}
              </div>
              <p className="mt-3 text-sm text-gray-500">{standard.description}</p>
            </div>
          )
        })}
      </div>

      {scanMutation.data && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Latest Scan Results</h2>
            <span className="text-sm text-gray-500">
              {new Date(scanMutation.data.timestamp).toLocaleString()}
            </span>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Status</p>
              <p className={`text-lg font-bold ${
                scanMutation.data.summary.overall_status === 'compliant'
                  ? 'text-green-600'
                  : 'text-red-600'
              }`}>
                {scanMutation.data.summary.overall_status}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Total Findings</p>
              <p className="text-lg font-bold text-gray-900">
                {scanMutation.data.summary.total_findings}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Critical</p>
              <p className={`text-lg font-bold ${
                scanMutation.data.summary.critical_findings > 0
                  ? 'text-red-600'
                  : 'text-gray-900'
              }`}>
                {scanMutation.data.summary.critical_findings}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
