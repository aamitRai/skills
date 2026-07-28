# Frontend Coding Standards — gigcx-ai-interview-frontend

## 1. File Separation Rules

**Never mix concerns in one file.** Each of these lives in its own file, always:

| Concern | Rule |
|---|---|
| Component JSX | `ComponentName.tsx` |
| Component styles (if not Tailwind-only) | `ComponentName.module.css` (co-located, same folder) |
| Types/PropTypes | Inline or `ComponentName.types.ts` if complex |
| Hooks used by one component only | Co-locate as `useComponentName.ts` in same folder |
| Hooks reused across features | `src/hooks/useThing.ts` |
| API calls | `src/api/*.api.ts` — components never call `axios`/`fetch` directly |
| Constants/enums | `src/constants/*.ts` — no magic strings/numbers in components |
| Validation schemas | `src/lib/validators.ts` or `ComponentName.schema.ts` |

**Example structure for a non-trivial component:**
```
components/interview/InterviewCard/
├── InterviewCard.tsx
├── InterviewCard.module.css   (only if Tailwind utilities aren't enough)
├── useInterviewCard.ts         (local hook, if logic is non-trivial)
└── index.ts                     (barrel: export { default } from "./InterviewCard")
```

Simple components (no local hook/css) stay as a single file: `components/ui/Button.tsx`.

---

## 2. CSS Rules

- **Tailwind utility classes** are the default for layout/spacing/color. Don't write custom CSS for things Tailwind already does.
- If a component needs styles Tailwind can't express cleanly (complex keyframes, third-party overrides), create a **CSS module**: `ComponentName.module.css`, imported as:
  ```jsx
  import styles from "./InterviewCard.module.css";
  ```
- **Never use inline `style={{}}`** except for truly dynamic runtime values (e.g. a computed progress-bar width).
- Global styles ONLY in `src/index.css` — Tailwind directives, CSS custom properties (`@theme` in v4), and base resets. No component-specific rules there.
- Don't use plain `.css` files scoped to a component without `.module.css` — it leaks globally and causes collisions.

---

## 3. Import Order

Every file follows this exact grouping, separated by a blank line, alphabetized within each group:

```jsx
// 1. React / framework core
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// 2. Third-party libraries
import { zodResolver } from "@hookform/resolvers/zod";
import clsx from "clsx";
import { useForm } from "react-hook-form";

// 3. Internal absolute imports (alias-based) — api, hooks, contexts, lib
import { loginUser } from "@/api/auth.api";
import { useAuth } from "@/hooks/useAuth";
import { cn } from "@/lib/utils";

// 4. Internal components
import Button from "@/components/ui/Button";
import PageLayout from "@/components/layout/PageLayout";

// 5. Local/relative imports (same feature folder)
import InterviewTimer from "./InterviewTimer";

// 6. Styles (always last)
import styles from "./LoginPage.module.css";
```

**Rules:**
- No relative-path spaghetti (`../../../lib/utils`) — configure a `@/` alias in `vite.config.ts` and `jsconfig.tson`/`tsconfig.tson`, use it for everything outside the current folder.
- One import per line; no wildcard imports (`import * as X`) unless a library requires it (e.g. sometimes needed for icon sets).
- Type-only imports (if TS is added later) get their own line with `import type`.

**vite.config.ts alias setup:**
```js
import { resolve } from "path";

export default {
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
    },
  },
};
```

---

## 4. Component Standards

- **One component per file**, matching filename (`Button.tsx` exports `Button`).
- **Function components only**, no class components.
- **Named exports for utilities/hooks, default export for the component itself.**
- Props destructured in the function signature, not accessed via `props.x`:
  ```jsx
  // Good
  function Button({ variant = "primary", children, onClick }) { ... }

  // Avoid
  function Button(props) { return <button onClick={props.onClick}>...} }
  ```
- Order within a component file:
  1. imports
  2. constants local to the file (e.g. `const VARIANTS = {...}`)
  3. the component function
  4. helper functions used only by that component (below the component, or extracted to a hook if stateful)
  5. `export default`

---

## 5. Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Component files | PascalCase | `InterviewCard.tsx` |
| Component folders | PascalCase | `InterviewCard/` |
| Hooks | camelCase, `use` prefix | `useInterviewTimer.ts` |
| Utility/lib files | camelCase | `formatDate.ts` |
| Constants files | camelCase | `roles.ts` |
| API files | `domain.api.ts` | `interview.api.ts` |
| CSS modules | match component | `InterviewCard.module.css` |
| Context files | PascalCase + `Context` | `AuthContext.tsx` |
| Boolean vars/props | `is`/`has`/`should` prefix | `isLoading`, `hasError` |
| Event handlers | `handle` prefix (internal), `on` prefix (prop) | `handleSubmit`, `onSubmit` |

---

## 6. API Layer Standards

- One `axiosClient.ts` with base URL, interceptors (auth token injection, 401 redirect, error normalization).
- API functions return data only, never the full axios response:
  ```js
  // api/interview.api.ts
  export async function getInterviewById(id) {
    const { data } = await axiosClient.get(`/interviews/${id}`);
    return data;
  }
  ```
- Components/hooks call these functions — never `axios.get(...)` inline in a component.

---

## 7. State & Data Fetching

- Local UI state → `useState`.
- Cross-cutting state (auth, theme) → Context, one per concern, not one giant `AppContext`.
- Server data fetching → co-located custom hook (`useInterview.ts`) wrapping the API call + loading/error state, so components stay declarative:
  ```jsx
  const { data, isLoading, error } = useInterview(interviewId);
  ```
- If the app grows, consider React Query/TanStack Query for caching instead of hand-rolled fetch hooks — flag this as a future upgrade, don't hand-roll caching logic.

---

## 8. Forms (react-hook-form)

- Always destructure `register`, `handleSubmit`, `formState: { errors }` explicitly — no `...rest` spreading unless necessary.
- Validation schema lives outside the component in `lib/validators.ts` or co-located `*.schema.ts`.
- Error messages rendered via a shared `<FormError />` component, not repeated JSX per field.

---

## 9. Linting & Formatting (enforce, don't rely on convention alone)

Add to `devDependencies` and enforce in CI/pre-commit:
```json
"eslint": "^8.x",
"eslint-plugin-react": "^7.x",
"eslint-plugin-react-hooks": "^4.x",
"eslint-plugin-import": "^2.x",
"prettier": "^3.x",
"eslint-config-prettier": "^9.x"
```

Key `.eslintrc` rules to turn on:
- `import/order` — enforces the import grouping in section 3 automatically.
- `react-hooks/exhaustive-deps` — catches missing dependency arrays.
- `no-unused-vars`, `no-console` (warn, allow in dev only).

`.prettierrc` baseline:
```json
{
  "semi": true,
  "singleQuote": false,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

---

## 10. Quick Checklist Before Committing

- [ ] No inline styles unless truly dynamic
- [ ] No direct `axios`/`fetch` calls inside components
- [ ] No magic strings — pulled from `constants/`
- [ ] Imports grouped and ordered correctly
- [ ] Component does one thing; logic >30 lines extracted to a hook
- [ ] No relative `../../../` imports — use `@/` alias
- [ ] File name matches default export name