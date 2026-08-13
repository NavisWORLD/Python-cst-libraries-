# CST Libraries v0.3.0 — Packaged Apps

This release turns the CST Libraries repository into a downloadable application suite in addition to the Python, C++17, Cosmic Rust, and CST-L developer libraries.

## Release assets

- `CST-Libraries-Windows-Setup.exe` — one-click per-user Windows installer.
- `CST-Libraries-macOS.dmg` — macOS disk image containing the CST Studio `.app`.
- `CST-Libraries-macOS.app.zip` — zipped macOS application bundle.
- `CST-Cosmic-Mobile-Android.apk` — installable Android APK built by GitHub Actions.
- `CST-Cosmic-Mobile-iOS-Simulator.app.zip` — iOS Simulator application.
- `CST-Cosmic-Mobile-iOS-UNSIGNED.ipa` — unsigned iPhoneOS package for signing/provisioning workflows. It is not installable on a stock iPhone until signed with an Apple Developer identity and provisioning profile.
- Python wheel and source distribution.

## Apple signing boundary

The macOS app is ad-hoc signed in CI so the bundle is structurally signed, but it is not Apple-notarized. The iPhone application source and unsigned build are complete; App Store/TestFlight/direct device installation require Apple Developer credentials that cannot be fabricated by the repository.

## What the apps expose

CST Studio provides a local state lab, durable semantic memory controls, synaptic/kernel diagnostics, runtime health, and builder information. The mobile experience uses local device storage and a portable Dyn12-style state laboratory, with host integration points available for future sensors and adapters.
