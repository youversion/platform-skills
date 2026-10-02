---
name: youversion-platform-react
description: "YouVersion Bible: for React, to get Bible text, html, and information. Sample code for visual components: BibleTextView, BibleCard, and BibleReader"
---

# YouVersion Platform React SDK - for React applications

## Default workflow

1. Determine whether the user wants **UI components**, **hooks**, or **direct core API** usage in React.
2. If the user is not yet in a React app, briefly provide the minimal scaffold from `references/react-scaffold.md`, then continue with a concrete SDK example.
3. Confirm the app key source. Default to `process.env`-based usage (for example `import.meta.env.VITE_YVP_APP_KEY` in Vite); if a key is not present then ask the user for one - it can be obtained at https://platform.youversion.com
4. Wrap the React tree with `YouVersionProvider` using `appKey`.
5. For simple scripture rendering, prefer `BibleCard` (`@youversion/platform-react-ui`) unless the user asks for a custom UI. That shows the verse location, copyright, etc.
6. Use `BibleTextView` to display the scripture text "bare bones" with no extra UI elements.
7. Use `BibleReader` to display a fully featured Bible UX, including pickers for the user to navigate in the Bible, change Bible versions, etc.
8. For custom rendering/state, use hooks (for example `usePassage`) from `@youversion/platform-react-hooks`.
9. If the user needs lower-level calls (e.g., listing versions), use `@youversion/platform-core` (typically from server code, route handlers, or controlled client-side flows).
10. For custom styled HTML from core, prefer `getPassageDisplay` and apply its stylesheets, container attributes, and current attribution. For `usePassage` HTML, add the Bible CSS and font resources and scoped container from the [HTML display guide](https://developers.youversion.com/guides/display-bible-html), and fetch attribution with `useVersion`. Render attribution as text.

## Component documentation to consult

- Read `component_documentation/youversion-provider.md` when the user needs provider setup, auth configuration, or the exact conditional prop shape for `YouVersionProvider`.
- Read `component_documentation/bible-card.md` when the user wants the pre-styled passage card called `BibleCard`, a quick example, or its props. This is a excellent, simple, and attractive way to display standalone bible text.
- Read `component_documentation/bible-text-view.md` when the user wants bare scripture rendering, typography-related props, or the attribution/copyright note for `BibleTextView`.
- Read `component_documentation/bible-reader.md` when the user wants a full Bible reading component, adjustments for it using `BibleReader.Root` and `BibleReader.Toolbar` props, or controlled vs uncontrolled examples.
- Read `component_documentation/verse-of-the-day.md` when the user wants the Verse of the Day widget, its basic example, or its props.

These files contain component-specific documentation distilled into three parts: what the widget is, a basic code example, and the props/types to reference while answering.

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

This example includes both stylesheets from the [HTML display guide](https://developers.youversion.com/guides/display-bible-html); React 19 places stylesheet links with `precedence` in the document head. It fetches attribution for the same version as the passage. For plain text, use `format: "text"` and render `passage.content` normally.

```tsx
import { YouVersionProvider, usePassage, useVersion } from '@youversion/platform-react-hooks';

function BibleVerse() {
  const versionId = 3034;
  const { passage, loading, error } = usePassage({ versionId, usfm: 'JHN.3.16', format: 'html' });
  const { version, loading: versionLoading, error: versionError } = useVersion(versionId);

  if (loading || versionLoading) return <div>Loading...</div>;
  if (error || versionError) return <div>Could not load passage.</div>;
  const attribution = version?.copyright?.trim() || version?.promotional_content?.trim();
  if (!passage || !version || !attribution) return <div>Unable to display scripture with attribution.</div>;

  return (
    <article>
      <h2>{passage.reference} ({version.localized_abbreviation || version.abbreviation})</h2>
      <div data-yv-sdk="" data-slot="yv-bible-renderer" dangerouslySetInnerHTML={{ __html: passage.content }} />
      <p>{attribution}</p>
    </article>
  );
}

export function App() {
  const appKey = import.meta.env.VITE_YVP_APP_KEY;
  return (
    <>
      <link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" precedence="youversion" />
      <link
        rel="stylesheet"
        href={`https://api.youversion.com/v1/fonts/1/stylesheet?app_key=${encodeURIComponent(appKey)}`}
        precedence="youversion"
      />
      <YouVersionProvider appKey={appKey}>
        <BibleVerse />
      </YouVersionProvider>
    </>
  );
}
```

## Default core API example (React-adjacent)

```ts
import { ApiClient, BibleClient } from '@youversion/platform-core';

const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY! });
const bibleClient = new BibleClient(apiClient);

const display = await bibleClient.getPassageDisplay({ versionId: 3034, passageId: 'JHN.3.16' });
```

Use the client in the project's browser or server runtime; server-side HTML transformation needs `jsdom`. For styled display, render `display.html` with its `containerAttributes`, add `display.stylesheets` to the document head, and render `display.attribution.text` normally. Prefer ready-made components when custom HTML is unnecessary.

## Gotchas

- Always ensure `YouVersionProvider` wraps components/hooks that rely on SDK context.
- `YouVersionProvider` is implemented in @youversion/platform-react-hooks and re-exported by @youversion/platform-react-ui. Import from whichever is convenient.
- Render HTML as HTML only when requested as HTML; plain-text content and attribution must be rendered as text.
- Custom layouts, including `BibleTextView`, must display the selected version's required attribution. Use `copyright` with `promotional_content` as a fallback; report missing attribution instead of omitting it.
- `appKey` is not a secret; it can be used client-side.
- Some Bible versions require explicit license acceptance on platform.youversion.com.
- For public-domain English demos, default to `3034` (Berean Standard Bible).

## Common customizations

- You can restrict the Bible catalog by language or version, or exclude versions, using provider configuration. See [version filters](https://developers.youversion.com/sdks/react/components#limit-which-bible-versions-the-sdk-uses).
- You can set UI locale/direction independently of scripture direction, and choose light, dark, or system theme. See [components](https://developers.youversion.com/sdks/react/components) and [theming](https://developers.youversion.com/sdks/react/guides/theming).
- For a custom reader layout or verse-selection handling, use the SDK's pickers and `BibleReader.Root.onVerseSelect` as needed. For card sizing, use `BibleCard.maxWidth`. See [component documentation](https://developers.youversion.com/sdks/react/components) for current props rather than inventing them.

## References to load on demand

- Read `references/react-scaffold.md` when user needs a React project setup baseline.
- Read files in `component_documentation/` when the user asks for component-specific usage, examples, or prop details for `YouVersionProvider`, `BibleCard`, `BibleTextView`, `BibleReader`, or `VerseOfTheDay`.

## Self-check before answering

- [ ] Chose the right package path (UI vs hooks vs core).
- [ ] Know the app key to use, or have asked for one before proceeding.
- [ ] Wrapped usage in `YouVersionProvider` with an app key.
- [ ] Included a concrete scripture example (`reference` or `usfm`).
- [ ] Included loading/error handling for hook examples.
- [ ] Applied stylesheets and container attributes for custom HTML and displayed required attribution.
- [ ] Mentioned version/licensing considerations when relevant.
