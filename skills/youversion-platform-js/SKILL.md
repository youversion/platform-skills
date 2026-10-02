---
name: youversion-platform-js
description: YouVersion JavaScript and TypeScript SDK usage with `@youversion/platform-core`. Use for browser, Node.js, or serverless SDK examples, Bible discovery, passage text, or display-ready Bible HTML. For React UI, use the React skill; for raw HTTP, use the API skill.
---

# YouVersion Platform JS

Use this skill for JavaScript or TypeScript SDK answers.

## Use This Skill When

- The user explicitly wants `@youversion/platform-core`.
- The user wants browser, Node.js, serverless, or TypeScript SDK examples rather than raw HTTP requests.
- The user wants to list versions, fetch a version object, or render passage HTML through the SDK.
- The user wants a standalone HTML page generated from a JS script.

## Reach For Another Skill When

- The user wants raw REST requests, headers, query parameters, or response JSON. Use skill `youversion-platform-api`.
- The user wants a React app or React Bible UI components instead of low-level SDK examples. Use the React-focused YVP skill.

## YVP Mental Model

- `ApiClient` wraps the app key, and `BibleClient` is the main Bible-specific SDK surface.
- App keys are not secrets. Use the project's configuration: `process.env.YVP_APP_KEY` on the server, or a public app key in browser code.
- Bible versions use numeric ids such as `3034` or `111`.
- Version discovery is still app-key and license dependent, so list versions before choosing an id when the id is unknown.
- Passages use USFM notation such as `JHN.3.16`.
- `getPassage(versionId, usfm, format)` returns an object whose `content` is the scripture payload in either `html` or `text`.
- For styled Bible HTML, prefer `getPassageDisplay({ versionId, passageId })`: it returns transformed HTML, current attribution, stylesheets, and container attributes.
- Display the selected version's name or abbreviation and required attribution. Do not silently omit attribution.

## Default Workflow

1. Identify the runtime and preserve the user's existing project setup. Use `references/node-scaffold.md` only for a new Node.js project.
2. Check the app key source and initialize `ApiClient` and `BibleClient` from `@youversion/platform-core`.
3. If the version id is unknown, use `bibleClient.getVersions("en")` (or the requested language) and select from `versions.data`; do not invent an id.
4. Use `getVersion(versionId)` for version metadata. For styled HTML, use `getPassageDisplay({ versionId, passageId })`; for plain text, use `getPassage(versionId, usfm, "text")`.
5. When rendering a display result, add its `stylesheets` to the document head, apply its `containerAttributes` to the scripture container, render `display.html` as HTML, and render `display.attribution.text` as text.
6. For Node.js HTML transformation, install the optional peer `jsdom`. Browsers use `DOMParser`; serverless runtimes must support the server transformation dependencies. Plain-text retrieval does not need a DOM.
7. When the user requests a browser-openable artifact, produce a complete HTML document using `assets/standalone-page-template.html` and `references/node-sdk-examples.md`, or use the browser example in `references/browser-sdk-examples.md`.

## Response style

- Give a direct answer first.
- Prefer one runnable example in the user's runtime over several disconnected snippets.
- Use ECMAScript modules; in browsers use the project's bundler or module setup rather than a bare package import in an unconfigured HTML file.
- Keep examples narrow and practical: initialize, list versions, fetch passage HTML, emit page.
- Provide a scaffold only when the user needs one, matching their runtime, then continue with the SDK example.
- When the user does not know the version id yet, lead with `getVersions(...)` before `getPassage(...)`.
- Use `getVersion(...)` when attribution or metadata matters rather than hard-coding version labels.
- Never make up scripture content. Hallucinating Bible text is unacceptable; only quote `passage.content` or passage text if you actually fetched it in the current environment or the user supplied it.

## Default initialization (Node.js)

Use this package and setup by default:

```bash
npm install @youversion/platform-core
```

```js
const { ApiClient, BibleClient } = await import("@youversion/platform-core");
const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY });
const bibleClient = new BibleClient(apiClient);
```

## Default version-list example

Use this example unless the user asks for a different language:

```js
const versions = await bibleClient.getVersions("en");
for (const v of versions.data) {
  console.log(v.id, v.abbreviation, v.title);
}
```

Explain that this lists versions available to the current app key and its accepted licenses.

## Default version metadata example

Use this shape when the user needs attribution or wants details for one version:

```js
const version = await bibleClient.getVersion(3034);

console.log({
  id: version.id,
  abbreviation: version.abbreviation,
  title: version.title,
  localizedTitle: version.localized_title,
  copyright: version.copyright,
});
```

## Default passage examples

For styled Bible HTML:

```js
const display = await bibleClient.getPassageDisplay({
  versionId: 3034,
  passageId: "JHN.3.16",
});
```

For plain text:

```js
const passage = await bibleClient.getPassage(3034, "JHN.3.16", "text");
```

Use `3034` (Berean Standard Bible) for a public-domain English example; `111` (NIV) requires an accepted license. Discover the version first when the user's desired version id is unknown.

`getPassageDisplay` fetches current metadata on each call, uses `copyright` with `promotional_content` as a fallback, and fails if attribution is missing. It returns data only: the caller installs resources and renders the result.

For lower-level HTML retrieval, `getPassage` defaults to HTML with sanitization/transformation enabled; its sixth argument can disable transformation for raw API HTML. Prefer the display API when the result will be styled and shown to users. See the [JavaScript SDK](https://developers.youversion.com/sdks/javascript/index) and [HTML display guide](https://developers.youversion.com/guides/display-bible-html).

## Gotchas

- `getPassageDisplay` is available in `@youversion/platform-core` 2.15.0. Check the installed version in existing projects before using the new API; follow current SDK documentation if an upgrade is needed.
- The app key may be in `process.env.YVP_APP_KEY`; it is NOT a secret so can be put in HTML sources.
- Render `display.html` as HTML. Escape ordinary text and attribute values in generated HTML, including reference, version labels, attribution, and stylesheet URLs. Render plain-text passage content as text.
- Do not guess version ids from language alone. Use `getVersions(...)` first when the id is unknown.
- Do not fabricate Bible text or imply that `getPassage(...)` returned specific scripture content unless you actually executed that call in the current environment.
- Do not imply that `getVersions(...)` or `getVersion(...)` returned specific live results unless you actually executed them in the current environment.
- Use all returned stylesheet descriptors and container attributes; a CSS link alone is not the complete display setup.
- Default to version `3034` when the user wants a public-domain example.
- For custom plain-text or lower-level HTML layouts, fetch the selected version's metadata and display `copyright?.trim() || promotional_content?.trim()`; report missing attribution instead of displaying uncredited scripture.

## References to load on demand

- Read `references/node-scaffold.md` when the user is not yet inside Node.js.
- Read `references/node-sdk-examples.md` for server code or a generated HTML page.
- Read `references/browser-sdk-examples.md` for browser SDK rendering.
- Use `assets/standalone-page-template.html` when generating a complete page artifact.

## Self-check before answering

- [ ] Included Node.js scaffold if needed.
- [ ] Used `@youversion/platform-core` with `ApiClient` and `BibleClient`.
- [ ] Included `getVersions("en")` when version discovery matters.
- [ ] Used `getPassageDisplay` for styled HTML or `getPassage(..., "text")` for plain text.
- [ ] Produced a full HTML document when the user asked for browser-openable output.
- [ ] Applied the returned stylesheets and container attributes for HTML rendering.
- [ ] Displayed required attribution with scripture.
