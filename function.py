import os
import hmac
import hashlib
import sqlite3
import socket

Host = "127.0.0.1"
Port = 3030
Dir = '.\\DATA'

#Creamos esta funcion para recorrer todas las carpetas del directorio 
# y obtener asi una lista de todos los ficheros que contienen
def search_files (directorio):
    result = []
    for nombre_directorio, dirs, ficheros in os.walk(directorio):       
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+ "\\" +nombre_fichero)
    return result

def serch_in_database(connection, file):
    hash_file_list = connection.execute("SELECT * FROM ficheros").fetchall()
    for elemento in hash_file_list:
        if elemento[0] == file:
            return elemento
        else:
            pass

def hash_comparator(hash_client, hash_server):
    if hash_client == hash_server:
        return 'VERIFICATION_HASH_OK'
    else:
        return 'VERIFICATION_HASH_FAIL'
    

def populate_database(connection, directorio):
    lista = search_files (directorio)
    conn.execute("drop table if exists ficheros")
    conn.execute('''create table ficheros(
    fichero     text not null,
    hash        text not null);''')
    try:
        for file in lista:
            hashsha = hashlib.sha256()
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
                    #challenge = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
            conn.execute('''insert into ficheros values (?,?)''',(file,hashsha.hexdigest()))   
            
        conn.commit()
        #print(str(conn.execute("SELECT * FROM ficheros").fetchall()))
        
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

'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    conn = sqlite3.connect(':memory:')
    populate_database(Dir)
    s.bind((Host,Port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
'''

if __name__ == '__main__':
    conn = sqlite3.connect(':memory:')
    #search_files(ejemplo_dir)
    populate_database(conn, '.\\DATA')
    print(serch_in_database(conn, '.\\DATA\\decide\\decide\\locale\\es\\LC_MESSAGES\\django.mo'))
    #print(calc_hmac('clavisima', 'mensaje ocult'))
    #print(calc_hmac('clavisima', 'mensaje oculto'))
#    print(calc_hmac('CKIZO2', '1','cd5060334b2a8e31719aa3a15433c2e655c84d99f262c058eba4a83f6232e19a'))