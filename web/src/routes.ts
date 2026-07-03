import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("pages/HomePage.tsx"),
  route("/workspace", "pages/WorkspaceDemoPage.tsx"),
  route("/graph", "pages/GraphPageLazy.tsx"),
  route("/docs", "pages/DocsPage.tsx"),
] satisfies RouteConfig;
