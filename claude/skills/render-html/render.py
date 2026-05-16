#!/usr/bin/env python3
"""Render Markdown into a navigable, shareable HTML document, or pass an
already-authored HTML/SVG artifact through unmodified. Opens the result in
the default browser.

Usage:
    render.py [INPUT] [--title T] [--out PATH] [--style-ref PATH]
              [--no-open] [--no-toc] [--no-toolbar]

Two paths:
  * Pass-through: input begins with <!DOCTYPE / <html / <svg. The file is a
    bespoke artifact; it is written and opened verbatim. No injection.
  * Document mode: Markdown is converted, then a sticky section TOC, a copy/
    print toolbar, reading-time, and a print stylesheet are injected.

Markdown conversion prefers the `markdown` PyPI package when importable;
otherwise a conservative stdlib-only converter is used. No install required.
"""

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import webbrowser
from pathlib import Path

# --------------------------------------------------------------------------- #
# Markdown -> HTML
# --------------------------------------------------------------------------- #

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text) or "section"


def _inline(s: str) -> str:
    s = _INLINE_CODE.sub(lambda m: f"<code>{m.group(1)}</code>", s)
    s = _BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", s)
    s = _ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", s)
    s = _LINK.sub(
        lambda m: f'<a href="{m.group(2)}" rel="noopener">{m.group(1)}</a>', s
    )
    return s


def _convert_with_library(text: str):
    try:
        import markdown  # type: ignore
    except ImportError:
        return None
    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "sane_lists", "toc"]
    )
    body = md.markdown(text) if hasattr(md, "markdown") else markdown.markdown(
        text, extensions=["fenced_code", "tables", "sane_lists", "toc"]
    )
    # Library path: derive TOC by re-scanning rendered headings.
    return body


