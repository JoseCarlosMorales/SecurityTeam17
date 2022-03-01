import os
import hashlib
from traceback import print_tb
import sqlite3

ejemplo_dir = '.\\DATA'

#Creamos esta funcion para recorrer todas las carpetas del directorio 
# y obtener así una lista de todos los ficheros que contienen
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
    hash        text not null);''')
    try:
        for file in lista:
            #print (file)
            hashsha = hashlib.sha256()
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
            conn.execute('''insert into ficheros values (?,?)''',(file,hashsha.hexdigest()))
            
        conn.commit()
        print(str(conn.execute("SELECT * FROM ficheros").fetchall()))
        
    except Exception as e:
        print("Error: %s" % (e))
        return ""

    except:
        print("Error desconocido")
        return ""


if __name__ == '__main__':
    search_files(ejemplo_dir)
    getsha256file('.\\DATA')
    