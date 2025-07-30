# buildozer.spec

[buildozer]
# (int) Log level (0 = error only, 2 = warning, 4 = info, 6 = debug)
log_level = 2

[app]
# (str) Title of your application
title                = Webnyeremeny
# (str) Package name
package.name         = webnyeremeny
# (str) Package domain (reverse DNS notation)
package.domain       = org.example

# (str) Where your Python code lives
source.dir           = .
# (str) Python entry point, relative to source.dir
entrypoint           = main.py

# (str) Application version
version              = 0.1.0

# (list) Permissions
android.permissions  = INTERNET, WRITE_EXTERNAL_STORAGE
# (list) Python modules to include in the APK
requirements         = python3,kivy,requests

# Android build configuration
android.api                  = 27
android.ndk                  = 23b
android.build_tools_version  = 34.0.0
android.minapi               = 21

# (list) Architectures to build for (comma-separated)
android.archs                = armeabi-v7a, arm64-v8a

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_licenses  = True
