<?php
/* Gravação no Supabase com a service key (ignora a RLS; só existe no
   servidor) e limite simples de requisições por chave. */

require_once __DIR__ . '/an-config.php';

function an_db_set_transport($f) { $GLOBALS['AN_DB_TRANSPORT'] = $f; }

/* Um único ponto de saída para a rede, para o teste trocar o transporte.
   Devolve ['status' => int, 'body' => string] ou null se a rede falhou. */
function an_db_http($metodo, $url, $corpo, $headers) {
    if (!empty($GLOBALS['AN_DB_TRANSPORT'])) {
        return call_user_func($GLOBALS['AN_DB_TRANSPORT'], $metodo, $url, $corpo, $headers);
    }
    if (!function_exists('curl_init')) {
        error_log('an_db_http sem curl | ' . $url);
        return null;
    }
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST  => $metodo,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => $headers,
        CURLOPT_POSTFIELDS     => $corpo,
        CURLOPT_TIMEOUT        => 8,
    ]);
    $body = curl_exec($ch);
    $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $erro = curl_error($ch);
    curl_close($ch);
    if ($body === false) {
        error_log('an_db_http falhou | ' . $url . ' | ' . $erro);
        return null;
    }
    return ['status' => $status, 'body' => (string) $body];
}

function an_db_insert($tabela, array $linha) {
    $cfg = an_config();
    $url = $cfg['SUPABASE_URL'] ?? '';
    $key = $cfg['SUPABASE_SERVICE_KEY'] ?? '';
    if ($url === '' || $key === '') {
        error_log('an_db_insert sem config.local.php | ' . $tabela);
        return false;
    }
    $r = an_db_http('POST', $url . '/rest/v1/' . rawurlencode($tabela), json_encode($linha), [
        'apikey: ' . $key,
        'Authorization: Bearer ' . $key,
        'Content-Type: application/json',
        'Prefer: return=minimal',
    ]);
    if (!$r || $r['status'] < 200 || $r['status'] >= 300) {
        error_log('an_db_insert ' . $tabela . ' status ' . ($r['status'] ?? 'rede') . ' | ' . substr($r['body'] ?? '', 0, 300));
        return false;
    }
    return true;
}

/* Chave do limite: HMAC do IP com um segredo do servidor. Sem o segredo,
   o nome do arquivo não volta a ser o IP (um sha1 de IPv4 se reverte por
   força bruta em segundos). */
function an_chave_limite($ip, $segredo) {
    return hash_hmac('sha256', 'an-clique|' . $ip, $segredo);
}

/* Apaga arquivos de limite parados há mais de $idade_s segundos. */
function an_limite_limpa($dir, $idade_s) {
    $corte = time() - $idade_s;
    foreach (glob($dir . '/*') ?: [] as $f) {
        if (is_file($f) && filemtime($f) < $corte) @unlink($f);
    }
}

/* Janela fixa por arquivo: no máximo $max chamadas a cada $janela_s
   segundos para a mesma chave. A chave já chega como hash (nada de IP
   em claro no disco). */
function an_limite_ok($chave, $max, $janela_s, $dir) {
    if (!is_dir($dir) && !@mkdir($dir, 0700, true)) return true;
    $arq = $dir . '/' . preg_replace('/[^a-f0-9]/', '', $chave);
    $agora = time();
    $fh = @fopen($arq, 'c+');
    if (!$fh) return true;
    flock($fh, LOCK_EX);
    $dados = json_decode(stream_get_contents($fh), true);
    if (!is_array($dados) || $agora - ($dados['inicio'] ?? 0) >= $janela_s) {
        $dados = ['inicio' => $agora, 'n' => 0];
    }
    $dados['n']++;
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($dados));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $dados['n'] <= $max;
}
