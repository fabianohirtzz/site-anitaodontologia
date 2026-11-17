-- Base das tabelas da Dra. Anita no Supabase compartilhado (projeto do HD360).
-- Regra: nenhuma política "using (true)" em tabela an_. Só quem está em
-- an_usuarios lê dados da Dra.; quem grava pelo servidor usa a service key.

create table if not exists public.an_usuarios (
  user_id   uuid primary key references auth.users(id) on delete cascade,
  nome      text,
  criado_em timestamptz not null default now()
);

create or replace function public.an_eh_usuario()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from public.an_usuarios where user_id = auth.uid());
$$;

revoke all on function public.an_eh_usuario() from public, anon;
grant execute on function public.an_eh_usuario() to authenticated;

create table if not exists public.an_cliques (
  id            bigint generated always as identity primary key,
  criado_em     timestamptz not null default now(),
  ref           text not null check (ref ~ '^[0-9]{5}$'),
  pagina        text,
  origem        text not null check (origem in ('google_ads','google_organico','instagram','facebook','doctoralia','outro_site','direto')),
  utm_source    text,
  utm_medium    text,
  utm_campaign  text,
  utm_term      text,
  gclid         text,
  referrer_host text,
  texto         text
);

create index if not exists an_cliques_ref_idx on public.an_cliques (ref, criado_em desc);

alter table public.an_usuarios enable row level security;
alter table public.an_cliques  enable row level security;

revoke all on public.an_usuarios, public.an_cliques from anon;
revoke insert, update, delete on public.an_usuarios, public.an_cliques from authenticated;

create policy an_usuarios_le_proprio on public.an_usuarios
  for select to authenticated using (user_id = auth.uid());

create policy an_cliques_le_equipe on public.an_cliques
  for select to authenticated using (public.an_eh_usuario());
