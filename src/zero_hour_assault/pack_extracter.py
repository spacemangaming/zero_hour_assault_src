# pack extractor for python written by nbm studios
from pack_file import *
from security import *
from file_directories import *

pack = input("Please enter the pack name you wish to extract, such as sounds.dat")
if file_exists(pack) == False:
    print("The file does not exist!")
    exit()
if directory_exists("packs") == False:
    directory_create("packs")
directory_create("packs/" + pack)
enc = input(
    "Please enter the encryption key used while creating this pack. If no key, press enter."
)
end = input(
    "Enter anything you want added to the end of the file names, such as .ogg or .wav"
)
print("Searching files ...")
pfile = pack_file()
pfile.open(pack)
list = pfile.list_files()
input(
    "There are " + str(len(list)) + " files in the pack. Hit enter to start extracting!"
)
pattern = "packs/" + pack
filenum = 0
for each in list:
    filenum += 1
    print("file " + str(filenum) + " of " + str(len(list)) + " ...")
    d = pfile.get_file(each.decode())
    with open (pattern + "/" + each.decode() + end, "wb") as f: f.write(d.read()); d.close()
pfile.close()
if enc == "":
    print("done! The pack has been extracted!")
    exit()
print("The pack has been extracted, now decrypting ...")
for each in find_files("packs/" + pack):
    if enc != "":
        file_decrypt(pattern + "/" + each, enc)
print("Done! The pack has been decrypted!")
exit()
