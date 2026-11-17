<?php
/* Recebe o aviso de clique no WhatsApp enviado por js/rastreio.js
   (sendBeacon) e grava em an_cliques. Responde sempre sem corpo:
   204 gravado, 400 inválido, 405 método, 413 grande demais, 429 limite. */

require __DIR__ . '/lib/an-clique.php';

header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    http_response_code(405);
    exit;
}

/* Pasta do limite fora do public_html (home da conta), não no /tmp
   compartilhado do servidor. Limpeza ocasional de arquivos com mais de 1 h. */
$cfg = an_config();
$dir_limite = dirname(__DIR__) . '/tmp/an-limite';
if (mt_rand(1, 50) === 1) an_limite_limpa($dir_limite, 3600);
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$chave = an_chave_limite($ip, ($cfg['SUPABASE_SERVICE_KEY'] ?? '') . '|limite');
if (!an_limite_ok($chave, 30, 60, $dir_limite)) {
    http_response_code(429);
    exit;
}

$bruto = file_get_contents('php://input', false, null, 0, 4097);
if ($bruto === false || strlen($bruto) > 4096) {
    http_response_code(413);
    exit;
}

$entrada = json_decode($bruto, true);
$linha = is_array($entrada) ? an_clique_valida($entrada) : null;
if ($linha === null) {
    http_response_code(400);
    exit;
}

/* Responde primeiro: o navegador do paciente não espera o Supabase. */
http_response_code(204);
if (function_exists('fastcgi_finish_request')) {
    fastcgi_finish_request();
} else {
    ignore_user_abort(true);
    flush();
}

an_db_insert('an_cliques', $linha);
