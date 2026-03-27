---
name: youversion-platform-js
description: YouVersion JavaScript/TypeScript sdk for working with Bible text and Bible versions. Use when asked to display Bible text (Scripture), to use @youversion/platform-core, to  list bible versions available, to fetch Bible passage html, or generate a complete html document that renders scripture.
---

# YouVersion Platform JS - for JavaScript / TypeScript / Node.js

## Default workflow

1. Determine whether the user is already running code inside Node.js or has a similar JavaScript-based project.
2. If not, briefly provide the minimal scaffold from `references/node-scaffold.md`, then continue with the SDK example instead of stopping at setup.
3. Check that `process.env.YVP_APP_KEY` is defined; if not ask the user for their app key which is available via registration at https://platform.youversion.com
4. Initialize `ApiClient` and `BibleClient` with `@youversion/platform-core` and `process.env.YVP_APP_KEY`.
5. For version discovery, default to `bibleClient.getVersions("en")` unless the user asks for another language. Other common language codes: "es", "de", "fr", "pt".
6. For passage retrieval, use `bibleClient.getPassage(versionId, usfm)` and explain that `content` is already formatted HTML.
7. Never fabricate Bible text. If you did not actually execute `getPassage(...)` in the current environment, do not quote verse text as if it were returned by the API.
8. When the user wants something they can open in a browser, emit a full standalone HTML document. Use `assets/standalone-page-template.html` or inline the same structure.
9. Include the required page include exactly as shown below when rendering passage HTML in the generated page:

```html
<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />
```

## Response style

- Give a direct answer first.
- Prefer one self-contained runnable Node.js example over several disconnected snippets.
- Use ECMAScript module examples (`.mjs` or `"type": "module"`) so `await import(...)` works cleanly.
- Keep examples narrow and practical: initialize, list versions, fetch passage HTML, emit page.
- If the user is not yet inside Node.js, explain the scaffold briefly and move on to the real example.
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

## Default passage example

Use this example shape:

```js
let passage = await bibleClient.getPassage(111, "JHN.3.16", "html");
```

Explain:

- Bible version `111` (NIV, used above) is a good example version id from the versions list; it has a separate license to accept on platform.youversion.com.
- Bible version `3034` (Berean Standard Bible) is a good public-domain English default version not requiring a separate license, just an app_key.
- The third parameter defaults to "html"; it can also be "text" for plain text.
- `passage.content` is the formatted HTML to place into the page body.

When helpful, show the returned object shape:

```js
{
  id: "JHN.3.16",
  content: "<div><div class=\"p\"><span class=\"yv-v\" v=\"16\"></span><span class=\"yv-vlbl\">16</span>For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. </div></div>",
  reference: "John 3:16"
}
```

## Bible version information example

let bibleVersion = await bibleClient.getVersion(3034);
console.log(bibleVersion)
{
  id: 3034,
  abbreviation: 'BSB',
  promotional_content: 'Public Domain',
  copyright: 'Public Domain',
  language_tag: 'en',
  localized_abbreviation: 'BSB',
  publisher_url: null,
  localized_title: 'Berean Standard Bible',
  title: 'Berean Standard Bible',
  books: [
    'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS',
    'JDG', 'RUT', '1SA', '2SA', '1KI', '2KI',
    '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB',
    'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER',
    'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO',
    'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP',
    'HAG', 'ZEC', 'MAL', 'MAT', 'MRK', 'LUK',
    'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL',
    'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI',
    '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE',
    '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'
  ],
  youversion_deep_link: 'https://www.bible.com/versions/3034',
}


## Standalone HTML output

When the user asks for a standalone page, generate a complete HTML document rather than only returning `passage.content`.

Default structure:

1. Fetch versions if you need version metadata such as title or copyright.
2. Fetch the passage with `getPassage`.
3. Fill `assets/standalone-page-template.html` with the passage HTML and metadata.
4. Write the final HTML to disk with Node.js if the user wants a file.

## Gotchas

- This skill is for Node.js server-side or build-time code. Do not tell the user to call the SDK directly from a plain browser-only HTML page.
- The app key may be in `process.env.YVP_APP_KEY`; it is NOT a secret so can be put in HTML sources.
- Do not escape `passage.content` when inserting it into the final page. It is the HTML payload you want to render (or plain text if that's what you fetched).
- Do not fabricate Bible text or imply that `getPassage(...)` returned specific scripture content unless you actually executed that call in the current environment.
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
