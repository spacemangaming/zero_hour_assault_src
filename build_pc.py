import os
import sys
import shutil
import subprocess
import hashlib
import zipfile

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"Command failed with exit code {res.returncode}")
        sys.exit(res.returncode)

def main():
    # Define files and their relative paths from src/zero_hour_assault
    cython_mappings = {
        "zero_hour_assault.py": "src/zero_hour_assault/zero_hour_assault.py",
        "sign.py": "src/zero_hour_assault/utils/sign.py",
        "moving_sound_client_handler.py": "src/zero_hour_assault/utils/moving_sound_client_handler.py",
        "ticket_dialogs.py": "src/zero_hour_assault/ui/ticket_dialogs.py",
        "joystick.py": "src/zero_hour_assault/ui/joystick.py",
        "internet.py": "src/zero_hour_assault/utils/internet.py",
        "audio.py": "src/zero_hour_assault/audio/audio.py",
        "buffer.py": "src/zero_hour_assault/utils/buffer.py",
        "cid.py": "src/zero_hour_assault/utils/cid.py",
        "constants.py": "src/zero_hour_assault/core/constants.py",
        "dlg.py": "src/zero_hour_assault/ui/dlg.py",
        "dlgplay.py": "src/zero_hour_assault/ui/dlgplay.py",
        "door.py": "src/zero_hour_assault/utils/door.py",
        "downloader.py": "src/zero_hour_assault/utils/downloader.py",
        "events.py": "src/zero_hour_assault/core/events.py",
        "file_directories.py": "src/zero_hour_assault/utils/file_directories.py",
        "globals.py": "src/zero_hour_assault/core/globals.py",
        "inventory.py": "src/zero_hour_assault/utils/inventory.py",
        "key_hold.py": "src/zero_hour_assault/ui/key_hold.py",
        "map.py": "src/zero_hour_assault/utils/map.py",
        "menu.py": "src/zero_hour_assault/ui/menu.py",
        "menu_system.py": "src/zero_hour_assault/ui/menu_system.py",
        "Miscellaneous.py": "src/zero_hour_assault/utils/Miscellaneous.py",
        "net.py": "src/zero_hour_assault/net/net.py",
        "network.py": "src/zero_hour_assault/net/network.py",
        "oal.py": "src/zero_hour_assault/audio/oal.py",
        "pack_file.py": "src/zero_hour_assault/utils/pack_file.py",
        "player.py": "src/zero_hour_assault/utils/player.py",
        "rotation.py": "src/zero_hour_assault/utils/rotation.py",
        "savedata.py": "src/zero_hour_assault/utils/savedata.py",
        "security.py": "src/zero_hour_assault/utils/security.py",
        "sound.py": "src/zero_hour_assault/audio/sound.py",
        "sound_pool.py": "src/zero_hour_assault/audio/sound_pool.py",
        "sound_positioning.py": "src/zero_hour_assault/audio/sound_positioning.py",
        "source.py": "src/zero_hour_assault/audio/source.py",
        "speech.py": "src/zero_hour_assault/audio/speech.py",
        "timer.py": "src/zero_hour_assault/utils/timer.py",
        "translation.py": "src/zero_hour_assault/utils/translation.py",
        "updater.py": "src/zero_hour_assault/net/updater.py",
        "variable_management.py": "src/zero_hour_assault/utils/variable_management.py",
        "vector.py": "src/zero_hour_assault/utils/vector.py",
        "input.py": "src/zero_hour_assault/ui/input.py"
    }

    print("Cythonizing files...")
    for filename, filepath in cython_mappings.items():
        if os.path.exists(filepath):
            dir_name = os.path.dirname(filepath)
            base_name = os.path.basename(filepath)
            print(f"Cythonizing {filepath} in {dir_name}...")
            # Run Cythonize inside the file's directory so it places the build and pyd files locally
            run_cmd([sys.executable, "-m", "Cython.Build.Cythonize", "-3", "-i", base_name], cwd=dir_name)
        else:
            print(f"Warning: File {filepath} not found, skipping cythonization.")

    print("Building with pyinstaller...")
    pyinstaller_args = [sys.executable, "-m", "PyInstaller", "--clean", "--noupx", "main.py", "--windowed"]
    
    # Add version file if it exists
    if os.path.exists("app_info.txt"):
        pyinstaller_args += ["--version-file", "app_info.txt"]
    
    # Add paths so PyInstaller finds the cythonized modules
    pyinstaller_args += [
        "--paths", "src",
        "--paths", "src/zero_hour_assault",
        "--paths", "src/zero_hour_assault/audio",
        "--paths", "src/zero_hour_assault/core",
        "--paths", "src/zero_hour_assault/net",
        "--paths", "src/zero_hour_assault/ui",
        "--paths", "src/zero_hour_assault/utils"
    ]
    
    run_cmd(pyinstaller_args)

    # Clean up cython generated files (.c files and .pyd files from source folders)
    # print("Cleaning up cython build files...")
    # for filename, filepath in cython_mappings.items():
    #     dir_name = os.path.dirname(filepath)
    #     name_no_ext = os.path.splitext(filename)[0]
    #     # remove .c files
    #     c_file = os.path.join(dir_name, name_no_ext + ".c")
    #     if os.path.exists(c_file):
    #         os.remove(c_file)
    #     # remove build folders inside subdirectories
    #     build_dir = os.path.join(dir_name, "build")
    #     if os.path.exists(build_dir) and os.path.isdir(build_dir):
    #         shutil.rmtree(build_dir)

    # Rename the output executable to zero_hour_assault.exe
    dist_main_dir = os.path.join("dist", "main")
    if os.path.exists(dist_main_dir):
        old_exe = os.path.join(dist_main_dir, "main.exe")
        new_exe = os.path.join(dist_main_dir, "zero_hour_assault.exe")
        if os.path.exists(old_exe):
            if os.path.exists(new_exe):
                os.remove(new_exe)
            os.rename(old_exe, new_exe)

    # Create release folder
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)

    print("Copying files to release directory...")
    # Copy all files from dist/main to release
    shutil.copytree(dist_main_dir, release_dir, dirs_exist_ok=True)

    # Copy lang folder
    if os.path.exists("lang"):
        shutil.copytree("lang", os.path.join(release_dir, "lang"), dirs_exist_ok=True)

    # Copy packs folder if exists
    if os.path.exists("packs"):
        shutil.copytree("packs", os.path.join(release_dir, "packs"), dirs_exist_ok=True)


    # Copy dlls to both release/ (root) and release/_internal/ (dependencies)
    internal_dir = os.path.join(release_dir, "_internal")
    os.makedirs(internal_dir, exist_ok=True)
    dll_files = [
        "OpenAL32.dll", "SRAL.dll", "phonon.dll", "anticheat.dll",
        "nvdaControllerClient.dll", "opus.dll", "portaudio.dll"
    ]
    for dll in dll_files:
        if os.path.exists(dll):
            shutil.copy(dll, os.path.join(release_dir, dll))
            shutil.copy(dll, os.path.join(internal_dir, dll))

    # Copy FMOD DLLs from third_party/fmod/
    fmod_src_dir = os.path.join("third_party", "fmod")
    fmod_dlls = ["fmod.dll", "fmodstudio.dll"]
    for dll in fmod_dlls:
        src_dll = os.path.join(fmod_src_dir, dll)
        if os.path.exists(src_dll):
            shutil.copy(src_dll, os.path.join(release_dir, dll))
            shutil.copy(src_dll, os.path.join(internal_dir, dll))
            print(f"Bundled FMOD DLL: {dll}")
        else:
            print(f"Warning: FMOD DLL {src_dll} not found.")

    # Copy VC++ runtime DLLs from Python directory to prevent python312.dll loading crashes on clean systems
    search_dirs = [
        sys.base_exec_prefix,
        sys.exec_prefix,
        os.path.dirname(sys.executable),
        os.path.join(sys.base_exec_prefix, "DLLs")
    ]
    for dll in ["vcruntime140.dll", "vcruntime140_1.dll"]:
        found = False
        for d in search_dirs:
            python_dll = os.path.join(d, dll)
            if os.path.exists(python_dll):
                shutil.copy(python_dll, os.path.join(internal_dir, dll))
                print(f"Bundled: {dll} from {d}")
                found = True
                break
        if not found:
            print(f"Warning: Could not find {dll} in any search directories.")

    # Copy other root files to release
    root_copy_files = [
        "sndver.txt", "sndversion.txt", "changelog.txt", "readme.html",
        "rules.txt", "privacy.txt", "zero_hour_assault.jkm"
    ]
    for file in root_copy_files:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(release_dir, file))

    # Try signing executable
    if os.path.exists("nbm_digital_ltd.pfx"):
        print("Signing executable...")
        signtool_path = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"
        if os.path.exists(signtool_path):
            run_cmd([signtool_path, "sign", "/f", "nbm_digital_ltd.pfx", "/fd", "SHA256", "/t", "http://timestamp.digicert.com", os.path.join(release_dir, "zero_hour_assault.exe")])
        else:
            print("signtool.exe not found, skipping signing.")
    else:
        print("nbm_digital_ltd.pfx not found, skipping signing.")

    # Package update_package.zip (WITHOUT sounds.dat and without raw sounds directory to keep size small)
    print("Packaging update_package.zip...")
    update_zip_path = "update_package.zip"
    if os.path.exists(update_zip_path):
        os.remove(update_zip_path)
    
    with zipfile.ZipFile(update_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            rel_root = os.path.relpath(root, release_dir)
            if rel_root == "sounds" or rel_root.replace("\\", "/").startswith("sounds/"):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, rel_path)

    # Compute SHA-256 hash of update_package.zip
    print("Calculating SHA-256 for update_package.zip...")
    sha256 = hashlib.sha256()
    with open(update_zip_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    hash_hex = sha256.hexdigest().lower()
    with open("update_package.zip.sha256", "w") as f:
        f.write(hash_hex)
    print(f"Hash: {hash_hex}")

    # Copy sounds.dat to release and package zero_hour_assault.zip
    if os.path.exists("sounds.dat"):
        print("Copying sounds.dat to release...")
        shutil.copy("sounds.dat", os.path.join(release_dir, "sounds.dat"))
    else:
        print("Warning: sounds.dat not found, full package will not contain it.")

    print("Packaging zero_hour_assault.zip...")
    full_zip_path = "zero_hour_assault.zip"
    if os.path.exists(full_zip_path):
        os.remove(full_zip_path)

    with zipfile.ZipFile(full_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, rel_path)

    # Clean up cython .pyd files from source folders to avoid cluttering git working tree
    # print("Removing temporary compiled .pyd files from source folders...")
    # for filename, filepath in cython_mappings.items():
    #     dir_name = os.path.dirname(filepath)
    #     name_no_ext = os.path.splitext(filename)[0]
    #     for f in os.listdir(dir_name):
    #         if f.startswith(name_no_ext) and f.endswith(".pyd"):
    #             try:
    #                 os.remove(os.path.join(dir_name, f))
    #             except Exception as e:
    #                 print(f"Could not remove temporary file {f}: {e}")

    print("Build complete!")

if __name__ == "__main__":
    main()
