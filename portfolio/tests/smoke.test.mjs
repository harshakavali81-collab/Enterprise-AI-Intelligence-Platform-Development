import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root=resolve(dirname(fileURLToPath(import.meta.url)), '..');
const html=readFileSync(resolve(root,'index.html'),'utf8');
const css=readFileSync(resolve(root,'style.css'),'utf8');
const script=readFileSync(resolve(root,'script.js'),'utf8');

test('portfolio is a self-contained static website',()=>{
 assert.match(html,/<!doctype html>/i);
 assert.match(html,/href="\.\/style\.css"/);
 assert.match(html,/src="\.\/script\.js"/);
 assert.match(html,/id="projectGrid"/);
 assert.match(html,/id="projectDialog"/);
 assert.ok(css.length>5000);
 assert.ok(existsSync(resolve(root,'favicon.svg')));
 assert.ok(existsSync(resolve(root,'vercel.json')));
});

test('catalog contains the 20 unique verified GitHub repositories',()=>{
 const names=[...script.matchAll(/\{repo:"([^"]+)"/g)].map(x=>x[1]);
 assert.equal(names.length,20);
 assert.equal(new Set(names).size,20);
 assert.ok(names.includes('CivicShield-AI'));
 assert.ok(names.includes('AstraSentinel-AI'));
 assert.ok(names.includes('Multilingual-Project'));
 assert.ok(names.includes('TransactionShield-a-Real-Time-Fraud-Detection-and-Risk-Scoring-Platform.'));
});

test('only documented static demos are mirrored',()=>{
 assert.ok(existsSync(resolve(root,'demos/banking/index.html')));
 assert.ok(existsSync(resolve(root,'demos/marketing/index.html')));
 for(const path of ['demos/banking/index.html','demos/marketing/index.html']){
  const demo=readFileSync(resolve(root,path),'utf8');
  assert.match(demo,/<!doctype html>/i);
  assert.match(demo,/<title>/i);
 }
});

test('responsive, accessible and contact-ready',()=>{
 assert.match(html,/name="viewport"/);
 assert.match(html,/<main id="main">/);
 assert.match(html,/aria-label="Main navigation"/);
 assert.match(html,/mailto:kavaliharshavardhan98@gmail.com/);
 assert.match(css,/@media\(max-width:580px\)/);
 assert.match(css, /prefers-reduced-motion/);
});
