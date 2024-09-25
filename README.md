# Revshell-Windows-rubber_ducky

Este proyecto está diseñado para facilitar la ejecución remota de comandos en una máquina Windows a través de un Rubber Ducky. El script utiliza un archivo de PowerShell que se descarga y ejecuta automáticamente, permitiendo así obtener una reverse shell.

## Características

- **Desactivación de Windows Defender**: El Rubber Ducky incluye un script que desactiva temporalmente Windows Defender para permitir la ejecución del código malicioso sin interferencias.
- **Descarga y Ejecución de PowerShell**: Se utiliza un comando PowerShell para descargar y ejecutar un script desde un servidor HTTP, permitiendo la ejecución de cualquier comando en la máquina víctima.
- **Reverse Shell**: El proyecto establece una conexión de reverse shell, lo que permite al atacante tomar control de la máquina comprometida.
- **Servidor HTTP**: Incluye un servidor HTTP en Python que comparte el archivo PowerShell para su descarga.

## ¿Cómo Funciona?

1. La herramienta lista las interfaces de red disponible para hacer el uso de la ip:
![image](https://github.com/user-attachments/assets/5a0f9689-2706-46c7-b7d9-35e2cea3a82b)

2. La herramienta levanta un servidor en python y se pone en escucha con netcat.
![image](https://github.com/user-attachments/assets/14480c85-b19a-4189-b9ad-6c7439deadaa)

3. Una vez levantado todo el ruber ducky esta listo para hacer su trabajo

## Requisitos

- Rubber Ducky o un dispositivo similar capaz de ejecutar scripts.
- Python (para el servidor HTTP).

## Uso

1. Conecta el Rubber Ducky a la máquina víctima.
2. Asegúrate de que el servidor HTTP esté en ejecución.
3. La conexión de reverse shell se establecerá automáticamente, permitiendo la ejecución remota de comandos.

## Seguridad

Este proyecto se presenta únicamente con fines educativos y de concientización sobre seguridad. El uso indebido de este código está estrictamente prohibido. Asegúrate de tener el permiso adecuado antes de realizar pruebas de seguridad en cualquier sistema.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, no dudes en enviar un pull request.
