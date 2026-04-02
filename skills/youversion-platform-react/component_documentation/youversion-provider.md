# YouVersionProvider

## What It Is

Required provider that configures the YouVersion Platform SDK. Wrap all your code which accesses YouVersion Platform features with `YouVersionProvider`.

Authentication is optional and can be enabled with the `includeAuth` prop. If you set `includeAuth={true}` you must provide an `authRedirectUrl`.

> Note: Your `authRedirectUrl` must be in your Callback URI list in your app settings.

## Basic Code Example

```tsx
import { YouVersionProvider } from "@youversion/platform-react-ui";

function App() {
  return (
    <YouVersionProvider
      appKey="YOUR_APP_KEY"
      includeAuth={true}
      authRedirectUrl="https://yourapp.com"
    >
      {/* Your app */}
    </YouVersionProvider>
  );
}
```

## Props

The `YouVersionProvider` uses conditional props for TypeScript safety:

```tsx
// Base props
interface YouVersionProviderPropsBase {
  children: ReactNode;
  appKey: string;
  apiHost?: string;
  theme?: "light" | "dark" | "system";
}

// With authentication (authRedirectUrl becomes required when includeAuth is true)
interface YouVersionProviderPropsWithAuth extends YouVersionProviderPropsBase {
  authRedirectUrl: string;
  includeAuth: true;
}

// Without authentication (authRedirectUrl cannot be used when includeAuth is false)
interface YouVersionProviderPropsWithoutAuth extends YouVersionProviderPropsBase {
  includeAuth?: false;
  authRedirectUrl?: never;
}

// Final type is a union of the two configurations
type YouVersionProviderProps =
  | YouVersionProviderPropsWithAuth
  | YouVersionProviderPropsWithoutAuth;
```
