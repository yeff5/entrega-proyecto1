#users.py
Sistema de control de aparcamiento mediante códigos QR

Desarrollado en Python, este software simplifica la tarea de registrar usuarios y generar códigos QR  capas de administrar un estacionamiento.
A través de estos códigos, el acceso se valida y se asignan plazas en el estacionamiento de forma automatizada,
diferenciando entre estudiantes y profesores. El sistema confirma que la información del usuario

- se genera un  códigos QR encriptados.
- Utiliza  almacenamiento de datos en formato JSON.
- llama el archivo parking_spaces.py
- recibe los datos recibidos por parking_server.py.
- El registro verifica que el usuario no esté duplicado por id.
- roles tienen espacios exclusivos (estudiantes y profesores).

#parking_spaces.py
- Se definen las coordenadas de 10 espacios de parqueo Para cada espacio.
- Se convierte el cuadro a escala de grises.
- Se aplica umbral adaptativo e inversión del color.
- Se cuenta el número de píxeles blancos en cada región.
- La imagen procesada se mostrará brevemente y se cerrará automáticamente.

#Objetivos pendientes
- aunque se asignan plazas aun no lee el codigo qr.
- una interfaz agradable para el usuario.
- Mostrar la plaza asignada al usuario gráficamente en la interfaz.
- Registrar la hora de entrada y salida de los usuarios.
- conectar el servidor y el cliente en computadoras independientes.
