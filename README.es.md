# Weekly AI Feed

**Lea las ediciones diarias de AIHOT mediante una API JSON semanal.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Proyectos relacionados

- [AIHOT](https://github.com/KKKKhazix/AIHOT) — Publica el feed usado aquí.
- [Weekly API request #18](https://github.com/KKKKhazix/AIHOT/issues/18) — Pide una vista REST semanal menos densa.
- [Daily RSS route](https://github.com/KKKKhazix/AIHOT/blob/main/apps/api/src/routes/feeds.ts) — Define la ruta real `/feed/daily.xml`.

Estos enlaces describen proyectos relacionados, sin afiliación.

## Probar

```sh
python3 weekly_feed.py demo
```

## Qué comprueba esta herramienta

Analiza el RSS público `/feed/daily.xml` y sirve localmente `/api/weekly?week=YYYY-Www`. El índice conserva fechas, títulos y enlaces; no inventa resúmenes.

## Usar con sus datos

```sh
curl -fsSL https://aihot.news/feed/daily.xml > /tmp/aihot-daily.xml
python3 weekly_feed.py serve --file /tmp/aihot-daily.xml --port 8765
curl "http://127.0.0.1:8765/api/weekly?week=2026-W40"
```

Descargue el feed público e inicie el servidor local con el XML guardado. Se analizó un ejemplo RSS real el 30 de septiembre de 2026.

## Alcance y límites

AIHOT conserva como máximo 30 ediciones en este feed; no se reconstruyen semanas antiguas o incompletas. La API es un índice, no un resumen redactado; solo escucha en localhost y no modifica AIHOT.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
