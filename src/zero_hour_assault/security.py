# Encryption and decryption functions written by Ivan soto and edited by nbm studios for use on nbm studios projects


from file_directories import *
import hashlib
import pickle as p

from Cryptodome.Cipher import AES
import os, platform, shutil
import subprocess


iv = "flajef8ejri3l25m"


def string_encrypt(data, key):
    encryptor = AES.new(
        hashlib.sha256(key.encode()).digest(), AES.MODE_CFB, iv.encode()
    )
    return encryptor.encrypt(data)


def string_decrypt(data, key):
    decryptor = AES.new(
        hashlib.sha256(key.encode()).digest(), AES.MODE_CFB, iv.encode()
    )
    decryptedData = decryptor.decrypt(data)
    return decryptedData


def file_encrypt(file, key):
    encrypted = string_encrypt(file_get_contents(file, "rb"), key)
    file_put_contents(file, encrypted, "wb")


def file_decrypt(file, key):
    encrypted = file_get_contents(file, "rb")
    decrypted = string_decrypt(encrypted, key)
    file_put_contents(file, decrypted, "wb")


def string_hash(string, method, binary=True):
    string = string.encode()
    if method == 1:
        hash_object = hashlib.sha256(string)
        return hash_object.hexdigest()
    elif method == 2:
        hash_object = hashlib.sha512(string)
        return hash_object.hexdigest()


