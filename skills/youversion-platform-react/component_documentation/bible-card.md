# BibleCard

## What It Is

Pre-styled widget displaying a Bible passage with reference, text, and attribution.

## Basic Code Example

```tsx
import { BibleCard } from "@youversion/platform-react-ui";

export default function Page() {
  return (
    <BibleCard reference="JHN.3.16" versionId={3034} background="light" />
  );
}
```

## Props

```ts
type BibleCardProps = {
  /** USFM passage reference (e.g., "JHN.3.16") */
  reference: string;
  /** Bible version identifier */
  versionId: number;
  /** Theme variant: light or dark */
  background?: "light" | "dark";
  /** Show version picker (default: false) */
  showVersionPicker?: boolean;
};
```
