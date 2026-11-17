<?php
/* Limpa o corpo enviado pelo js/rastreio.js e monta a linha de an_cliques.
   Nenhum IP, user agent ou referrer completo vai para o banco. */

require_once __DIR__ . '/an-origem.php';
require_once __DIR__ . '/an-db.php';

function an_campo($v, $max) {
    if (!is_string($v)) return null;
    $v = trim($v);
    if ($v === '') return null;
    return mb_substr($v, 0, $max);
}

function an_clique_valida(array $e) {
    $ref = $e['ref'] ?? null;
    if (!is_string($ref) || !preg_match('/^[0-9]{5}$/', $ref)) return null;

    $pagina = $e['pagina'] ?? '/';
    if (!is_string($pagina) || $pagina === '' || $pagina[0] !== '/' || substr($pagina, 0, 2) === '//' || strlen($pagina) > 200) {
        return null;
    }

    $host = null;
    $ref_url = an_campo($e['referrer'] ?? null, 500);
    if ($ref_url) {
        $h = parse_url($ref_url, PHP_URL_HOST);
        if (is_string($h) && $h !== '') $host = mb_substr(strtolower($h), 0, 300);
    }

    $linha = [
        'ref'           => $ref,
        'pagina'        => $pagina,
        'utm_source'    => an_campo($e['utm_source'] ?? null, 300),
        'utm_medium'    => an_campo($e['utm_medium'] ?? null, 300),
        'utm_campaign'  => an_campo($e['utm_campaign'] ?? null, 300),
        'utm_term'      => an_campo($e['utm_term'] ?? null, 300),
        'gclid'         => an_campo($e['gclid'] ?? null, 300),
        'gbraid'        => an_campo($e['gbraid'] ?? null, 300),
        'wbraid'        => an_campo($e['wbraid'] ?? null, 300),
        'referrer_host' => $host,
        'texto'         => an_campo($e['texto'] ?? null, 500),
    ];
    $linha['origem'] = an_origem($linha);
    return $linha;
}
