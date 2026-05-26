import os
import sys
from collections import defaultdict

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip module is required but not installed.")
    print("Please install it using: pip install pyperclip")
    sys.exit(1)


def count_extensions(include_noext=False):
    current_dir = os.getcwd()
    ext_counts = defaultdict(int)

    for root, dirs, files in os.walk(current_dir):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext:
                ext_name = ext[1:].lower()
                ext_counts[ext_name] += 1
            elif include_noext:
                ext_counts['<noext>'] += 1

    return ext_counts


def get_file_extensions():
    print("\nFile extension statistics in current folder:")
    stats = count_extensions(include_noext=True)  # noext her zaman gösterilsin
    if not stats:
        print("No files found.")
    else:
        for ext, count in sorted(stats.items(), key=lambda x: -x[1]):
            print(f"{ext}: {count}")
    print()

    while True:
        user_input = input("Enter file extensions separated by spaces (e.g., txt md py), or 'noext' for files without extensions: ").strip()
        if not user_input:
            print("Please enter at least one file extension.")
            continue

        extensions = set()
        include_noext = False
        for ext in user_input.split():
            if ext.lower() == "noext":
                include_noext = True
            else:
                clean_ext = ext.lstrip('.').lower()
                if clean_ext:
                    extensions.add(clean_ext)

        if extensions or include_noext:
            return extensions, include_noext
        else:
            print("No valid extensions found. Please try again.")


def should_include_file(filename, target_extensions, include_noext):
    name, ext = os.path.splitext(filename)
    if ext:
        return ext[1:].lower() in target_extensions
    else:
        return include_noext


def read_file_safely(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[Error reading file: {str(e)}]"
    return "[Error: Unable to read file with any supported encoding]"


def collect_files_content(target_extensions, include_noext):
    final_content = []
    files_processed = 0
    current_dir = os.getcwd()
    print(f"\nScanning directory: {current_dir}")
    print(f"Looking for extensions: {', '.join(sorted(target_extensions))}" + (" + noext" if include_noext else ""))
    print()

    for root, dirs, files in os.walk(current_dir):
        for filename in files:
            if should_include_file(filename, target_extensions, include_noext):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, current_dir)
                print(f"Processing: {relative_path}")
                final_content.append(f"=== {relative_path} ===")
                file_content = read_file_safely(file_path)
                final_content.append(file_content)
                final_content.append("")  # Newline
                files_processed += 1

    print(f"\nProcessed {files_processed} files.\n")
    return "\n".join(final_content)


def main():
    print("File Content Collector")
    print("=" * 40)

    try:
        extensions, include_noext = get_file_extensions()

        combined_content = collect_files_content(extensions, include_noext)
        if combined_content.strip():
            pyperclip.copy(combined_content)
            print("Content has been copied to clipboard!")

            preview_length = 200
            if len(combined_content) > preview_length:
                print(f"\nPreview (first {preview_length} characters):")
                print(combined_content[:preview_length] + "...")
            else:
                print(f"\nComplete content:")
                print(combined_content)
        else:
            print("No matching files found.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
