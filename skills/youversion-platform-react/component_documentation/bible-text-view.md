# BibleTextView

## What It Is

Display any Bible passage with proper formatting.

> Note: When using the `BibleTextView` component, you are responsible for displaying any required Bible version copyright notice, as required by the license.
>
> This component gives you full flexibility over layout, so display the selected version's `copyright`, falling back to `promotional_content`, as text. Report missing attribution instead of silently omitting it. If you want these credits handled for you automatically, use the `BibleCard` component instead.

## Basic Code Example

Render this component inside `YouVersionProvider` (see [provider setup](youversion-provider.md)). Fetch metadata for the same version before displaying scripture.

```tsx
import { BibleTextView } from "@youversion/platform-react-ui";
import { useVersion } from "@youversion/platform-react-hooks";

function MyComponent() {
  const versionId = 3034;
  const { version, loading, error } = useVersion(versionId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Could not load Bible version.</div>;
  const attribution = version?.copyright?.trim() || version?.promotional_content?.trim();
  if (!version || !attribution) return <div>Unable to display scripture with attribution.</div>;

  return (
    <article>
      <h2>{version.localized_abbreviation || version.abbreviation}</h2>
      <BibleTextView
        reference="JHN.3.16"
        versionId={versionId}
        fontFamily="serif"
        fontSize={20}
        lineHeight={1.5}
      />
      <p>{attribution}</p>
    </article>
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
