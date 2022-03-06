import socket
import os
import hashlib
import uuid
import hmac

Host = "127.0.0.1"
Port = 3030
Dir = ".\\DATA_CLIENT"

def search_files (directorio):
    result = []
    for nombre_directorio, _, ficheros in os.walk(directorio):
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+ "\\" +nombre_fichero)
    return result

def calc_hmac(challenge, token, hashfile):
    mensaje = bytes(str(token) + str(hashfile), 'utf-8')
    challenge = bytes(challenge, 'utf-8')
    res = hmac.new(challenge, mensaje, hashlib.sha256)
    return res.hexdigest()

def get_all_files_and_tokens():
    file_list = []
    files = search_files(Dir)
    for file in files:
        hashsha = hashlib.sha256()
        token = uuid.uuid4().hex
        with open(file, "rb") as f:
            for binary in iter(lambda: f.read(4096), b""):
                hashsha.update(binary)
        file_list.append(((file,hashsha.hexdigest()),token))
    return file_list

def mac_comparator(mac_client, mac_server):
    if mac_client == mac_server:
        return 'INTEGRITY_FILE_OK'
    else:
        return 'INTEGRITY_FILE_FAIL'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((Host,Port))
    data = s.recv(4096)