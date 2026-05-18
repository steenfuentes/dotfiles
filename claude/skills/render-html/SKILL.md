---
name: render-html
description: Deliver output as a self-contained HTML file opened in the browser. Two modes — author a rich interactive HTML artifact (specs, code reviews, design prototypes, reports, throwaway editors) when the content benefits from diagrams/interaction/navigation, or fast-render prose/reports through a deterministic styled template. Use when the user asks to see output, a report, a plan, a review, a design, or an answer as HTML / as a web page / in the browser, or requests HTML-structured output.
compatibility: Requires python3. Optionally uses the `markdown` PyPI package in document mode; falls back to a built-in converter when absent.
allowed-tools: Bash(python3 *) Write Read Glob Grep
argument-hint: [title]
---

# render-html

HTML is worth its higher generation cost only when the output uses what HTML can do that Markdown cannot: tables, SVG diagrams, CSS structure, navigation, interaction, and a round-trip back into the agent. A styled prose dump does not justify the cost. Choose the mode deliberately.

## Mode selection (decide first)

Do not classify by surface form ("is this prose or a spec"). Decide by a value/cost test: would an abstraction, worked example, figure, comparison, or interactive control let the response carry information that prose carries less efficiently — structure, sequence, magnitude, spatial layout, side-by-side tradeoffs, tunable parameters? If yes, that expression earns its cost and belongs in the response. The whole reason to use HTML is to stop suppressing the visual and worked-example thinking the model would otherwise flatten into prose or fake with ASCII. An explanatory answer that benefits from a figure is the central case, not an exception.

**Artifact mode** — the model authors a bespoke, self-contained HTML file directly. This is the home for any response where richness pays for itself: not only specs, reviews, prototypes, reports, and editors, but also a conceptual explanation that wants an SVG abstraction, a comparison that wants a table or grid, or an answer that lands better with a worked example beside the prose. Reach for it whenever a figure/example/interaction increases understanding per unit cost.

**Document mode** — the deterministic renderer over Markdown. The narrow case: genuinely linear prose where no figure, example, or structure would add understanding — a written answer, a narrative summary, notes. Its value is consistent styling, a navigable long-form read, and shareability.

Two guardrails keep this from inverting into reflexive over-formatting: (1) do not scaffold a short or trivial answer — a three-sentence answer stays three sentences in chat, not an HTML file; (2) a visual that only restates the prose is negative value — include one only when it carries what the prose cannot carry as efficiently. The bar is informational, not decorative.

When unsure whether a figure would help: it usually would. Default to artifact mode for explanatory or structural work; reserve document mode for plain exposition; never strip a useful figure out of a response because it "reads like prose."

## Context first

Before generating, pull real context — this is the agent's edge over a generic HTML generator. Read the relevant files (Glob/Grep/Read), git history, and any connected MCP data the task references. Ground the artifact in actual code, data, and history, not assumptions.

## Artifact mode

Author one self-contained `.html` file. No external network requests, no CDN, inline CSS/JS/SVG. Then place and open it via the renderer in pass-through (step 3); the renderer does not modify authored HTML.

Standing requirements:

- **SVG for all diagrams, flowcharts, and spatial/visual structure.** Never ASCII art, never unicode blocks to approximate color.
- **Navigable when long.** Past ~100 lines of content, add tabs or a sticky section nav; do not emit a wall of text.
- **Mobile responsive.** Usable at narrow widths.
- **Export affordance is mandatory for any interactive or decision-shaping artifact.** End with a visible button that turns the user's work back into something pasteable into the agent: "Copy as prompt", "Copy as JSON", "Copy as Markdown", or "Copy diff" — whichever fits. This closes the two-way loop; an interactive artifact without it is incomplete.
- **Style reference.** If a design-system HTML file is provided via `--style-ref PATH` or exists at `.claude/design-system.html`, read it and match its tokens (color, type, spacing). Otherwise apply the `frontend-design` skill's conventions; do not produce default-AI styling.

Use-case patterns (illustrative, not a closed list — the test above governs):

- **Explanatory answer with a figure** — a conceptual question answered in prose, with an SVG abstraction of the mechanism, a worked example traced step by step, or a small comparison table where it sharpens the point. This is a primary case, not a lesser one.
- **Spec / planning / exploration** — when exploring, lay multiple distinct options in one file (grid), each labeled with its tradeoff. For an implementation plan: mockups, a data-flow SVG, and the key code snippets inline, optimized for one-pass reading.
- **Code review / understanding** — render the actual diff with inline margin annotations; color-code findings by severity; add flowcharts/module maps. Targeted at the reviewer's stated unfamiliarity.
- **Design / prototype** — interactive controls (sliders, knobs, toggles) to tune the thing live; a copy-parameters button exporting the settings that worked.
- **Report / research / learning** — long-form doc, interactive explainer, or slideshow; SVG for every diagram; structure for a single read by a non-author (leadership, teammates).
- **Custom editor** — a throwaway, single-purpose UI for the one piece of data in play (draggable triage columns, constrained config form with dependency warnings, side-by-side template editor with live preview). Always ends with the export button.

## Document mode

1. Compose the answer as Markdown.
2. Write it to `response.md` in the working directory.
3. Render (see Procedure).

The renderer adds, deterministically: a sticky section TOC with anchored deep links, reading-time, a print stylesheet, and an injected toolbar ("Copy as Markdown" / "Copy page" / Print) that operationalizes the export loop for prose. Do not hand-add these.

## Procedure

Artifact mode:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py path/to/authored.html --title "$ARGUMENTS"
```

The renderer detects a complete HTML/SVG document and passes it through unmodified, writes it to the working directory, and opens it. It never injects TOC/toolbar into authored artifacts.

Document mode:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py response.md --title "$ARGUMENTS"
```

Optional flags: `--style-ref PATH` (record a design-system reference path in output metadata), `--no-open` (headless/CI), `--no-toc`, `--no-toolbar`. Omit `--title` to derive it from the first heading. Report the absolute path printed; for a shareable link the user can upload the file to static hosting (e.g. S3) themselves — do not upload on their behalf.

## Tradeoffs (apply the value/cost test knowing these)

- HTML generation is ~2–4x slower than Markdown. The latency is the cost side of the test, not a reason to suppress a figure that genuinely earns it.
- HTML diffs are noisy and hard to review in version control. For artifacts that live in a repo and change often, prefer Markdown or keep the HTML as a generated, git-ignored view.
- The real failure modes are at both ends: stripping a useful abstraction out of an explanation because it "looks like prose", and scaffolding a trivial answer that should have been three sentences. The value/cost test, not a content category, is what separates them.

## Constraints

- Self-contained: inline everything, zero network requests.
- Write only inside the working directory.
- Do not open the browser when `--no-open` is set.

## Resources

- `scripts/render.py` — pass-through detector, Markdown converter (stdlib fallback), TOC/toolbar/print injection for document mode. No install required.
