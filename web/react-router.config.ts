import type { Config } from "@react-router/dev/config";

export default {
  appDirectory: "src",
  ssr: false,
  async prerender() {
    // Only prerender the home page. /graph needs WebGL (can't prerender)
    // and /docs fetches API data. Both still work as client-side routes
    // after hydration.
    return ["/"];
  },
} satisfies Config;
