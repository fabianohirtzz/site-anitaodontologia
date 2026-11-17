-- Isolamento das tabelas an_ no Supabase compartilhado (HD360, PO, Márcio).
-- Roda tudo numa transação e desfaz no fim. Qualquer falha levanta erro;
-- sucesso devolve a linha 'isolamento ok'.
begin;

insert into public.an_cliques (ref, origem) values ('12345', 'direto');

-- 1. Usuário logado que NÃO está em an_usuarios: não vê nada.
select set_config('request.jwt.claims', '{"sub":"00000000-0000-0000-0000-000000000001","role":"authenticated"}', true);
set local role authenticated;
do $$ begin
  if (select count(*) from public.an_cliques) <> 0 then
    raise exception 'FALHA: usuario de fora leu an_cliques';
  end if;
end $$;
reset role;

-- 2. Usuário que está em an_usuarios: vê a linha.
do $$
declare u uuid;
begin
  select id into u from auth.users order by created_at limit 1;
  if u is null then raise exception 'sem usuario em auth.users para o teste'; end if;
  insert into public.an_usuarios (user_id, nome) values (u, 'teste isolamento');
  perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true);
end $$;
set local role authenticated;
do $$ begin
  if (select count(*) from public.an_cliques) <> 1 then
    raise exception 'FALHA: usuario da Dra. nao leu an_cliques';
  end if;
end $$;
reset role;

-- 3. Anônimo: sem permissão nenhuma.
set local role anon;
do $$ begin
  perform 1 from public.an_cliques;
  raise exception 'FALHA: anon leu an_cliques';
exception when insufficient_privilege then null;
end $$;
do $$ begin
  insert into public.an_cliques (ref, origem) values ('99999', 'direto');
  raise exception 'FALHA: anon gravou em an_cliques';
exception when insufficient_privilege then null;
end $$;
reset role;

select 'isolamento ok' as resultado;
rollback;