def _convert_fallback(text: str):
    """Conservative Markdown subset converter. Returns (html, toc_entries)."""
    out, toc = [], []
    lines = text.split("\n")
    i, n = 0, len(lines)
    seen = {}

    while i < n:
        line = lines[i]

        m = re.match(r"^```(\w+)?\s*$", line)
        if m:
            lang = m.group(1) or ""
            i += 1
            buf = []
            while i < n and not re.match(r"^```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(buf))
            cls = f' class="language-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        if line.strip() == "":
            i += 1
            continue

        if re.match(r"^(\s*[-*_]){3,}\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            level = len(h.group(1))
            raw = h.group(2).strip()
            base = _slug(raw)
            sid = base
            if base in seen:
                seen[base] += 1
                sid = f"{base}-{seen[base]}"
            else:
                seen[base] = 0
            content = _inline(html.escape(raw))
            out.append(f'<h{level} id="{sid}">{content}</h{level}>')
            if level in (2, 3):
                toc.append((level, sid, re.sub(r"<[^>]+>", "", content)))
            i += 1
            continue

        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").lstrip())
                i += 1
            out.append(f"<blockquote><p>{_inline(html.escape(' '.join(buf)))}</p></blockquote>")
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                item = re.sub(r"^\s*[-*+]\s+", "", lines[i])
                items.append(f"<li>{_inline(html.escape(item))}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                items.append(f"<li>{_inline(html.escape(item))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Table (pipe syntax with header separator)
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            def cells(r):
                return [c.strip() for c in r.strip().strip("|").split("|")]
            header = cells(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(cells(lines[i]))
                i += 1
            thead = "".join(f"<th>{_inline(html.escape(c))}</th>" for c in header)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{_inline(html.escape(c))}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        buf = []
        while i < n and lines[i].strip() != "" and not re.match(
            r"^(#{1,6}\s|```|>|\s*[-*+]\s|\s*\d+\.\s|(\s*[-*_]){3,}\s*$)",
            lines[i],
        ):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{_inline(html.escape(' '.join(buf)))}</p>")

    return "\n".join(out), toc


_H_TAG = re.compile(r'<h([23])(?:\s[^>]*)?>(.*?)</h\1>', re.DOTALL | re.IGNORECASE)


def to_body_html(text: str):
    lib = _convert_with_library(text)
    if lib is not None:
        # Ensure headings have ids and harvest a TOC.
        toc, seen = [], {}

        def add_id(m):
            level, inner = m.group(1), m.group(2)
            label = re.sub(r"<[^>]+>", "", inner).strip()
            base = _slug(label)
            sid = base
            if base in seen:
                seen[base] += 1
                sid = f"{base}-{seen[base]}"
            else:
                seen[base] = 0
            toc.append((int(level), sid, label))
            return f'<h{level} id="{sid}">{inner}</h{level}>'

        body = _H_TAG.sub(add_id, lib)
        return body, toc
    return _convert_fallback(text)


# --------------------------------------------------------------------------- #
# Document assembly (document mode only)
# --------------------------------------------------------------------------- #

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{style_ref_meta}
<style>
  :root {{
    --bg:#fff; --fg:#1a1a1a; --muted:#6b7280; --border:#e5e7eb;
    --code-bg:#f4f4f5; --accent:#2563eb; --bar:#fafafa;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg:#0d0d0f; --fg:#e6e6e6; --muted:#9ca3af; --border:#2a2a30;
      --code-bg:#1c1c20; --accent:#60a5fa; --bar:#141417;
    }}
  }}
  * {{ box-sizing:border-box; }}
  html {{ scroll-behavior:smooth; }}
  body {{ margin:0; background:var(--bg); color:var(--fg);
    font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .bar {{ position:sticky; top:0; z-index:10; display:flex; gap:8px;
    align-items:center; padding:8px 16px; background:var(--bar);
    border-bottom:1px solid var(--border); font-size:.82rem; }}
  .bar .meta {{ color:var(--muted); margin-right:auto; }}
  .bar button {{ font:inherit; font-size:.82rem; cursor:pointer;
    background:var(--bg); color:var(--fg); border:1px solid var(--border);
    border-radius:6px; padding:5px 10px; }}
  .bar button:hover {{ border-color:var(--accent); color:var(--accent); }}
  .layout {{ display:flex; max-width:1100px; margin:0 auto;
    gap:40px; padding:40px 24px 96px; }}
  nav.toc {{ flex:0 0 220px; position:sticky; top:64px; align-self:flex-start;
    max-height:calc(100vh - 96px); overflow-y:auto; font-size:.86rem; }}
  nav.toc a {{ display:block; padding:3px 0; color:var(--muted);
    text-decoration:none; border-left:2px solid transparent; padding-left:10px; }}
  nav.toc a.lvl3 {{ padding-left:22px; }}
  nav.toc a:hover, nav.toc a.active {{ color:var(--accent);
    border-left-color:var(--accent); }}
  main {{ flex:1; min-width:0; max-width:760px; }}
  h1,h2,h3,h4 {{ line-height:1.25; margin:1.8em 0 .6em; font-weight:650;
    scroll-margin-top:64px; }}
  h1 {{ font-size:1.9rem; margin-top:0; }}
  h2 {{ font-size:1.45rem; border-bottom:1px solid var(--border); padding-bottom:.3em; }}
  h3 {{ font-size:1.15rem; }}
  p,ul,ol,blockquote,pre,table {{ margin:0 0 1.1em; }}
  a {{ color:var(--accent); text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  code {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    font-size:.88em; background:var(--code-bg); padding:.15em .4em; border-radius:4px; }}
  pre {{ background:var(--code-bg); padding:16px 18px; border-radius:8px;
    overflow-x:auto; border:1px solid var(--border); }}
  pre code {{ background:none; padding:0; font-size:.85rem; }}
  blockquote {{ margin-left:0; padding:.3em 1.1em; color:var(--muted);
    border-left:3px solid var(--border); }}
  hr {{ border:none; border-top:1px solid var(--border); margin:2.4em 0; }}
  table {{ border-collapse:collapse; width:100%; font-size:.95rem; }}
  th,td {{ border:1px solid var(--border); padding:8px 12px; text-align:left; }}
  th {{ background:var(--code-bg); }}
  ul,ol {{ padding-left:1.5em; }} li {{ margin:.3em 0; }}
  footer {{ margin-top:64px; color:var(--muted); font-size:.8rem;
    border-top:1px solid var(--border); padding-top:16px; }}
  @media (max-width:860px) {{
    .layout {{ flex-direction:column; gap:0; }}
    nav.toc {{ position:static; max-height:none; flex:none;
      border-bottom:1px solid var(--border); padding-bottom:12px; margin-bottom:8px; }}
  }}
  @media print {{
    .bar, nav.toc {{ display:none; }}
    .layout {{ display:block; padding:0; }}
    a {{ color:inherit; text-decoration:underline; }}
    pre,blockquote,table {{ page-break-inside:avoid; }}
  }}
</style>
</head>
<body>
{toolbar}
<div class="layout">
{toc}
<main>
{body}
<footer>Generated {stamp}{style_ref_note}</footer>
</main>
</div>
<script>
(function(){{
  var src = {source_json};
  function copy(t){{ navigator.clipboard && navigator.clipboard.writeText(t); }}
  var b;
  if ((b=document.getElementById('cp-md'))) b.onclick=function(){{
    copy(src); b.textContent='Copied'; setTimeout(function(){{b.textContent='Copy as Markdown';}},1200); }};
  if ((b=document.getElementById('cp-pg'))) b.onclick=function(){{
    copy(document.querySelector('main').innerText); b.textContent='Copied';
    setTimeout(function(){{b.textContent='Copy page';}},1200); }};
  if ((b=document.getElementById('pr'))) b.onclick=function(){{ window.print(); }};
  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  var heads=links.map(function(a){{return document.getElementById(a.getAttribute('href').slice(1));}});
  function spy(){{ var y=window.scrollY+80, idx=0;
    heads.forEach(function(h,i){{ if(h&&h.offsetTop<=y) idx=i; }});
    links.forEach(function(a,i){{ a.classList.toggle('active', i===idx); }}); }}
  if (links.length) {{ window.addEventListener('scroll',spy,{{passive:true}}); spy(); }}
}})();
</script>
</body>
</html>
"""

_PASSTHROUGH = re.compile(r"^\s*(<!doctype html|<html|<svg)", re.IGNORECASE)
_FIRST_HEADING = re.compile(r"^\s{0,3}#{1,2}\s+(.+?)\s*$", re.MULTILINE)


def derive_title(text, explicit):
    if explicit:
        return explicit
    m = _FIRST_HEADING.search(text)
    if m:
        return _INLINE_CODE.sub(r"\1", m.group(1)).strip()
    return "Output"


def build_toc(entries):
    if len(entries) < 3:
        return ""
    rows = "".join(
        f'<a class="lvl{lvl}" href="#{sid}">{html.escape(label)}</a>'
        for lvl, sid, label in entries
    )
    return f'<nav class="toc">{rows}</nav>'


def build_toolbar(words):
    rt = max(1, round(words / 200))
    return (
        '<div class="bar">'
        f'<span class="meta">{words:,} words · ~{rt} min read</span>'
        '<button id="cp-md">Copy as Markdown</button>'
        '<button id="cp-pg">Copy page</button>'
        '<button id="pr">Print</button>'
        "</div>"
    )


def build_document(text, title, want_toc, want_toolbar, style_ref):
    if _PASSTHROUGH.match(text):
        return text  # bespoke artifact — verbatim, no injection
    body, toc_entries = to_body_html(text)
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body)))
    source_json = json.dumps(text).replace("</", "<\\/")
    sr_meta = f'<meta name="x-style-ref" content="{html.escape(style_ref)}">' if style_ref else ""
    sr_note = f' · style ref: {html.escape(style_ref)}' if style_ref else ""
    return _TEMPLATE.format(
        title=html.escape(derive_title(text, title)),
        style_ref_meta=sr_meta,
        toolbar=build_toolbar(words) if want_toolbar else "",
        toc=build_toc(toc_entries) if want_toc else "",
        body=body,
        stamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        style_ref_note=sr_note,
        source_json=source_json,
    )


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="Render Markdown/HTML and open it.")
    ap.add_argument("input", nargs="?", help="Input file; stdin if omitted")
    ap.add_argument("--title", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--style-ref", default=None,
                    help="Design-system reference path, recorded in output metadata")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--no-toolbar", action="store_true")
    args = ap.parse_args()

    if args.input:
        src = Path(args.input)
        if not src.is_file():
            print(f"error: input not found: {src}", file=sys.stderr)
            return 1
        text = src.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 1

    document = build_document(
        text, args.title,
        want_toc=not args.no_toc,
        want_toolbar=not args.no_toolbar,
        style_ref=args.style_ref,
    )

    out = (Path(args.out) if args.out
           else Path.cwd() / f"claude-output-{int(time.time())}.html")
    out.write_text(document, encoding="utf-8")
    abs_path = out.resolve()
    print(abs_path)

    if not args.no_open:
        webbrowser.open(f"file://{abs_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
