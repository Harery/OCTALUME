import { useQuery } from '@tanstack/react-query'
import { FileText } from 'lucide-react'
import api from '@/lib/api'
import { useState } from 'react'

interface Artifact {
  id: string
  phase: number
  name: string
  artifact_type: string
  created_at: string
}

export default function Artifacts() {
  const [filter, setFilter] = useState({ phase: '', type: '', search: '' })

  const { data, isLoading } = useQuery({
    queryKey: ['artifacts', filter],
    queryFn: () => api.get('/api/artifacts', { params: filter }).then(r => r.data),
  })

  if (isLoading) {
    return <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div></div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Artifacts</h1>
        <span className="text-sm text-gray-500">{data?.count || 0} total</span>
      </div>

      <div className="card">
        <div className="flex gap-4">
          <select
            value={filter.phase}
            onChange={(e) => setFilter(f => ({ ...f, phase: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
          >
            <option value="">All Phases</option>
            {[1,2,3,4,5,6,7,8].map(p => <option key={p} value={p}>Phase {p}</option>)}
          </select>

          <select
            value={filter.type}
            onChange={(e) => setFilter(f => ({ ...f, type: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
          >
            <option value="">All Types</option>
            <option value="document">Document</option>
            <option value="code">Code</option>
            <option value="test">Test</option>
            <option value="configuration">Configuration</option>
            <option value="design">Design</option>
            <option value="report">Report</option>
            <option value="decision">Decision</option>
          </select>

          <input
            type="text"
            placeholder="Search artifacts..."
            value={filter.search}
            onChange={(e) => setFilter(f => ({ ...f, search: e.target.value }))}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
          />
        </div>
      </div>

      {!data?.artifacts?.length ? (
        <div className="card text-center py-12">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No artifacts found.</p>
        </div>
      ) : (
        <div className="card overflow-hidden p-0">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phase</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data?.artifacts?.map((artifact: Artifact) => (
                <tr key={artifact.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-mono text-primary-600">{artifact.id}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{artifact.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-500">{artifact.phase}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                      {artifact.artifact_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {new Date(artifact.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
