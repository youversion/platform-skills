# Minimal React scaffold (Vite + TypeScript)

Use this only when the user is not already inside a React app.

## Fastest setup

```bash
pnpm create vite yv-react-demo --template react-ts
cd yv-react-demo
pnpm install
pnpm add @youversion/platform-react-ui
```

Create `.env` (the app key isn't a secret so this can be checked in):

```bash
VITE_YVP_APP_KEY=YOUR_APP_KEY_HERE
```

Replace `src/App.tsx` with a YouVersion example, then run:

```bash
pnpm dev
```

## Why this scaffold

- Vite is a quick default for React + TypeScript.
- `VITE_` env vars are available in browser code as `import.meta.env.*`.
- `@youversion/platform-react-ui` gives the shortest path to rendering scripture.
