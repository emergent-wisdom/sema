import { Links, Meta, Outlet, Scripts, ScrollRestoration, type MetaFunction } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const plausibleBootstrap = `
  if (["semahash.org", "www.semahash.org"].includes(window.location.hostname)) {
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://plausible.io/js/pa-2brno4TEeC51MdCh3HMPq.js";
    document.head.appendChild(script);

    window.plausible = window.plausible || function () {
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };
    window.plausible.init = window.plausible.init || function (options) {
      window.plausible.o = options || {};
    };
    window.plausible.init();
  }
`;

// Default title/description, overridable per-route: a child route's meta()
// can spread these matches and replace just the title/description entries.
export const meta: MetaFunction = () => [
  { title: "Sema — Content-Addressed Semantics" },
  {
    name: "description",
    content:
      "Sema is a content-addressed commons of ~450 cognitive patterns where the definition IS the identifier. Interactive browser, HTTP API, and MCP server.",
  },
]

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

        <meta name="author" content="Henrik Westerberg" />

        <meta property="og:title" content="Sema — When the Hash Is the Word" />
        <meta property="og:description" content="A content-addressed commons of cognitive patterns where the definition is the identifier." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://semahash.org" />

        <Meta />
        <Links />
        {/* Plausible is intentionally limited to the canonical production hosts. */}
        <script dangerouslySetInnerHTML={{ __html: plausibleBootstrap }} />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function Root() {
  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  );
}
