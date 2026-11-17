<?php
/* Classifica a origem de um clique no WhatsApp.
   Ordem: anúncio pago > UTM conhecido > host do referrer > página de links
   da bio > direto (vazio ou o próprio site) > outro site. */

function an_host_termina($host, $sufixos) {
    foreach ($sufixos as $s) {
        if ($host === $s || substr($host, -strlen('.' . $s)) === '.' . $s) return true;
    }
    return false;
}

function an_eh_google($host) {
    return (bool) preg_match('/(^|\.)google\.[a-z.]+$/', $host);
}

function an_origem(array $d) {
    $src    = strtolower(trim($d['utm_source'] ?? ''));
    $medium = strtolower(trim($d['utm_medium'] ?? ''));
    $gclid  = trim($d['gclid'] ?? '');
    $host   = strtolower(trim($d['referrer_host'] ?? ''));
    $pagina = $d['pagina'] ?? '';

    if ($gclid !== '') return 'google_ads';
    if ($src === 'google' && in_array($medium, ['cpc', 'ppc', 'paid', 'paidsearch'], true)) return 'google_ads';

    if ($src === 'google') return 'google_organico';
    if (in_array($src, ['instagram', 'ig'], true)) return 'instagram';
    if (in_array($src, ['facebook', 'fb'], true)) return 'facebook';
    if ($src === 'doctoralia') return 'doctoralia';

    if ($host !== '' && !an_host_termina($host, ['anitaodontologia.com.br'])) {
        if (an_eh_google($host)) return 'google_organico';
        if (an_host_termina($host, ['instagram.com'])) return 'instagram';
        if (an_host_termina($host, ['facebook.com', 'fb.com'])) return 'facebook';
        if (an_host_termina($host, ['doctoralia.com.br'])) return 'doctoralia';
        return 'outro_site';
    }

    if (substr($pagina, -strlen('/links.html')) === '/links.html') return 'instagram';
    return 'direto';
}
