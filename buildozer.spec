# buildozer.spec

[buildozer]
log_level = 2

[app]
title                = Webnyeremeny
package.name         = webnyeremeny
package.domain       = org.example

source.dir           = .
entrypoint           = main.py
version              = 0.1.0

android.permissions  = INTERNET, WRITE_EXTERNAL_STORAGE
requirements         = python3,kivy,requests

android.api                  = 27
# bump to NDK r25b
android.ndk                  = 25b
android.build_tools_version  = 34.0.0
android.minapi               = 21

android.archs                = armeabi-v7a, arm64-v8a
android.accept_sdk_licenses  = True

# point at the CI-installed SDK/NDK
android.sdk_path             = /home/runner/android-sdk
android.ndk_path             = /home/runner/android-sdk/ndk/25.2.9519653
