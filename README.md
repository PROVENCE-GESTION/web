# web

## Vérification des URL en doublon

Utilisez le script suivant pour identifier les URLs du sitemap présentes plusieurs fois :

```bash
python scripts/check_duplicate_urls.py
```

Le script renvoie un code de sortie non nul si des doublons sont trouvés afin de faciliter son utilisation en CI.
