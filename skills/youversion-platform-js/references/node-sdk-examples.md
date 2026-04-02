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

## Fetch version metadata for attribution

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

Useful when the user needs attribution text, the localized title, or the list of supported books.

## Fetch a passage as HTML or text

```js
const passageHtml = await bibleClient.getPassage(3034, "JHN.3.16", "html");
console.log(passageHtml.reference);
console.log(passageHtml.content);

const passageText = await bibleClient.getPassage(3034, "JHN.3.16", "text");
console.log(passageText.content);
```

Notes:

- The third parameter defaults to `"html"`.
- `passage.content` is the returned scripture payload.
- Do not quote the Bible text in an answer unless you actually executed the call in the current environment or the user supplied the text.

## Generate a standalone HTML page

This example loads the bundled template, injects passage HTML plus attribution, and writes a page to disk.

```js
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const { ApiClient, BibleClient } = await import("@youversion/platform-core");

const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY });
const bibleClient = new BibleClient(apiClient);

const [version, passage] = await Promise.all([
  bibleClient.getVersion(3034),
  bibleClient.getPassage(3034, "JHN.3.16", "html"),
]);

const templateUrl = new URL("../assets/standalone-page-template.html", import.meta.url);
const template = await readFile(fileURLToPath(templateUrl), "utf8");

const html = template
  .replaceAll("{{reference}}", passage.reference)
  .replaceAll("{{version_title}}", version.localized_title || version.title)
  .replaceAll("{{version_abbreviation}}", version.localized_abbreviation || version.abbreviation)
  .replaceAll("{{passage_html}}", passage.content)
  .replaceAll(
    "{{copyright_html}}",
    version.copyright ? `<p class="copyright">${version.copyright}</p>` : ""
  );

await writeFile("passage.html", html, "utf8");
console.log("Wrote passage.html");
```

The bundled template already includes the required stylesheet:

```html
<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />
```
