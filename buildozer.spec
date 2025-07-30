# buildozer.spec

[app]
# (str) Title of your application
title = Webnyeremeny

# (str) Package name
package.name = webnyeremeny

# (str) Package domain (reverse DNS notation)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

[buildozer]
# (int) Log level (0 = error only, 2 = warning, 4 = info, 6 = debug)
log_level = 2

[app]
# (str) Python entry point, relative to source.dir
entrypoint = main.py

# (list) Python modules to include in the APK
requirements = python3,kivy,requests

# (str) Android API to target
android.api = 27

# (str) Android NDK version to use
android.ndk = 23b

# (str) Android build tools version
android.build_tools_version = 34.0.0

# (int) Minimum Android API your APK will support
android.minapi = 21

# (list) Architectures to build for (comma-separated)
android.archs = armeabi-v7a, arm64-v8a

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_licenses = True

# (list) Java .jars to add (optional)
# android.add_jars = some_lib.jar

# (list) Gradle dependencies to add (optional)
# android.gradle_dependencies = 'com.android.support:appcompat-v7:27.1.1'

# (str) Android entry point, default is ok
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok
# android.theme = '@android:style/Theme.NoTitleBar'

[buildozer:android]
# (bool) Copy library instead of making libpymodules.so
# android.copy_libs = 1
