# Node SDK Examples

Use this reference when the user wants a runnable JavaScript or TypeScript example with `@youversion/platform-core`.

## List versions and pick one

Use discovery before passage lookup when the user knows only a language, title, or abbreviation.

```js
const { ApiClient, BibleClient } = await import("@youversion/platform-core");

const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY });
const bibleClient = new BibleClient(apiClient);

const versions = await bibleClient.getVersions("en");

for (const version of versions.data) {
  console.log(version.id, version.abbreviation, version.title);
}
```

Explain that `versions.data` is filtered by the current app key and accepted licenses.

## Fetch version metadata

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

Useful for version details. Prefer `getPassageDisplay` when rendering styled HTML; for a custom plain-text layout, display the selected version label and `version.copyright?.trim() || version.promotional_content?.trim()`, and report an error if both are missing.

## Fetch a passage as HTML or text

```js
const passageHtml = await bibleClient.getPassage(3034, "JHN.3.16", "html");
console.log(passageHtml.reference);
console.log(passageHtml.content);

const passageText = await bibleClient.getPassage(3034, "JHN.3.16", "text");
console.log(passageText.content);
```

Notes:

- The third parameter defaults to `"html"`, with transformation enabled. Node.js HTML transformation needs `jsdom`; prefer `getPassageDisplay` for styled display.
- `passage.content` is the returned scripture payload.
- Do not quote the Bible text in an answer unless you actually executed the call in the current environment or the user supplied the text.

## Generate a standalone HTML page

Install `@youversion/platform-core` and `jsdom` for server-side HTML transformation. Copy `assets/standalone-page-template.html` beside the user's `index.mjs`; this example resolves the template relative to that script.

```js
import { readFile, writeFile } from "node:fs/promises";
import { ApiClient, BibleClient } from "@youversion/platform-core";

const bibleClient = new BibleClient(new ApiClient({ appKey: process.env.YVP_APP_KEY }));
const passageId = "JHN.3.16";
const display = await bibleClient.getPassageDisplay({ versionId: 3034, passageId });

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]);
}

const values = {
  reference: escapeHtml(passageId),
  version_title: escapeHtml(display.version.localized_title || display.version.title),
  version_abbreviation: escapeHtml(display.version.localized_abbreviation || display.version.abbreviation),
  stylesheet_links: display.stylesheets.map(({ rel, href }) =>
    `<link rel="${escapeHtml(rel)}" href="${escapeHtml(href)}">`
  ).join("\n"),
  container_attributes: Object.entries(display.containerAttributes).map(([name, value]) =>
    `${name}="${escapeHtml(value)}"`
  ).join(" "),
  passage_html: display.html,
  attribution_text: escapeHtml(display.attribution.text),
};

const template = await readFile(new URL("./standalone-page-template.html", import.meta.url), "utf8");
const html = template.replace(/{{(\w+)}}/g, (_, key) => {
  if (!(key in values)) throw new Error(`Unknown template placeholder: ${key}`);
  return values[key];
});
await writeFile("passage.html", html, "utf8");
console.log("Wrote passage.html");
```

Only `display.html` is inserted as scripture HTML; attribution and other text are escaped. The display API supplies current attribution and both Bible CSS and font resources. Do not download or self-host the font files. See [Display Bible HTML](https://developers.youversion.com/guides/display-bible-html).
