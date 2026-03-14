[app]

title = Flowtix
package.name = flowtix
package.domain = org.flowtix

source.dir = .
source.include_exts = py,kv,json

version = 1.0

requirements = python3,kivy,yt-dlp,google-api-python-client,google-auth,google-auth-oauthlib,google-auth-httplib2

orientation = portrait

fullscreen = 0

log_level = 2

# Android settings

android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET

android.archs = arm64-v8a, armeabi-v7a

# Packaging

p4a.branch = master

android.release_artifact = apk

# Python for Android

p4a.bootstrap = sdl2

# Include files

source.include_patterns = *.py,*.kv,*.json

# App entry

entrypoint = main.py
