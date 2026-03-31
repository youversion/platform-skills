# Swift SDK examples

Use these when the user asks for fuller implementation patterns.

## Scripture examples

### Verse

```swift
BibleTextView(
    BibleReference(versionId: 3034, bookUSFM: "JHN", chapter: 3, verse: 16)
)
```

### Verse range

```swift
BibleTextView(
    BibleReference(versionId: 3034, bookUSFM: "JHN", chapter: 3, verseStart: 16, verseEnd: 20)
)
```

### Chapter

```swift
ScrollView {
    BibleTextView(
        BibleReference(versionId: 3034, bookUSFM: "JHN", chapter: 3)
    )
}
```

## Bible reader tab

```swift
BibleReaderView(
    appName: "Sample App",
    signInMessage: "Sign in to see your YouVersion highlights in this Sample App."
)
```

## Sign in flow

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

struct LoginView: View {
    @State private var contextProvider = ContextProvider()

    var body: some View {
        SignInWithYouVersionButton {
            Task {
                do {
                    _ = try await YouVersionAPI.Users.signIn(
                        permissions: [.profile, .email],
                        contextProvider: contextProvider
                    )
                } catch {
                    print(error)
                }
            }
        }
    }
}
```

## Verse of the Day

### Built-in component

```swift
VotdView()
```

### Fetch and customize

```swift
let dayOfYear = Calendar.current.ordinality(of: .day, in: .year, for: Date())!
let votd = try await YouVersionAPI.VOTD.verseOfTheDay(dayOfYear: dayOfYear)
```
