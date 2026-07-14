import { Navigate } from 'react-router-dom'

// /workspace was the old public URL; the page is now the registry.
export default function WorkspaceRedirect() {
  return <Navigate to="/registry" replace />
}
