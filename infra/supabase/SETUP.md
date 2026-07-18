# Supabase setup (people-data)

Division of labor: **Railway runs the code** (server, frontend, vocabulary
SQLite on a volume); **Supabase holds the people-data** (signups/users, later
stars + workspace records) so GTM can work in its dashboard and build
automations without touching the server. Workspace login stays on our own
GitHub OAuth — we do not use Supabase Auth.

## One-time setup (project owner, ~10 min)

1. **Create the project** — supabase.com → New project.
   - Organization: Emergent Wisdom
   - Region: an EU region close to the application and its users.
   - Save the database password in your password manager.
2. **Apply the schema** — Dashboard → SQL Editor → paste `schema.sql` → Run.
   The current bootstrap is safe to re-run unchanged. Future schema changes
   still need explicit, versioned migrations.
3. **Invite the team** — Settings → Team → invite (Developer role is enough
   for dashboard + automation work).
4. **Reserve the server connection** — Dashboard → Connect → *Session pooler*
   (port **5432**) for the persistent Railway backend. Store the URI on the
   Railway service as `SUPABASE_DB_URL`; don't paste it into chats or commits.
   The variable is intentionally unused until the server database adapter
   lands. Transaction mode on port 6543 is for short-lived connections and
   requires prepared statements to be disabled in the database driver.

## Notes for automations

- `signups.status` (`new` → `contacted` → …) and `notes` are yours to drive
  pipelines from; `updated_at` is trigger-maintained, so "changed since"
  automations are reliable.
- RLS is on with no `anon` or `authenticated` policies, so browser/Data API
  access is blocked. Dashboard access and direct Postgres access follow the
  database role's privileges; a database connection is not a service-role API
  key. Keep any admin connection or server-only secret out of client code.

## What connects to this later

- `POST /api/signup` on the server (writes to `signups`) — lands with the
  signup form.
- The GitHub OAuth callback will upsert `users` once the server database
  adapter lands.
- Stars/workspace tables will be added here by that work, with the same
  RLS posture.
