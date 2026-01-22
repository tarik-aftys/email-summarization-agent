# Guide pour publier sur GitHub

## Étapes à suivre

### 1. ✅ Git initialisé
Git a été initialisé dans votre projet.

### 2. Vérifier les fichiers à commiter
```powershell
git status
```

**IMPORTANT** : Vérifiez que `config/token.json` et `config/client_secret.json` n'apparaissent PAS dans la liste.

### 3. Faire le premier commit
```powershell
git add .
git commit -m "Initial commit: Email Summarization Agent"
```

### 4. Créer le repository sur GitHub

1. Allez sur https://github.com
2. Cliquez sur le bouton **"+"** en haut à droite
3. Sélectionnez **"New repository"**
4. Remplissez :
   - **Repository name** : `emailSummarizationAgent` (ou un autre nom)
   - **Description** : "Agent d'IA pour résumer automatiquement les emails Gmail"
   - **Visibility** : Public ou Private (votre choix)
   - **NE COCHEZ PAS** "Initialize with README" (vous en avez déjà un)
5. Cliquez sur **"Create repository"**

### 5. Connecter votre projet local à GitHub

GitHub vous donnera des commandes, mais voici les commandes à exécuter :

```powershell
# Remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE_USERNAME/emailSummarizationAgent.git
git branch -M main
git push -u origin main
```

### 6. Vérification

Allez sur votre repository GitHub et vérifiez que :
- ✅ Le code est présent
- ✅ Le README.md s'affiche
- ✅ Les fichiers dans `config/` ne sont PAS visibles
- ✅ Les fichiers dans `outputs/` ne sont PAS visibles

## Commandes complètes (copier-coller)

```powershell
# 1. Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# 2. Vérifier ce qui sera commité
git status

# 3. Faire le commit
git commit -m "Initial commit: Email Summarization Agent"

# 4. Ajouter le remote (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/emailSummarizationAgent.git

# 5. Renommer la branche en main
git branch -M main

# 6. Pousser sur GitHub
git push -u origin main
```

## Sécurité

✅ Les fichiers suivants sont **AUTOMATIQUEMENT EXCLUS** :
- `config/token.json`
- `config/client_secret.json`
- `config/*.json`
- `outputs/` (tout le dossier)

Ces fichiers resteront uniquement sur votre machine locale.

