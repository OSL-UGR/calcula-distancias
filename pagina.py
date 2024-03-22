import os
from api.accesoApi import devolverInfo, obtenerKey
from flask import (Flask, render_template, request,
                   jsonify, redirect, url_for)
import re

app = Flask(__name__)
RUTA_PASS = "config/Distancia/credenciales.txt"
key = ""


def setIps():
    file = open("whitelist.txt")
    line = file.readline()
    ips = []
    while (line):
        line = line[:-1]
        ips.append(line)
        line = file.readline()
    return '(?:% s)' % '|'.join(ips)


ips = setIps()


def validateIp(ip):
    print(ips)
    if (re.match(ips, ip)):
        return True
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular-distancia', methods=['POST'])
def calcular_distancia():

    # recibe los datos del campo de destino
    data = request.form.get('otro')
    # print("Valor recibido del campo Destino:", data)

    valores = devolverInfo(data, key)
    # Cambiar estas 3 variables, que es lo que afecta
    # a lo que aparece en la web
    if (valores == "Destino no encontrado"):
        latitud = longitud = 0
        mensaje = "No se pudo localizar el destino"
    else:
        latitud = valores["coords"][0]
        longitud = valores["coords"][1]
        mensaje = """Ciudad: %s\nDistancia desde el centro de\
                la ciudad de origen: %.2f km""" % (valores["destino"],
                                                   valores["distancia"])

    return jsonify({'status': 'OK', 'mensaje': mensaje, 'latitud': latitud,
                    'longitud': longitud})


@app.route('/calcular-distancia', methods=['GET'])
def volverAIndex():
    return redirect(url_for('index'))


@app.before_request
def limit_remote_addr():
    if (request.path != url_for('static', filename='style.css') and
            not validateIp(request.remote_addr)):
        return render_template('error.html')


def launch_server(port):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.run(host='0.0.0.0', debug=True, port=port)


if __name__ == '__main__':
    key = obtenerKey(RUTA_PASS)
    puerto = 8002
    launch_server(puerto)
