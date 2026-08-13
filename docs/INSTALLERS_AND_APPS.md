# Installers and Applications Manual

## Windows
Download `CST-Libraries-Windows-Setup.exe` from the latest packaged GitHub Release. The installer writes CST Studio to the current user's local application directory and creates Start Menu/Desktop shortcuts. No administrator privilege is required.

## macOS
Download `CST-Libraries-macOS.dmg`, open it, and launch `CST Studio.app`. CI applies an ad-hoc signature. Public distribution without Gatekeeper warnings requires an Apple Developer ID certificate and notarization credentials.

## Android
Download `CST-Cosmic-Mobile-Android.apk`. The release workflow builds the native Capacitor Android project on GitHub's Ubuntu runner. Android may require the user to allow installation from the browser/file manager used to open the APK.

## iPhone / iPad
The project contains the complete Capacitor iOS source and CI builds both a Simulator app and an unsigned iPhoneOS IPA. Apple requires a valid signing identity and provisioning profile for installation on normal physical iPhones, TestFlight, or the App Store. Add those credentials as repository secrets and extend the signing step; do not commit certificates or private keys.

## Desktop app architecture
`apps/desktop/cst_studio.py` is a dependency-light Tk application that imports the same `cstlib` package developers use directly. PyInstaller freezes it into native desktop bundles.

## Mobile architecture
`apps/mobile/` contains a Capacitor application. Its web layer provides on-device state and memory experiments without a network dependency. Native Capacitor hosts make future camera, microphone, motion, Bluetooth, or local-network adapters possible while keeping permissions explicit.

## Release automation
`.github/workflows/release.yml` builds all supported platform assets and creates/updates the `v0.3.0` GitHub Release. Release artifacts are generated from clean GitHub-hosted runners so a developer does not need Windows, macOS, Android Studio, and Xcode on one machine.
