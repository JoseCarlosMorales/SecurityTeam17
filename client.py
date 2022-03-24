import socket
import hashlib
import uuid
import hmac
import config
from time import gmtime, strftime
import re

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
    return cadena

def valida_tester(tester):
    if(tester == "n" or tester == "s"or tester == "N"or tester == "S"):
        return True
    else:
        return False

def valida_cuenta(cuenta):
    pattern = 'ES\w'
    return re.search(pattern, cuenta)

def valida_cantidad(cantidad):
    try:
        num = float(cantidad)
        if num <=0:
            return False
        else:
            return True
    except ValueError:
        return False
    


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((config.HOST,config.PORT))
    data = s.recv(4096)
    valid = False
    print("Desea realizar un test automático (s/n): ", end='')
    while not valid:
        tester = input()
        valid = valida_tester(tester)
        if not valid:
            print("Desea realizar un test automático (s/n): ", end='')
        if valid:
            if(tester == "s" or tester == "S"):
                mensajes_a_enviar = search_message()
                cont_ok = 0
                cont_fail = 0
                for elemento in mensajes_a_enviar:
                    mensaje = create_message(elemento)
                    s.send(mensaje)
                    resultado = parse(s.recv(4096).decode())
                    print(resultado)
            else:
                valid_cuenta = False
                while not valid_cuenta:
                    origen = input("Cuenta Origen: ")
                    val_or = valida_cuenta(origen)
                    destino = input("Cuenta destino: ")
                    val_des = valida_cuenta(destino)
                    valid_cuenta = val_or and val_des
                    if not valid_cuenta:
                        print("ERROR: Una o más cuentas son incorrectas, deben comenzar por ES \n")
                    else:
                        valid_cantidad = False
                        while not valid_cantidad:
                            cantidad = input("Cantidad: ")
                            valid_cantidad = valida_cantidad(cantidad)
                            if not valid_cantidad:
                                print("ERROR: Introduza una cantidad valida \n")
                            else:
                                content = origen + " " + destino + " " + cantidad
                                mensaje = create_message(content)
                                s.send(mensaje)
                                resultado = parse(s.recv(4096).decode())
                                print(resultado)
        
    
