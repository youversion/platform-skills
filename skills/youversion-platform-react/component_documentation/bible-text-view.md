# BibleTextView

## What It Is

Display any Bible passage with proper formatting.

> Note: When using the `BibleTextView` component, you are responsible for displaying any required Bible version copyright notice, as required by the license.
>
> This component gives you full flexibility over layout, so be sure to add copyright or attribution credits yourself where appropriate in your UI. If you want these credits handled for you automatically, use the `BibleCard` component instead.

## Basic Code Example

```tsx
import { BibleTextView } from "@youversion/platform-react-ui";

function MyComponent() {
  return (
    <BibleTextView
      reference="JHN.3.16"
      versionId={3034}
      fontFamily="serif"
      fontSize={20}
      lineHeight={1.5}
    />
  );
}
```

## Props

```tsx
type BibleTextViewProps = {
  /** USFM reference (e.g., "JHN.3.16" or "PSA.23.1-6") */
  reference: string;
  /** Bible version ID */
  versionId: number;
  /** Font customization */
  fontFamily?: string;
  fontSize?: number;
  lineHeight?: number;
  /** Show verse numbers (default: true) */
  showVerseNumbers?: boolean;
  /** Show footnotes (default: true) */
  renderNotes?: boolean;
};
```
