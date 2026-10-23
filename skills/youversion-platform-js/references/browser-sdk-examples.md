# Browser SDK rendering

Use `@youversion/platform-core` in the user's existing browser bundler/module setup. App keys are public; do not use Node's `process.env` in a plain browser script. In Vite, a public environment variable is available through `import.meta.env.VITE_YVP_APP_KEY`.

Start with these elements in the page:

```html
<article id="scripture"></article>
<p id="attribution"></p>
```

```js
import { ApiClient, BibleClient } from "@youversion/platform-core";

const bibleClient = new BibleClient(new ApiClient({ appKey: "YOUR_APP_KEY" }));
const root = document.getElementById("scripture");
const credit = document.getElementById("attribution");
if (!root || !credit) throw new Error("Missing scripture display elements");

try {
  const display = await bibleClient.getPassageDisplay({
    versionId: 3034,
    passageId: "JHN.3.16",
  });
  for (const { rel, href } of display.stylesheets) {
    const installed = [...document.querySelectorAll('link[rel="stylesheet"]')]
      .some((link) => link.getAttribute("href") === href);
    if (!installed) {
      const link = document.createElement("link");
      link.rel = rel;
      link.href = href;
      document.head.append(link);
    }
  }
  for (const [name, value] of Object.entries(display.containerAttributes)) {
    root.setAttribute(name, value);
  }
  root.innerHTML = display.html;
  credit.textContent = `${display.version.localized_abbreviation || display.version.abbreviation} — ${display.attribution.text}`;
} catch (error) {
  root.textContent = "Unable to load scripture.";
  credit.textContent = "";
  console.error(error);
}
```

The SDK uses the browser's `DOMParser` for HTML transformation, so `jsdom` is not needed here. Keep attribution as text. For another client framework, apply the same resources and attributes and render only the scripture HTML through its HTML rendering API. See [Display Bible HTML](https://developers.youversion.com/guides/display-bible-html).
