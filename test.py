from lib import cargarInscriptes, mandarMails

inscriptes = cargarInscriptes()

if inscriptes is None:
    exit(0)

mandarMails(inscriptes['inscriptes'])
