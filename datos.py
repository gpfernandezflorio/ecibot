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
CUENTA = 'clemen.dc.uba'
## Información del mail (se reemplazarán "{nombre}" por el nombre y apellido del destinatario y "{hash}" por su hash asignado)
ASUNTO = "Acceso al servidor de la ECI 2021"
MENSAJE = """\
Estimado/a {nombre}, mediante el siguiente enlace podrá acceder al servidor de Discord de la ECI 2021.
LINK

Al ingresar, tendrá acceso al canal mesa-de-entrada donde deberá enviar el siguiente código de registro:
<<||{hash}||>>

El código es único por persona. No lo comparta con nadie.

Saludos,
equipo organizador de la ECI 2021"""

# Mensaje enviado cuando se registra correctamente une usuarie
msgUsuarieRegistrade = ":white_check_mark: Le usuarie **{user}** se registró correctamente con el hash de **{real}**."
# Mensaje enviado cuando el hash es correcto pero falla al cambiarle el nombre
msgErrorAlCambiarNombre = ":warning: Le usuarie **{user}** envió un hash correcto pero no le puedo cambiar el nombre."
# Mensaje enviado cuando el hash es correcto pero falla al quitarle el rol
msgErrorAlQuitarRol = ":warning: Le usuarie **{user}** envió un hash correcto pero no le puedo sacar el rol."
# Mensaje enviado cuando se recibe un hash inválido
msgHashInvalido = "{user}: el código que mandaste no es válido."
# Mensaje enviado cuando se recibe un hash repetido
msgErrorRepetido = ":exclamation: Le usuarie **{user}** envió un hash ({hash}) que ya se había usando antes ({time}):\n" + \
    "Id anterior: {idAnterior} ; id actual: {idActual}\nInscripte anterior: {realAnterior} ; inscripte actual {realActual}."
# Tiempo (en segundos) que tarda en eliminarse un mensaje de "hash inválido"
timeoutMensajeHashInvalido = 5

## Otros
PORT = 465  # For SSL
ARCHIVO_JSON = 'x.json'
