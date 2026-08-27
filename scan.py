import os
import requests
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()
API_KEY = os.getenv("VT_API_KEY")

def consultar_hash(hash_input):
    url = f"https://www.virustotal.com/api/v3/files/{hash_input}"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    
    print("\n[*] Consultando VirusTotal...")
    respuesta = requests.get(url, headers=headers)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        nombre = datos['data']['attributes'].get('meaningful_name', 'Nombre no disponible')
        stats = datos['data']['attributes']['last_analysis_stats']
        
        maliciosos = stats['malicious']
        total = sum(stats.values())
        
        print("\n================ RESULTADO DEL TRIAJE ================")
        print(f"Hash analizado: {hash_input}")
        print(f"Nombre del archivo: {nombre}")
        print(f"Detecciones maliciosas: {maliciosos} de {total} motores.")
        
        if maliciosos > 0:
            print("Estado: ⚠️ AMENAZA DETECTADA (POSIBLE MALWARE)")
        else:
            print("Estado: ✅ ARCHIVO LIMPIO")
        print("======================================================\n")

    elif respuesta.status_code == 404:
        print("\n[!] El Hash no fue encontrado en la base de datos de VirusTotal.")
    else:
        print(f"\n[!] Error en la consulta. Código HTTP: {respuesta.status_code}")

# Inicio del programa interactivo
if __name__ == "__main__":
    print("=== SOC TRIAGE TOOL v1.0 ===")
    hash_usuario = input("Ingresa el Hash (MD5, SHA256) que quieres analizar: ").strip()
    
    if hash_usuario:
        consultar_hash(hash_usuario)
    else:
        print("[!] No ingresaste ningún hash.")