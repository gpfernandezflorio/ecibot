import os
from dotenv import load_dotenv
import discord
from acciones import conectar, conectar_debug, recibir_mensaje_discord
from datetime import datetime

INICIADO = False

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DEBUG = os.getenv('DEBUG')=="YES"

    if (DEBUG):
        conectar_debug()
    else:
        client = discord.Client()

        @client.event
        async def on_message(message):
            await recibir_mensaje_discord(message)

        @client.event
        async def on_ready():
            global INICIADO
            if not INICIADO:
                await conectar(client)
                INICIADO = True
            print(str(datetime.now()) + " READY")

        client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
