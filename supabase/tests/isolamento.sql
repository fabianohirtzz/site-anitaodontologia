-- Isolamento das tabelas an_ no Supabase compartilhado (HD360, PO, Márcio).
-- Roda tudo numa transação e desfaz no fim; pode ser repetido em produção.
-- Qualquer falha levanta erro; sucesso devolve 'isolamento ok'.
begin;
insert into public.an_cliques (ref, origem, gbraid) values ('12345', 'google_ads', 'g');

-- 1. Logado que NÃO está em an_usuarios: não lê, não grava, não trunca.
select set_config('request.jwt.claims', '{"sub":"00000000-0000-0000-0000-000000000001","role":"authenticated"}', true);
set local role authenticated;
do $$ begin
  if (select count(*) from public.an_cliques) <> 0 then raise exception 'FALHA: usuario de fora leu an_cliques'; end if;
  if (select count(*) from public.an_usuarios) <> 0 then raise exception 'FALHA: usuario de fora leu an_usuarios'; end if;
end $$;
do $$ begin
  insert into public.an_cliques (ref, origem) values ('99999', 'direto');
  raise exception 'FALHA: authenticated gravou';
exception when insufficient_privilege then null; end $$;
do $$ begin
  truncate public.an_cliques;
  raise exception 'FALHA: authenticated truncou';
exception when insufficient_privilege then null; end $$;
reset role;

-- 2. Usuário em an_usuarios: vê todas as linhas que o postgres vê.
do $$ declare u uuid; begin
  select id into u from auth.users order by created_at limit 1;
  if u is null then raise exception 'sem usuario em auth.users para o teste'; end if;
  insert into public.an_usuarios (user_id, nome) values (u, 'teste');
  perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true);
end $$;
create temp table _total on commit drop as select count(*) n from public.an_cliques;
grant select on _total to authenticated;
set local role authenticated;
do $$ begin
  if (select count(*) from public.an_cliques) <> (select n from _total) or (select n from _total) < 1 then
    raise exception 'FALHA: usuario da Dra. nao viu tudo';
  end if;
end $$;
reset role;

-- 3. Anônimo: sem permissão nenhuma.
set local role anon;
do $$ begin perform 1 from public.an_cliques; raise exception 'FALHA: anon leu';
exception when insufficient_privilege then null; end $$;
reset role;

select 'isolamento ok' as resultado;
rollback;
