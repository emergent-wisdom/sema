-- Supabase schema for Sema's people-data.
-- Compute stays on Railway; vocabulary DBs stay SQLite. This database
-- holds the relational data a human operates on (GTM dashboard +
-- automations) and, later, registry data (stars, workspace records).
--
-- Apply: Supabase Dashboard -> SQL Editor -> paste -> Run. The current
-- bootstrap is safe to rerun unchanged; future changes need migrations.
--
-- Security model: RLS is ENABLED with no anon/authenticated policies,
-- so browser/Data API clients cannot read or write rows. Dashboard access
-- and direct Postgres connections still follow their database role's
-- privileges. Nothing is publicly readable.

-- ── signups ──────────────────────────────────────────────────────────
-- People expressing interest before the product exists for them:
-- waitlist entries, event contacts, inbound from the site or Discord.
create table if not exists public.signups (
  id          uuid primary key default gen_random_uuid(),
  email       text not null unique check (email = lower(trim(email))),
  name        text,
  -- where this signup came from: 'site', 'discord', 'event:<name>', ...
  source      text not null default 'site',
  -- free-form: what they said they want to use sema for
  context     text,
  -- GTM working fields (Arne's): pipeline stage + notes
  status      text not null default 'new',   -- new / contacted / active / closed
  notes       text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table public.signups enable row level security;

create index if not exists idx_signups_status  on public.signups (status);
create index if not exists idx_signups_created on public.signups (created_at desc);

-- keep updated_at honest for automations that key off it
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists trg_signups_touch on public.signups;
create trigger trg_signups_touch
  before update on public.signups
  for each row execute function public.touch_updated_at();

-- ── users ────────────────────────────────────────────────────────────
-- Workspace users (GitHub identity), populated by the server once the
-- multi-tenant workspace ships. Kept separate from signups on purpose:
-- a signup is a lead; a user is an authenticated account.
create table if not exists public.users (
  id            uuid primary key default gen_random_uuid(),
  github_id     bigint not null unique,
  github_login  text not null,
  name          text,
  email         text,
  avatar_url    text,
  first_seen_at timestamptz not null default now(),
  last_login_at timestamptz not null default now()
);

alter table public.users enable row level security;

create index if not exists idx_users_login on public.users (github_login);
