# Simple sound unpacker for Zero Hour Assault
import sys
import os

# Get script location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add source directories to Python path
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault", "utils"))

from pack_file import pack_file
from security import file_decrypt
from file_directories import (
    directory_exists,
    directory_create,
    file_exists
)


def main():
    pack_name = "sounds.dat"
    output_dir = "unpacked_sounds"

    decryption_key = (
        "asdasdasdasasdasdsa1231232132112321321$$1231231231221321312"
        "%*]9CfY%!yfo?3.m]C16(VW:?DB:70v4n7d`tht}jiylhC%L&;ix(Y;9BB?"
        "`k-hYhR^=n%C;#kykxV?)GFbzC5x6R<-W?o<c|xQw"
    )

    if not file_exists(pack_name):
        print(f"Error: Could not find '{pack_name}'.")
        return

    if not directory_exists(output_dir):
        directory_create(output_dir)

    print(f"Opening '{pack_name}'...")

    pfile = pack_file()

    try:
        pfile.open(pack_name)

        file_list = pfile.list_files()
        total_files = len(file_list)

        print(f"Found {total_files} files in archive.")

        for idx, entry in enumerate(file_list, start=1):
            try:
                filename = (
                    entry.decode("utf-8", errors="replace")
                    if isinstance(entry, bytes)
                    else str(entry)
                )

                print(f"[{idx}/{total_files}] Extracting {filename}")

                target_path = os.path.join(output_dir, filename)

                # Create subdirectories if needed
                target_dir = os.path.dirname(target_path)
                if target_dir:
                    os.makedirs(target_dir, exist_ok=True)

                file_data = pfile.get_file(filename)

                with open(target_path, "wb") as f:
                    f.write(file_data.read())

                file_data.close()

                try:
                    file_decrypt(target_path, decryption_key)
                except Exception as decrypt_error:
                    print(
                        f"Warning: Failed to decrypt "
                        f"{filename}: {decrypt_error}"
                    )

            except Exception as extract_error:
                print(f"Error extracting {filename}: {extract_error}")

    except Exception as e:
        print(f"Failed to open archive: {e}")

    finally:
        try:
            pfile.close()
        except Exception:
            pass

    print(f"\nFinished. Extracted files are in '{output_dir}'.")


if __name__ == "__main__":
    main()