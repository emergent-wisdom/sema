import { RegistryPage } from './RegistryPage'

// /connect is the agent-connection surface. It reuses the registry
// component with the connect screen opened — one component, two URLs,
// until /connect grows into its own page (site-architecture pass 3).
export default function ConnectRoute() {
  return <RegistryPage initialScreen="connect" />
}
