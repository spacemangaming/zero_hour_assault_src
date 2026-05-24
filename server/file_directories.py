# directory functions written by nbm studios
import os
import shutil


def directory_create(path):
    try:
        os.mkdir(path)
        return True
    except:
        return False


def directory_delete(path):
    try:
        shutil.rmtree(path)
        return True
    except:
        return False
import os

def directory_exists2(path):
    # Normalize the path to avoid issues with trailing slashes
    path = os.path.normpath(path)

    # Get the directory name and the target folder name
    parent_dir, target_dir = os.path.split(path)
    
    # If the parent directory doesn't exist, return False
    if not os.path.isdir(parent_dir):
        return False

    # List all entries in the parent directory
    for entry in os.listdir(parent_dir):
        # Compare case-insensitively
        if entry.lower() == target_dir.lower() and os.path.isdir(os.path.join(parent_dir, entry)):
            return True

    return False

def directory_exists(path):
    return os.path.isdir(path)


def file_exists(path):
    return os.path.isfile(path)

def find_files(path):
    l = []
    for each in os.listdir(path):
        if os.path.isfile(path + "/" + each):
            l.append(each)
    return l


def find_directories(path):
    l = []
    for each in os.listdir(path):
        if os.path.isdir(path + "/" + each):
            l.append(each)
    return l


def file_copy(path, dest, overwrite=False):
    if overwrite == False and os.path.isfile(path):
        return False
    else:
        shutil.copy(path, dest)
        return True


def file_delete(path):
    if os.path.isfile(path):
        os.remove(path)
        return True
    else:
        return False


def find_recursive(path, wildcard="*.*"):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if wildcard in file or wildcard == "*.*":
                files.append(os.path.join(r, file))

    return files


def file_put_contents(filename, content, mode="w"):
    try:
        f = open(filename, mode)
    except: return False
    f.write(content)
    f.close()


def file_get_contents(filename, mode="r"):
    ret = ""
    if file_exists(filename) == False:
        return ""
    f = open(filename, mode)
    ret = f.read()
    f.close()
    return ret
