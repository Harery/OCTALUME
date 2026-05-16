# Social Preview Image

GitHub renders a 1280×640 image when this repo is shared on Twitter/X, LinkedIn,
Slack, Discord, Hacker News, etc. A strong preview is one of the highest-ROI
things you can do for discoverability.

## How to upload

1. Generate the image (see spec below).
2. Go to https://github.com/Harery/OCTALUME/settings → scroll to **Social preview**.
3. Click **Edit** → **Upload an image** → drag your 1280×640 PNG.
4. Save. The preview takes 5–10 minutes to propagate through CDNs.

You can verify with:
- https://www.opengraph.xyz/url/https%3A%2F%2Fgithub.com%2FHarery%2FOCTALUME
- https://cards-dev.twitter.com/validator

## Image spec

- **Dimensions:** 1280 × 640 px (2:1)
- **Safe area:** keep all text within the centered 1120 × 580 area; Twitter
  crops the edges on mobile.
- **Format:** PNG (preferred) or JPG, < 1 MB.
- **Theme:** dark navy / deep purple background, glowing octagon motif —
  matches the "Octa + Lume (light)" brand.
- **Typography:** Inter or Geist, bold for the wordmark, medium for tagline.

## Recommended composition

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   ╔══════════╗     OCTALUME                                  │
│   ║   ⬣      ║     ─────────                                 │
│   ║  octa    ║     The AI-Native SDLC Framework              │
│   ║  lume    ║     for Regulated Enterprises                 │
│   ╚══════════╝                                               │
│                                                              │
│      8 Phases  ·  Quality Gates  ·  Multi-Agent              │
│              HIPAA · SOC 2 · PCI · GDPR                      │
│                                                              │
│                            github.com/Harery/OCTALUME        │
└──────────────────────────────────────────────────────────────┘
```

## Required text on the card

1. **Wordmark:** OCTALUME (largest element, top-left or centered)
2. **Tagline:** "The AI-Native SDLC Framework for Regulated Enterprises"
3. **Three keywords:** 8 Phases · Quality Gates · Multi-Agent Orchestration
4. **Compliance row (small):** HIPAA · SOC 2 · PCI DSS · GDPR
5. **URL (bottom-right, small):** github.com/Harery/OCTALUME

## Generators you can use (no design skills required)

- https://socialify.git.ci/ — auto-generates from repo metadata
- https://www.canva.com/ — search "GitHub social preview" template
- https://og-playground.vercel.app/ — code-driven, perfect-pixel
- Figma template: 1280×640 frame, drop logo + tagline

## Octagon SVG motif (drop into Figma / Canva)

```svg
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <polygon points="60,10 140,10 190,60 190,140 140,190 60,190 10,140 10,60"
           fill="none" stroke="#7c3aed" stroke-width="6"/>
  <polygon points="60,10 140,10 190,60 190,140 140,190 60,190 10,140 10,60"
           fill="#7c3aed" opacity="0.15"/>
  <text x="100" y="115" text-anchor="middle"
        font-family="Inter, sans-serif" font-weight="800"
        font-size="48" fill="#f8fafc">8</text>
</svg>
```

## Once uploaded

Post on X / LinkedIn with the link — the preview will render automatically.
See [MARKETING.md](MARKETING.md) for ready-to-paste post copy.
