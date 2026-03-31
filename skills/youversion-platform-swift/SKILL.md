---
name: youversion-platform-swift
description: YouVersion Swift SDK for iOS/iPadOS apps that render scripture and integrate YouVersion features. Use when asked for Swift or SwiftUI examples with YouVersionPlatform, including SDK installation (SPM/CocoaPods), app-key configuration, BibleTextView/BibleCardView usage, BibleReaderView integration, Sign In with YouVersion flows, and Verse of the Day (VotdView or API) examples.
---

# YouVersion Platform Swift SDK

## Default workflow

1. Confirm the user is building in Swift/SwiftUI (iOS/iPadOS).
2. If project setup is missing, provide the minimal setup from `references/swift-setup.md` and continue with the requested feature example.
3. Ensure initialization includes `YouVersionPlatform.configure(appKey: "YOUR_APP_KEY_HERE")` early in app startup.
4. Give one complete, runnable SwiftUI example (not many disconnected snippets) that directly answers the request.
5. Prefer SDK-native UI components first (`BibleTextView`, `BibleCardView`, `BibleReaderView`, `SignInWithYouVersionButton`, `VotdView`) before custom API plumbing.
6. For VOTD custom UI, show `YouVersionAPI.VOTD.verseOfTheDay(dayOfYear:)` and then render with `BibleTextView`.
7. For authentication, include a strong `ContextProvider` reference and async/await `Task` flow.

## Response style

- Answer directly first.
- Prioritize practical SwiftUI code that compiles with modern Swift concurrency.
- Keep examples focused and complete (imports + view/app context).
- Mention platform requirements when relevant: iOS 17+ / iPadOS 17+.
- If a request overlaps direct REST/API questions, explain that this skill focuses on Swift SDK usage and mention API docs for advanced endpoint work.

## Installation defaults

Use one of these defaults based on user context:

### Swift Package Manager

```swift
dependencies: [
    .package(url: "https://github.com/youversion/platform-sdk-swift.git", from: "0.1.0")
]
```

### CocoaPods

```ruby
pod 'YouVersionPlatform', '~> 1.0'
```

## Default initialization

```swift
import SwiftUI
import YouVersionPlatform

@main
struct YourApp: App {
    init() {
        YouVersionPlatform.configure(appKey: "YOUR_APP_KEY_HERE")
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

## Scripture display defaults

Use `BibleReference` with `BibleTextView`:

```swift
BibleTextView(
    BibleReference(versionId: 3034, bookUSFM: "JHN", chapter: 3, verse: 16)
)
```

Common variants:

- Verse range: `verseStart` + `verseEnd`
- Chapter: omit verse fields
- Long passage: wrap in `ScrollView`

When a public-domain example is needed, default to version `3034` (BSB).

## Bible Reader default

```swift
BibleReaderView(
    appName: "Sample App",
    signInMessage: "Sign in to see your YouVersion highlights in this app."
)
```

## Sign In default

Use this pattern when users ask for auth/login:

```swift
import SwiftUI
import AuthenticationServices
import YouVersionPlatform

final class ContextProvider: NSObject, ASWebAuthenticationPresentationContextProviding {
    func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        guard let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
              let window = scene.windows.first else {
            return ASPresentationAnchor()
        }
        return window
    }
}

struct SignInExampleView: View {
    @State private var contextProvider = ContextProvider()

    var body: some View {
        SignInWithYouVersionButton {
            Task {
                do {
                    let result = try await YouVersionAPI.Users.signIn(
                        permissions: [.profile, .email],
                        contextProvider: contextProvider
                    )
                    print("Access token: \(result.accessToken)")
                } catch {
                    print("Sign in failed: \(error)")
                }
            }
        }
    }
}
```

## Verse of the Day defaults

Simple component:

```swift
VotdView()
```

Custom flow:

```swift
let dayOfYear = Calendar.current.ordinality(of: .day, in: .year, for: Date())!
let votd = try await YouVersionAPI.VOTD.verseOfTheDay(dayOfYear: dayOfYear)
```

Then render with `BibleTextView(votd.reference)` or equivalent custom UI.

## Gotchas

- Configure the SDK once during app startup before using SDK views/API calls.
- Keep a strong reference to the auth context provider in SwiftUI state.
- The SDK persists access tokens locally; losing/removing token data effectively logs users out.
- For SDK component requests, avoid replacing built-in views with manual WebView/API layers unless explicitly requested.

## References to load on demand

- Read `references/swift-setup.md` when users need quick project setup or install help.
- Read `references/swift-examples.md` when users ask for fuller end-to-end feature examples.

## Self-check before answering

- [ ] Used Swift/SwiftUI examples (not JS/REST-first snippets).
- [ ] Included `YouVersionPlatform.configure(appKey:)` when setup/init is relevant.
- [ ] Used SDK-native components where applicable.
- [ ] Included `ContextProvider` + strong reference for sign-in flows.
- [ ] Used `VotdView` or `YouVersionAPI.VOTD.verseOfTheDay(dayOfYear:)` for VOTD requests.
