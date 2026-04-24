# Technical Approach

**RFP #MC-2026-0417 — Meridian Components Inventory Dashboard Modernization**
**Date:** April 28, 2026

---

## Approach Overview

We will work directly in the existing Vue 3 / FastAPI codebase rather than proposing a rewrite. The system's architecture is sound; the gaps are in execution. Our approach is to establish ground truth first, then deliver requirements in Meridian's stated priority order.

---

## R4 — Architecture Review (Week 1)

We begin with a direct review of the codebase — not a retread of the previous vendor's handoff notes. We will produce a current-state architecture document suitable for handoff to Meridian IT, covering component structure, API contracts, data flow, and known technical debt. This review informs accurate scoping for everything that follows.

*Assumption: Meridian will provide repository access at engagement start.*

---

## R3 — Automated Browser Testing (established before R1 changes reach production)

Before any code changes are approved, we will establish end-to-end browser test coverage for critical user flows: inventory browsing and filtering, order management, spending summary, and the new Restocking view once built. Tests run against the live application and will be documented so Meridian IT can maintain and extend them.

*Assumption: Critical flows to be confirmed with Meridian IT at kickoff. Our proposed default scope is listed above.*

---

## R1 — Reports Module Remediation (Weeks 2–4)

We will audit the Reports module against the full issue log and resolve all defects — filter behavior, internationalization gaps, and data pattern inconsistencies among them. We will not close this item until Meridian's operations team has reviewed and signed off. Any issues discovered during audit beyond the logged eight will be flagged before remediation, not billed without discussion.

*Assumption: Meridian will share the full issue log at engagement start. If unavailable, we will audit from scratch and align on scope within the first week.*

---

## R2 — Restocking Recommendations (Weeks 4–8)

We will build a new Restocking view within the existing dashboard. The view will surface purchase order recommendations based on current stock levels, demand forecasts, and an operator-supplied budget ceiling. Design will follow the existing visual language (vendor discretion per Q3 response); we will share mockups for operations team review before building.

*Assumption: Stock, demand, and budget data is available via existing APIs or JSON data files. Any data gaps will be surfaced during architecture review.*

---

## Desired Items (D1–D3)

UI modernization (D1), extended i18n (D2), and dark mode (D3) will be scoped and scheduled based on progress against the Q3 milestone. We will provide an updated view of remaining capacity at the R2 delivery checkpoint. None of these items will be started at the expense of R1–R4 delivery.

---

## SDLC Foundations (recommended addition)

In parallel with Phase 1, we recommend establishing the engineering infrastructure that makes every subsequent change — by us or any future vendor — safer and faster: CI/CD via GitHub Actions, static analysis via SonarQube, branch protection, automated dependency management via Dependabot, and a staging environment. Full rationale and effort estimate in `06-sdlc-improvements.md`. We recommend including this work; the browser test suite (R3) is significantly more valuable when it runs automatically on every PR.
