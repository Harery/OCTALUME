import { useQuery } from '@tanstack/react-query'
import { Bot, Circle } from 'lucide-react'
import api from '@/lib/api'

interface Agent {
  id: string
  name: string
  phase: number | null
  status: string
  current_task: string | null
  is_healthy: boolean
}

export default function Agents() {
  const { data, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: () => api.get('/api/agents').then(r => r.data),
    refetchInterval: 5000,
  })

  if (isLoading) {
    return <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div></div>
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Agents</h1>

      {!data?.agents?.length ? (
        <div className="card text-center py-12">
          <Bot className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No agents spawned yet.</p>
          <p className="text-sm text-gray-400 mt-1">
            Use <code className="bg-gray-100 px-2 py-0.5 rounded">octalume agent spawn</code> to create agents.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {data?.agents?.map((agent: Agent) => (
            <div key={agent.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`
                    w-10 h-10 rounded-lg flex items-center justify-center
                    ${agent.status === 'running' ? 'bg-green-100' : ''}
                    ${agent.status === 'idle' ? 'bg-gray-100' : ''}
                    ${agent.status === 'completed' ? 'bg-blue-100' : ''}
                    ${agent.status === 'failed' ? 'bg-red-100' : ''}
                  `}>
                    <Bot className={`
                      w-5 h-5
                      ${agent.status === 'running' ? 'text-green-600' : ''}
                      ${agent.status === 'idle' ? 'text-gray-500' : ''}
                      ${agent.status === 'completed' ? 'text-blue-600' : ''}
                      ${agent.status === 'failed' ? 'text-red-600' : ''}
                    `} />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{agent.name}</h3>
                    <p className="text-xs text-gray-500 font-mono">{agent.id}</p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Circle className={`w-2 h-2 ${agent.is_healthy ? 'fill-green-500 text-green-500' : 'fill-red-500 text-red-500'}`} />
                  <span className={`
                    px-2 py-0.5 rounded text-xs font-medium
                    ${agent.status === 'running' ? 'bg-green-100 text-green-700' : ''}
                    ${agent.status === 'idle' ? 'bg-gray-100 text-gray-600' : ''}
                    ${agent.status === 'completed' ? 'bg-blue-100 text-blue-700' : ''}
                    ${agent.status === 'failed' ? 'bg-red-100 text-red-700' : ''}
                  `}>
                    {agent.status}
                  </span>
                </div>
              </div>

              {agent.current_task && (
                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 mb-1">Current Task</p>
                  <p className="text-sm text-gray-700">{agent.current_task}</p>
                </div>
              )}

              <div className="mt-4 text-sm text-gray-500">
                Phase: {agent.phase || 'N/A'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
