# pack creator for python written by nbm studios
from pack_file import *
from security import *
from file_directories import *

folder = input("Please enter the folder that contains the sounds that you want to pack")
key = input("Enter an encryption key. If no key, press enter.")
name = input("Please enter the name of the pack, such as sounds.dat")
print("Searching... please wait...")
if directory_exists(folder) == False:
    print("The folder does not exist!")
    exit()
files = find_files(folder)
if len(files) <= 0:
    print("No files were found!")
    exit()
input(
    "There are " + str(len(files)) + " files on the pack! Hit enter to start packing!"
)
print("Packing files... Please wait... This may take several minutes.")
pack = pack_file()
pack.create(name)
if file_exists(name) == False:
    print("Unable to create the pack!")
    exit()
print("Adding files ...")
filenum = 0
directory_create(folder + "/encrypted")
for file in files:
    filenum += 1
    print("file " + str(filenum) + " of " + str(len(files)) + " ...")
    file_copy(folder + "/" + file, folder + "/encrypted/" + file, True)
    if key != "":
        file_encrypt(folder + "/encrypted/" + file, key)
    pack.add_file(folder + "/encrypted/" + file, file)
    try: file_delete(folder + "/encrypted/" + file)
    except: pass
try: directory_delete(folder + "/encrypted")
except: pass
pack.close()
print("Done! The pack has been created!")
exit()
