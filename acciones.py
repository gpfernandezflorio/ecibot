import discord
from lib import *

servidorActivo = None
canalActivo = None
canalAdmin = None
inscriptes = None

from datos import msgHashInvalido, msgErrorAlQuitarPermisos, timeoutMensajeHashInvalido, msgUsuarieRegistrade

def inicializar():
    global inscriptes
    inscriptes = cargarInscriptes()

async def conectar(cliente):
    global servidorActivo, canalActivo, canalAdmin
    if (cliente):
        for guild in cliente.guilds:
            if guild.id == id_servidor:
                print("Servidor encontrado: "+str(guild.id))
                servidorActivo = guild

                for c in guild.channels:
                    if c.id == id_canal:
                        print("Canal encontrado: "+str(c.id))
                        canalActivo = c
                    if c.id == id_canal_admin:
                        print("Canal Admin encontrado: "+str(c.id))
                        canalAdmin = c
                if canalAdmin is None:
                    print("Error: Canal Admin no encontrado")
                    exit(0)
                elif canalActivo is None:
                    print("Error: Canal no encontrado")
                    exit(0)
                else:
                    inicializar()
                    return
        print("Error: Servidor no encontrado")
        exit(0)
    print("Error: Cliente inválido")
    exit(0)

async def recibir_mensaje_discord(message):
    if message.guild.id != servidorActivo.id or message.channel.id != canalActivo.id:
        pass
    elif message.author.id == id_me:
        await message.delete(delay=timeoutMensajeHashInvalido)
    else:
        await message.delete(delay=0.1)
        respuesta = procesar_mensaje(message.content)
        if respuesta is None:
            await message.channel.send(msgHashInvalido.format(user=message.author.name))
        else:
            await canalAdmin.send(msgUsuarieRegistrade.format(user=message.author.name,real=respuesta))
            try:
                await message.author.remove_roles(servidorActivo.get_role(id_rol))
            except:
                await canalAdmin.send(msgErrorAlQuitarPermisos.format(user=message.author.name))


def conectar_debug():
    inicializar()
    debug_chat()

def debug_chat():
    while(True):
        mensaje = input("SEND: ")
        if len(mensaje)==0:
            break
        respuesta = procesar_mensaje(mensaje)
        if not (respuesta is None):
            print(respuesta)

def procesar_mensaje(txt):
    hash = txt
    return dameInscriptePorHash(inscriptes['inscriptes'], hash)
