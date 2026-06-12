[app]

# (str) Title of your application
title = Zero Hour Assault

# (str) Package name
package.name = zerohourassault

# (str) Package domain (needed for android packaging)
package.domain = com.spacemangaming

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,ogg,wav,txt,json,lng,jkm,dll,so,mhr

# (list) List of exclusions using pattern matching
source.exclude_dirs = tests, bin, server, .venv, .git, cython_cache, release, build, dist, logs, scratch

# (str) Application version
version = 2.50

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.10.12,hostpython3==3.10.12,pygame,websocket-client,pynacl,pycryptodomex,requests,urllib3,certifi,chardet,idna,numpy,deep-translator

# (str) Custom source folders for requirements
# Point to custom sources of requirements if needed

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (list) List of service to declare
#services =

#
# Android specific
#

# (bool) Indicate if the XML export should be blocked
#android.block_xml = False

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data directory (True) or public (False)
android.private_storage = True

# (bool) Accept SDK license without prompting (needed for CI)
android.accept_sdk_license = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded)
#android.ant_path =

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In newer python-for-android versions, arm64-v8a is the standard
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) python-for-android branch to use (defaults to master)
p4a.branch = v2024.01.21


# (list) List of Java files to add to the android project
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Gradle dependencies
#android.gradle_dependencies =

# (list) Packaging options to prevent issues with duplicate files in APK
#android.packaging_options =

# (bool) If True, then skip signup of APK with debug key
#android.skip_apk_signing = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build folder (defaults to <app directory>/.buildozer)
#build_dir = ./.buildozer

# (str) Path to bin directory (defaults to <app directory>/bin)
#bin_dir = ./bin
