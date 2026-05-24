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
        f.write(content)
        f.close()
        return True
    except: return False
def file_get_contents(filename, mode="r",encoding=""):
    try:
        ret = ""
        if file_exists(filename) == False:
            return ""
        if encoding == "": f = open(filename, mode)
        if encoding != "": f = open(filename, mode, encoding=encoding)
        ret = f.read()
        f.close()
        return ret
    except: return ""