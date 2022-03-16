import os
import hmac
import hashlib
import sqlite3
import socket
import config
from time import gmtime, strftime

def init_database(connection):
    nonce_list = connection.execute("SELECT * FROM nonces").fetchall()
    for nonce in nonce_list:
        if nonce[1]: #comparar que la fecha no sea mas antigua que 1 dia (formatear un datetime con el text almacenado en la base de datos)
            pass
    return None

def search_in_database(connection, nonce):
    nonce_list = connection.execute("SELECT * FROM nonces").fetchall()
    for nonce in nonce_list:
        if nonce[0] == nonce: #Denegar el mensaje
            pass
        else: #Todo ok
            pass

def hash_comparator(socket, challenge, nonce, hash_client, hash_server):
    if hash_client == hash_server:
        lista = [hash_server, calc_hmac(challenge, nonce, hash_server)]
        socket.send(bytes(str(lista),'utf-8'))
    else:
        lista = [hash_server, 'VERIFICATION_HASH_FAIL']
        socket.send(bytes(str(lista),'utf-8'))
    

def populate_database(connection, directorio):
    lista = search_files(directorio)
    connection.execute("drop table if exists nonces")
    #En la creacion de la tabla: create table if not exists nonces
    connection.execute('''create table nonces(
    nonce     text not null,
    date       text not null);''')
    try:
        for file in lista:
            hashsha = hashlib.sha256()
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
            connection.execute('''insert into ficheros values (?,?)''',(file,hashsha.hexdigest())) 
            #En el socket ^         
        connection.commit()
        
    except Exception as e:
        print("Error: %s" % (e))
        return ""

    except:
        print("Error desconocido")
        return ""

def creacion_logs(ok, fail):
    total = ok + fail
    porcentaje_ok = ok/total*100
    porcentaje_fail = fail/total*100

    nombre_log = './logs/'+strftime("%Y-%m-%d %H-%M-%S", gmtime())+'_log.txt'
    with open(str(nombre_log), 'w') as f:
        f.write('Fecha: '+str(strftime("%Y-%m-%d %H-%M-%S", gmtime()))+'\nPorcentaje de ACIERTO: '+str(porcentaje_ok)+'%\nPorcentaje de FALLO: '+str(porcentaje_fail)+'%\nTotal de ficheros: '+str(total)+'\nFicheros modificados: '+str(fail))
    

def calc_hmac(message, key):
    res = hmac.new(key, message, hashlib.sha256)
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
    bd = sqlite3.connect('nonce.db')
    populate_database(bd, config.DIR_SERVER)
    s.bind((config.HOST,config.PORT))
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
            nonce = parseo[2]
            data_db = search_in_database(bd, direccion_archivo)
            sol = hash_comparator(conn,'clave_secreta', nonce , hash_archivo, data_db[1])
    
    '''
    s.connect((config.HOST,config.PORT))
    data = s.recv(4096)
    archivo_a_enviar = get_all_files_and_nonces()
    cont_ok = 0
    cont_fail = 0
    for elemento in archivo_a_enviar:
        #poner el man-in-the-middle aquí
        s.send(bytes(str(elemento), 'utf-8'))
        lista_final = parse(s.recv(4096).decode())
        comparador_mac = mac_comparator(lista_final[1],calc_hmac('clave_secreta',elemento[1], elemento[0][1]))
        if(comparador_mac == 'INTEGRITY_FILE_OK'):
            cont_ok += 1
        else:
            cont_fail += 1
    creacion_logs(cont_ok, cont_fail)
    '''