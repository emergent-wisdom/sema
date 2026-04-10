import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Sema — Content-Addressed Semantics</title>
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

        <meta name="description" content="Sema is a content-addressed commons of ~450 cognitive patterns where the definition IS the identifier. Interactive browser, HTTP API, and MCP server." />
        <meta name="author" content="Henrik Westerberg" />

        <meta property="og:title" content="Sema — When the Hash Is the Word" />
        <meta property="og:description" content="A content-addressed commons of cognitive patterns where the definition is the identifier." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://semahash.org" />

        <Meta />
        <Links />
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
