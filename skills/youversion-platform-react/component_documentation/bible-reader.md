# BibleReader

## What It Is

A complete Bible reading experience with version picker, chapter navigation, and customizable text display.

### Sub-components

- `BibleReader.Root` - Container with context provider
- `BibleReader.Content` - Displays passage text with book/chapter header
- `BibleReader.Toolbar` - Version and chapter picker controls

## Basic Code Example

```tsx
import { BibleReader } from "@youversion/platform-react-ui";

function App() {
  return (
    <div className="h-screen">
      <BibleReader.Root>
        <BibleReader.Content />
        <BibleReader.Toolbar />
      </BibleReader.Root>
    </div>
  );
}
```

## Props

### Root Props

```ts
type BibleReaderRootProps = {
  /** Controlled book ID (3-letter USFM code like "JHN") */
  book?: string;
  /** Default book when uncontrolled */
  defaultBook?: string;
  onBookChange?: (book: string) => void;

  /** Controlled chapter number */
  chapter?: string;
  /** Default chapter when uncontrolled */
  defaultChapter?: string;
  onChapterChange?: (chapter: string) => void;

  /** Controlled version ID */
  versionId?: number;
  /** Default Bible Version when uncontrolled */
  defaultVersionId?: number;
  onVersionChange?: (versionId: number) => void;

  /** Font customization */
  fontFamily?: string;
  fontSize?: number;
  lineHeight?: number;

  /** Toggle verse numbers (default: true) */
  showVerseNumbers?: boolean;

  /** Theme (default: "light") */
  background?: "light" | "dark";

  children?: ReactNode;
};
```

### Toolbar Props

```ts
{ border = "top" }: { border?: "top" | "bottom" }
```

## Additional Examples

```tsx
// Dark theme with custom styling
<BibleReader.Root
  background="dark"
  fontSize={18}
  lineHeight={2.0}
  showVerseNumbers={false}
>
  <BibleReader.Toolbar border="bottom" />
  <BibleReader.Content />
</BibleReader.Root>;
```

```tsx
import { useState } from "react";
import { BibleReader } from "@youversion/platform-react-ui";

// Controlled state
function ControlledReader() {
  const [book, setBook] = useState("PSA");
  const [chapter, setChapter] = useState("23");

  return (
    <BibleReader.Root
      book={book}
      chapter={chapter}
      onBookChange={setBook}
      onChapterChange={setChapter}
    >
      <BibleReader.Content />
      <BibleReader.Toolbar />
    </BibleReader.Root>
  );
}
```
