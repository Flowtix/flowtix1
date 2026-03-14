[app]

title = AtlasUploader
package.name = atlasuploader
package.domain = org.atlas

source.dir = .
source.include_exts = py,kv

version = 1.0

requirements = python3,kivy,yt-dlp,google-api-python-client,google-auth-oauthlib

orientation = portrait

android.api = 31
android.minapi = 21

android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET

p4a.branch = develop

log_level = 2