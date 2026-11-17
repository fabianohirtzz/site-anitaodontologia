// js/rastreio.js: código de referência no WhatsApp e origem da visita.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const codigo = readFileSync(new URL('../js/rastreio.js', import.meta.url), 'utf8');
const WA = 'https://wa.me/5548991450038?text=Ol%C3%A1%2C%20Dra.%20Anita!';
const DIA = 864e5;
const T = Date.UTC(2026, 10, 17);

function carrega(extra = {}) {
  const ctx = { URL, console, navigator: {}, location: { pathname: '/procedimentos.html', hostname: 'anitaodontologia.com.br', href: 'https://anitaodontologia.com.br/procedimentos.html' }, ...extra };
  vm.createContext(ctx);
  vm.runInContext(codigo, ctx);
  return ctx.AnRastreio;
}

const texto = (href) => decodeURIComponent(new URL(href).searchParams.get('text') ?? '');

test('ref tem 5 digitos com zeros a esquerda', () => {
  const R = carrega();
  assert.equal(R.ref(() => 0), '00000');
  assert.equal(R.ref(() => 0.99999), '99999');
  assert.match(R.ref(), /^\d{5}$/);
});

test('comRef acrescenta o codigo ao texto', () => {
  const R = carrega();
  const h = R.comRef(WA, '48213');
  assert.equal(texto(h), 'Olá, Dra. Anita! (ref. 48213)');
  assert.ok(h.endsWith('%20(ref.%2048213)'));
  assert.ok(h.startsWith('https://wa.me/5548991450038?text='));
});

test('nao duplica ref', () => {
  const R = carrega();
  const h = R.comRef(R.comRef(WA, '48213'), '67890');
  assert.equal(texto(h), 'Olá, Dra. Anita! (ref. 67890)');
});

test('capturaOrigem guarda gclid', () => {
  const R = carrega();
  const o = R.capturaOrigem('https://anitaodontologia.com.br/?gclid=X&utm_source=google&utm_medium=cpc', '', T, null);
  assert.equal(o.gclid, 'X');
  assert.equal(o.utm_medium, 'cpc');
  assert.equal(o.ts, T);
});

test('direto nao apaga origem paga', () => {
  const R = carrega();
  const salvo = { gclid: 'X', ts: T - 10 * DIA };
  assert.deepEqual({ ...R.capturaOrigem('https://anitaodontologia.com.br/sobre.html', '', T, salvo) }, salvo);
  const velho = { gclid: 'X', ts: T - 91 * DIA };
  assert.equal(R.capturaOrigem('https://anitaodontologia.com.br/sobre.html', '', T, velho), null);
});

test('referrer interno nao sobrescreve a origem salva', () => {
  const R = carrega();
  const salvo = { utm_source: 'instagram', ts: T - DIA };
  assert.deepEqual({ ...R.capturaOrigem('https://anitaodontologia.com.br/contato.html', 'https://anitaodontologia.com.br/', T, salvo) }, salvo);
});

test('referrer externo vira a nova origem', () => {
  const R = carrega();
  const o = R.capturaOrigem('https://anitaodontologia.com.br/', 'https://www.google.com/', T, { gclid: 'X', ts: T - DIA });
  assert.equal(o.referrer, 'https://www.google.com/');
  assert.equal(o.gclid, undefined);
});

test('abre mesmo sem storage', () => {
  const ctx = { URL, console, navigator: {}, location: { pathname: '/', hostname: 'anitaodontologia.com.br', href: 'https://anitaodontologia.com.br/' } };
  Object.defineProperty(ctx, 'localStorage', { get() { throw new Error('bloqueado'); } });
  vm.createContext(ctx);
  vm.runInContext(codigo, ctx);
  const a = { href: WA };
  const ev = { target: { closest: (sel) => (sel === 'a[data-wa]' ? a : null) } };
  assert.doesNotThrow(() => ctx.AnRastreio.aoClicar(ev));
  assert.match(texto(a.href), /\(ref\. \d{5}\)$/);
});

test('envia o clique por sendBeacon com a origem salva', () => {
  const enviados = [];
  const R = carrega({ navigator: { sendBeacon: (url, corpo) => { enviados.push({ url, corpo }); return true; } } });
  R.endpoint = 'https://anitaodontologia.com.br/clique.php';
  R.origemAtual = { gclid: 'teste', ts: T };
  const a = { href: WA };
  R.aoClicar({ target: { closest: () => a } });
  assert.equal(enviados.length, 1);
  assert.equal(enviados[0].url, 'https://anitaodontologia.com.br/clique.php');
  const dados = JSON.parse(enviados[0].corpo);
  assert.equal(dados.gclid, 'teste');
  assert.equal(dados.pagina, '/procedimentos.html');
  assert.match(dados.ref, /^\d{5}$/);
  assert.ok(dados.texto.endsWith(`(ref. ${dados.ref})`));
});

test('sem endpoint (GitHub Pages) nao envia nada', () => {
  const enviados = [];
  const R = carrega({ navigator: { sendBeacon: () => enviados.push(1) } });
  R.endpoint = null;
  R.aoClicar({ target: { closest: () => ({ href: WA }) } });
  assert.equal(enviados.length, 0);
});

test('guarda gbraid e wbraid do anuncio no iPhone', () => {
  const R = carrega();
  const o = R.capturaOrigem('https://anitaodontologia.com.br/?gbraid=G&wbraid=W', 'https://www.google.com/', T, null);
  assert.equal(o.gbraid, 'G');
  assert.equal(o.wbraid, 'W');
});
