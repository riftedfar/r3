# XenoCord V8 — Safe Audio Lab

A clean Android audio-control prototype built from scratch. This is **not** a modified Discord client and does not require Discord credentials.

## Included
- Dark, responsive Android UI
- Local audio test tone with adjustable pitch and output level
- Optional Android audio-session effects: bass boost, virtualizer, and equalizer
- Graceful handling when a device does not support an effect
- Local-only settings; no account login, analytics, ads, or network permission
- GitHub Actions workflow to build a debug APK

## Important limitations
Android audio effects created by this app apply to this app's own audio session. They do not automatically process Discord's microphone or output. A normal Android app cannot reliably inject processing into another app's audio stream without a supported system-level route.

This repository does not contain the original XenoCord V5 source code, so V8 is a clean prototype rather than a verified source-level upgrade of V5. Features that depended on private Discord APIs, client injection, or token-based login are intentionally not reproduced.

## Build
Open this project in Android Studio, or run:
```bash
gradle assembleDebug
```
Use JDK 17 and Android SDK platform 35. The generated APK is at `app/build/outputs/apk/debug/app-debug.apk`.

## Safety
- No Discord token or password fields
- No network permissions
- No background service
- No microphone permission
- No claims of zero bugs; test on your device before relying on it
