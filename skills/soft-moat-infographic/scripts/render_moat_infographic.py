#!/usr/bin/env python3
"""Render soft pastel Chinese infographic HTML and optionally export an image.

Supports pluggable themes via the top-level "theme" JSON field or --theme.
"classic" preserves the original cool off-white look; "social-pink" is a
Bilibili-inspired blush palette.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


THEMES: dict[str, dict[str, Any]] = {
    # Cool off-white paper, teal/blue accents. The original look; default.
    "classic": {
        "default_accent": "teal",
        "accents": {
            "teal": {"accent": "#18B89F", "soft": "rgba(24, 184, 159, 0.09)", "border": "rgba(24, 184, 159, 0.24)"},
            "mint": {"accent": "#33C0A3", "soft": "rgba(51, 192, 163, 0.09)", "border": "rgba(51, 192, 163, 0.24)"},
            "blue": {"accent": "#347EDC", "soft": "rgba(52, 126, 220, 0.08)", "border": "rgba(52, 126, 220, 0.21)"},
            "cobalt": {"accent": "#3858D6", "soft": "rgba(56, 88, 214, 0.08)", "border": "rgba(56, 88, 214, 0.20)"},
            "violet": {"accent": "#9A64E8", "soft": "rgba(154, 100, 232, 0.09)", "border": "rgba(154, 100, 232, 0.20)"},
            "amber": {"accent": "#E28B14", "soft": "rgba(226, 139, 20, 0.09)", "border": "rgba(226, 139, 20, 0.22)"},
            "gray": {"accent": "#8FA0B3", "soft": "rgba(143, 160, 179, 0.08)", "border": "rgba(143, 160, 179, 0.20)"},
        },
        "tokens": {
            "page-bg": "#EDEFF3",
            "ink": "#252B38",
            "heading-ink": "#171D2A",
            "subtitle-ink": "#596270",
            "body-ink": "#354052",
            "credit-ink": "#737D88",
            "note-ink": "#2C5B9B",
            "arrow-ink": "#4A89CE",
            "flow-accent": "#15A891",
            "eyebrow-bg": "linear-gradient(90deg, #2F7CE6, #12B697)",
            "watermark-ink": "rgba(88, 143, 154, 0.09)",
            "map-line-a": "#7EA9B7",
            "map-line-b": "#C6CDD8",
            "card-shadow": "rgba(35, 47, 68, 0.034)",
            "canvas-bg": (
                "linear-gradient(118deg, rgba(255,255,255,0.98), rgba(242,248,250,0.93) 44%, rgba(252,250,247,0.96)),\n"
                "    linear-gradient(72deg, rgba(44,126,204,0.045), transparent 36%, rgba(26,184,159,0.045) 78%, transparent),\n"
                "    repeating-linear-gradient(90deg, rgba(42,70,96,0.014) 0 1px, transparent 1px 72px),\n"
                "    #F5F7FA"
            ),
        },
    },
    # Bilibili-inspired social pink: blush paper, pink/blue duality.
    "social-pink": {
        "default_accent": "pink",
        "accents": {
            "pink": {"accent": "#FB7299", "soft": "rgba(251, 114, 153, 0.09)", "border": "rgba(251, 114, 153, 0.24)"},
            "blue": {"accent": "#00A1D6", "soft": "rgba(0, 161, 214, 0.08)", "border": "rgba(0, 161, 214, 0.22)"},
            "sky": {"accent": "#0CB6F2", "soft": "rgba(12, 182, 242, 0.09)", "border": "rgba(12, 182, 242, 0.22)"},
            "amber": {"accent": "#FF9D00", "soft": "rgba(255, 157, 0, 0.09)", "border": "rgba(255, 157, 0, 0.22)"},
            "green": {"accent": "#00B853", "soft": "rgba(0, 184, 83, 0.08)", "border": "rgba(0, 184, 83, 0.20)"},
            "coral": {"accent": "#FF6B6B", "soft": "rgba(255, 107, 107, 0.09)", "border": "rgba(255, 107, 107, 0.22)"},
            "gray": {"accent": "#9499A0", "soft": "rgba(148, 153, 160, 0.08)", "border": "rgba(148, 153, 160, 0.20)"},
        },
        "tokens": {
            "page-bg": "#F6F7F8",
            "ink": "#18191C",
            "heading-ink": "#18191C",
            "subtitle-ink": "#61666D",
            "body-ink": "#3E434C",
            "credit-ink": "#9499A0",
            "note-ink": "#2A87B0",
            "arrow-ink": "#3FA9D3",
            "flow-accent": "#F26183",
            "eyebrow-bg": "linear-gradient(90deg, #FF9DB6, #FB7299)",
            "watermark-ink": "rgba(196, 122, 148, 0.09)",
            "map-line-a": "#DCA0B2",
            "map-line-b": "#D9C9CF",
            "card-shadow": "rgba(122, 58, 80, 0.04)",
            "canvas-bg": (
                "linear-gradient(118deg, rgba(255,255,255,0.98), rgba(255,241,245,0.94) 44%, rgba(255,249,243,0.97)),\n"
                "    linear-gradient(72deg, rgba(251,114,153,0.05), transparent 36%, rgba(0,161,214,0.05) 78%, transparent),\n"
                "    repeating-linear-gradient(90deg, rgba(110,56,74,0.014) 0 1px, transparent 1px 72px),\n"
                "    #FBF6F7"
            ),
        },
    },
}


DEFAULT_DATA: dict[str, Any] = {
    "layout": "cards",
    "theme": "classic",
    "width": 1080,
    "height": 576,
    "eyebrow": "AI MODEL GUIDE",
    "title": "没有最强的模型，只有最对的",
    "subtitle": "USE CASE · COST · OUTPUT QUALITY · LEARN THE PATTERN",
    "watermark": "AI",
    "credit": "by @白星Hans",
    "cards": [
        {
            "label": "品牌片",
            "heading": "Model A",
            "metric": "¥15",
            "metric_suffix": "/条",
            "body": "画质上限最高，适合正式宣传和高预算投放。",
            "badge": "画质最高",
            "accent": "cobalt",
        },
        {
            "label": "种草内容",
            "heading": "Model B",
            "metric": "¥3",
            "metric_suffix": "/条",
            "body": "质感接近实拍，适合批量测试脚本和素材方向。",
            "badge": "真实感强",
            "accent": "teal",
        },
        {
            "label": "草稿验证",
            "heading": "Model C",
            "metric": "¥0.5",
            "metric_suffix": "/条",
            "body": "成本低，适合先跑分镜和概念，不追求单条成片。",
            "badge": "量大管够",
            "accent": "amber",
        },
        {
            "label": "叙事故事",
            "heading": "Model D",
            "metric": "按需",
            "metric_suffix": "计费",
            "body": "多镜头转场自然，适合叙事型产品内容。",
            "badge": "转场自然",
            "accent": "blue",
        },
        {
            "label": "长片内容",
            "heading": "Model E",
            "metric": "按需",
            "metric_suffix": "计费",
            "body": "支持更长的视频结构，适合课程、解说和故事类内容。",
            "badge": "长片友好",
            "accent": "violet",
        },
    ],
}


def resolve_theme(data: dict[str, Any]) -> dict[str, Any]:
    key = str(data.get("theme") or "classic").lower()
    if key not in THEMES:
        raise ValueError(f"theme must be one of: {', '.join(sorted(THEMES))}; got '{key}'")
    return THEMES[key]


def theme_css_vars(theme: dict[str, Any]) -> str:
    return "\n".join(f"  --{key}: {value};" for key, value in theme["tokens"].items())


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def paragraph_html(value: Any) -> str:
    if isinstance(value, list):
        return "".join(f"<p>{esc(item)}</p>" for item in value if str(item).strip())
    text = esc(value)
    parts = [part.strip() for part in text.splitlines() if part.strip()]
    if len(parts) > 1:
        return "".join(f"<p>{part}</p>" for part in parts)
    return f"<p>{text}</p>" if text else ""


def tone_style(name: str, theme: dict[str, Any]) -> str:
    accents: dict[str, dict[str, str]] = theme["accents"]
    tone = accents.get(name) or accents[theme["default_accent"]]
    return f"--accent:{tone['accent']};--soft:{tone['soft']};--line:{tone['border']};"


def render_card(card: dict[str, Any], layout: str, theme: dict[str, Any]) -> str:
    accent = str(card.get("accent") or theme["default_accent"])
    metric = esc(card.get("metric", ""))
    suffix = esc(card.get("metric_suffix", ""))
    metric_html = ""
    if metric:
        metric_html = f'<div class="metric"><span>{metric}</span><em>{suffix}</em></div>'
    note = esc(card.get("note", ""))
    note_html = f'<div class="note">{note}</div>' if note else ""
    badge = esc(card.get("badge", ""))
    badge_html = f'<div class="badge">{badge}</div>' if badge else ""
    return f"""
      <section class="card {layout}-card" style="{tone_style(accent, theme)}">
        <div class="label">{esc(card.get("label", ""))}</div>
        <h2>{esc(card.get("heading", ""))}</h2>
        {metric_html}
        <div class="body-copy">{paragraph_html(card.get("body", ""))}</div>
        {note_html}
        <div class="card-spacer"></div>
        {badge_html}
      </section>
    """


def render_cards(data: dict[str, Any], theme: dict[str, Any]) -> str:
    cards = data.get("cards") or []
    count = max(1, len(cards))
    cards_html = "\n".join(render_card(card, "cards", theme) for card in cards)
    return f'<div class="cards-grid" style="--count:{count};">{cards_html}</div>'


def render_flow(data: dict[str, Any], theme: dict[str, Any]) -> str:
    cards = data.get("cards") or []
    parts: list[str] = ['<div class="flow-grid">']
    for index, card in enumerate(cards):
        parts.append(render_card(card, "flow", theme))
        if index < len(cards) - 1:
            parts.append('<div class="arrow">→</div>')
    parts.append("</div>")
    return "\n".join(parts)


def build_html(data: dict[str, Any]) -> str:
    layout = str(data.get("layout", "cards")).lower()
    if layout not in {"cards", "flow"}:
        raise ValueError("layout must be 'cards' or 'flow'")
    theme = resolve_theme(data)

    width = int(data.get("width") or 1080)
    height = int(data.get("height") or (541 if layout == "flow" else 576))
    content = render_flow(data, theme) if layout == "flow" else render_cards(data, theme)
    eyebrow = esc(data.get("eyebrow", ""))
    title = esc(data.get("title", ""))
    subtitle = esc(data.get("subtitle", ""))
    watermark = esc(data.get("watermark", "AI"))
    credit = esc(data.get("credit") or "by @白星Hans")
    eyebrow_html = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ""
    title_html = f"<h1>{title}</h1>" if title else ""
    bg_map = f"""
    <svg class="bg-map" viewBox="0 0 {width} {height}" preserveAspectRatio="none" aria-hidden="true">
      <g class="map-a" stroke-width="1.1" stroke-opacity="0.10">
        <path d="M610 60 C675 20 760 34 815 84 C870 134 950 118 1038 170" />
        <path d="M650 105 C718 70 777 82 831 128 C886 175 966 160 1054 214" />
        <path d="M698 150 C756 125 820 138 870 178 C930 226 992 220 1082 254" />
        <path d="M775 40 C742 86 746 142 786 178 C830 216 818 272 760 318" />
        <path d="M900 22 C865 72 870 125 912 164 C956 205 956 265 912 318" />
        <path d="M120 380 C190 338 278 344 340 392 C415 452 505 434 570 492" />
        <path d="M76 420 C162 382 250 392 322 444 C392 494 494 482 626 526" />
      </g>
      <g class="map-b" stroke-width="0.9" stroke-opacity="0.12">
        <path d="M42 160 C128 138 214 146 302 182 C385 216 480 212 560 178" />
        <path d="M46 206 C142 184 235 194 320 230 C412 270 500 260 585 220" />
        <path d="M36 254 C132 238 226 250 314 288 C404 326 502 318 608 270" />
      </g>
    </svg>
    """

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
{theme_css_vars(theme)}
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--page-bg); }}
body {{
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", Arial, sans-serif;
  color: var(--ink);
}}
.canvas {{
  position: relative;
  width: {width}px;
  height: {height}px;
  overflow: hidden;
  background: var(--canvas-bg);
}}
.canvas::before {{
  content: attr(data-watermark);
  position: absolute;
  top: -48px;
  left: 92px;
  z-index: 0;
  font-size: 218px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: 12px;
  color: var(--watermark-ink);
  pointer-events: none;
  white-space: nowrap;
}}
.canvas::after {{
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.52), rgba(255,255,255,0.14) 58%, rgba(255,255,255,0.42)),
    repeating-linear-gradient(0deg, transparent 0 23px, rgba(67,87,111,0.015) 23px 24px);
  pointer-events: none;
}}
.bg-map {{
  position: absolute;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  mix-blend-mode: multiply;
}}
.bg-map path {{
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  vector-effect: non-scaling-stroke;
}}
.bg-map .map-a {{ stroke: var(--map-line-a); }}
.bg-map .map-b {{ stroke: var(--map-line-b); }}
.inner {{
  position: relative;
  z-index: 2;
  height: 100%;
  padding: 32px 32px 22px;
  display: flex;
  flex-direction: column;
}}
.layout-flow .inner {{ padding: 46px 44px 28px; }}
.header {{ min-height: 104px; }}
.layout-flow .header {{ min-height: 96px; }}
.eyebrow {{
  display: inline-flex;
  align-items: center;
  max-width: 680px;
  min-height: 24px;
  padding: 0 14px;
  border-radius: 8px;
  background: var(--eyebrow-bg);
  color: white;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 4px;
  text-transform: uppercase;
}}
.layout-flow .eyebrow {{
  background: transparent;
  color: var(--flow-accent);
  padding: 0;
  letter-spacing: 0;
  font-size: 26px;
  min-height: 0;
}}
h1 {{
  margin: 8px 0 4px;
  max-width: 760px;
  font-size: 34px;
  line-height: 1.08;
  font-weight: 900;
  letter-spacing: 0;
}}
.layout-flow h1 {{
  margin-top: 0;
  color: var(--flow-accent);
  font-size: 30px;
}}
.subtitle {{
  color: var(--subtitle-ink);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 6px;
  text-transform: uppercase;
}}
.layout-flow .subtitle {{ letter-spacing: 5px; }}
.cards-grid {{
  display: grid;
  grid-template-columns: repeat(var(--count), minmax(0, 1fr));
  gap: 14px;
  flex: 1;
}}
.card {{
  position: relative;
  display: flex;
  min-width: 0;
  flex-direction: column;
  border: 1px solid var(--line);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.66), rgba(255,255,255,0.28)),
    linear-gradient(135deg, rgba(255,255,255,0.24), transparent 42%),
    var(--soft);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.74),
    0 14px 34px var(--card-shadow);
  backdrop-filter: blur(6px);
  overflow: hidden;
}}
.card::before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(130deg, rgba(255,255,255,0.36), transparent 34%),
    repeating-linear-gradient(0deg, transparent 0 36px, rgba(255,255,255,0.16) 36px 37px),
    repeating-linear-gradient(90deg, transparent 0 48px, rgba(255,255,255,0.10) 48px 49px);
  opacity: 0.78;
  pointer-events: none;
}}
.cards-card {{
  padding: 18px 16px 16px;
}}
.flow-card {{
  min-height: 282px;
  padding: 28px 22px 22px;
}}
.label {{
  position: relative;
  z-index: 1;
  margin-bottom: 8px;
  color: var(--accent);
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 2px;
}}
h2 {{
  position: relative;
  z-index: 1;
  margin: 0;
  color: var(--heading-ink);
  font-size: 26px;
  line-height: 1.08;
  font-weight: 900;
  letter-spacing: 1px;
}}
.flow-card h2 {{ margin-top: 12px; font-size: 22px; }}
.metric {{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin: 8px 0 12px;
  color: var(--accent);
}}
.metric span {{
  font-size: 38px;
  line-height: 1;
  font-weight: 900;
}}
.flow-card .metric span {{ font-size: 44px; }}
.metric em {{
  color: var(--ink);
  font-style: normal;
  font-size: 11px;
  font-weight: 700;
}}
.body-copy {{
  position: relative;
  z-index: 1;
  color: var(--body-ink);
  font-size: 13px;
  font-weight: 600;
  line-height: 1.82;
  text-align: left;
}}
.flow-card .body-copy {{ font-size: 14px; line-height: 1.78; }}
.body-copy p {{ margin: 0 0 5px; }}
.note {{
  position: relative;
  z-index: 1;
  margin-top: 18px;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.38);
  color: var(--note-ink);
  font-size: 12px;
  font-weight: 800;
  line-height: 1.6;
}}
.card-spacer {{ flex: 1; }}
.badge {{
  position: relative;
  z-index: 1;
  align-self: flex-start;
  margin-top: 14px;
  padding: 6px 12px;
  border-radius: 8px;
  background: var(--accent);
  color: white;
  font-size: 10px;
  font-weight: 850;
  letter-spacing: 0;
}}
.flow-grid {{
  display: grid;
  grid-template-columns: 1fr 42px 1fr 42px 1fr;
  align-items: center;
  gap: 0;
  flex: 1;
}}
.arrow {{
  color: var(--arrow-ink);
  font-size: 28px;
  font-weight: 500;
  text-align: center;
  opacity: 0.80;
}}
.credit {{
  position: absolute;
  right: 24px;
  bottom: 16px;
  z-index: 3;
  color: var(--credit-ink);
  font-size: 10px;
  font-weight: 700;
}}
</style>
</head>
<body>
  <main class="canvas layout-{layout}" data-watermark="{watermark}">
    {bg_map}
    <div class="inner">
      <header class="header">
        {eyebrow_html}
        {title_html}
        <div class="subtitle">{subtitle}</div>
      </header>
      {content}
    </div>
    <div class="credit">{credit}</div>
  </main>
</body>
</html>
"""


