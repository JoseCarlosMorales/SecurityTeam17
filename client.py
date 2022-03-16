import socket
import os
import hashlib
import uuid
import hmac
import config
from time import gmtime, strftime

def calc_hmac(message, key):
    res = hmac.new(key, message, hashlib.sha256)
    return res.hexdigest()

def create_message(text):
    nonce = uuid.uuid4().hex
    message = str(text) + '|' + str(nonce)
    mac = calc_hmac(message, config.KEY)
    result = bytes(str(message) + ',' + str(mac), 'utf-8')
    return result

def parse(cadena):
    cadena = str(cadena)
    cadena = cadena.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
    lista = cadena.split(',')
    return lista
    


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((config.HOST,config.PORT))
    data = s.recv(4096)
    s.send(bytes(str(elemento), 'utf-8'))