<?php
/* ============================================================
   MODELO, sem segredo. Copie para "config.local.php" (mesma pasta,
   raiz do site) NO SERVIDOR, pelo gerenciador de arquivos do cPanel,
   e preencha os valores reais. O config.local.php não é versionado
   (.gitignore) nem enviado pelo workflow de publicação.
============================================================ */

// Supabase compartilhado (projeto do HD360).
$SUPABASE_URL = 'https://euzmbswywwhmicjlszqw.supabase.co';

// service_role key (SEGREDO: acesso total, ignora a RLS).
// Supabase > Project Settings > API > "service_role".
$SUPABASE_SERVICE_KEY = 'COLOQUE_AQUI_A_SERVICE_ROLE_KEY';
