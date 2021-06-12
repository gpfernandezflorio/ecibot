import os
from dotenv import load_dotenv
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    print("ERROR en cargarInscriptes:\n\tAunque crearJson no falló, no puedo encontrar el archivo {csv}.".format(csv=ARCHIVO_CSV))
    return None

def crearJson():
    if not os.path.isfile(ARCHIVO_CSV):
        print("ERROR en crearJson:\n\tNo se encuentra el archivo {csv}.".format(csv=ARCHIVO_CSV))
        return True
    csvfile = open(ARCHIVO_CSV, 'r')
    lineas = csvfile.read().split('\n')
    csvfile.close()
    if len(lineas) > 0:
        header = lineas[0].split(',')
        lineas = lineas[1:]
        resultado = []
        for linea in lineas:
            if (len(linea) > 0):
                nuevo = {}
                atributos = linea.split(',')
                if len(atributos)==len(header):
                    for i in range(len(header)):
                        nuevo[header[i]] = atributos[i]
                    resultado.append(nuevo)
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

def dameInscriptePorHash(inscriptes, hash):
    for inscripte in inscriptes:
        if inscripte[KEY_HASH] == hash:
            return "{name} {sname} ({mail})".format(
                name=inscripte[KEY_NOMBRE],
                sname=inscripte[KEY_APELLIDO],
                mail=inscripte[KEY_EMAIL])
    return None

def mandarMails(inscriptes):
    sender = CUENTA+"@gmail.com"
    password = input("Ingresar contraseña para {sender}: ".format(sender=sender))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
            server.login(sender, password)
            for inscripte in inscriptes:
                nombre = "desconocide"
                if KEY_NOMBRE in inscripte:
                    nombre = inscripte[KEY_NOMBRE]
                    if KEY_APELLIDO in inscripte:
                        nombre += ' ' + inscripte[KEY_APELLIDO]
                hash = "ABC"
                if KEY_HASH in inscripte:
                    hash = inscripte[KEY_HASH]
                email = "gpfernandez@dc.uba.ar"
                if KEY_EMAIL in inscripte:
                    hash = inscripte[KEY_EMAIL]
                message = MIMEMultipart("alternative")
                message["Subject"] = ASUNTO
                message["From"] = sender
                message["To"] = email
                message.attach(MIMEText(MENSAJE.format(nombre=nombre, hash=hash), "plain"))
                print(message)
                #server.sendmail(sender, email, message.as_string())
    except:
        print("Contraseña incorrecta")
