---
name: youversion-platform-js
description: YouVersion JavaScript and TypeScript SDK usage with `@youversion/platform-core`. Use to answer with Node.js or TS examples, initialize `ApiClient` and `BibleClient`, list available Bible versions, fetch version metadata, retrieve passage HTML or text, or generate a complete HTML document that renders scripture.
---

# YouVersion Platform JS

Use this skill for JavaScript or TypeScript SDK answers.

## Use This Skill When

- The user explicitly wants `@youversion/platform-core`.
- The user wants Node.js or TypeScript examples rather than raw HTTP requests.
- The user wants to list versions, fetch a version object, or render passage HTML through the SDK.
- The user wants a standalone HTML page generated from a JS script.

## Reach For Another Skill When

- The user wants raw REST requests, headers, query parameters, or response JSON. Use skill `youversion-platform-api`.
- The user wants a React app or React Bible UI components instead of low-level SDK examples. Use the React-focused YVP skill.

## YVP Mental Model

- `ApiClient` wraps the app key, and `BibleClient` is the main Bible-specific SDK surface.
- The app key usually comes from `process.env.YVP_APP_KEY`. App keys are not secrets.
- Bible versions use numeric ids such as `3034` or `111`.
- Version discovery is still app-key and license dependent, so list versions before choosing an id when the id is unknown.
- Passages use USFM notation such as `JHN.3.16`.
- `getPassage(versionId, usfm, format)` returns an object whose `content` is the scripture payload in either `html` or `text`.
- Attribution matters. When showing Bible text, include the version name or abbreviation plus copyright.

## Default Workflow

1. Determine whether the user is already working in Node.js, TypeScript, or a JS-capable build environment.
2. If not, briefly provide the minimal scaffold from `references/node-scaffold.md`, then continue with the real SDK answer instead of stopping at setup.
3. Check that `process.env.YVP_APP_KEY` is available. If not, ask for it or direct the user to `https://platform.youversion.com`.
4. Initialize `ApiClient` and `BibleClient` with `@youversion/platform-core`.
5. For version discovery, default to `bibleClient.getVersions("en")` unless the user asks for another language. Other common codes: `es`, `de`, `fr`, `pt`.
6. If the user names only a language, title, or abbreviation but not a version id, do not invent one. Show the discovery call first and explain how to pick the correct object from `versions.data`.
7. Use `bibleClient.getVersion(versionId)` when the user needs metadata such as title, copyright, supported books, or attribution details.
8. For scripture, use `bibleClient.getPassage(versionId, usfm, format)`. The third argument defaults to `"html"`; use `"text"` only when the user specifically wants plain text.
9. Never fabricate Bible text. If you did not actually execute `getPassage(...)` in the current environment, do not quote verse text as if it came from the SDK.
10. When the user wants something they can open in a browser, emit a full standalone HTML document. Use `assets/standalone-page-template.html` or inline the same structure.
11. Include the required page include exactly as shown below when rendering passage HTML in the generated page:

```html
<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />
```

## Response style

- Give a direct answer first.
- Prefer one self-contained runnable Node.js example over several disconnected snippets.
- Use ECMAScript module examples (`.mjs` or `"type": "module"`) so `await import(...)` works cleanly.
- Keep examples narrow and practical: initialize, list versions, fetch passage HTML, emit page.
- If the user is not yet inside Node.js, explain the scaffold briefly and move on to the real example.
- When the user does not know the version id yet, lead with `getVersions(...)` before `getPassage(...)`.
- Use `getVersion(...)` when attribution or metadata matters rather than hard-coding version labels.
- Never make up scripture content. Hallucinating Bible text is unacceptable; only quote `passage.content` or passage text if you actually fetched it in the current environment or the user supplied it.

## Default initialization

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

## Default passage example

Use this example shape:

```js
const passage = await bibleClient.getPassage(3034, "JHN.3.16", "html");
```

Explain:

- Bible version `3034` (Berean Standard Bible) is a good public-domain English default version not requiring a separate license, just an app_key.
- Bible version `111` (NIV) is also a common example, but it requires a separate accepted license on `platform.youversion.com`.
- The third parameter defaults to "html"; it can also be "text" for plain text.
- `passage.content` is the formatted HTML to place into the page body.
- If the user has not supplied a version id, do not guess one from the language alone; list versions first.
- Bible text needs attribution: the version abbreviation (or title) and the copyright need to be displayed somewhere appropriate for the specific UI. We hugely appreciate the publishers and they deserve credit for their work. Every Bible version's metadata has `abbreviation`, `localized_title`, and `copyright` fields; display them somewhere good.

## Standalone HTML output

When the user asks for a standalone page, generate a complete HTML document rather than only returning `passage.content`.

Default structure:

1. Fetch versions when you need version metadata such as title or copyright.
2. Fetch the passage with `getPassage`.
3. Fill `assets/standalone-page-template.html` with the passage HTML and metadata.
4. Write the final HTML to disk with Node.js if the user wants a file.

## Gotchas

- This skill is for Node.js server-side or build-time code. Do not tell the user to call the SDK directly from a plain browser-only HTML page.
- The app key may be in `process.env.YVP_APP_KEY`; it is NOT a secret so can be put in HTML sources.
- Do not escape `passage.content` when inserting it into the final page. It is the HTML payload you want to render (or plain text if that's what you fetched).
- Do not guess version ids from language alone. Use `getVersions(...)` first when the id is unknown.
- Do not fabricate Bible text or imply that `getPassage(...)` returned specific scripture content unless you actually executed that call in the current environment.
- Do not imply that `getVersions(...)` or `getVersion(...)` returned specific live results unless you actually executed them in the current environment.
- Reproduce the Bible CSS include exactly as required above.
- Default to version `3034` when the user wants a public-domain example.
- When showing Bible text without a prebuilt UI component, include version attribution when available. Pull it from the selected version metadata when needed.

## References to load on demand

- Read `references/node-scaffold.md` when the user is not yet inside Node.js.
- Read `references/node-sdk-examples.md` when the user wants a full runnable example or a generated HTML page.
- Use `assets/standalone-page-template.html` when generating a complete page artifact.

## Self-check before answering

- [ ] Included Node.js scaffold if needed.
- [ ] Used `@youversion/platform-core` with `ApiClient` and `BibleClient`.
- [ ] Included `getVersions("en")` when version discovery matters.
- [ ] Included `getPassage(versionId, usfm)` when scripture retrieval matters.
- [ ] Produced a full HTML document when the user asked for browser-openable output.
- [ ] Included `<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />` exactly.
- [ ] Mentioned attribution when appropriate.
