from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Brand colors
ACC_PURPLE = RGBColor(0xA1, 0x00, 0xFF)   # Signature purple
ACC_BLACK  = RGBColor(0x00, 0x00, 0x00)
ACC_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
ACC_GRAY   = RGBColor(0x46, 0x46, 0x46)
ACC_LGRAY  = RGBColor(0xF2, 0xF2, 0xF2)
ACC_DGRAY  = RGBColor(0x1A, 0x1A, 0x1A)
ACC_MGRAY  = RGBColor(0xCC, 0xCC, 0xCC)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # completely blank

def add_rect(slide, l, t, w, h, color, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    return shape

def add_textbox(slide, text, l, t, w, h,
                font_name="Arial", font_size=18, bold=False, italic=False,
                color=ACC_WHITE, align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_label(slide, text, l, t):
    add_textbox(slide, text, l, t, 8, 0.35,
                font_size=9, bold=True, color=ACC_PURPLE,
                font_name="Arial")

def purple_bar(slide, height=0.06):
    add_rect(slide, 0, SLIDE_H.inches - height, SLIDE_W.inches, height, ACC_PURPLE)

def accent_chevron(slide, l=12.5, t=6.9, size=0.45):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(size*2), Inches(size))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = ">"
    run.font.name = "Arial"
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = ACC_PURPLE

def slide_number(slide, n, total):
    add_textbox(slide, f"{n} / {total}", 12.2, 7.1, 1, 0.3,
                font_size=8, color=ACC_MGRAY, align=PP_ALIGN.RIGHT)

def divider_line(slide, l, t, w):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACC_PURPLE
    shape.line.fill.background()

TOTAL = 13

# ── Slide 1: Title ─────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_BLACK)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
add_rect(sl, 0, SLIDE_H.inches - 0.08, SLIDE_W.inches, 0.08, ACC_PURPLE)

add_textbox(sl, "CONFIDENTIAL — PREPARED FOR MERIDIAN COMPONENTS",
            0.8, 0.4, 11, 0.4, font_size=9, bold=True, color=ACC_PURPLE)
add_textbox(sl, "Modernizing Your\nInventory Dashboard",
            0.8, 1.1, 10, 2.5, font_size=48, bold=True, color=ACC_WHITE)
add_textbox(sl, "Response to RFP #MC-2026-0417",
            0.8, 3.8, 10, 0.6, font_size=20, color=ACC_MGRAY)
add_textbox(sl, "April 28, 2026",
            0.8, 4.5, 4, 0.4, font_size=14, color=ACC_GRAY)
accent_chevron(sl)
slide_number(sl, 1, TOTAL)

# ── Slide 2: The Situation ──────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "THE SITUATION", 0.8, 0.35)
add_textbox(sl, "Your team is held back\nby unfinished work",
            0.8, 0.7, 11, 1.4, font_size=32, bold=True, color=ACC_BLACK)
divider_line(sl, 0.8, 2.2, 1.2)

cards = [
    ("REPORTS", "8+ known defects", "Filters, i18n gaps, and data inconsistencies the previous vendor never resolved"),
    ("RESTOCKING", "Feature never built", "Your operations team still lacks the purchase order recommendation tool they requested"),
    ("TESTING", "Zero test coverage", "IT can't safely approve changes — every fix requires a risk review instead of a deploy"),
]
colors = [RGBColor(0xCC,0x00,0x00), RGBColor(0xFF,0x8C,0x00), RGBColor(0xCC,0x00,0x00)]
for i, (pill, title, body) in enumerate(cards):
    x = 0.8 + i * 4.15
    add_rect(sl, x, 2.55, 3.9, 3.8, ACC_LGRAY)
    add_rect(sl, x, 2.55, 3.9, 0.06, colors[i])
    add_textbox(sl, pill, x+0.2, 2.7, 3.5, 0.35, font_size=8, bold=True, color=colors[i])
    add_textbox(sl, title, x+0.2, 3.1, 3.5, 0.55, font_size=16, bold=True, color=ACC_BLACK)
    add_textbox(sl, body, x+0.2, 3.75, 3.5, 2.0, font_size=12, color=ACC_GRAY)

accent_chevron(sl)
slide_number(sl, 2, TOTAL)

# ── Slide 3: Root Cause ─────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_BLACK)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "ROOT CAUSE", 0.8, 0.35)
add_textbox(sl, "This is a vendor execution\nproblem — not a technology problem.",
            0.8, 0.7, 11, 2.0, font_size=36, bold=True, color=ACC_WHITE)
divider_line(sl, 0.8, 2.85, 1.2)
add_textbox(sl,
    "The underlying stack — Vue 3, FastAPI, a clean component architecture — is sound. "
    "The gaps are in delivery: unresolved defects, deferred testing, and a handoff document "
    "thin enough to suggest the previous vendor was already out the door.\n\nWe've seen this before. We know how to fix it.",
    0.8, 3.05, 10.5, 3.0, font_size=16, color=ACC_MGRAY)

accent_chevron(sl)
slide_number(sl, 3, TOTAL)

# ── Slide 4: Our Approach ───────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "OUR APPROACH", 0.8, 0.35)
add_textbox(sl, "Ground truth first. Deliver in priority order.",
            0.8, 0.7, 11, 0.9, font_size=30, bold=True, color=ACC_BLACK)
divider_line(sl, 0.8, 1.7, 1.2)

approach_cards = [
    ("WK 1–2", "Architecture Review", "Direct codebase review — not the previous vendor's notes. Accurate scoping before we commit."),
    ("BEFORE ANY CHANGE SHIPS", "Test Coverage First", "E2E browser tests in place before any fix reaches production. IT's approval gate, cleared early."),
    ("WK 3–5", "Reports Remediation", "Every logged defect resolved. Operations sign-off required before we close the item."),
    ("WK 6–10", "Restocking Feature", "PO recommendations based on stock levels, demand forecasts, and a budget ceiling your team controls."),
]
for i, (tag, title, body) in enumerate(approach_cards):
    col = i % 2
    row = i // 2
    x = 0.8 + col * 6.3
    y = 2.0 + row * 2.5
    add_rect(sl, x, y, 5.9, 2.2, ACC_LGRAY)
    add_rect(sl, x, y, 5.9, 0.06, ACC_PURPLE)
    add_textbox(sl, tag, x+0.2, y+0.18, 5.5, 0.3, font_size=8, bold=True, color=ACC_PURPLE)
    add_textbox(sl, title, x+0.2, y+0.55, 5.5, 0.5, font_size=15, bold=True, color=ACC_BLACK)
    add_textbox(sl, body, x+0.2, y+1.1, 5.5, 1.0, font_size=12, color=ACC_GRAY)

accent_chevron(sl)
slide_number(sl, 4, TOTAL)

# ── Slides 5–7: R1, R2, R3 ─────────────────────────────────────────────────────
req_slides = [
    ("R1 — REPORTS REMEDIATION", "Fix what was promised.\nBefore we move on.",
     "We audit the full issue log and resolve every defect — filter behavior, i18n gaps, data inconsistencies, and anything additional uncovered during review. We don't close this item until your operations team signs off.",
     "Any issues discovered beyond the logged eight are flagged and scoped before billing — never added silently."),
    ("R2 — RESTOCKING RECOMMENDATIONS", "The feature your team\nhas been waiting for.",
     "A new view inside the existing dashboard — no new system to learn. Surfaces purchase order recommendations based on live stock levels, demand forecasts, and an operator-supplied budget ceiling.",
     "Mockups shared with operations team before build starts. Accepted by ops before we invoice."),
    ("R3 — AUTOMATED BROWSER TESTING", "Your IT team's approval\ngate, cleared for good.",
     "End-to-end test coverage for critical user flows, in place before any change reaches production. Not a deliverable at the end — infrastructure we build at the start so every fix is covered as it lands.",
     "Tests are documented and handed off to Meridian IT. Future deploys approved by running the suite, not by risk review."),
]
for idx, (label, title, body, callout) in enumerate(req_slides):
    sl = prs.slides.add_slide(blank_layout)
    add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
    add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
    purple_bar(sl)
    add_label(sl, label, 0.8, 0.35)
    add_textbox(sl, title, 0.8, 0.7, 10, 1.6, font_size=34, bold=True, color=ACC_BLACK)
    divider_line(sl, 0.8, 2.45, 1.2)
    add_textbox(sl, body, 0.8, 2.65, 10.5, 2.2, font_size=16, color=ACC_GRAY)
    add_rect(sl, 0.8, 4.9, 10.5, 1.8, ACC_LGRAY)
    add_rect(sl, 0.8, 4.9, 0.08, 1.8, ACC_PURPLE)
    add_textbox(sl, "Our commitment", 1.1, 5.0, 9.5, 0.4, font_size=10, bold=True, color=ACC_PURPLE)
    add_textbox(sl, callout, 1.1, 5.45, 9.8, 1.1, font_size=13, color=ACC_GRAY)
    accent_chevron(sl)
    slide_number(sl, 5 + idx, TOTAL)

# ── Slide 8: Timeline ───────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_BLACK)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "TIMELINE", 0.8, 0.35)
add_textbox(sl, "Required items complete by Q3.",
            0.8, 0.7, 11, 0.8, font_size=32, bold=True, color=ACC_WHITE)
divider_line(sl, 0.8, 1.6, 1.2)

rows = [
    ("Kickoff",                "May 19",    "Engagement start, access confirmed"),
    ("Architecture complete",  "Jun 2",     "R4 delivered; test scope confirmed with IT"),
    ("Reports remediated",     "Jun 23",    "R1 complete; operations sign-off"),
    ("Tests live",             "Jul 7",     "R3 complete; IT approval gate cleared"),
    ("Restocking shipped",     "Aug 25",    "R2 complete; operations accepted"),
    ("Final delivery",         "Sep 30",    "All deliverables, documentation, handoff"),
]
add_rect(sl, 0.8, 1.9, 11.7, 0.45, RGBColor(0x28,0x00,0x5A))
add_textbox(sl, "MILESTONE",   0.9,  1.95, 4,   0.35, font_size=9, bold=True, color=ACC_MGRAY)
add_textbox(sl, "DATE",        5.4,  1.95, 2,   0.35, font_size=9, bold=True, color=ACC_MGRAY)
add_textbox(sl, "DELIVERABLE", 7.6,  1.95, 4.5, 0.35, font_size=9, bold=True, color=ACC_MGRAY)

for i, (ms, date, deliv) in enumerate(rows):
    y = 2.45 + i * 0.72
    bg = RGBColor(0x1A,0x1A,0x1A) if i % 2 == 0 else ACC_DGRAY
    add_rect(sl, 0.8, y, 11.7, 0.65, bg)
    bold = (ms == "Final delivery")
    col = ACC_PURPLE if bold else ACC_WHITE
    add_textbox(sl, ms,    0.9, y+0.12, 4.3, 0.45, font_size=13, bold=bold, color=col)
    add_textbox(sl, date,  5.4, y+0.12, 2,   0.45, font_size=13, color=ACC_MGRAY)
    add_textbox(sl, deliv, 7.6, y+0.12, 4.5, 0.45, font_size=13, color=ACC_MGRAY)

accent_chevron(sl)
slide_number(sl, 8, TOTAL)

# ── Slide 9: Pricing ────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "PRICING", 0.8, 0.35)
add_textbox(sl, "Fixed-fee where we're confident.\nNTE where we need flexibility.",
            0.8, 0.7, 11, 1.4, font_size=30, bold=True, color=ACC_BLACK)
divider_line(sl, 0.8, 2.2, 1.2)

price_rows = [
    ("Architecture Review (R4)",          "Fixed fee",  "$4,440",  False),
    ("SDLC Foundations (recommended)",    "Fixed fee",  "$3,300",  False),
    ("Reports Remediation (R1)",          "Fixed fee",  "$9,900",  False),
    ("Browser Testing (R3)",              "Fixed fee",  "$6,600",  False),
    ("Restocking Feature (R2)",           "T&M, NTE",   "$19,800", False),
    ("TOTAL (R1–R4 + SDLC)",             "",           "$44,040", True),
]
add_rect(sl, 0.8, 2.4, 11.7, 0.4, ACC_PURPLE)
add_textbox(sl, "PHASE",      0.9,  2.45, 6,   0.3, font_size=9, bold=True, color=ACC_WHITE)
add_textbox(sl, "STRUCTURE",  7.2,  2.45, 2,   0.3, font_size=9, bold=True, color=ACC_WHITE)
add_textbox(sl, "AMOUNT",     10.3, 2.45, 2,   0.3, font_size=9, bold=True, color=ACC_WHITE)

for i, (phase, struct, amt, bold) in enumerate(price_rows):
    y = 2.9 + i * 0.58
    bg = ACC_LGRAY if i % 2 == 0 else ACC_WHITE
    if bold:
        bg = RGBColor(0xF0, 0xE6, 0xFF)
    add_rect(sl, 0.8, y, 11.7, 0.52, bg)
    tc = ACC_PURPLE if bold else ACC_BLACK
    add_textbox(sl, phase,  0.9,  y+0.1, 6.1, 0.38, font_size=13, bold=bold, color=tc)
    add_textbox(sl, struct, 7.2,  y+0.1, 2.8, 0.38, font_size=13, color=ACC_GRAY)
    add_textbox(sl, amt,    10.3, y+0.1, 2,   0.38, font_size=13, bold=bold, color=ACC_PURPLE)

add_textbox(sl, "Payment tied to accepted deliverables. If a milestone slips, we absorb the catch-up cost.",
            0.8, 6.7, 11, 0.4, font_size=11, italic=True, color=ACC_GRAY)

accent_chevron(sl)
slide_number(sl, 9, TOTAL)

# ── Slide 10: Experience ────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "RELEVANT EXPERIENCE", 0.8, 0.35)
add_textbox(sl, "We've done this before — specifically.",
            0.8, 0.7, 11, 0.8, font_size=30, bold=True, color=ACC_BLACK)
divider_line(sl, 0.8, 1.6, 1.2)

exp = [
    ("R1 ANALOGUE", "Logistics dashboard remediation",
     "Inherited a Vue 3 / Python app from a departing vendor. Full remediation + E2E test suite in 12 weeks. IT approved production deployments independently within 30 days."),
    ("R2 ANALOGUE", "PO recommendation engine",
     "Built restocking recommendations into an existing ops dashboard — stock levels, lead times, budget ceiling. Adopted by operations team within the first week of deployment."),
    ("D2 ANALOGUE", "Multi-warehouse i18n rollout",
     "Extended an English-only platform to Japanese and Korean for warehouse floor staff. Tokyo team onboarding time reduced 40% post-rollout."),
]
for i, (tag, title, body) in enumerate(exp):
    x = 0.8 + i * 4.2
    add_rect(sl, x, 1.95, 3.9, 4.7, ACC_LGRAY)
    add_rect(sl, x, 1.95, 3.9, 0.06, ACC_PURPLE)
    add_textbox(sl, tag,   x+0.2, 2.1,  3.5, 0.35, font_size=8, bold=True, color=ACC_PURPLE)
    add_textbox(sl, title, x+0.2, 2.55, 3.5, 0.7,  font_size=15, bold=True, color=ACC_BLACK)
    add_textbox(sl, body,  x+0.2, 3.35, 3.5, 3.0,  font_size=12, color=ACC_GRAY)

accent_chevron(sl)
slide_number(sl, 10, TOTAL)

# ── Slide 11: Why Us ────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_BLACK)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "WHY US", 0.8, 0.35)
add_textbox(sl, "What's different this time.",
            0.8, 0.7, 11, 0.8, font_size=32, bold=True, color=ACC_WHITE)
divider_line(sl, 0.8, 1.6, 1.2)

why = [
    ("We start from the code, not the docs",
     "Architecture review in week one. Our scoping is based on what's actually in the system — not what the previous vendor said was there."),
    ("Tests before changes, not after",
     "Coverage is infrastructure, not a deliverable. Every fix is tested as it lands. IT gets the approval gate they need to move fast."),
    ("Fixed milestones, real accountability",
     "Payment tied to accepted deliverables. If we slip, we absorb catch-up costs. Meridian doesn't pay for our delays."),
    ("Operations-first, not IT-first",
     "The Restocking feature is the unlock your ops team has been waiting for. We sequence to deliver that value early."),
]
for i, (title, body) in enumerate(why):
    col = i % 2
    row = i // 2
    x = 0.8 + col * 6.3
    y = 2.0 + row * 2.4
    add_rect(sl, x, y, 5.9, 2.1, ACC_DGRAY)
    add_rect(sl, x, y, 0.06, 2.1, ACC_PURPLE)
    add_textbox(sl, title, x+0.25, y+0.2, 5.4, 0.55, font_size=14, bold=True, color=ACC_WHITE)
    add_textbox(sl, body,  x+0.25, y+0.8, 5.4, 1.1,  font_size=12, color=ACC_MGRAY)

accent_chevron(sl)
slide_number(sl, 11, TOTAL)

# ── Slide 12: SDLC ─────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_WHITE)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "ENGINEERING FOUNDATIONS", 0.8, 0.35)
add_textbox(sl, "Setting you up for whoever comes next.",
            0.8, 0.7, 11, 0.8, font_size=30, bold=True, color=ACC_BLACK)
divider_line(sl, 0.8, 1.6, 1.2)

sdlc = [
    ("CI/CD", "GitHub Actions",
     "Every PR runs the full test suite automatically. No manual 'did you test this?' — the pipeline answers that."),
    ("CODE QUALITY", "SonarQube",
     "Automatic quality and security analysis on every PR. IT gets a quality gate without reading every diff."),
    ("WORKFLOW", "Branch Protection",
     "No direct pushes to main. PRs require approval + passing CI. One hour to configure; eliminates a class of incidents."),
    ("SECURITY", "Dependabot + Staging",
     "Automated dependency security PRs within 24hrs of disclosure. Changes promoted through staging before production."),
]
for i, (tag, title, body) in enumerate(sdlc):
    col = i % 2
    row = i // 2
    x = 0.8 + col * 6.3
    y = 2.0 + row * 2.4
    add_rect(sl, x, y, 5.9, 2.1, ACC_LGRAY)
    add_rect(sl, x, y, 5.9, 0.06, ACC_PURPLE)
    add_textbox(sl, tag,   x+0.2, y+0.18, 5.5, 0.3, font_size=8, bold=True, color=ACC_PURPLE)
    add_textbox(sl, title, x+0.2, y+0.55, 5.5, 0.5, font_size=15, bold=True, color=ACC_BLACK)
    add_textbox(sl, body,  x+0.2, y+1.1,  5.5, 1.0, font_size=12, color=ACC_GRAY)

accent_chevron(sl)
slide_number(sl, 12, TOTAL)

# ── Slide 13: Close ─────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W.inches, SLIDE_H.inches, ACC_BLACK)
add_rect(sl, 0, 0, 0.5, SLIDE_H.inches, ACC_PURPLE)
purple_bar(sl)

add_label(sl, "NEXT STEPS", 0.8, 0.35)
add_textbox(sl, "Let's get your\ndashboard working.",
            0.8, 0.9, 11, 2.2, font_size=48, bold=True, color=ACC_WHITE)
divider_line(sl, 0.8, 3.3, 1.2)
add_textbox(sl, "Questions to procurement@meridiancomponents.example by April 28.",
            0.8, 3.6, 11, 0.5, font_size=16, color=ACC_MGRAY)
add_textbox(sl, "Engagement start: May 19    ·    Final delivery: September 30",
            0.8, 4.2, 11, 0.5, font_size=16, color=ACC_MGRAY)
add_textbox(sl, "RFP #MC-2026-0417",
            0.8, 6.5, 6, 0.4, font_size=11, color=ACC_GRAY)
accent_chevron(sl)
slide_number(sl, 13, TOTAL)

out = "/Users/krzysztof.najda/projects/claude-training/meridian-workshop/proposal/capabilities-deck.pptx"
prs.save(out)
print(f"Saved: {out}")
