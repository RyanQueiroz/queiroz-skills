---
name: frontend
description: Build user-facing UI that is accessible, responsive, and follows the project's design system. Use when a ticket creates or changes a page, component, layout, form, or any visible interface state.
---

# Frontend

Build UI that looks like a design-aware engineer on this team wrote it: the project's own components and tokens, every state handled, usable by keyboard and screen reader, solid from phone to desktop.

## 1. Learn the house style

Before writing a component, read what exists:

- The component library and primitives the repo already uses (shadcn, a local `components/ui`, MUI). Reuse them; add a new primitive only when none fits.
- Design tokens: colors, spacing scale, radii, type scale, in Tailwind config, CSS variables, or a theme file.
- Two or three existing screens close to the one you are building: layout, density, how they show loading and errors.
- How the app manages state and fetches data (React Query, SWR, server components, a store).

**Done when** you can name the component source, the token source, and the reference screen your work will match.

## 2. Build

**Components.** Compose small components instead of one with many config props. Keep data fetching apart from presentation: a container loads, a view renders. Split a component past roughly 200 lines. Follow the repo's file layout.

**State.** Take the simplest rung that works: local state, then lifted state, then URL state for filters and pagination, then the repo's server-state library for remote data, then context for read-heavy app-wide values. A global store only when the repo already uses one for this kind of state. Props drilled past three levels mean the tree needs restructuring.

**Design system.** Use semantic tokens (`text-muted`, `bg-surface`), never raw hex or off-scale values like `13px`. One `h1` per page; no skipped heading levels. Real content in mocks and seeds, so wrapping and overflow show up.

**The AI look.** Match the project's palette and density. These are the tells to replace with the design system's values: purple or indigo defaults, gradients the design system does not use, `rounded-2xl` on everything, generic hero sections, uniform card grids that ignore priority, oversized padding, heavy shadows.

**Every state.** Loading (skeleton for content), empty (says what to do next), error (says what failed and offers a retry), success, and no permission when it applies. A blank screen is a bug.

**Accessibility (WCAG 2.1 AA).**

- Actions are `<button>`, navigation is `<a>`. A clickable `div` is a bug.
- Every input has a visible label; icon-only buttons have `aria-label`.
- Every interactive element works by keyboard, with a visible focus ring. Dialogs move focus in, trap it, and return it on close.
- Text contrast at least 4.5:1 (3:1 for large text). Color is never the only signal: pair it with text or an icon.
- Dynamic updates that matter are announced (`aria-live`, `role="status"`).
- Form errors name the field and the fix, and sit next to the field.
- Touch targets at least 44x44 px on mobile.

**Responsive.** Mobile first, then widen. Check 320, 768, 1024, and 1440 px.

**Copy.** UI strings follow the product's language and tone. For a Portuguese product, write natural PT-BR with correct accents.

**Done when** the code covers every state the ticket's screen can reach.

## 3. Prove it

Drive the screen through the project's `verify` skill, the way a user would:

- Screenshot the screen at 320 and 1440 px, and in each state you can trigger (empty, loading, error, filled).
- Tab through the screen and confirm the focus order and that every control responds to Enter or Space.
- Read the browser console: no errors or React warnings from your code.
- If the repo has axe, Playwright accessibility checks, or Storybook tests, run them.

Keep the screenshots with the `verify` evidence.

**Done when** each bullet has a screenshot, a console log, or a command output as proof.
