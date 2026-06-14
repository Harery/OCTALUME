# Stage 9 — Mermaid Visual Diagrams
Layer: Atomic | Output: docs/diagrams.md
⚠ No new questions at this layer. Diagrams are derived from approved stages 1–8.

## Execute on load

Derive all diagrams entirely from prior stage outputs:
- docs/product-spec.md (S1)
- docs/BRD.md (S2)
- docs/MVP.md (S3)
- docs/tech-stack.md (S6)
- docs/technical-analyst-plan.md (S6)
- docs/logic.md (S8)

Each Mermaid block MUST render without error.
Test mentally: no undefined node references, no unclosed brackets, valid syntax.
Scope: MVP only. No diagrams for deferred features.

## Output — docs/diagrams.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIAGRAMS
docs/diagrams.md
[Derived from approved stages 1–8]
[Scope: MVP only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. System architecture
```mermaid
[Architecture diagram — stack components + connections + data flow]
```

## 2. Site architecture / URL map
```mermaid
[Sitemap diagram — all public-facing pages + crawl paths for SEO]
```

## 3. Core user flow (happy path)
```mermaid
[Flowchart — entry point to success state for the core loop]
```

## 4. Data entity relationships
```mermaid
[ERD — MVP entities only]
```

## 5. Auth flow
```mermaid
[Sequence diagram — signup / login / session / logout]
```

## 6. Deployment pipeline
```mermaid
[CI/CD flow — commit → test → build → deploy on Ubuntu]
```

## 7. State machine (if applicable)
```mermaid
[State diagram — for the primary stateful entity in the product]
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Gate → `stages/s10-build.md`
