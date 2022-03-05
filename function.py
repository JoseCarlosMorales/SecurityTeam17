import os
import hmac
import hashlib
import uuid
import sqlite3


ejemplo_dir = '.\\DATA'

#Creamos esta funcion para recorrer todas las carpetas del directorio 
# y obtener así una lista de todos los ficheros que contienen
def calc_hmac(clave, mensaje):
    clave = bytes(clave, 'utf-8')
    mensaje = bytes(mensaje, 'utf-8')
    res = hmac.new(clave, mensaje, hashlib.sha256)
    
    return res.hexdigest()

def search_files (directorio):
    result = []
    for nombre_directorio, dirs, ficheros in os.walk(ejemplo_dir):       
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+ "\\" +nombre_fichero)
    return result

def getsha256file(directorio):
    lista = search_files (directorio)
    conn = sqlite3.connect(':memory:')
    conn.execute("drop table if exists ficheros")
    conn.execute('''create table ficheros(
    fichero     text not null,
    hash        text not null,
    token       text not null);''')
    try:
        for file in lista:
            #print (file)
            hashsha = hashlib.sha256()
            token = uuid.uuid4().hex
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
            conn.execute('''insert into ficheros values (?,?,?)''',(file,hashsha.hexdigest(),token))   
            
        conn.commit()
        print(str(conn.execute("SELECT * FROM ficheros").fetchall()))
        
    except Exception as e:
        print("Error: %s" % (e))
        return ""

    except:
        print("Error desconocido")
        return ""


if __name__ == '__main__':
    #search_files(ejemplo_dir)
    #getsha256file('.\\DATA')
    print(calc_hmac('clavisima', 'mensaje ocult'))
    print(calc_hmac('clavisima', 'mensaje oculto'))