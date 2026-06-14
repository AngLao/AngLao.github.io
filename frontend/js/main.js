/* ═══════════════════════════════════════════════════════════
   全球新闻日报 — 数据驱动前端渲染
   零框架依赖 · 纯 Vanilla JS
   ═══════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const CATEGORIES = {
    World:       { label: '国际', color: '#0891b2' },
    Politics:    { label: '政治', color: '#dc2626' },
    Economy:     { label: '经济', color: '#059669' },
    Technology:  { label: '科技', color: '#2563eb' },
    Science:     { label: '科学', color: '#7c3aed' },
    Environment: { label: '环境', color: '#16a34a' },
    Sports:      { label: '体育', color: '#ea580c' },
    Culture:     { label: '文化', color: '#d946ef' },
  };
  const CAT_ORDER = Object.keys(CATEGORIES);

  // ── detect page ──────────────────────────────────────
  const path = location.pathname.replace(/\/$/, '');
  const pageName = path.endsWith('archive.html') ? 'archive'
                 : path.endsWith('about.html')   ? 'about'
                 : 'index';

  // ── footer date ──────────────────────────────────────
  const fd = document.getElementById('footer-date');
  if (fd) {
    fd.textContent = '新闻内容版权归原始来源所有 · 自动生成于 '
      + new Date().toISOString().slice(0, 10);
  }

  // ── helpers ──────────────────────────────────────────
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => [...(ctx || document).querySelectorAll(sel)];

  function h(tag, attrs, ...children) {
    const el = document.createElement(tag);
    if (attrs) Object.entries(attrs).forEach(([k, v]) => {
      if (k === 'className') el.className = v;
      else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v);
    });
    children.forEach(c => {
      if (typeof c === 'string') el.appendChild(document.createTextNode(c));
      else if (c instanceof Node) el.appendChild(c);
    });
    return el;
  }

  // ── news card ────────────────────────────────────────
  function newsCard(item, large) {
    const cat = CATEGORIES[item.cat] || { label: item.cat, color: '#6b7280' };
    const timeStr = (item.date || '').slice(0, 10);

    const badge = h('span', { className: 'cat-badge', style: `--cat-color:${cat.color}` }, cat.label);
    const source = h('span', { className: 'source' }, '\u260e ' + item.source);
    const time = h('span', { className: 'time' },
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> '
      + timeStr
    );

    const meta = h('div', { className: 'news-meta' }, badge, source, time);
    const title = h('h3', { className: 'news-title' },
      h('a', { href: item.url, target: '_blank', rel: 'noopener' }, item.title)
    );

    const body = h('div', { className: 'news-body' }, title, meta);

    if (large && item.summary) {
      const s = item.summary.length > 200 ? item.summary.slice(0, 200) + '...' : item.summary;
      body.appendChild(h('p', { className: 'news-summary' }, s));
    }

    const cls = large ? 'news-card large' : 'news-card';
    return h('article', { className: cls }, body);
  }

  // ── render index ─────────────────────────────────────
  function renderIndex(data) {
    // hero stats
    const heroDate = $('#hero-date');
    const heroStats = $('#hero-stats');
    if (heroDate) heroDate.textContent = data.date;
    if (heroStats) heroStats.textContent =
      '共 ' + data.stats.total + ' 条新闻 · 来自 ' + data.stats.sources + ' 家媒体';

    // top stories (first 5)
    const top = data.items.slice(0, 5);
    const topGrid = $('#top-grid');
    if (topGrid) top.forEach(item => topGrid.appendChild(newsCard(item, true)));

    // category sections
    const container = $('#category-sections');
    if (!container) return;

    CAT_ORDER.forEach(catKey => {
      const items = data.categories[catKey];
      if (!items || !items.length) return;
      const info = CATEGORIES[catKey];
      const heading = h('h2', {
        className: 'cat-heading',
        style: `--cat-color:${info.color}`
      }, info.label, h('span', { className: 'count' }, items.length + ''));

      const grid = h('div', { className: 'news-grid' });
      items.slice(0, 12).forEach(item => grid.appendChild(newsCard(item, false)));

      container.appendChild(
        h('section', { className: 'cat-section', 'data-category': catKey }, heading, grid)
      );
    });
  }

  // ── render archive ───────────────────────────────────
  function renderArchive(data) {
    const countEl = $('#archive-count');
    if (countEl) countEl.textContent = '共 ' + data.dates.length + ' 期日报';

    const container = $('#archive-months');
    if (!container) return;

    // group by month
    const months = {};
    data.dates.sort().reverse().forEach(d => {
      const ym = d.slice(0, 7);
      (months[ym] = months[ym] || []).push(d);
    });

    Object.keys(months).sort().reverse().forEach(ym => {
      const daysDiv = h('div', { className: 'archive-days' });
      months[ym].forEach(d => {
        daysDiv.appendChild(
          h('a', { href: 'daily/' + d + '.html', className: 'archive-day' }, d)
        );
      });
      container.appendChild(
        h('section', { className: 'archive-month' },
          h('h2', null, ym),
          daysDiv
        )
      );
    });
  }

  // ── init ─────────────────────────────────────────────
  function init() {
    if (pageName === 'index') {
      fetch('data/news.json')
        .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(renderIndex)
        .catch(e => {
          const el = $('#category-sections');
          if (el) el.innerHTML = '<p class="error">⚠ 数据加载失败，请稍后重试</p>';
          console.error('news.json load error:', e);
        });
    } else if (pageName === 'archive') {
      fetch('data/archive.json')
        .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(renderArchive)
        .catch(e => {
          const el = $('#archive-months');
          if (el) el.innerHTML = '<p class="error">⚠ 归档数据加载失败</p>';
          console.error('archive.json load error:', e);
        });
    }
    // about page — nothing to load, content is static
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
