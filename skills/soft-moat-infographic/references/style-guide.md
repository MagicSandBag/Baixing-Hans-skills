# Soft Moat Infographic Style Guide

## Source Analysis

The reference images are JPEG exports at 1080 x 576 and 1080 x 541. Their metadata does not identify the originating software. Observable traits point to a browser/Figma-like layout rather than hand drawing: fixed grid columns, text blocks aligned to consistent margins, translucent card fills, CSS-like gradients, subtle borders, and oversized low-opacity watermark typography. Treat the original source as unknowable from the JPEG alone; reproduce the style with HTML/CSS by default.

## Visual DNA

- Airy white canvas, slightly cool: `#F2F5F8`, `#F6F8FA`, `#F2F7F9`.
- Main ink: `#252B38`; secondary ink: `#596473`; tertiary ink: `#8791A0`.
- Accent palette:
  - teal: `#18B89F`
  - mint: `#33C0A3`
  - blue: `#347EDC`
  - cobalt: `#3858D6`
  - violet: `#9A64E8`
  - amber: `#E28B14`
  - gray: `#8FA0B3`
- Pastel card fills:
  - teal wash: `rgba(24, 184, 159, 0.10)`
  - blue wash: `rgba(52, 126, 220, 0.09)`
  - violet wash: `rgba(154, 100, 232, 0.10)`
  - amber wash: `rgba(226, 139, 20, 0.10)`
  - gray wash: `rgba(143, 160, 179, 0.09)`

## Typography

Use a CJK system stack:

```css
font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", Arial, sans-serif;
```

Recommended sizes for a 1080px-wide image:

- Eyebrow pill: 10-11px, 700 weight.
- Title: 32-38px, 800-900 weight, 1.08 line-height.
- English subtitle: 10-12px, 600-700 weight, 5-7px letter spacing.
- Card label: 10-12px, 700 weight.
- Card heading: 24-28px, 850-900 weight.
- Metric: 38-48px, 800-900 weight.
- Body: 13-15px, 1.75-1.95 line-height.
- Badge/note: 10-12px, 700 weight.

Never make the body text look like a paragraph page. Break information into short, judgment-rich chunks.

## Layout Patterns

### Cards Layout

Use when comparing models, tools, plans, channels, roles, or options.

- Canvas: 1080 x 576.
- Outer padding: 32px top, 32px sides, 22px bottom.
- Header height: about 105px.
- Grid: 4-6 columns, 14-18px gap.
- Card height: about 400px.
- Put the badge at the bottom to create the long quiet lower area.

### Flow Layout

Use when explaining a market transition, causal chain, or strategic conclusion.

- Canvas: 1080 x 541.
- Outer padding: 44px sides, 46px top.
- Header height: about 115px.
- Three cards: equal width, about 302px wide and 280px tall.
- Use thin arrows between cards. Keep arrows muted blue/gray.
- Make the final card slightly greener/teal and more saturated to signal conclusion.

## Background Treatment

Use one very faint oversized watermark word such as `AI`, `MODEL`, `MOAT`, or the topic keyword. It should sit behind the content and be barely readable. Add a high-transparency map/topographic line layer when the image needs more depth: 0.10-0.20 stroke opacity, muted teal/gray strokes, no filled shapes, and no lines competing with text. Avoid decorative bubbles, strong radial blobs, and saturated gradient backgrounds. The background should feel like paper plus light passing through frosted glass.

## Information Architecture

Good prompts produce:

1. A title with a hard claim.
2. A subtitle that compresses the dimensions being compared.
3. Cards with one primary number or concept each.
4. A short body explaining "when to use it" or "why it matters".
5. A bottom badge or note that summarizes the card's role.

Use `by @白星Hans` as the default credit unless the user explicitly asks for a different signature.

Bad prompts produce:

- Too many paragraphs.
- Vague labels like "优势" without a concrete tradeoff.
- Repeated colors with no hierarchy.
- Decorative charts with no data.
- Heavy shadows or saturated colored blocks.
