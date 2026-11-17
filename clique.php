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

$ip = $_SERVER['REMOTE_ADDR'] ?? '';
if (!an_limite_ok(sha1('an-clique|' . $ip), 30, 60, sys_get_temp_dir() . '/an-limite')) {
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
