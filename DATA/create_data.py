import random

def creator():
    i = 0
    with open('./data/messages_data.txt', 'w') as f:
        while i < 10000:
            numero = random.randrange(00000, 99999)
            if len(str(numero)) == 5:
                numero2 = random.randrange(00000, 99999)
                cantidad = random.randrange(0000, 9999)
                if len(str(numero2)) == 5 and numero2 != numero:
                    f.write(str(numero)+' '+str(numero2)+ ' ' +str(cantidad)+'\n')
                    i += 1
                else:
                    pass
            else:
                pass
            i += 1

creator()