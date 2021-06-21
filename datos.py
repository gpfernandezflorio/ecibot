## Nombre del csv con la data de la planilla de Google
ARCHIVO_CSV = 'x.csv'

## Separador del csv
SEPARADOR_CSV   = ';'
## Orden esperado en las columnas
KEY_NOMBRE      = "NOMBRE"
KEY_APELLIDO    = "APELLIDO"
KEY_EMAIL       = "EMAIL"
ORDEN_ESPERADO = [KEY_EMAIL, KEY_NOMBRE, KEY_APELLIDO]

## Cuenta emisora de mails
CUENTA = 'eci2021-bot@dc.uba.ar'
## Link al servidor
LINK_SERVIDOR = "MJbmsCwXy8"
## Información del mail (se reemplazarán "{nombre}" por el nombre y apellido del destinatario y "{hash}" por su hash asignado)
ASUNTO = "Acceso al servidor de la ECI 2021"
MENSAJE = """\
Hola {nombre},

Leé atentamente estas instrucciones antes de hacer nada, ya que hay varios pasos para acceder y validar tu cuenta en el servidor de Discord de la ECI 2021.

Si no tenés una cuenta de Discord, create una desde acá: https://discord.com/register

Después logueate desde la app, o desde acá: https://discord.com/login

Al ingresar, vas a tener a la izquierda varios íconos, y uno con un signo "+" grande. Hacele click, y en la ventanita que aparece, apretá en el mensaje que aparece abajo que dice "Únete a un servidor". Ahí colocá la clave de invitación al servidor de la ECI que es esta:
{link}

Al ingresar al servidor de la ECI, vas a tener acceso sólo al canal #mesa-de-entrada, donde tenés que enviar el siguiente código de validación:
<<||{hash}||>>
(copiá la línea completa, incluyendo los <<|| y ||>>)

Eso te va a validar automáticamente y te va a dejar entrar al Discord. El código es único por persona. ¡No lo compartas con nadie!

Por favor, no respondas a este mensaje. Yo soy sólo un bot. Si tenés problemas para ingresar, enviá un mail a eci2021@dc.uba.ar (y armate de mucha paciencia, somos muchos).

Saludos,
Los organizadores de la ECI 2021""".replace("{link}", LINK_SERVIDOR)

# Mensaje enviado cuando se registra correctamente une usuarie
msgUsuarieRegistrade = ":white_check_mark: Le usuarie **{user}** se registró correctamente con el hash de **{real}**."
# Mensaje enviado cuando se registra correctamente une usuarie que ya se había registrado antes
msgUsuarieRegistrade2 = ":repeat: Le usuarie **{user}** volvió a ingresar el hash de **{real}** pero como está usando el mismo id le dejé entrar."
# Mensaje enviado cuando el hash es correcto pero falla al cambiarle el nombre
msgErrorAlCambiarNombre = ":warning: Le usuarie **{user}** envió un hash correcto pero no le puedo cambiar el nombre."
# Mensaje enviado cuando el hash es correcto pero falla al quitarle el rol
msgErrorAlQuitarRol = ":warning: Le usuarie **{user}** envió un hash correcto pero no le puedo sacar el rol."
# Mensaje enviado cuando se recibe un hash inválido
msgHashInvalido = "{user}: el código que mandaste no es válido."
# Mensaje enviado cuando se reciben muchos mensajes juntos
msgBanPorFlood = "{user}: esperá un minuto antes de volver a mandar un código."
# Mensaje enviado cuando se recibe un hash repetido
msgErrorRepetido = ":exclamation: Le usuarie **{user}** envió un hash ({hash}) que ya se había usando antes ({time}):\n" + \
    "Id anterior: {idAnterior} ; id actual: {idActual}\nInscripte anterior: **{realAnterior}** ; inscripte actual **{realActual}**."
# Tiempo (en segundos) que tarda en eliminarse un mensaje de "hash inválido"
timeoutMensajeHashInvalido = 10

## Otros
NOMBRE_SMTP = "smtp.dc.uba.ar" # "smtp.gmail.com"
PORT = 587 # 465
ARCHIVO_JSON = 'x.json'
