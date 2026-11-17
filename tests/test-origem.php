<?php
/* an_origem: de onde veio quem clicou no WhatsApp. */
require __DIR__ . '/../lib/an-origem.php';

$falhas = 0;
function confere($desc, $esperado, $d) {
    global $falhas;
    $obtido = an_origem($d);
    if ($obtido !== $esperado) {
        $falhas++;
        echo "FALHA: $desc: esperado $esperado, obtido $obtido\n";
    }
}

confere('gclid', 'google_ads', ['gclid' => 'abc']);
confere('google cpc', 'google_ads', ['utm_source' => 'google', 'utm_medium' => 'cpc']);
confere('referrer google', 'google_organico', ['referrer_host' => 'www.google.com.br']);
confere('utm instagram', 'instagram', ['utm_source' => 'instagram']);
confere('referrer instagram', 'instagram', ['referrer_host' => 'l.instagram.com']);
confere('pagina links', 'instagram', ['pagina' => '/links.html']);
confere('referrer facebook', 'facebook', ['referrer_host' => 'm.facebook.com']);
confere('referrer doctoralia', 'doctoralia', ['referrer_host' => 'www.doctoralia.com.br']);
confere('outro site', 'outro_site', ['referrer_host' => 'exemplo.com']);
confere('navegacao interna', 'direto', ['referrer_host' => 'anitaodontologia.com.br']);
confere('vazio', 'direto', []);
confere('gclid vence instagram', 'google_ads', ['gclid' => 'x', 'referrer_host' => 'l.instagram.com']);

confere('gbraid (iOS)', 'google_ads', ['gbraid' => 'x', 'referrer_host' => 'www.google.com']);
confere('wbraid', 'google_ads', ['wbraid' => 'x']);

exit($falhas ? 1 : 0);
