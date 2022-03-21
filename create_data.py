import random
import config

def creator():

    i = config.NUM_TRANSACCIONES

    with open('./DATA/messages_data.txt', 'w') as f:
        while i > 0:
            numero = random.randrange(0000000000000000000000, 9999999999999999999999)
            if len(str(numero)) == 22:
                numero2 = random.randrange(0000000000000000000000, 9999999999999999999999)
                cantidad = random.randrange(00000, 99999)
                if len(str(numero2)) == 22 and numero2 != numero:
                    f.write('ES'+str(numero)+' ES'+str(numero2)+ ' ' +str(cantidad)+'\n')
                    i -= 1
                else:
                    pass
            else:
                pass

creator()