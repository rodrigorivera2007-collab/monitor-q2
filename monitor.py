import feedparser
import os
import time
import urllib.parse

MIS_ALERTAS = {
    "Google Noticias": "https://www.google.com/alerts/feeds/01887550311641805276/7716548066590087574",
    "Facebook": "https://www.google.com/alerts/feeds/01887550311641805276/135799460851061576",
    "Instagram": "https://www.google.com/alerts/feeds/01887550311641805276/3450936725565665775",
    "X (Twitter)": "https://www.google.com/alerts/feeds/01887550311641805276/6701889539388378885",
    "YouTube": "https://www.google.com/alerts/feeds/01887550311641805276/9628050986709898055",
    "LinkedIn": "https://www.google.com/alerts/feeds/01887550311641805276/5498586337459388710"
}

ARCHIVO_NOTAS = "registro_quetzal2.txt"

def limpiar_link_google(url_bruta):
    try:
        parsed_url = urllib.parse.urlparse(url_bruta)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'url' in query_params:
            return query_params['url'][0]
    except:
        pass
    return url_bruta

def actualizar():
    ahora = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"=== INICIANDO ESCANEO: {ahora} ===")
    
    if not os.path.exists(ARCHIVO_NOTAS):
        with open(ARCHIVO_NOTAS, "w", encoding="utf-8") as f:
            f.write(f"REGISTRO DE MONITOREO QUETZAL-2\n{'='*60}\n")
        print(f"Archivo {ARCHIVO_NOTAS} creado.")

    with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
        historial = f.read()

    nuevos_totales = 0
    
    for nombre_fuente, rss_url in MIS_ALERTAS.items():
        print(f"Revisando {nombre_fuente}...", end=" ")
        feed = feedparser.parse(rss_url)
        nuevos_en_fuente = 0
        
        if not feed.entries:
            print("Vacío (sin publicaciones recientes).")
            continue

        with open(ARCHIVO_NOTAS, "a", encoding="utf-8") as f:
            for entrada in feed.entries:
                link_real = limpiar_link_google(entrada.link)
                
                if link_real not in historial:
                    bloque = (
                        f"ORIGEN:  {nombre_fuente}\n"
                        f"TITULAR: {entrada.title}\n"
                        f"LINK:    {link_real}\n"
                        f"FECHA:   {entrada.published}\n"
                        f"{'-' * 60}\n"
                    )
                    f.write(bloque)
                    nuevos_en_fuente += 1
                    nuevos_totales += 1
                    historial += link_real
        
        if nuevos_en_fuente > 0:
            print(f"¡Encontrado! ({nuevos_en_fuente} nuevos)")
        else:
            print("Sin novedades nuevas.")

    print(f"\nRESUMEN: Se agregaron {nuevos_totales} entradas nuevas al archivo.")
    print("="*40)

if __name__ == "__main__":
    actualizar()
