<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:cv="http://www.cienciavitae.pt/ns/person-extended"
    xmlns:curriculum="http://www.cienciavitae.pt/ns/curriculum"
    xmlns:citation-name="http://www.cienciavitae.pt/ns/citation-name"
    xmlns:output="http://www.cienciavitae.pt/ns/output"
    xmlns:service="http://www.cienciavitae.pt/ns/service"
    xmlns:common="http://www.cienciavitae.pt/ns/common"
    xmlns:person-info="http://www.cienciavitae.pt/ns/person-info"
    xmlns:identifying-info="http://www.cienciavitae.pt/ns/identifying-info"
    xmlns:resume="http://www.cienciavitae.pt/ns/resume"
    xmlns:email="http://www.cienciavitae.pt/ns/email"
    xmlns:author-identifier="http://www.cienciavitae.pt/ns/author-identifier"
    xmlns:extra="http://extra"
    exclude-result-prefixes="cv curriculum citation-name output service common person-info identifying-info resume email author-identifier extra">

  <xsl:output method="html" indent="yes" encoding="UTF-8" doctype-system="about:legacy-compat"/>

  <xsl:template match="/">
    <html lang="en">
      <head>
        <title><xsl:value-of select="curriculum:curriculum/identifying-info:identifying-info/citation-name:citation-names/citation-name:citation-name"/></title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body { max-width: 1200px; margin: 2em auto; padding: 0 16px; color: #111; background: #fff;
                 font: 18px/1.5 ui-monospace, "JetBrains Mono", "Fira Code", Menlo, Consolas, "DejaVu Sans Mono", monospace; }
          h1::before { content: "# "; color: #aaa; }
          h2::before { content: "## "; color: #aaa; }
          a { color: #0645ad; text-decoration: none; }
          a:hover { text-decoration: underline; }
          .wrap { overflow-x: auto; }
          table { border-collapse: collapse; border: 2px solid #111; width: 100%; }
          th, td { border: 1px solid #ccc; padding: 8px 10px; text-align: left; vertical-align: top; }
          th { background: #eee; border-bottom: 2px solid #111; white-space: nowrap; }
          td:first-child { color: #999; }
          td i { color: #666; font-style: normal; }
          .notice { border: 2px dashed #999; padding: 8px 12px; }
          th.paper { width: 40%; }
          select { font: inherit; width: 100%; }
          .tag { display: inline-block; background: #eee; color: #333; padding: 0 6px; margin: 2px 0; font-size: 0.8em; white-space: nowrap; }
          .tag.active { background: #111; color: #fff; }
          footer { margin-top: 2em; color: #666; font-size: 0.8em; }
        </style>
      </head>
      <body>
        <xsl:apply-templates select="curriculum:curriculum"/>
        <!-- footer: date of the gencv.py run and where each column comes from (see scrap.py) -->
        <footer>
          <xsl:if test="curriculum:curriculum/extra:updated">
            Last update: <xsl:value-of select="curriculum:curriculum/extra:updated"/>.
          </xsl:if>
          Citations: <a href="https://www.crossref.org">Crossref</a>.
          IF: Clarivate's Journal Citation Reports, as shown on each journal's website.
          SJR: <a href="https://www.scimagojr.com">SCImago Journal Rank</a>, best quartile across subject categories.
          CORE: <a href="https://portal.core.edu.au/conf-ranks/">CORE conference rankings</a>.
        </footer>
        <script><![CDATA[
// Sortable and filterable table (ported from rpmcruz.github.io/mytable.js).
// <th data-type="sort"> sorts on click (data-first gives the first direction);
// <th data-type="filter"> becomes a dropdown; a cell with .tag links has several values.
(function() {
  const table = document.getElementById('papers');
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const ths = Array.from(table.tHead.rows[0].cells);
  const RANK = {'A*': 0, 'A': 1, 'B': 2, 'C': 3};  // CORE ranks, best first
  const filters = {};
  let sortCol = null, sortDir = 1;
  function values(row, i) {
    const tags = row.cells[i].querySelectorAll('.tag');
    return tags.length ? Array.from(tags, t => t.textContent.trim()) : [row.cells[i].textContent.trim()];
  }
  function key(v) {
    if (v in RANK) return RANK[v];
    const n = parseFloat(v);
    return isNaN(n) ? v.toLowerCase() : n;
  }
  function compare(a, b) {
    if (a === '' || b === '') return (a === '') - (b === '');  // empty always last
    const ka = key(a), kb = key(b);
    if (typeof ka !== typeof kb) return typeof ka === 'number' ? -1 : 1;  // numbers before text
    return sortDir * (ka < kb ? -1 : ka > kb ? 1 : 0);
  }
  function update() {
    let shown = rows.filter(r => Object.entries(filters).every(([i, sel]) => sel.value === '' || values(r, i).includes(sel.value)));
    if (sortCol !== null)
      shown = shown.slice().sort((r1, r2) => compare(values(r1, sortCol)[0], values(r2, sortCol)[0]));
    tbody.replaceChildren(...shown);
    shown.forEach((r, i) => r.cells[0].textContent = i + 1);
    const tag = tagCol >= 0 ? filters[tagCol].value : '';
    table.querySelectorAll('.tag').forEach(t => t.classList.toggle('active', t.textContent.trim() === tag));
  }
  ths.forEach((th, i) => {
    if (th.dataset.type === 'sort') {
      const link = document.createElement('a');
      link.href = '#';
      link.textContent = th.textContent.trim();
      const arrow = document.createElement('span');
      arrow.className = 'arrow';
      th.replaceChildren(link, arrow);
      link.onclick = e => {
        e.preventDefault();
        sortDir = sortCol === i ? -sortDir : (th.dataset.first === 'desc' ? -1 : 1);
        sortCol = i;
        table.querySelectorAll('th .arrow').forEach(a => a.textContent = '');
        arrow.textContent = sortDir === 1 ? ' ▲' : ' ▼';
        update();
      };
    } else if (th.dataset.type === 'filter') {
      const counts = {};
      rows.forEach(r => values(r, i).forEach(v => { if (v) counts[v] = (counts[v] || 0) + 1; }));
      const sel = document.createElement('select');
      sel.add(new Option(th.textContent.trim(), ''));
      Object.keys(counts).sort().forEach(v => sel.add(new Option(v + ' (' + counts[v] + ')', v)));
      sel.onchange = update;
      th.replaceChildren(sel);
      filters[i] = sel;
    }
  });
  // clicking a tag filters by it; clicking the active tag clears the filter
  const tagCol = ths.findIndex(th => th.dataset.multi);
  tbody.addEventListener('click', e => {
    const t = e.target.closest('.tag');
    if (!t || tagCol < 0) return;
    e.preventDefault();
    const sel = filters[tagCol];
    sel.value = sel.value === t.textContent.trim() ? '' : t.textContent.trim();
    update();
  });
  update();
})();
        ]]></script>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="curriculum:curriculum">
    <h1><xsl:value-of select="identifying-info:identifying-info/citation-name:citation-names/citation-name:citation-name"/></h1>
    <!-- links: email and Google Scholar (from the XML author identifiers) -->
    <p>
      <a href="mailto:{identifying-info:identifying-info/email:emails/email:email[@preferred-email='true']/email:email-address}"><xsl:value-of select="identifying-info:identifying-info/email:emails/email:email[@preferred-email='true']/email:email-address"/></a>
      <xsl:for-each select="identifying-info:identifying-info/author-identifier:author-identifiers/author-identifier:author-identifier[author-identifier:identifier-type/@code='GOOGLE']">
        · <a href="https://scholar.google.com/citations?user={author-identifier:identifier}">Google Scholar</a>
      </xsl:for-each>
    </p>
    <xsl:choose>
      <xsl:when test="extra:resume">  <!-- biography from the YAML -->
        <p><xsl:value-of select="extra:resume"/></p>
      </xsl:when>
      <xsl:when test="identifying-info:identifying-info/resume:resume">
        <p><xsl:value-of select="identifying-info:identifying-info/resume:resume"/></p>
      </xsl:when>
    </xsl:choose>
    <xsl:if test="extra:notice">  <!-- notice box from the YAML; {email} becomes a link -->
      <xsl:variable name="email" select="identifying-info:identifying-info/email:emails/email:email[@preferred-email='true']/email:email-address"/>
      <p class="notice">
        <xsl:choose>
          <xsl:when test="contains(extra:notice, '{email}')">
            <xsl:value-of select="substring-before(extra:notice, '{email}')"/>
            <a href="mailto:{$email}"><xsl:value-of select="$email"/></a>
            <xsl:value-of select="substring-after(extra:notice, '{email}')"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="extra:notice"/>
          </xsl:otherwise>
        </xsl:choose>
      </p>
    </xsl:if>

    <h2>Publications</h2>
    <div class="wrap">
    <table id="papers" border="1" cellpadding="4">
      <thead>
        <tr>
          <th>#</th>
          <th data-type="sort" data-first="desc">Year</th>
          <th class="paper">Paper</th>
          <th data-type="filter">Type</th>
          <th data-type="filter" data-multi="1">Tags</th>
          <th data-type="sort" data-first="desc">Citations</th>
          <th data-type="sort" data-first="desc">IF</th>
          <th data-type="sort" data-first="asc">SJR</th>
          <th data-type="sort" data-first="asc">CORE</th>
        </tr>
      </thead>
      <tbody>
        <!-- only outputs with a DOI (skips abstracts, posters, submissions and preprints without one) -->
        <xsl:apply-templates select="output:outputs/output:output[output:*/output:identifiers/output:identifier[output:identifier-type/@code='doi']]">
          <xsl:sort select="output:*/output:publication-date/@year | output:*/output:publication-year | output:conference-paper/output:presentation-date/@year | output:conference-poster/output:conference-date/@year | output:preprint/output:date-submitted/@year" order="descending"/>
        </xsl:apply-templates>
      </tbody>
    </table>
    </div>
  </xsl:template>

  <xsl:template match="output:output">
    <xsl:variable name="doi" select="output:*/output:identifiers/output:identifier[output:identifier-type/@code='doi']/output:identifier"/>
    <xsl:variable name="title" select="output:*/output:article-title | output:*/output:paper-title | output:*/output:chapter-title | output:*/output:title"/>
    <tr>
      <td><xsl:value-of select="position()"/></td>

      <td>
        <xsl:choose>
          <xsl:when test="output:*/output:publication-date/@year">
            <xsl:value-of select="output:*/output:publication-date/@year"/>
          </xsl:when>
          <xsl:when test="output:*/output:publication-year">
            <xsl:value-of select="output:*/output:publication-year"/>
          </xsl:when>
          <xsl:when test="output:conference-paper/output:presentation-date/@year">
            <xsl:value-of select="output:conference-paper/output:presentation-date/@year"/>
          </xsl:when>
          <xsl:when test="output:conference-poster/output:conference-date/@year">
            <xsl:value-of select="output:conference-poster/output:conference-date/@year"/>
          </xsl:when>
          <xsl:when test="output:preprint/output:date-submitted/@year">
            <xsl:value-of select="output:preprint/output:date-submitted/@year"/>
          </xsl:when>
        </xsl:choose>
      </td>

      <td>
        <a href="https://doi.org/{$doi}"><xsl:value-of select="translate($title, '&#160;', ' ')"/></a>
        <br/>
        <i>
          <xsl:choose>
            <xsl:when test="extra:extra/extra:venue">
              <xsl:value-of select="extra:extra/extra:venue"/>
            </xsl:when>
            <xsl:when test="output:journal-article/output:journal">
              <xsl:value-of select="output:journal-article/output:journal"/>
            </xsl:when>
            <xsl:when test="output:conference-paper/output:proceedings-title">
              <xsl:value-of select="output:conference-paper/output:proceedings-title"/>
            </xsl:when>
            <xsl:when test="output:conference-poster/output:conference-name">
              <xsl:value-of select="output:conference-poster/output:conference-name"/>
            </xsl:when>
            <xsl:when test="output:book/output:publisher">
              <xsl:value-of select="output:book/output:publisher"/>
            </xsl:when>
          </xsl:choose>
        </i>
      </td>

      <td>
        <xsl:choose>
          <xsl:when test="output:output-type/@code='P101'">journal</xsl:when>
          <xsl:when test="output:output-type/@code='P127'">preprint</xsl:when>
          <xsl:otherwise>conference</xsl:otherwise>
        </xsl:choose>
      </td>

      <td>
        <xsl:for-each select="extra:extra/extra:tags/extra:tag">
          <a class="tag" href="#"><xsl:value-of select="."/></a>
          <xsl:text> </xsl:text>
        </xsl:for-each>
      </td>

      <td><xsl:value-of select="extra:extra/extra:citations"/></td>
      <td><xsl:value-of select="extra:extra/extra:impact-factor"/></td>
      <td><xsl:value-of select="extra:extra/extra:sjr-rank"/></td>
      <td><xsl:value-of select="extra:extra/extra:core-rank"/></td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
