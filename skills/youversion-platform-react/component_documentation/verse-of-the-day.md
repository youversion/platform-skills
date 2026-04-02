# VerseOfTheDay

## What It Is

Display the YouVersion Verse of the Day.

## Basic Code Example

```tsx
import { VerseOfTheDay } from "@youversion/platform-react-ui";

function MyApp() {
  return <VerseOfTheDay />;
}
```

## Props

```tsx
type VerseOfTheDayProps = {
  /** Bible version ID (default: 3034 - BSB) */
  versionId?: number;
  /** Day of year (1-366). Defaults to today */
  dayOfYear?: number;
  /** Show decorative sun icon (default: true) */
  showSunIcon?: boolean;
  /** Show Bible App attribution (default: true) */
  showBibleAppAttribution?: boolean;
  /** Show share button (default: true) */
  showShareButton?: boolean;
  /** Card size (default: "default") */
  size?: "default" | "lg";
};
```
