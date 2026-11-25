# STYLE.md

palette: primary #E2231A (OCBC red; swap in the exact hex from the official template),
         ink #1F1F1F, muted #8C8C8C, light grey #E5E5E5, background #FFFFFF,
         accent = #E2231A, used ONLY for the element that carries each slide's message
type: display Arial/Helvetica Bold (or the template font) / body Arial
      titles may wrap to two lines at 28pt (accepted at review C05: one line would cost the numbers)
      min sizes: title 28pt, body 14pt, source 9pt
chart tokens: grid #E5E5E5 0.5pt; direct labels instead of legends; accent vs grey
      emphasis (~90% grey ink, one red element); bars start at 0; units on every axis (IDR bn, %, days)
figure style block: none. This deck is all-exhibit, so no generated imagery and no API key are needed
theme intensity: 0. The beats run underneath and the panel sees a pure consulting surface
compliance: aggregates only, no customer-level data; footer "Internal – Confidential"
charts: rendered as PNG images by charts.py (matplotlib), so they display in Google Slides and on mobile.
      The data stays in data/E##.csv; rebuild to update.
icons: Lucide (ISC licence, icons/LICENSE-lucide.txt), red or ink, on a round badge. Used only on text
      slides (summary, options, criteria, workplan, guardrails, ask); never on chart slides
