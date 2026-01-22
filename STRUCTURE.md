# Structure du Projet

## Organisation des dossiers

```
emailSummarizationAgent/
│
├── main.py                 # Point d'entrée principal
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation principale
├── .gitignore             # Fichiers à ignorer par Git
│
├── src/                   # Code source
│   ├── __init__.py
│   ├── emailExtract.py    # Extraction des emails depuis Gmail
│   └── agent.py           # Agent de résumé avec IA
│
├── config/                # Configuration (NON COMMITÉ)
│   ├── .gitkeep
│   ├── client_secret.json # Credentials Gmail (à ajouter manuellement)
│   └── token.json         # Token OAuth (généré automatiquement)
│
└── outputs/               # Résultats générés (NON COMMITÉ)
    ├── .gitkeep
    ├── emails.txt         # Emails bruts récupérés
    ├── summary.json       # Résumés en JSON
    └── summary.txt        # Résumés formatés
```

## Séparation Code / Résultats

✅ **Code source** : Dans `src/`
✅ **Configuration** : Dans `config/`
✅ **Résultats** : Dans `outputs/`

## Avantages de cette structure

1. **Séparation claire** : Code, config et résultats sont séparés
2. **Sécurité** : Les fichiers sensibles sont dans `config/` (exclus de Git)
3. **Organisation** : Facile de trouver ce qu'on cherche
4. **Maintenance** : Structure professionnelle et scalable

