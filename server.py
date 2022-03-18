from datetime import datetime
import hmac
import hashlib
import sqlite3
import socket
import config
from time import gmtime, strftime

def init_database(connection):
    connection.execute('''create table if not exists nonces(
    nonce     text not null,
    date       text not null);''')
    nonce_list = connection.execute("SELECT * FROM nonces").fetchall()
    if not nonce_list:
        return 
    today = datetime.now()
    for nonce in nonce_list:
        date = datetime.strptime(nonce[1], '%d/%m/%y %H:%M:%S')
        if (date.day - today.day) < 0 or (date.month - today.month) < 0 or (date.year - today.year) < 0:
            connection.execute("DELETE FROM nonces WHERE nonce=?", (nonce[0],))

def search_nonce_in_database(connection, Nonce):
    nonce_list = connection.execute("SELECT * FROM nonces").fetchall()
    for nonce in nonce_list:
        if nonce[0] == Nonce: #Denegar el mensaje
            return "CONFIDENTIALITY_VIOLATED"

def hmac_comparator(hmac_client, hmac_server):
    if hmac_client == hmac_server:
        return "HMAC_OK"
    else:
        return "HMAC_FAIL"

def creacion_logs(ok, fail):
    total = ok + fail
    porcentaje_ok = ok/total*100
    porcentaje_fail = fail/total*100

    nombre_log = './logs/'+strftime("%Y-%m-%d %H-%M-%S", gmtime())+'_log.txt'
    with open(str(nombre_log), 'w') as f:
        f.write('Fecha: '+str(strftime("%Y-%m-%d %H-%M-%S", gmtime()))+'\nPorcentaje de ACIERTO: '+str(porcentaje_ok)+'%\nPorcentaje de FALLO: '+str(porcentaje_fail)+'%\nTotal de transacciones: '+str(total)+'\nTransacciones correctas: '+str(ok)+'\nTransacciones erroneas: '+str(fail))
    
def calc_hmac(message, key):
    key = bytes(key, 'utf-8')
    message = bytes(message, 'utf-8')
    res = hmac.new(key, message, hashlib.sha256)
    return res.hexdigest()

def parse(cadena):
    cadena = str(cadena)
    cadena = cadena.replace('[', '').replace(']', '').replace('\n', '').replace(' ','').replace('\'', '')
    lista = cadena.split(',')
    return lista
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    bd = sqlite3.connect('nonce.db')
    init_database(bd)
    s.bind((config.HOST,config.PORT))
    s.listen()
    conn, addr = s.accept()
    conn.send(b'Connected')
    with conn:
        print(f"Connected by {addr}")
        cont_ok = 0
        cont_fail = 0
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            parseo = parse(data.decode())
            mensaje = parseo[0]
            mensaje_and_nonce = mensaje.split('|')
            nonce = mensaje_and_nonce[1]
            hmac_client = parseo[1]
            
            hmac_server = calc_hmac(mensaje, config.KEY)

            result_search_nonce_db = search_nonce_in_database(bd, nonce)
            result_compare_hmac = hmac_comparator(hmac_client, hmac_server)

            if result_search_nonce_db == "CONFIDENTIALITY_VIOLATED" or result_compare_hmac == "HMAC_FAIL":
                if(result_search_nonce_db == "CONFIDENTIALITY_VIOLATED"):
                    cont_fail += 1
                    conn.send(bytes("CONFIDENTIALITY_VIOLATED", "utf-8"))
                else:
                    cont_fail += 1
                    conn.send(bytes("HMAC_FAIL", "utf-8"))
            else:
                bd.execute("INSERT INTO NONCES VALUES (?, ?)", (nonce, datetime.now().strftime('%d/%m/%y %H:%M:%S')))
                cont_ok += 1
                conn.send(bytes("TRANSACTION_OK", "utf-8"))
        
        creacion_logs(cont_ok, cont_fail)