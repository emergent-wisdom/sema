import {
  isRouteErrorResponse,
  Link,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useRouteError,
  type MetaFunction,
} from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LocalHeader } from "@/components/LocalHeader";
import { LiveAdditionsTracker } from "@/hooks/useLiveAdditions";

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
  { title: "Sema — Local view" },
  {
    name: "description",
    content:
      "The Sema local view: watch an agent build a vocabulary on this computer, in a list and a 3D graph.",
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
      <LiveAdditionsTracker />
      <Outlet />
    </QueryClientProvider>
  );
}

// Unknown addresses and render failures land here instead of React Router's
// bare default. It renders outside Root, so it brings its own query client.
export function ErrorBoundary() {
  const error = useRouteError();
  const notFound = isRouteErrorResponse(error) && error.status === 404;

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-zinc-950 text-zinc-100">
        <LocalHeader />
        <main className="mx-auto max-w-3xl px-6 py-20 sm:py-28">
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-emerald-400">
            {notFound ? "404" : "Error"}
          </p>
          <h1 className="mt-3 text-4xl font-light tracking-tight text-zinc-50 sm:text-5xl">
            {notFound ? "Page not found" : "Something went wrong"}
          </h1>
          <p className="mt-5 text-base leading-7 text-zinc-400">
            {notFound
              ? "This address does not match a page of the local view."
              : "The page could not load. Reload the page or go back to the vocabulary."}
          </p>
          <Link
            to="/"
            className="mt-8 inline-flex items-center rounded-lg bg-emerald-400 px-5 py-2.5 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-300"
          >
            Go to the vocabulary
          </Link>
        </main>
      </div>
    </QueryClientProvider>
  );
}
