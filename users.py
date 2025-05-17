# Estos son los paquetes que se deben instalar
# pip install pycryptodome
# pip install pyqrcode
# pip install pypng
# pip install pyzbar
# pip install pillow

# No modificar estos módulos que se importan
from pyzbar.pyzbar import decode
from PIL import Image
from json import dumps
from json import loads
from hashlib import sha256
from Crypto.Cipher import AES
import base64
import pyqrcode
from os import urandom
import io
from datetime import datetime
import json


# Nombre del archivo con la base de datos de usuarios
usersFileName=r"assets\Base_de_datos.json"

# Fecha actual
date='28 de abril de 2025'
# Clave aleatoria para encriptar el texto de los códigos QR
key=213123

# Función para encriptar (no modificar)
def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

# Función para desencriptar (no modificar)
def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# Función que genera un código QR (no modificar)
def generateQR(id,program,role,buffer):
    # Variables globales para la clave y la fecha
    global key
    global date

    # Información que irá en el código QR, antes de encriptar
    data={'id': id, 'program':program,'role':role}
    datas=dumps(data).encode("utf-8")

    # Si no se ha asignado una clave se genera
    if key is None:
        key =urandom(32) 
        # Se almacena la fecha actual
        date=datetime.today().strftime('%Y-%m-%d')
    
    # Si cambió la fecha actual se genera una nueva clave y 
    # se actualiza la fecha
    if date !=datetime.today().strftime('%Y-%m-%d'):
        key =urandom(32) 
        date=datetime.today().strftime('%Y-%m-%d')

    # Se encripta la información
    encrypted = list(encrypt_AES_GCM(datas,key))

    # Se crea un JSON convirtiendo los datos encriptados a base64 para poder usar texto en el QR
    qr_text=dumps({'qr_text0':base64.b64encode(encrypted[0]).decode('ascii'),
                                'qr_text1':base64.b64encode(encrypted[1]).decode('ascii'),
                                'qr_text2':base64.b64encode(encrypted[2]).decode('ascii')})
    
    # Se crea el código QR a partir del JSON
    qrcode = pyqrcode.create(qr_text)

    # Se genera una imagen PNG que se escribe en el buffer                    
    qrcode.png(buffer,scale=8)          


# Se debe codificar esta función
# Argumentos: id (entero), password (cadena), program (cadena) y role (cadena)
# Si el usuario ya existe deber retornar  "User already registered"
# Si el usuario no existe debe registar el usuario en la base de datos y retornar  "User succesfully registered"
def registerUser(id, password, program, role):  
    base_de_datos = []
    registro = False 

    try:
        with open(usersFileName, 'r', encoding='utf-8') as datos:
            base_de_datos = json.load(datos)
    except (FileNotFoundError, json.JSONDecodeError):
        print("error archivo no encontrado o JSon con mal formato")
        return("error archivo no encontrado o JSon con mal formato")
        base_de_datos = []

    # Verificar si ya existe un usuario con la misma IP
    for usuario in base_de_datos:
        if usuario.get('id') == id:
            print('usuario ya existente')
            registro = True    
            return('usuario ya estaba registrado')       
            
    if not registro:  
        persona = {}      

        persona['id'] = id
        persona['password'] = password
        persona['program'] = program
        persona['role'] = role
        persona['lugar'] = 'vacio'

        base_de_datos.append(persona)

        with open(usersFileName,'w', encoding='utf-8') as datos:
            json.dump(base_de_datos, datos, indent=4)
            return("Usuario registrado")
    


#Se debe complementar esta función
# Función que genera el código QR
# retorna el código QR si el id y la contraseña son correctos (usuario registrado)
# Ayuda (debe usar la función generateQR)

def getQR(id, password):
    buffer = io.BytesIO()
    id = str(id)

    try:
        with open(usersFileName, "r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        return buffer

    for user in users:
        if str(user['id']) == id and user['password'] == password:
            generateQR(user['id'], user['program'], user['role'], buffer)
            return buffer

    return buffer

# Se debe complementar esta función
# Función que recibe el código QR como PNG
# debe verificar si el QR contiene datos que pueden ser desencriptados con la clave (key), y si el usuario está registrado
# Debe asignar un puesto de parqueadero dentro de los disponibles.
def sendQR(png):
    global key

    try:
        # Leer y decodificar el QR
        decodedQR = decode(Image.open(io.BytesIO(png)))
        if not decodedQR:
            return "QR not readable"

        data = loads(decodedQR[0].data.decode('ascii'))

        # Desencriptar información
        decrypted = loads(decrypt_AES_GCM((
            base64.b64decode(data["qr_text0"]),
            base64.b64decode(data["qr_text1"]),
            base64.b64decode(data["qr_text2"])
        ), key))

        user_id = decrypted['id']
        user_role = decrypted['role']

        # Cargar base de datos
        with open(usersFileName, "r", encoding="utf-8") as f:
            users = json.load(f)

        # Buscar usuario
        user_found = None
        for user in users:
            if str(user['id']) == str(user_id):
                user_found = user
                break

        if not user_found:
            return "User not registered"

        # Verificar si ya tiene lugar
        if user_found['lugar'] != "vacio":
            return user_found['lugar']

        # Crear lista de lugares ocupados por rol
        occupied = set(u['lugar'] for u in users if u['role'] == user_role and u['lugar'] != "vacio")

        # Definir lugares disponibles según el rol
        if user_role == "Student":
            available_spots = [f"S{i}" for i in range(1, 21)]
        elif user_role == "Teacher":
            available_spots = [f"T{i}" for i in range(1, 11)]
        else:
            return "Invalid role"

        # Asignar primer lugar libre
        for spot in available_spots:
            if spot not in occupied:
                user_found['lugar'] = spot
                break
        else:
            return "No spots available"

        # Guardar cambios
        with open(usersFileName, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

        return user_found['lugar']

    except Exception as e:
        return f"Error processing QR: {str(e)}"
