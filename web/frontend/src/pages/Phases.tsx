import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Play, CheckCircle } from 'lucide-react'
import api from '@/lib/api'

interface Phase {
  number: number
  name: string
  status: string
  owner: string
  artifacts_count: number
  started_at: string | null
  completed_at: string | null
}

interface PhasesResponse {
  current_phase: number
  phases: Phase[]
}

export default function Phases() {
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery<PhasesResponse>({
    queryKey: ['phases'],
    queryFn: () => api.get('/api/phases').then(r => r.data),
  })

  const startMutation = useMutation({
    mutationFn: (phase: number) => api.post(`/api/phases/${phase}/start`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['phases'] }),
  })

  const completeMutation = useMutation({
    mutationFn: (phase: number) => api.post(`/api/phases/${phase}/complete`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['phases'] }),
  })

  const transitionMutation = useMutation({
    mutationFn: (phase: number) => api.post(`/api/phases/${phase}/transition`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['phases'] }),
  })

  if (isLoading) {
    return <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div></div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Phases</h1>
        <div className="text-sm text-gray-500">
          Current: Phase {data?.current_phase}
        </div>
      </div>

      <div className="grid gap-4">
        {data?.phases?.map((phase: Phase) => (
          <div key={phase.number} className="card">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className={`
                  w-12 h-12 rounded-lg flex items-center justify-center text-lg font-bold
                  ${phase.status === 'completed' ? 'bg-green-500 text-white' : ''}
                  ${phase.status === 'in_progress' ? 'bg-yellow-500 text-white' : ''}
                  ${phase.status === 'blocked' ? 'bg-red-500 text-white' : ''}
                  ${phase.status === 'not_started' ? 'bg-gray-200 text-gray-600' : ''}
                `}>
                  {phase.number}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{phase.name}</h3>
                  <p className="text-sm text-gray-500">Owner: {phase.owner}</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className={`
                  px-3 py-1 rounded-full text-xs font-medium
                  ${phase.status === 'completed' ? 'bg-green-100 text-green-700' : ''}
                  ${phase.status === 'in_progress' ? 'bg-yellow-100 text-yellow-700' : ''}
                  ${phase.status === 'blocked' ? 'bg-red-100 text-red-700' : ''}
                  ${phase.status === 'not_started' ? 'bg-gray-100 text-gray-600' : ''}
                `}>
                  {phase.status}
                </span>

                {phase.status === 'not_started' && phase.number === data?.current_phase && (
                  <button
                    onClick={() => startMutation.mutate(phase.number)}
                    className="btn btn-primary text-sm"
                    disabled={startMutation.isPending}
                  >
                    <Play className="w-4 h-4 mr-1" />
                    Start
                  </button>
                )}

                {phase.status === 'in_progress' && (
                  <button
                    onClick={() => completeMutation.mutate(phase.number)}
                    className="btn btn-primary text-sm"
                    disabled={completeMutation.isPending}
                  >
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Complete
                  </button>
                )}

                {phase.status === 'completed' && phase.number === data?.current_phase && phase.number < 8 && (
                  <button
                    onClick={() => transitionMutation.mutate(phase.number)}
                    className="btn btn-secondary text-sm"
                    disabled={transitionMutation.isPending}
                  >
                    Next Phase
                  </button>
                )}
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 flex items-center gap-6 text-sm text-gray-500">
              <span>Artifacts: {phase.artifacts_count}</span>
              {phase.started_at && <span>Started: {new Date(phase.started_at).toLocaleDateString()}</span>}
              {phase.completed_at && <span>Completed: {new Date(phase.completed_at).toLocaleDateString()}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
