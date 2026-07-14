import { type RouteConfig, index, route } from "@react-router/dev/routes";

// routes.ts executes under Node at build time; tsconfig.app has no node types.
declare const process: { env: Record<string, string | undefined> };

// Registry pages are still preview-gated: enabled on the tryout service,
// compiled out of the public site until the multi-tenant backend lands.
const registryEnabled = process.env.VITE_ENABLE_WORKSPACE === "true";

export default [
  index("pages/HomePage.tsx"),
  ...(registryEnabled
    ? [
        route("/registry", "pages/RegistryPage.tsx"),
        route("/connect", "pages/ConnectRoute.tsx"),
        route("/vocabularies/bootstrap", "pages/VocabularyPage.tsx"),
        // Old public URL — kept as a redirect so bookmarks survive.
        route("/workspace", "pages/WorkspaceRedirect.tsx"),
      ]
    : []),
  route("/graph", "pages/GraphPageLazy.tsx"),
  route("/docs", "pages/DocsPage.tsx"),
] satisfies RouteConfig;
