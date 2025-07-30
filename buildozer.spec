[app]

# (str) Title of your application
title = Webnyeremeny

# (str) Package name
package.name = webnyeremeny

# (str) Package domain (unique)
package.domain = org.webnyeremeny.app

# (str) Source code where main.py is located
source.dir = .

# (str) The main .py file to use as the entry point
source.main = main.py

# (str) Version number
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd,pandas,requests,beautifulsoup4

# (str) Custom source folders for requirements
# (empty for now)
requirements.source = 

# (list) Include these files in the APK
source.include_exts = py,kv,png,jpg,txt,csv

# (list) Include specific files/folders
include_patterns = assets/*,*.csv,*.txt

# (str) Application icon
icon.filename = %(source.dir)s/assets/logos/placeholder.png

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Supported orientation (portrait, landscape, all)
orientation = portrait

# (str) Android entry point, defaults to ok
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android permissions (none needed now, but add if scraping/storage used)
android.permissions = INTERNET

# (str) Android NDK API (use 27 for compatibility)
android.api = 27
android.ndk = 23b

# (str) Build tool version
android.build_tools_version = 34.0.0

# (str) Minimum API your APK will support
android.minapi = 21

# (str) Android SDK version to compile against
android.sdk = 34

# (str) Android NDK directory (optional)
# android.ndk_path = 

# (str) Android SDK directory (optional)
# android.sdk_path = 

# (list) Java .jar files to add
android.add_jars =

# (str) Architectures to build for
android.arch = armeabi-v7a, arm64-v8a

# (str) Package format (currently only "apk")
android.package_format = apk

# (str) Path to a keystore file
#android.release_keyalias = mykey
#android.release_keystore = mykey.keystore

[buildozer]

# (str) Path to build output
build_dir = ./.buildozer

# (str) Log level
log_level = 2

# (bool) Show log from adb logcat
logcat = 1
