# SDLC Improvements & Engineering Foundations

**RFP #MC-2026-0417 — Meridian Components Inventory Dashboard Modernization**
**Date:** April 28, 2026

---

## Overview

Beyond the four required deliverables, we recommend establishing the engineering foundations that make future changes safe, fast, and auditable. These are industry-standard practices for any team that expects to maintain a production web application beyond a single vendor engagement. We include them because the previous vendor's exit left Meridian with no safety net — we want to make sure that doesn't happen again, regardless of who does the next piece of work.

---

## Recommended Improvements

### CI/CD Pipeline — GitHub Actions

Automate build, test, and deployment on every pull request and merge to main. Every code change runs the browser test suite (R3) automatically before it can be merged. No manual "did you test this?" — the pipeline answers that question.

**Why GitHub Actions:** Native to GitHub, zero additional infrastructure, free tier covers Meridian's usage volume. Industry standard for teams of this size.

### Static Code Analysis — SonarQube

Integrate SonarQube (Cloud free tier) into the CI pipeline to catch code quality issues, security hotspots, and technical debt automatically on every PR. Gives Meridian IT a quality gate they can enforce without reviewing every diff manually.

**What it catches:** Duplicated code, security vulnerabilities (OWASP top 10), test coverage gaps, maintainability issues. Produces a dashboard your IT team can review without reading source code.

### Branch Protection & PR Workflow

Enforce a standard pull request workflow:
- No direct pushes to `main`
- PRs require at least one approval
- CI checks (tests + SonarQube) must pass before merge
- Squash merges keep history clean

This is a configuration change, not a build — takes under an hour and eliminates an entire class of "who pushed what to main" incidents.

### Dependency Management — Dependabot

Enable GitHub Dependabot to automatically open PRs for dependency updates (npm, Python pip). Security patches surface within 24 hours of disclosure rather than being discovered during an audit.

### Environment Promotion

Establish two environments: **staging** (auto-deployed from `main`) and **production** (manually promoted). Your IT team approves the production deploy; the pipeline does the rest. Currently there is no staging environment — changes go directly to production with no safety net.

---

## What This Unlocks

| Without | With |
|---|---|
| Manual testing before every change | Automated test suite runs on every PR |
| IT risk review per deployment | IT approves once (pipeline config); deploys self-service after |
| Security issues found in audits | SonarQube flags them before merge |
| Dependency vulnerabilities discovered late | Dependabot PRs within 24hrs of disclosure |
| No visibility into code quality over time | SonarQube dashboard — trends visible to IT |

---

## Effort & Timing

SDLC setup runs in parallel with Phase 1 (architecture review) — most of it is configuration, not code. We estimate 16–20 hours total. We recommend including it in the engagement rather than deferring it; the test suite (R3) is significantly more valuable when it runs automatically on every change.

*This work is included in our revised pricing as an optional Phase 1b add-on. See updated pricing section.*