def read_data(path: Path | None) -> dict[str, Any]:
    if path is None:
        return dict(DEFAULT_DATA)
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    data = dict(DEFAULT_DATA)
    data.update(loaded)
    return data


def write_html(data: dict[str, Any], html_path: Path) -> None:
    html_path.write_text(build_html(data), encoding="utf-8")


def render_image(html_path: Path, output_path: Path, width: int, height: int, scale: float, quality: int) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError(
            "Playwright is required for image export. The HTML file was written; install Playwright or open it in a browser."
        ) from exc

    image_type = output_path.suffix.lower().lstrip(".")
    if image_type == "jpg":
        image_type = "jpeg"
    if image_type not in {"png", "jpeg"}:
        raise ValueError("output image must end with .png, .jpg, or .jpeg")

    with sync_playwright() as playwright:
        browser = None
        last_error: Exception | None = None
        for launch_kwargs in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
            try:
                browser = playwright.chromium.launch(**launch_kwargs)
                break
            except Exception as exc:  # pragma: no cover - browser availability is environment-specific
                last_error = exc
        if browser is None:
            raise RuntimeError(
                "No Playwright-compatible browser is available. Run `python -m playwright install chromium`, "
                "or install Microsoft Edge/Chrome, or render the written HTML manually."
            ) from last_error
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        kwargs: dict[str, Any] = {"path": str(output_path), "type": image_type, "full_page": False}
        if image_type == "jpeg":
            kwargs["quality"] = quality
        page.screenshot(**kwargs)
        browser.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON payload. Uses demo content when omitted.")
    parser.add_argument("--output", type=Path, default=Path("soft-moat-infographic.png"), help="Output .png/.jpg/.jpeg/.html path.")
    parser.add_argument("--theme", choices=sorted(THEMES), default=None, help="Theme override; defaults to the JSON 'theme' field or 'classic'.")
    parser.add_argument("--html-only", action="store_true", help="Only write HTML, even when output is an image path.")
    parser.add_argument("--scale", type=float, default=3.0, help="Browser device scale factor for image export. Use 3 for high-resolution social graphics.")
    parser.add_argument("--quality", type=int, default=95, help="JPEG quality, 1-100.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    data = read_data(args.input)
    if args.theme:
        data["theme"] = args.theme
    width = int(data.get("width") or 1080)
    height = int(data.get("height") or (541 if data.get("layout") == "flow" else 576))
    output_path: Path = args.output
    html_path = output_path if output_path.suffix.lower() == ".html" else output_path.with_suffix(".html")

    write_html(data, html_path)
    print(f"Wrote HTML: {html_path}")

    if args.html_only or output_path.suffix.lower() == ".html":
        return 0

    render_image(html_path, output_path, width, height, args.scale, args.quality)
    print(f"Wrote image: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
