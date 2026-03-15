import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Phases from './pages/Phases'
import Agents from './pages/Agents'
import Artifacts from './pages/Artifacts'
import Compliance from './pages/Compliance'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/phases" element={<Phases />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/artifacts" element={<Artifacts />} />
          <Route path="/compliance" element={<Compliance />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
