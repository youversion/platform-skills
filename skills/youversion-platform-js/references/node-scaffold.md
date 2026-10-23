# Minimal Node.js scaffold

Use this only when the user is not already running code inside Node.js.

## Fastest setup

```bash
mkdir yv-js-demo
cd yv-js-demo
npm init -y
npm pkg set type=module
npm install @youversion/platform-core
export YVP_APP_KEY='YOUR_APP_KEY_HERE'
```

### Transformed HTML only

Plain-text retrieval and version discovery do not need a DOM. Browsers use `DOMParser` and do not need `jsdom`.

If the deployed Node.js server transforms Bible HTML, install `jsdom` as a runtime dependency:

```bash
npm install jsdom
```

If transformation runs only during a build to generate static pages, install it as a development dependency instead:

```bash
npm install -D jsdom
```

Use uppercase `-D` for `--save-dev` (see [npm install](https://docs.npmjs.com/cli/v11/commands/npm-install)). Production installs can omit development dependencies, so server-side execution alone does not make `jsdom` a development dependency.

### Run the example

Create `index.mjs`, paste the example code, then run:

```bash
node index.mjs
```

## Why this scaffold

- `npm pkg set type=module` enables ESM so `await import("@youversion/platform-core")` works naturally.
- `YVP_APP_KEY` keeps the app key out of source code.
- A single `index.mjs` file is enough for quick experiments and for generating a standalone HTML page.

## Minimal starter file

```js
const { ApiClient, BibleClient } = await import("@youversion/platform-core");

const apiClient = new ApiClient({ appKey: process.env.YVP_APP_KEY });
const bibleClient = new BibleClient(apiClient);

const versions = await bibleClient.getVersions("en");
console.log(`You have ${versions.data.length} Bible versions available in English`);
```
