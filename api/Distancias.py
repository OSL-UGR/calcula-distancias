import requests


def pagina(punto, key):
    response = requests.get(f"https://dev.virtualearth.net/REST/v1/Locations?query={punto}&maxResults=1&key={key}")
    jsonBonico = response.json()

    if (jsonBonico["resourceSets"][0]["estimatedTotal"] <= 0):
        resultado = "Destino no encontrado"
    else:
        info = jsonBonico["resourceSets"][0]["resources"][0]
        nombre = info["name"]
        coordenadas = info["point"]["coordinates"]
        confianza = info["confidence"]

        resultado = [nombre, coordenadas, confianza]

    return resultado
