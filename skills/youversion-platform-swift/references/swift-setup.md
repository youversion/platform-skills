# Minimal Swift SDK setup

Use this when the user needs quick project setup before feature implementation.

## Requirements

- iOS 17+ / iPadOS 17+
- YouVersion Platform app key from https://platform.youversion.com/

## Swift Package Manager (recommended)

In Xcode:
1. File → Add Package Dependencies
2. Add: `https://github.com/youversion/platform-sdk-swift.git`
3. Select package and add to target

Or in `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/youversion/platform-sdk-swift.git", from: "0.1.0")
]
```

## CocoaPods option

```ruby
pod 'YouVersionPlatform', '~> 1.0'
```

Then run:

```bash
pod install
```

## Minimum app bootstrap

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

## First sanity check view

```swift
import SwiftUI
import YouVersionPlatform

struct ContentView: View {
    var body: some View {
        ScrollView {
            BibleTextView(
                BibleReference(versionId: 3034, bookUSFM: "JHN", chapter: 3, verse: 16)
            )
            .padding()
        }
    }
}
```
