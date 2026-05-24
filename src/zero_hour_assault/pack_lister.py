import os
from tkinter import Tk, filedialog, messagebox

class PackFile:
    def open(self, filename):
        if not os.path.isfile(filename):
            return False
        self.filename = filename
        return True

    def list_files(self):
        # Dummy implementation for listing files in the pack file
        # In a real implementation, this should read and return file names from the pack file
        return ["sound1.ogg", "sound2.ogg", "sound3.ogg"]

def string_replace(string, old, new, replace_all=True):
    return string.replace(old, new)

def clipboard_copy_text(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update() # now it stays on the clipboard after the window is closed
    r.destroy()

def main():
    obj = PackFile()

    # Open file dialog to select the pack file
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename(title="Simple pack lister", filetypes=(("Pack files", "*.dat"), ("All files", "*.*")))

    if not filename:
        return

    success = obj.open(filename)
    if not success:
        messagebox.showerror("Error", "Either this file does not exist or it is not a valid pack file")
        return

    final_list = ""
    file_list = obj.list_files()

    for file in file_list:
        final_list += string_replace(file, ".ogg", "") + "\r\n"

    final_list += f"total files: {len(file_list)}\r\n"
    clipboard_copy_text(final_list)
    messagebox.showinfo("Complete!", "The sound list is now on your clipboard.")

if __name__ == "__main__":
    main()
