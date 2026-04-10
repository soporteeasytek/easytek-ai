# Social Scraper

Herramienta CLI para capturar datos de perfiles de redes sociales **sin necesidad de navegador**. Diseñada para funcionar en entornos restringidos como OpenClaw/NemoClaw.

## Plataformas soportadas

| Plataforma | Sin API Key | Con API Key |
|---|---|---|
| **Instagram** | Perfil público, bio, seguidores, posts | Igual (usa instaloader) |
| **Facebook** | Datos limitados (meta tags, OG) | Perfil completo, posts, métricas |
| **Google Business** | Datos básicos de Maps | Perfil completo, reviews, horarios |
| **Website** | Meta tags, JSON-LD, contacto, tecnologías | N/A |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso rápido

```bash
# Instagram
python scraper.py instagram cocacola

# Facebook page
python scraper.py facebook cocacola

# Google Business Profile
python scraper.py google "Starbucks Times Square NYC"

# Cualquier website
python scraper.py website https://example.com

# Todas las plataformas de un negocio
python scraper.py all --ig cocacola --fb cocacola --gbp "Coca-Cola Atlanta" --web https://coca-cola.com

# Guardar a archivo
python scraper.py instagram cocacola -o resultado.json

# Modo verbose (debug)
python scraper.py -v instagram cocacola
```

## Variables de entorno opcionales

Para obtener datos más completos, configura estas API keys:

```bash
# Facebook Graph API (obtener en https://developers.facebook.com)
export FACEBOOK_ACCESS_TOKEN="tu_token"

# Google Places API (obtener en https://console.cloud.google.com)
export GOOGLE_PLACES_API_KEY="tu_key"
```

## Estructura del proyecto

```
social-scraper/
├── scraper.py              # CLI principal
├── requirements.txt        # Dependencias
├── README.md
└── platforms/
    ├── __init__.py
    ├── instagram.py        # Instagram scraper
    ├── facebook.py         # Facebook scraper
    ├── google_business.py  # Google Business Profile scraper
    └── website.py          # Website genérico scraper
```

## Ejemplo de salida (Instagram)

```json
{
  "platform": "instagram",
  "data": {
    "username": "cocacola",
    "full_name": "Coca-Cola",
    "biography": "...",
    "followers": 2900000,
    "following": 50,
    "posts_count": 1200,
    "is_private": false,
    "is_verified": true,
    "profile_pic_url": "https://...",
    "external_url": "https://coca-cola.com",
    "recent_posts": [...]
  }
}
```

## Limitaciones

- **Sin browser**: Funciona 100% con HTTP requests — compatible con OpenClaw/NemoClaw
- **Rate limits**: Las plataformas pueden bloquear IPs con muchas peticiones
- **Perfiles privados**: Solo se pueden scrape perfiles/páginas públicos
- **Facebook personal**: Los perfiles personales están muy protegidos; funciona mejor con Pages
