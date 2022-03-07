import socket
import os
import hashlib
import uuid
import hmac
from time import gmtime, strftime

Host = '127.0.0.1'
Port = 3030
Dir = '.\DATA_CLIENT'


def search_files(directorio):
    result = []
    for nombre_directorio, _, ficheros in os.walk(directorio):
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+ '\\' +nombre_fichero)
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

def parse(cadena):
    cadena = str(cadena)
    cadena = cadena.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
    lista = cadena.split(',')
    return lista
    

def creacion_logs(ok, fail):
    total = ok + fail
    porcentaje_ok = ok/total*100
    porcentaje_fail = fail/total*100
    
    nombre_log = './logs/'+strftime("%Y-%m-%d %H-%M-%S", gmtime())+'_log.txt'
    with open(str(nombre_log), 'w') as f:
        f.write('Fecha: '+str(strftime("%Y-%m-%d %H-%M-%S", gmtime()))+'\nPorcentaje de ACIERTO: '+str(porcentaje_ok)[:-10]+'%\nPorcentaje de FALLO: '+str(porcentaje_fail)[:-10]+'%')
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((Host,Port))
    data = s.recv(4096)
    archivo_a_enviar = get_all_files_and_tokens()
    cont_ok = 0
    cont_fail = 0
    for elemento in archivo_a_enviar:
        s.send(bytes(str(elemento), 'utf-8'))
        lista_final = parse(s.recv(4096).decode())
        comparador_mac = mac_comparator(lista_final[1],calc_hmac('clave_secreta',elemento[1], elemento[0][1]))
        if(comparador_mac == 'INTEGRITY_FILE_OK'):
            cont_ok += 1
        else:
            cont_fail += 1
    creacion_logs(cont_ok, cont_fail)