import os
import requests
from bs4 import BeautifulSoup

def extraer_manga(url, nombre_serie, num_capitulo):
    print(f"\n🚀 [Fase 1: EXTRACT] Iniciando Scraper Dedicado para {nombre_serie} - Cap {num_capitulo}")
    
    # 1. Crear el espacio de trabajo
    nombre_carpeta = f"{nombre_serie}_{num_capitulo}"
    os.makedirs(nombre_carpeta, exist_ok=True)
    
    # 2. Disfrazar nuestro bot de Python como un navegador Safari de Mac real
    # Las páginas no oficiales bloquean bots, con esto las engañamos.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    }

    try:
        print(f"🌐 Conectando con la página web...")
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() # Detiene todo si el link está caído
        
        # 3. Analizar el HTML de la página
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
             # 4. Encontrar todas las etiquetas de imagen (<img>)
        imagenes = sopa.find_all('img')
        
        contador = 1
        print(f"🔍 DIAGNÓSTICO: La página me entregó {len(imagenes)} etiquetas <img> en total.")
        print("📥 Descargando y ordenando páginas...")
        
        for img in imagenes:
            # 1. Modo Detective: Imprimir TODOS los atributos de la imagen para ver dónde esconden el link real
            print(f"\n🔍 Analizando atributos: {img.attrs}")
            
            # 2. Invertimos la prioridad: Primero buscamos en los 'data', y de ÚLTIMO en el 'src' normal.
            link_img = img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src')
            
            # 3. Si por desgracia agarramos el SVG fantasma, lo saltamos manualmente
            if link_img and link_img.startswith('data:image'):
                print("   ⚠️ Detectado placeholder Base64. Ignorando...")
                continue
                
            # Arreglamos el filtro para que sea a prueba de balas
            if link_img and any(ext in link_img.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                
                print(f"   🎯 Link real encontrado: {link_img}")
                # ... (Aquí sigue tu código de Bajar los bytes de la imagen)
                # Bajar los bytes de la imagen
                img_data = requests.get(link_img, headers=headers).content
                
                # Extraer la extensión (.jpg, .webp) y aplicar zero-padding (001, 002)
                extension = link_img.split('.')[-1]
                nombre_archivo = f"{contador:03d}.{extension}"
                ruta_archivo = os.path.join(nombre_carpeta, nombre_archivo)
                
                # Guardar el archivo en el disco duro
                with open(ruta_archivo, 'wb') as archivo_local:
                    archivo_local.write(img_data)
                    
                print(f"   ✔️ Guardada: {nombre_archivo}")
                contador += 1
        
        print(f"✅ ¡Misión cumplida! {contador - 1} páginas guardadas en: {nombre_carpeta}")
        return nombre_carpeta

    except Exception as error:
        print(f"❌ Error en el Scraper: {error}")
        return None

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # Ahora sí, pon tu URL rebelde de Blue Lock
    url_rebelde = "https://w45.blue-lock-manga.com/manga/blue-lock-chapter-16/"
    extraer_manga(url_rebelde, "Blue_Lock", "016")