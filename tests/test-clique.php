<?php
/* Validação do clique, gravação no PostgREST e limite por IP. */
require __DIR__ . '/../lib/an-clique.php';

$falhas = 0;
function ok($cond, $desc) {
    global $falhas;
    if (!$cond) { $falhas++; echo "FALHA: $desc\n"; }
}

// --- validação ---
$l = an_clique_valida([
    'ref' => '48213', 'pagina' => '/procedimentos.html',
    'referrer' => 'https://www.google.com/', 'texto' => 'Olá (ref. 48213)',
]);
ok(is_array($l), 'entrada valida devolve linha');
ok(($l['origem'] ?? '') === 'google_organico', 'origem google_organico');
ok(($l['referrer_host'] ?? '') === 'www.google.com', 'referrer_host extraido');
ok(!array_key_exists('referrer', $l ?? []), 'referrer completo nao vai para a tabela');
foreach (['ip', 'ip_hash', 'user_agent'] as $c) ok(!array_key_exists($c, $l ?? []), "sem campo $c");

ok(an_clique_valida(['ref' => '4821', 'pagina' => '/']) === null, 'ref com 4 digitos recusado');
ok(an_clique_valida(['ref' => 'abcde', 'pagina' => '/']) === null, 'ref nao numerico recusado');
ok(an_clique_valida(['ref' => '12345', 'pagina' => 'https://outro.com/x']) === null, 'pagina externa recusada');
ok(an_clique_valida(['ref' => '12345', 'pagina' => '/' . str_repeat('a', 200)]) === null, 'pagina acima de 200 recusada');
ok(an_clique_valida(['ref' => ['12345'], 'pagina' => '/']) === null, 'ref em lista recusado');

$l = an_clique_valida(['ref' => '12345', 'pagina' => '/', 'utm_campaign' => str_repeat('x', 400), 'texto' => str_repeat('y', 600)]);
ok(mb_strlen($l['utm_campaign']) === 300, 'campo texto truncado em 300');
ok(mb_strlen($l['texto']) === 500, 'texto truncado em 500');

// --- gravação ---
$chamadas = [];
an_db_set_transport(function ($metodo, $url, $corpo, $headers) use (&$chamadas) {
    $chamadas[] = compact('metodo', 'url', 'corpo', 'headers');
    return ['status' => 201, 'body' => ''];
});
$GLOBALS['AN_CONFIG'] = ['SUPABASE_URL' => 'https://x.supabase.co', 'SUPABASE_SERVICE_KEY' => 'k'];
ok(an_db_insert('an_cliques', ['ref' => '12345']) === true, 'insert devolve true em 201');
ok(count($chamadas) === 1 && $chamadas[0]['metodo'] === 'POST', 'um POST');
ok(($chamadas[0]['url'] ?? '') === 'https://x.supabase.co/rest/v1/an_cliques', 'url do PostgREST');
ok(in_array('Prefer: return=minimal', $chamadas[0]['headers'] ?? [], true), 'Prefer minimal');

an_db_set_transport(function () { return ['status' => 400, 'body' => 'erro']; });
ok(an_db_insert('an_cliques', ['ref' => '12345']) === false, 'insert devolve false em 400');

$GLOBALS['AN_CONFIG'] = [];
$chamadas = [];
an_db_set_transport(function () use (&$chamadas) { $chamadas[] = 1; return ['status' => 201, 'body' => '']; });
ok(an_db_insert('an_cliques', ['ref' => '12345']) === false && !$chamadas, 'sem config nao chama a rede');

// --- limite por IP ---
$dir = sys_get_temp_dir() . '/an-limite-' . uniqid();
$chave = sha1('203.0.113.9');
$passaram = 0;
for ($i = 0; $i < 30; $i++) if (an_limite_ok($chave, 30, 60, $dir)) $passaram++;
ok($passaram === 30, '30 chamadas passam');
ok(an_limite_ok($chave, 30, 60, $dir) === false, '31a na mesma janela barrada');
ok(an_limite_ok(sha1('198.51.100.1'), 30, 60, $dir) === true, 'outro IP nao e afetado');
array_map('unlink', glob("$dir/*") ?: []);
@rmdir($dir);

exit($falhas ? 1 : 0);
