-- Anúncio do Google no iOS chega com gbraid/wbraid no lugar do gclid.
-- E defesa em profundidade: authenticated só lê (sem truncate/trigger/references).
alter table public.an_cliques add column if not exists gbraid text;
alter table public.an_cliques add column if not exists wbraid text;

revoke all on public.an_cliques, public.an_usuarios from authenticated;
grant select on public.an_cliques, public.an_usuarios to authenticated;
