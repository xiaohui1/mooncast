import os, re, shutil, html, markdown

OUT = "_site"
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
if os.path.exists("assets"):
    shutil.copytree("assets", os.path.join(OUT, "assets"))

PAGES = [
    ("index.html", "README.md", "首页概览"),
    ("algorithms.html", "docs/ALGORITHMS.md", "核心算法白皮书"),
    ("deploy.html", "docs/DEPLOY.md", "部署指南"),
    ("faq.html", "docs/FAQ.md", "常见问题"),
    ("changelog.html", "CHANGELOG.md", "更新日志"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} · 月映 MoonCast</title>
  <link rel="icon" href="assets/logo.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
  <style>
    :root {{
      --bg: #f8fafc; --card: #ffffff; --text: #0f172a; --muted: #64748b;
      --border: #e2e8f0; --accent: #2563eb; --accent-soft: #eff6ff;
      --code-bg: #0f172a; --code-text: #e2e8f0;
      --surface-soft: #f8fafc;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0b1120; --card: #111827; --text: #f1f5f9; --muted: #94a3b8;
        --border: #1e293b; --accent: #60a5fa; --accent-soft: rgba(59,130,246,.14);
        --code-bg: #020617; --code-text: #e2e8f0;
        --surface-soft: rgba(255,255,255,.03);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }}
    .layout {{ max-width: 1140px; margin: 0 auto; display: grid; grid-template-columns: 240px 1fr; gap: 28px; padding: 28px 20px 64px; }}
    .sidebar {{ position: sticky; top: 24px; align-self: start; background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 17px; margin-bottom: 18px; text-decoration: none; color: var(--text); }}
    .brand img {{ width: 32px; height: 32px; }}
    .nav a {{ display: block; padding: 9px 12px; border-radius: 10px; color: var(--muted); text-decoration: none; font-size: 14px; font-weight: 500; margin-bottom: 4px; transition: background .15s, color .15s; }}
    .nav a:hover {{ background: var(--accent-soft); color: var(--accent); }}
    .nav a.active {{ background: var(--accent-soft); color: var(--accent); font-weight: 600; }}
    .ext {{ margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border); font-size: 13px; }}
    .ext a {{ color: var(--accent); text-decoration: none; display: block; padding: 5px 0; }}
    .content {{ background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 36px 40px; min-width: 0; }}
    .content h1, .content h2, .content h3, .content h4 {{ line-height: 1.35; margin-top: 1.6em; }}
    .content h1:first-child {{ margin-top: 0; }}
    .content a {{ color: var(--accent); text-decoration: none; }}
    .content a:hover {{ text-decoration: underline; }}
    .content blockquote {{ margin: 16px 0; padding: 12px 16px; border-left: 4px solid var(--accent); background: var(--accent-soft); border-radius: 0 10px 10px 0; }}
    .content pre {{ background: var(--code-bg); color: var(--code-text); padding: 16px; border-radius: 12px; overflow-x: auto; font-size: 13px; line-height: 1.55; }}
    .content code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9em; }}
    .content :not(pre) > code {{ background: var(--accent-soft); color: var(--accent); padding: 2px 6px; border-radius: 6px; }}
    .table-wrap {{ width: 100%; overflow-x: auto; margin: 16px 0; border-radius: 10px; }}
    .content table {{ width: 100%; border-collapse: collapse; margin: 0; font-size: 14px; }}
    .content th, .content td {{ border: 1px solid var(--border); padding: 10px 12px; text-align: left; }}
    .content th {{ background: var(--accent-soft); white-space: nowrap; }}
    .math-block {{ margin: 16px 0; padding: 14px 18px; background: var(--surface-soft); border: 1px solid var(--border); border-radius: 12px; overflow-x: auto; text-align: center; }}
    .math-inline {{ display: inline-block; vertical-align: baseline; padding: 0 2px; }}
    .mermaid-wrap {{ margin: 18px 0; padding: 18px 14px; background: var(--surface-soft); border: 1px solid var(--border); border-radius: 14px; overflow-x: auto; text-align: center; }}
    .mermaid {{ display: inline-block; min-width: 100%; }}
    @media (max-width: 840px) {{
      .layout {{ grid-template-columns: 1fr; padding: 16px 14px 48px; }}
      .sidebar {{ position: static; }}
      .nav {{ display: flex; flex-wrap: wrap; gap: 6px; }}
      .nav a {{ margin-bottom: 0; padding: 7px 11px; font-size: 13px; }}
      .content {{ padding: 22px 16px; }}
      .math-block {{ padding: 12px 10px; font-size: 14px; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <a class="brand" href="index.html">
        <img src="assets/logo.svg" alt="MoonCast" />
        <span>月映 · MoonCast</span>
      </a>
      <nav class="nav">
        {nav}
      </nav>
      <div class="ext">
        <a href="https://github.com/xiaohui1/mooncast/releases" target="_blank" rel="noopener">📦 下载安装包 (Releases) ↗</a>
        <a href="https://github.com/xiaohui1/mooncast" target="_blank" rel="noopener">⭐ GitHub 公开仓库 ↗</a>
      </div>
    </aside>
    <main class="content">
      {body}
    </main>
  </div>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script>
    window.addEventListener('DOMContentLoaded', () => {{
      const renderMath = () => {{
        if (!window.katex) return;
        document.querySelectorAll('.math-block[data-tex]').forEach((el) => {{
          window.katex.render(el.dataset.tex, el, {{ displayMode: true, throwOnError: false }});
        }});
        document.querySelectorAll('.math-inline[data-tex]').forEach((el) => {{
          window.katex.render(el.dataset.tex, el, {{ displayMode: false, throwOnError: false }});
        }});
      }};
      if (window.katex) {{
        renderMath();
      }} else {{
        const s = document.querySelector('script[src*="katex.min.js"]');
        if (s) s.addEventListener('load', renderMath);
      }}
    }});
  </script>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    if (document.querySelector('.mermaid')) {{
      const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      mermaid.initialize({{ startOnLoad: false, theme: dark ? 'dark' : 'default', securityLevel: 'loose' }});
      await mermaid.run({{ querySelector: '.mermaid' }});
    }}
  </script>
</body>
</html>
"""


def render_markdown_with_rich_blocks(md_text: str) -> str:
    tokens = {}

    def put_token(rendered_html: str) -> str:
        key = f"MOONCASTBLOCKTOKEN{len(tokens)}END"
        tokens[key] = rendered_html
        return key

    # 1. Extract fenced ```mermaid and ```math blocks (including indented ones inside lists)
    lines = md_text.splitlines()
    out_lines = []
    i = 0
    while i < len(lines):
        m = re.match(r'^(\s*)```(mermaid|math)\s*$', lines[i])
        if m:
            indent, kind = m.group(1), m.group(2)
            buf = []
            i += 1
            while i < len(lines) and not re.match(r'^\s*```\s*$', lines[i]):
                if indent and lines[i].startswith(indent):
                    buf.append(lines[i][len(indent):])
                else:
                    buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            body = "\n".join(buf).strip()
            if kind == "mermaid":
                rendered = f'<div class="mermaid-wrap"><div class="mermaid">{html.escape(body)}</div></div>'
            else:
                rendered = f'<div class="math-block" data-tex="{html.escape(body, quote=True)}"></div>'
            out_lines.append("")
            out_lines.append(indent + put_token(rendered))
            out_lines.append("")
            continue
        out_lines.append(lines[i])
        i += 1

    processed = "\n".join(out_lines)

    # 2. Extract GitHub inline math $`...`$ (skip regular fenced code blocks)
    final_lines = []
    in_fence = False
    for ln in processed.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            final_lines.append(ln)
            continue
        if in_fence:
            final_lines.append(ln)
            continue
        ln = re.sub(
            r'\$`([^`\n]+)`\$',
            lambda m: put_token(f'<span class="math-inline" data-tex="{html.escape(m.group(1).strip(), quote=True)}"></span>'),
            ln,
        )
        final_lines.append(ln)

    processed = "\n".join(final_lines)
    body_html = markdown.markdown(processed, extensions=["tables", "fenced_code"])

    # 3. Restore placeholders (unwrap <p> around block-level math/mermaid tokens)
    for key, rendered in tokens.items():
        if rendered.startswith("<div "):
            body_html = body_html.replace(f"<p>{key}</p>", rendered)
        body_html = body_html.replace(key, rendered)

    # 4. Wrap tables in horizontal scroll containers for mobile
    body_html = body_html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return body_html


for out_name, src_path, title in PAGES:
    if not os.path.exists(src_path):
        continue
    with open(src_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    md_text = (
        md_text
        .replace("docs/ALGORITHMS.md", "algorithms.html")
        .replace("docs/DEPLOY.md", "deploy.html")
        .replace("docs/FAQ.md", "faq.html")
        .replace("CHANGELOG.md", "changelog.html")
    )
    body_html = render_markdown_with_rich_blocks(md_text)
    nav_html = "\n        ".join(
        f'<a href="{p[0]}" class="{"active" if p[0]==out_name else ""}">{html.escape(p[2])}</a>'
        for p in PAGES
    )
    with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(title=html.escape(title), nav=nav_html, body=body_html))

open(os.path.join(OUT, ".nojekyll"), "w").close()
print("Built static docs:", [p[0] for p in PAGES])
