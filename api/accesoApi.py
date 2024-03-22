from api.Distancias import pagina
import os
import geopy.distance


def obtenerKey(ruta):
    home = os.path.expanduser('~')
    file = open(os.path.join(home, ruta), 'r')
    key = file.read()

    file.close()

    return key


def calcularDist(punto):
    coordDest = (punto[0], punto[1])
    coordGran = (37.17648315, -3.59793711)
    return geopy.distance.geodesic(coordDest, coordGran).km


def devolverInfo(punto, key):
    valores = pagina(punto, key)

    if (valores != "Destino no encontrado"):
        destino = valores[0]
        coordenadas = valores[1]
        confianza = valores[2]
        distancia = calcularDist(coordenadas)

        resultado = {"destino": destino, "distancia": distancia,
                     "coords": coordenadas, "conf": confianza}
    else:
        resultado = valores

    return resultado


def devolverInfoStr(punto, key):
    valores = devolverInfo(punto, key)

    if (valores != "Destino no encontrado"):
        resultado = '%s;%.2f;%s;%s' % (valores[0], valores[1], valores[2],
                                       valores[3])
    else:
        resultado = valores
    return resultado
