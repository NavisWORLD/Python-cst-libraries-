# CST Cosmic Mobile

Capacitor 8 mobile shell for CST Libraries. The reference UI implements local Dyn12-style state evolution, Gaussian relationship diagnostics, and durable on-device memory while the native host can be extended with platform sensors or remote/local CST adapters.

## Run the web layer
Open `web/index.html` in a browser for the UI logic.

## Android
```bash
npm install
npx cap add android
npx cap sync android
cd android
./gradlew assembleDebug
```

## iOS
Requires macOS + Xcode.
```bash
npm install
npx cap add ios
npx cap sync ios
npx cap open ios
```

The GitHub release workflow builds an Android APK and unsigned iOS simulator/device artifacts. A stock iPhone requires Apple signing/provisioning before a device IPA can be installed.
