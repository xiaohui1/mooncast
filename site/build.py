import os, shutil, html, markdown

OUT = "_site"
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
if os.path.exists("assets"):
    shutil.copytree("assets", os.path.join(OUT, "assets"))

PAGES = [
    ("index.html", "README.md", "首页概览"),
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
  <style>
    :root {{
      --bg: #f8fafc; --card: #ffffff; --text: #0f172a; --muted: #64748b;
      --border: #e2e8f0; --accent: #2563eb; --accent-soft: #eff6ff;
      --code-bg: #0f172a; --code-text: #e2e8f0;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0b1120; --card: #111827; --text: #f1f5f9; --muted: #94a3b8;
        --border: #1e293b; --accent: #60a5fa; --accent-soft: rgba(59,130,246,.14);
        --code-bg: #020617; --code-text: #e2e8f0;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }}
    .layout {{ max-width: 1120px; margin: 0 auto; display: grid; grid-template-columns: 240px 1fr; gap: 28px; padding: 28px 20px 64px; }}
    .sidebar {{ position: sticky; top: 24px; align-self: start; background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 17px; margin-bottom: 18px; text-decoration: none; color: var(--text); }}
    .brand img {{ width: 32px; height: 32px; }}
    .nav a {{ display: block; padding: 9px 12px; border-radius: 10px; color: var(--muted); text-decoration: none; font-size: 14px; font-weight: 500; margin-bottom: 4px; }}
    .nav a:hover {{ background: var(--accent-soft); color: var(--accent); }}
    .nav a.active {{ background: var(--accent-soft); color: var(--accent); font-weight: 600; }}
    .ext {{ margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border); font-size: 13px; }}
    .ext a {{ color: var(--accent); text-decoration: none; display: block; padding: 5px 0; }}
    .content {{ background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 36px 40px; min-width: 0; }}
    .content h1, .content h2, .content h3 {{ line-height: 1.35; margin-top: 1.6em; }}
    .content h1:first-child {{ margin-top: 0; }}
    .content a {{ color: var(--accent); text-decoration: none; }}
    .content a:hover {{ text-decoration: underline; }}
    .content blockquote {{ margin: 16px 0; padding: 12px 16px; border-left: 4px solid var(--accent); background: var(--accent-soft); border-radius: 0 10px 10px 0; }}
    .content pre {{ background: var(--code-bg); color: var(--code-text); padding: 16px; border-radius: 12px; overflow-x: auto; font-size: 13px; line-height: 1.55; }}
    .content code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9em; }}
    .content :not(pre) > code {{ background: var(--accent-soft); color: var(--accent); padding: 2px 6px; border-radius: 6px; }}
    .content table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
    .content th, .content td {{ border: 1px solid var(--border); padding: 10px 12px; text-align: left; }}
    .content th {{ background: var(--accent-soft); }}
    @media (max-width: 840px) {{
      .layout {{ grid-template-columns: 1fr; padding: 16px 14px 48px; }}
      .sidebar {{ position: static; }}
      .nav {{ display: flex; flex-wrap: wrap; gap: 6px; }}
      .nav a {{ margin-bottom: 0; }}
      .content {{ padding: 22px 18px; }}
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
</body>
</html>
"""

for out_name, src_path, title in PAGES:
    with open(src_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    # Fix markdown links for static HTML pages
    md_text = md_text.replace("docs/DEPLOY.md", "deploy.html").replace("docs/FAQ.md", "faq.html").replace("CHANGELOG.md", "changelog.html")
    body_html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    nav_html = "\n        ".join(
        f'<a href="{p[0]}" class="{"active" if p[0]==out_name else ""}">{html.escape(p[2])}</a>'
        for p in PAGES
    )
    with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(title=html.escape(title), nav=nav_html, body=body_html))

open(os.path.join(OUT, ".nojekyll"), "w").close()
print("Built static docs:", [p[0] for p in PAGES])
