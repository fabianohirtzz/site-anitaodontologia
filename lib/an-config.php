<?php
/* Configuração do servidor. Os valores reais vivem só em config.local.php
   na raiz do site, no servidor (fora do Git). Ver config.local.example.php. */

function an_config() {
    if (isset($GLOBALS['AN_CONFIG']) && is_array($GLOBALS['AN_CONFIG'])) {
        return $GLOBALS['AN_CONFIG'];
    }
    $cfg = [];
    $arq = dirname(__DIR__) . '/config.local.php';
    if (is_file($arq)) {
        $carrega = function ($arq) {
            include $arq;
            return [
                'SUPABASE_URL'         => isset($SUPABASE_URL) ? rtrim($SUPABASE_URL, '/') : '',
                'SUPABASE_SERVICE_KEY' => $SUPABASE_SERVICE_KEY ?? '',
            ];
        };
        $cfg = $carrega($arq);
    }
    $GLOBALS['AN_CONFIG'] = $cfg;
    return $cfg;
}
