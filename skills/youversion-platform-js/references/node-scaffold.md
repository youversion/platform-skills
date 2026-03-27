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
