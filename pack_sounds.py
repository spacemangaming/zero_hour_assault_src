# Simple sound packer and encryptor for Zero Hour Assault
import sys
import os

# Add source dirs to sys.path so we can import modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))

from pack_file import pack_file
from security import file_encrypt
from file_directories import directory_exists, directory_create, directory_delete, file_exists, find_files, file_copy, file_delete

def main():
    input_dir = "unpacked_sounds"
    pack_name = "sounds.dat"
    encryption_key = "asdasdasdasasdasdsa1231232132112321321$$1231231231221321312%*]9CfY%!yfo?3.m]C16(VW:?DB:70v4n7d`tht}jiylhC%L&;ix(Y;9BB?`k-hYhR^=n%C;#kykxV?)GFbzC5x6R<-W?o<c|xQw"

    if not directory_exists(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist in the project root.")
        print(f"Please extract the files first or create the '{input_dir}' folder and populate it with audio files.")
        return

    files = find_files(input_dir)
    total_files = len(files)
    if total_files == 0:
        print(f"Error: No files found inside the '{input_dir}' directory.")
        return

    # If sounds.dat already exists, remove it first
    if file_exists(pack_name):
        print(f"Existing '{pack_name}' found. Overwriting...")
        try:
            os.remove(pack_name)
        except Exception as e:
            print(f"Error: Could not overwrite '{pack_name}': {e}")
            return

    print(f"Creating new archive '{pack_name}'...")
    pack = pack_file()
    try:
        pack.create(pack_name)
    except Exception as e:
        print(f"Error: Could not create pack file: {e}")
        return

    # Create temporary folder for encrypted staging files
    temp_dir = os.path.join(input_dir, "encrypted_temp")
    if not directory_exists(temp_dir):
        directory_create(temp_dir)

    print(f"Starting packing and encryption for {total_files} files...")
    for idx, file in enumerate(files, start=1):
        print(f"[{idx}/{total_files}] Encrypting and packing {file}...")
        
        src_path = os.path.join(input_dir, file)
        temp_path = os.path.join(temp_dir, file)

        # Copy to temp encrypted directory
        file_copy(src_path, temp_path, True)

        # Encrypt the file
        try:
            file_encrypt(temp_path, encryption_key)
        except Exception as e:
            print(f"Error: Failed to encrypt {file}: {e}")
            pack.close()
            return

        # Add to pack archive
        pack.add_file(temp_path, file)

        # Clean up temp file
        try:
            file_delete(temp_path)
        except Exception:
            pass

    # Clean up staging directory
    try:
        directory_delete(temp_dir)
    except Exception:
        pass

    pack.close()
    print(f"\nSuccess! All {total_files} files successfully encrypted and compiled into '{pack_name}'.")

if __name__ == "__main__":
    main()
