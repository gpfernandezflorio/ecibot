import os
from dotenv import load_dotenv
import json
import dropbox
import smtplib, ssl
from threading import Thread
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import reduce
from datos import *

load_dotenv()
modo_testing = os.getenv('TEST_MODE')=="YES"
servidor = "TEST" if modo_testing else "ECI"
id_admin = int(os.getenv('DISCORD_ADMIN'))
print("ID ADMIN: " + str(id_admin))
id_me = int(os.getenv('DISCORD_ME'))
print("ID ME: " + str(id_me))
id_servidor = int(os.getenv('DISCORD_GUILD_'+servidor))
print("ID SERVIDOR: " + str(id_servidor))
id_canal = int(os.getenv('DISCORD_'+servidor+'_CH_MESA'))
print("ID CANAL: " + str(id_canal))
id_canal_admin = int(os.getenv('DISCORD_'+servidor+'_CH_ADMIN'))
print("ID CANAL ADMIN: " + str(id_canal_admin))
id_rol = int(os.getenv('DISCORD_'+servidor+'_ROLE'))
print("ID ROL: " + str(id_rol))
dropbox_token = os.getenv('DROPBOX_TOKEN')
dbx = dropbox.Dropbox(dropbox_token)

def cargarInscriptes():
    if not os.path.isfile(ARCHIVO_JSON):
        error = crearJson()
        if (error):
            return None
    if os.path.isfile(ARCHIVO_JSON):
        jsonfile = open(ARCHIVO_JSON, 'r')
        resultado = json.loads(jsonfile.read())
        jsonfile.close()
        return resultado
    print("ERROR en cargarInscriptes:\n\tAunque crearJson no falló, no puedo encontrar el archivo {json}.".format(json=ARCHIVO_JSON))
    return None

def crearJson():
    if not os.path.isfile(ARCHIVO_CSV):
        print("ERROR en crearJson:\n\tNo se encuentra el archivo {csv}.".format(csv=ARCHIVO_CSV))
        return True
    csvfile = open(ARCHIVO_CSV, 'r')
    lineas = csvfile.read().split('\n')
    csvfile.close()
    if len(lineas) > 0:
        header = obtenerHeader(lineas[0].split(SEPARADOR_CSV))
        lineas = lineas[1:]
        resultado = {}
        for linea in lineas:
            if (len(linea) > 0):
                nuevo = {}
                atributos = linea.split(SEPARADOR_CSV)
                if len(atributos)==len(header):
                    if reduce((lambda a, b: a and b), map((lambda x: len(x) != 0), atributos)):
                        for i in range(len(header)):
                            nuevo[header[i]] = purgarEspacios(atributos[i])
                        agregar(resultado, nuevo)
                else:
                    print("ERROR en crearJson:\n\tLe inscripte no tiene todos los campos requeridos:\n\t{datos}".format(datos=linea))
                    return True
        jsonfile = open(ARCHIVO_JSON, 'w')
        jsonfile.write(json.dumps(
            {"campos":header, "inscriptes":resultado}
        ))
        jsonfile.close()
        return False
    else:
        print("ERROR en crearJson:\n\tEl archivo {csv} está vacío".format(csv=ARCHIVO_CSV))
        return True

def agregar(dic, elemento):
    miHash = hash(elemento[KEY_NOMBRE] + elemento[KEY_APELLIDO])
    if (miHash in dic):
        print("COLISIÓN:")
        print(elemento)
        print(dic[miHash])
    else:
        dic[miHash] = elemento

def obtenerHeader(nombres):
    if len(nombres) != 3:
        print("Error en el csv:\n\tEl header debería tener 3 campos pero tiene {n}".format(n=len(nombres)))
        exit(0)
    print("IMPORTANTE: verifique que las columnas sean las correctas")
    print(nombres[0] + " -> " + ORDEN_ESPERADO[0])
    print(nombres[1] + " -> " + ORDEN_ESPERADO[1])
    print(nombres[2] + " -> " + ORDEN_ESPERADO[2])
    print("Si no coinciden, cambiar el valor de la variable 'ORDEN_ESPERADO' en datos.py")
    if (input("¿Confirmar? [y]:")!="y"):
        exit(0)
    return [KEY_EMAIL, KEY_NOMBRE, KEY_APELLIDO]

