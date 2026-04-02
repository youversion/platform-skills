---
name: youversion-platform-react
description: "YouVersion Bible: for React, to get Bible text, html, and information. Sample code for visual components: BibleTextView, BibleCard, and BibleReader"
---

# YouVersion Platform React SDK - for React applications

## Default workflow

1. Determine whether the user wants **UI components**, **hooks**, or **direct core API** usage in React.
2. If the user is not yet in a React app, briefly provide the minimal scaffold from `references/react-scaffold.md`, then continue with a concrete SDK example.
3. Confirm the app key source. Default to `process.env`-based usage (for example `import.meta.env.VITE_YVP_APP_KEY` in Vite), and mention registration at https://platform.youversion.com.
4. Wrap the React tree with `YouVersionProvider` using `appKey`.
5. For simple scripture rendering, prefer `BibleCard` (`@youversion/platform-react-ui`) unless the user asks for a custom UI. That shows the verse location, copyright, etc.
6. Use `BibleTextView` to display the scripture text "bare bones" with no extra UI elements.
7. Use `BibleReader` to display a fully featured Bible UX, including pickers for the user to navigate in the Bible, change Bible versions, etc.
8. For custom rendering/state, use hooks (for example `usePassage`) from `@youversion/platform-react-hooks`.
9. If the user needs lower-level calls (e.g., listing versions), use `@youversion/platform-core` (typically from server code, route handlers, or controlled client-side flows).
10. When displaying passage HTML from hooks/core manually, include the Bible CSS include:

```html
<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />
```

## Response style

- Give a direct answer first.
- Provide one runnable React-focused example per response path.
- Prefer TypeScript + TSX examples unless user requests plain JS.
- Keep examples practical: provider setup, one component/hook call, minimal error/loading handling.
- Use version `3034` for public-domain English defaults unless user asks for another version.

## Package selection guide

- `@youversion/platform-react-ui`: fastest path with ready-made components: `BibleTextView`, `BibleCard`, `BibleReader`, and `VerseOfTheDay`.
- `@youversion/platform-react-hooks`: custom rendering/state control while still using SDK-managed data hooks.
- `@youversion/platform-core`: direct API client (`ApiClient`, `BibleClient`) for advanced queries and version discovery.

## Default installation

Recommend one of these, depending on user goal:

```bash
pnpm add @youversion/platform-react-ui
```

```bash
pnpm add @youversion/platform-react-hooks
```

```bash
pnpm add @youversion/platform-core
```

## Default UI component example

```tsx
import { YouVersionProvider, BibleCard } from '@youversion/platform-react-ui';

export function App() {
  return (
    <YouVersionProvider appKey={import.meta.env.VITE_YVP_APP_KEY}>
      <BibleCard versionId={3034} reference="JHN.1.1-3" />
    </YouVersionProvider>
  );
}
```

## Default Verse of the Day example

```tsx
import { YouVersionProvider, VerseOfTheDay } from '@youversion/platform-react-ui';

export function App() {
  return (
    <YouVersionProvider appKey={import.meta.env.VITE_YVP_APP_KEY}>
      <VerseOfTheDay versionId={3034} />
    </YouVersionProvider>
  );
}
```

## Default hooks example

```tsx
import { YouVersionProvider, usePassage } from '@youversion/platform-react-hooks';

function BibleVerse() {
  const { passage, loading, error } = usePassage({ versionId: 3034, usfm: 'JHN.3.16' });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Could not load passage.</div>;

  return <div dangerouslySetInnerHTML={{ __html: passage?.content || '' }} />;
}

export function App() {
  return (
    <YouVersionProvider appKey={import.meta.env.VITE_YVP_APP_KEY}>
      <BibleVerse />
    </YouVersionProvider>
  );
}
```

## Default core API example (React-adjacent)

```ts
import { ApiClient, BibleClient } from '@youversion/platform-core';

const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY! });
const bibleClient = new BibleClient(apiClient);

const versions = await bibleClient.getVersions('en');
const passage = await bibleClient.getPassage(versions.data[0].id, 'JHN.3.16');
```

Explain that this is best used in backend/server contexts (or carefully controlled client usage), then passed into React UI.

## Gotchas

- Always ensure `YouVersionProvider` wraps components/hooks that rely on SDK context.
- `YouVersionProvider` is implemented in @youversion/platform-react-hooks and re-exported by @youversion/platform-react-ui. Import from whichever is convenient.
- If manually rendering `passage.content`, do not escape it; it is HTML payload meant for rendering.
- Include attribution/version metadata when rendering scripture text in custom layouts.
- `appKey` is not a secret; it can be used client-side.
- Some Bible versions require explicit license acceptance on platform.youversion.com.
- For public-domain English demos, default to `3034` (Berean Standard Bible).

## References to load on demand

- Read `references/react-scaffold.md` when user needs a React project setup baseline.

## Self-check before answering

- [ ] Chose the right package path (UI vs hooks vs core).
- [ ] Wrapped usage in `YouVersionProvider` with an app key.
- [ ] Included a concrete scripture example (`reference` or `usfm`).
- [ ] Included loading/error handling for hook examples.
- [ ] Added Bible CSS include when manually rendering passage HTML.
- [ ] Mentioned version/licensing considerations when relevant.
