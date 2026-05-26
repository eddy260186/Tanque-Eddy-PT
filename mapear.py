import os

def mapear_proyecto(ruta_base, archivo_salida):
    # Carpetas que el escáner va a ignorar para no ensuciar el mapa
    carpetas_ignoradas = {'.git', '__pycache__', 'venv', 'env', '.streamlit', 'node_modules'}
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("🗺️ MAPA DE ARQUITECTURA - EDDY PT SAAS ELITE 🗺️\n")
        f.write("="*50 + "\n\n")
        
        for raiz, directorios, archivos in os.walk(ruta_base):
            # Filtramos las carpetas basura
            directorios[:] = [d for d in directorios if d not in carpetas_ignoradas]
            
            # Calculamos la profundidad para hacer el diseño del árbol
            nivel = raiz.replace(ruta_base, '').count(os.sep)
            sangria = '│   ' * nivel
            
            # Escribimos la carpeta
            nombre_carpeta = os.path.basename(raiz)
            if nombre_carpeta:
                f.write(f"{sangria}📂 {nombre_carpeta}/\n")
            
            # Escribimos los archivos
            sub_sangria = '│   ' * (nivel + 1)
            for archivo in archivos:
                # Ignoramos archivos ocultos o compilados
                if not archivo.startswith('.') and not archivo.endswith('.pyc'):
                    f.write(f"{sub_sangria}📄 {archivo}\n")

if __name__ == "__main__":
    # Ejecuta el escáner en la carpeta actual y guarda el resultado
    mapear_proyecto('.', 'mapa_arquitectura.txt')
    print("✅ ¡Escaneo completado! Revisá el archivo mapa_arquitectura.txt")