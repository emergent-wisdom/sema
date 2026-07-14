import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("pages/HomePage.tsx"),
  ...(process.env.VITE_ENABLE_WORKSPACE === "true"
    ? [route("/workspace", "pages/RegistryPage.tsx")]
    : []),
  route("/graph", "pages/GraphPageLazy.tsx"),
  route("/docs", "pages/DocsPage.tsx"),
] satisfies RouteConfig;
