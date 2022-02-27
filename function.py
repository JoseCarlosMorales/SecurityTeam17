import os
import hashlib

ejemplo_dir = 'C:/Users/jcmor/Documents/SSII/SecurityTeam17/DATA/'

#Creamos esta funcion para recorrer todas las carpetas del directorio 
# y obtener así una lista de todos los ficheros que contienen
def search_files (directorio):
    result = []
    for nombre_directorio, dirs, ficheros in os.walk(ejemplo_dir):
        print(dirs)
        for nombre_fichero in ficheros:
            result.append(nombre_directorio+nombre_fichero)
    return result

'''
def getsha256file(directorio):
    lista = search_files (directorio)
    for file in lista:
        print (file)
        try:
            hashsha = hashlib.sha256()
            with open(file, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashsha.update(bloque)
            print(hashsha.hexdigest())

        except Exception as e:
            print("Error: %s" % (e))
            return ""

        except:
            print("Error desconocido")
            return ""
'''

if __name__ == '__main__':
    search_files(ejemplo_dir)
   # print(getsha256file('C:/Users/jcmor/Documents/SSII/SecurityTeam17/DATA/'))
    