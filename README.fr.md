# Weekly AI Feed

**Lisez les éditions quotidiennes d’AIHOT dans une API JSON par semaine.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Projets voisins

- [AIHOT](https://github.com/KKKKhazix/AIHOT) — Publie le flux consommé ici.
- [Weekly API request #18](https://github.com/KKKKhazix/AIHOT/issues/18) — Demande une vue REST hebdomadaire moins dense.
- [Daily RSS route](https://github.com/KKKKhazix/AIHOT/blob/main/apps/api/src/routes/feeds.ts) — Définit la vraie route `/feed/daily.xml`.

Ces liens décrivent des projets voisins, sans affiliation.

## Essayer

```sh
python3 weekly_feed.py demo
```

## Ce que cet outil vérifie

Lit le RSS public `/feed/daily.xml` et sert en local `/api/weekly?week=YYYY-Www`. L’index garde dates, titres et liens ; il n’invente aucun résumé.

## Utiliser avec vos données

```sh
curl -fsSL https://aihot.news/feed/daily.xml > /tmp/aihot-daily.xml
python3 weekly_feed.py serve --file /tmp/aihot-daily.xml --port 8765
curl "http://127.0.0.1:8765/api/weekly?week=2026-W40"
```

Téléchargez le flux public, puis démarrez le serveur local avec le XML enregistré. Un exemple RSS réel a été lu avec succès le 30 septembre 2026.

## Périmètre et limites

AIHOT conserve au plus 30 éditions dans ce flux ; les semaines anciennes ou incomplètes ne se reconstruisent pas. L’API est un index, pas une synthèse rédigée ; elle écoute uniquement sur localhost et ne modifie pas AIHOT.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
