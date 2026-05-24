# Simple sound unpacker for Zero Hour Assault
import sys
import os

# Add source dirs to sys.path so we can import modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))

from pack_file import pack_file
from security import file_decrypt
from file_directories import directory_exists, directory_create, file_exists

def main():
    pack_name = "sounds.dat"
    output_dir = "unpacked_sounds"
    decryption_key = "asdasdasdasasdasdsa1231232132112321321$$1231231231221321312%*]9CfY%!yfo?3.m]C16(VW:?DB:70v4n7d`tht}jiylhC%L&;ix(Y;9BB?`k-hYhR^=n%C;#kykxV?)GFbzC5x6R<-W?o<c|xQw"

    if not file_exists(pack_name):
        print(f"Error: Could not find '{pack_name}' in the project root directory.")
        return

    if not directory_exists(output_dir):
        directory_create(output_dir)

    print(f"Opening '{pack_name}'...")
    pfile = pack_file()
    try:
        pfile.open(pack_name)
    except Exception as e:
        print(f"Error: Could not parse '{pack_name}': {e}")
        return

    file_list = pfile.list_files()
    total_files = len(file_list)
    print(f"Found {total_files} files in the archive. Starting extraction...")

    for idx, each in enumerate(file_list, start=1):
        filename = each.decode()
        print(f"[{idx}/{total_files}] Extracting and decrypting {filename}...")
        
        # Extract file content in memory
        file_data = pfile.get_file(filename)
        target_path = os.path.join(output_dir, filename)
        
        # Write to disk
        with open(target_path, "wb") as f:
            f.write(file_data.read())
        file_data.close()

        # Decrypt file on disk using the game's official key
        try:
            file_decrypt(target_path, decryption_key)
        except Exception as e:
            print(f"Warning: Failed to decrypt {filename}: {e}")

    pfile.close()
    print(f"\nSuccess! All {total_files} files successfully extracted and decrypted into the '{output_dir}/' folder.")

if __name__ == "__main__":
    main()
