import os
import hmac
import hashlib
import sqlite3
import socket
import re

HOST = "127.0.0.1"
PORT = 3030
DIR = '.\DATA'

#Creamos esta funcion para recorrer todas las carpetas del directorio 
# y obtener asi una lista de todos los ficheros que contienen
def search_files(directorio):
    result = []
    for nombre_directorio, dirs, ficheros in os.walk(directorio):       
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+ '\\' +nombre_fichero)
    return result

def search_in_database(connection, file):
    hash_file_list = connection.execute("SELECT * FROM ficheros").fetchall()
    for elemento in hash_file_list:
        if elemento[0] == file:
            return elemento
        else:
            pass

def hash_comparator(socket, challenge, token, hash_client, hash_server):
    if hash_client == hash_server:
        lista = [hash_server, calc_hmac(challenge, token, hash_server)]
        socket.send(bytes(str(lista),'utf-8'))
    else:
        lista = [hash_server, 'VERIFICATION_HASH_FAIL']
        socket.send(bytes(str(lista),'utf-8'))
    

def populate_database(connection, directorio):
    lista = search_files(directorio)
    connection.execute("drop table if exists ficheros")
    connection.execute('''create table ficheros(
    fichero     text not null,
    hash        text not null);''')
    try:
        for file in lista:
            hashsha = hashlib.sha256()
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
            connection.execute('''insert into ficheros values (?,?)''',(file,hashsha.hexdigest()))          
        connection.commit()
        
    except Exception as e:
        print("Error: %s" % (e))
        return ""

    except:
        print("Error desconocido")
        return ""

def calc_hmac(challenge, token, hashfile):
    mensaje = bytes(str(token) + str(hashfile), 'utf-8')
    challenge = bytes(challenge, 'utf-8')
    res = hmac.new(challenge, mensaje, hashlib.sha256)
    return res.hexdigest()

def parse(cadena):
    cadena = str(cadena)
    cadena = cadena.replace('DATA_CLIENT', 'DATA')
    cadena = cadena.replace('[', '').replace(']', '').replace('\'', '').replace('(', '').replace(')', '').replace(' ', '')
    cadena = cadena.replace('\\', '*')
    cadena = cadena.replace('**', '\\')
    lista = cadena.split(',')
    return lista


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    bd = sqlite3.connect(':memory:')
    populate_database(bd, DIR)
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    conn.send(b'Connected')
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            parseo = parse(data.decode())
            direccion_archivo = parseo[0]
            hash_archivo = parseo[1]
            token = parseo[2]
            data_db = search_in_database(bd, direccion_archivo)
            sol = hash_comparator(conn,'clave_secreta', token , hash_archivo, data_db[1])