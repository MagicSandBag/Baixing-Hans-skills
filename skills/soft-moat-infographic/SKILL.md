---
name: soft-moat-infographic
description: "Generate soft pastel Chinese information graphics in the style of airy AI/business explainer cards: muted off-white canvas, translucent tinted cards, teal/blue/violet/amber accents, big concise Chinese titles, spaced English micro-subtitles, and comparison or three-step thesis layouts. Use when the user asks to make, recreate, summarize, or template this kind of informational image, AI model guide, business concept card, Xiaohongshu/WeChat-style infographic, or asks whether to generate it with HTML/CSS versus direct drawing."
---

# Soft Moat Infographic

## Core Judgment

Default to **HTML/CSS rendered to image**. The reference style is text-heavy, grid-based, and built from web-native primitives: translucent rounded cards, subtle borders, CSS gradients, big background watermark words, tight baseline alignment, and responsive Chinese text. A JPEG alone cannot prove the original toolchain, but HTML/CSS is the most maintainable way to reproduce it. Use direct canvas/PIL drawing only when no browser rendering is available or when the target output must be programmatic with no HTML artifact.

## Workflow

1. Distill the source notes into one sharp thesis.
2. Choose a layout:
   - `cards`: 4-6 vertical comparison cards, best for model/tool/option comparisons.
   - `flow`: 3 large cards connected by arrows, best for a causal argument or market evolution.
3. Write concise Chinese copy:
   - Title: 10-18 Chinese characters if possible.
   - Subtitle: uppercase English or pinyin-style microcopy with generous letter spacing.
   - Card labels: 4-8 Chinese characters.
   - Metrics: one large number, price, multiplier, or symbol per card when useful.
   - Body: 1-3 short lines. Avoid dense paragraphs.
4. Render with `scripts/render_moat_infographic.py` when an editable HTML plus image export is useful.
5. Verify visually: no clipped Chinese text, no line too long, cards aligned, accent colors balanced, watermark faint enough to stay background-only.

## Quick Start

Create a JSON payload and render it:

```bash
python C:/Users/28412/.codex/skills/soft-moat-infographic/scripts/render_moat_infographic.py --input data.json --output output.png --scale 3
```

The script always writes a sibling `.html` file. If Playwright is installed, it also exports PNG/JPEG. If Playwright is unavailable, open the HTML in a browser and export/screenshot from there, or install Playwright for automated rendering.

Use `--scale 3` or `--scale 4` for final PNG exports. A 1080 x 576 design becomes 3240 x 1728 at 3x, which preserves subtle map lines, card borders, and paper texture on high-density screens.

Use the bundled examples as starting points:

```bash
python C:/Users/28412/.codex/skills/soft-moat-infographic/scripts/render_moat_infographic.py --input C:/Users/28412/.codex/skills/soft-moat-infographic/assets/example_cards.json --output cards.png
python C:/Users/28412/.codex/skills/soft-moat-infographic/scripts/render_moat_infographic.py --input C:/Users/28412/.codex/skills/soft-moat-infographic/assets/example_flow.json --output flow.png
```

## Input Schema

```json
{
  "layout": "cards",
  "width": 1080,
  "height": 576,
  "eyebrow": "AI MODEL GUIDE · BY NAME",
  "title": "没有最强的模型，只有最对的",
  "subtitle": "5 MODELS · USE CASE · COST · OUTPUT QUALITY",
  "watermark": "AI",
  "credit": "by @白星Hans",
  "cards": [
    {
      "label": "品牌片",
      "heading": "Veo 3",
      "metric": "¥15",
      "metric_suffix": "/条",
      "body": "画质上限最高，适合品牌正式宣传。",
      "badge": "画质最高",
      "accent": "cobalt"
    }
  ]
}
```

For `flow`, keep three cards and optionally set `note` for each card. The script accepts `accent` values: `teal`, `mint`, `blue`, `cobalt`, `violet`, `amber`, `gray`.

## Style Reference

Read `references/style-guide.md` before making substantial changes to the look. Keep these defaults unless the user asks for a different style:

- Canvas: 1080 x 541 or 1080 x 576, off-white, very low-contrast texture/watermark.
- Typography: Chinese system sans, heavy title, small tracked English subtitle.
- Color: mostly neutral white/gray with a few cool accents; teal and blue dominate, amber/violet are supporting accents.
- Cards: translucent pastel fills, 1px soft border, 8px radius, minimal shadow.
- Composition: wide margins, generous whitespace, clear vertical hierarchy, bottom-right credit.

## Copy Rules

Do not write generic UI explanations such as "this image shows" or "this card contains". Write the actual infographic copy. Prefer useful judgments, tradeoffs, numbers, and labels. If the source material is weak, first improve the information architecture, then render.
