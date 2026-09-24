from pathlib import Path
import sys

root = Path(sys.argv[1])
template = Path(__file__).with_name("syndrone_beta_product_page.html")
page_dir = root / "syndrone_beta_product_page"
page_dir.mkdir(parents=True, exist_ok=True)
(page_dir / "index.html").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")

src_assets = Path(__file__).resolve().parents[1] / "release-assets" / "syndrone"
dst_assets = root / "downloads" / "syndrone"
dst_assets.mkdir(parents=True, exist_ok=True)
for p in src_assets.iterdir():
    if p.is_file():
        # The public Syndrone interface is uploaded directly to downloads/syndrone.
        # Do not overwrite it with the legacy release-assets copy during rebuilds.
        if p.name == "syndrone-interface.jpg" and (dst_assets / p.name).exists():
            continue
        (dst_assets / p.name).write_bytes(p.read_bytes())

for page_name in ("plugins.html", "index.html"):
    p = root / page_name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    opening = '<div class="wrap products">'
    card = r'''
    <article class="card" id="syndrone-card">
      <div class="media syndrone-media"><img src="/downloads/syndrone/syndrone-interface.jpg?v=105" alt="Syndrone plugin interface"></div>
      <div class="body">
        <div class="product-kicker">generative drone synthesizer · beta 1.0.5</div>
        <h2>Syndrone</h2>
        <p>A deep generative drone instrument with 16 synthesis structures, 16 Characters, long-form evolution, scene morphing, spatial motion, Mass/Supermassive and a greatly expanded four-slot modulation system.</p>
        <div class="meta"><span class="tag">macOS</span><span class="tag">Windows</span><span class="tag">AU / VST3</span><span class="tag">beta</span></div>
        <div class="actions">
          <a class="btn syndrone" href="/syndrone_beta_product_page/">explore Syndrone</a>
          <a class="btn" download href="/downloads/syndrone/Syndrone-1.0.5-macOS-Universal.pkg">Mac beta</a>
          <a class="btn" download href="/downloads/syndrone/Syndrone-1.0.5-Windows-x64-Setup.exe">Windows beta</a>
          <a class="btn" href="/downloads/syndrone/Syndrone-v1.0.5-Expanded-Landscape-User-Guide.pdf">User guide</a>
        </div>
      </div>
    </article>
'''
    if 'id="syndrone-card"' in text:
        start=text.find('<article class="card" id="syndrone-card">')
        end=text.find('</article>',start)
        if end!=-1:
            end += len('</article>')
            text=text[:start]+card.strip()+text[end:]
    elif opening in text:
        text=text.replace(opening, opening+"\n"+card, 1)

    css=r'''
<style id="syndrone-card-style">
.btn.syndrone{background:#c89f5f !important;border-color:#c89f5f !important;color:#122028 !important;box-shadow:0 7px 20px rgba(147,104,42,.22)}
.btn.syndrone:hover{filter:brightness(1.08);transform:translateY(-1px)}
.syndrone-media{background:#10242b;min-height:260px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.syndrone-media img{width:auto;max-width:540px;height:auto;max-height:100%;object-fit:contain;padding:10px;display:block}
</style>
'''
    if 'id="syndrone-card-style"' not in text and '</head>' in text:
        text=text.replace('</head>',css+'\n</head>',1)
    p.write_text(text,encoding="utf-8")

(root / "CNAME").write_text("plugins.slowfieldaudio.com\n", encoding="utf-8")
(root / ".nojekyll").touch()
