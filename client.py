import socket
import hashlib
import uuid
import hmac
import config
from time import gmtime, strftime

def calc_hmac(message, key):
    key = bytes(key, 'utf-8')
    message = bytes(message, 'utf-8')
    res = hmac.new(key, message, hashlib.sha256)
    return res.hexdigest()

def create_message(text):
    nonce = uuid.uuid4().hex
    message = str(text).replace(' ', '').replace('\n', '') + '|' + str(nonce)
    mac = calc_hmac(message, config.KEY)
    result = bytes(str(message) + ',' + str(mac), 'utf-8')
    return result

def search_message():
    result=[]
    with open('.\DATA\messages_data.txt') as f:
        for linea in f:
            result.append(linea)
    f.close()
    return result

def parse(cadena):
    cadena = str(cadena)
    cadena = cadena.replace('[', '').replace(']', '').replace('\\n', '')
    #lista = cadena.split(',')
    return cadena #lista


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((config.HOST,config.PORT))
    data = s.recv(4096)
    mensajes_a_enviar = search_message()
    cont_ok = 0
    cont_fail = 0
    for elemento in mensajes_a_enviar:
        mensaje = create_message(elemento)
        s.send(mensaje)
        resultado = parse(s.recv(4096).decode())
        print(resultado)