def dameInscriptePorHash(inscriptes, miHash):
    if miHash in inscriptes:
        return inscriptes[miHash]
    return None

def mandarMails(inscriptes):
    sender = CUENTA
    password = input("Ingresar contraseña para {sender}: ".format(sender=sender))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(NOMBRE_SMTP, PORT) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender, password)
            for miHash in inscriptes.keys():
                inscripte = dameInscriptePorHash(inscriptes, miHash)
                nombre = "desconocide"
                if KEY_NOMBRE in inscripte:
                    nombre = inscripte[KEY_NOMBRE]
                    if KEY_APELLIDO in inscripte:
                        nombre += ' ' + inscripte[KEY_APELLIDO]
                email = "gpfernandez@dc.uba.ar"
                if KEY_EMAIL in inscripte:
                    email = inscripte[KEY_EMAIL]
                message = MIMEMultipart("alternative")
                message["Subject"] = ASUNTO
                message["From"] = sender
                message["To"] = email
                contenido = MENSAJE.format(nombre=nombre, hash=miHash)
                message.attach(MIMEText(contenido, "plain"))
                print(message)
                print("XXX")
                print(contenido)
                print("---")
                #server.sendmail(sender, email, message.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Contraseña incorrecta")

def purgarEspacios(txt):
    while(txt.startswith(' ')):
        txt = txt[1:]
    while(txt.endswith(' ')):
        txt = txt[:-1]
    return txt

def hashUsado(miHash):
    return dropboxFS.get(miHash, None)
    # nombreCompleto = '{hash}.json'.format(hash=miHash)
    # return leerArchivo(nombreCompleto)
    # if not os.path.isdir('log'):
    #     os.mkdir('log')
    # if not os.path.isdir('log'):
    #     print("Error: no se pudo crear la carpeta 'log'")
    #     exit(0)
    # if os.path.isfile(nombreCompleto):
    #     jsonfile = open(nombreCompleto, 'r')
    #     resultado = json.loads(jsonfile.read())
    #     jsonfile.close()
    #     return resultado
    # else:
    #     return None

def marcarRegistro(miHash, inscripte, userID):
    info = {
        "timestamp":str(datetime.now()),
        #"inscripte":inscripte,
        "userID":userID
    }
    dropboxFS[miHash] = info
    process = Thread(target=guardarArchivo, args=['{hash}.json'.format(hash=miHash), json.dumps(info)])
    process.start()
    #guardarArchivo('{hash}.json'.format(hash=miHash), json.dumps(info))

def guardarArchivo(ruta, contenido):
    jsonfile = open(ruta, 'w')
    jsonfile.write(contenido)
    jsonfile.close()
    with open(ruta, 'rb') as f:
        dbx.files_upload(f.read(), "/ECIbot/"+ruta, mute=True, mode=dropbox.files.WriteMode.overwrite)

def leerArchivo(ruta):
    try:
        f, r = dbx.files_download("/ECIbot/"+ruta)
        return json.loads(r.content)
    except dropbox.exceptions.ApiError:
        return None

def cargarDropboxFS():
    dic = {}
    for entry in dbx.files_list_folder('/ECIbot/').entries:
        dic[entry.name[:-5]] = leerArchivo(entry.name)
    return dic

dropboxFS = cargarDropboxFS()
flood = {}

def antiflood(id):
    ahora = datetime.now()
    if (id in flood):
        anterior = flood[id]
        ts = anterior['ts']
        delta = (ahora-ts).total_seconds()
        anterior['ts'] = ahora
        if delta < 60:
            anterior['k']+= 1
        else:
            anterior['k'] = 1
        return anterior['k']
    flood[id] = {'k':1, 'ts': ahora}
    return 0
