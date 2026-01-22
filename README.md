#  Email Summarization Agent

Un agent d'IA intelligent qui récupère vos emails depuis Gmail et les résume automatiquement en utilisant des modèles de langage gratuits.

##  Fonctionnalités

-  **Authentification Gmail** via OAuth2
-  **Récupération automatique** des derniers emails
-  **Résumé intelligent** avec extraction de :
  - Points clés
  - Actions à faire
  - Échéances
  - Niveau d'urgence (Low, Medium, High)
-  **Sauvegarde** des résultats en JSON et texte
-  **Gratuit** - Utilise Hugging Face (pas de paiement requis)

##  Prérequis

- Python 3.7+
- Un compte Hugging Face

##  Installation

1. **Clonez le repository** :
```bash
git clone https://github.com/votre-username/emailSummarizationAgent.git
cd emailSummarizationAgent
```

2. **Installez les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configurez Gmail API** :
   - Allez sur [Google Cloud Console](https://console.cloud.google.com/)
   - Créez un nouveau projet
   - Activez l'API Gmail
   - Créez des identifiants OAuth 2.0 (Application de bureau)
   - Téléchargez `client_secret.json` et placez-le dans le dossier du projet
   - Ajoutez votre email comme utilisateur de test dans "OAuth consent screen"

4. **(Optionnel) Configurez Hugging Face** :
   - Créez un compte sur [Hugging Face](https://huggingface.co)
   - Allez dans Settings → Access Tokens
   - Créez un token (type: Read)
   - Définissez la variable d'environnement :
   ```powershell
   # Windows PowerShell
   $env:HF_API_KEY="votre_token_ici"
   
   # Linux/Mac
   export HF_API_KEY="votre_token_ici"
   ```

##  Utilisation

Exécutez simplement :
```bash
python main.py
```

Le script va :
1. S'authentifier avec Gmail (ouvrira un navigateur la première fois)
2. Récupérer les derniers emails
3. Les résumer avec l'IA
4. Sauvegarder les résultats dans `outputs/summary.json` et `outputs/summary.txt`

##  Structure du projet

```
emailSummarizationAgent/
├── main.py              # Point d'entrée principal
├── requirements.txt     # Dépendances Python
├── .gitignore          # Fichiers à ignorer par Git
├── README.md           # Documentation
│
├── src/                 # Code source
│   ├── __init__.py
│   ├── emailExtract.py  # Extraction des emails depuis Gmail
│   └── agent.py         # Agent de résumé avec IA
│
├── config/              # Fichiers de configuration (non commités)
│   ├── client_secret.json  # Credentials Gmail (à ajouter)
│   └── token.json          # Token OAuth (généré automatiquement)
│
└── outputs/             # Résultats générés (non commités)
    ├── emails.txt
    ├── summary.json
    └── summary.txt
```

##  Configuration

### Modèle IA utilisé

Par défaut, le projet utilise `Qwen/Qwen2.5-3B-Instruct` de Hugging Face (gratuit).


### Nombre d'emails à traiter est par défaut 10

Modifiez `MAX_RESULTS` dans `emailExtract.py` pour changer le nombre d'emails récupérés (défaut: 10).

##  Fichiers générés

Tous les fichiers générés sont sauvegardés dans le dossier `outputs/` :

- `outputs/emails.txt` : Emails bruts récupérés
- `outputs/summary.json` : Résumés en format JSON
- `outputs/summary.txt` : Résumés formatés en texte

