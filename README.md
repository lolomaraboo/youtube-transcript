# YouTube Transcript Extractor

Outil simple pour extraire les transcriptions de vidéos YouTube et les sauvegarder dans Obsidian.

## Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Rendre le script exécutable
chmod +x yt_transcript.py

# Créer un symlink dans PATH (optionnel)
mkdir -p ~/.local/bin
ln -sf ~/Documents/APP_HOME/CascadeProjects/windsurf-project/youtube-transcript/yt_transcript.py ~/.local/bin/yt
```

Assurez-vous que `~/.local/bin` est dans votre PATH :
```bash
# Ajouter dans ~/.zshrc ou ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

## Utilisation

### Afficher la transcription dans le terminal
```bash
yt https://youtube.com/watch?v=VIDEO_ID
# ou simplement
yt VIDEO_ID
```

### Copier dans le presse-papier
```bash
yt VIDEO_ID --copy
```

### Sauvegarder dans Obsidian
```bash
yt VIDEO_ID --save --title "Titre de la vidéo" --tags dev,python,tutorial
```

### Options combinées
```bash
# Copier ET sauvegarder
yt VIDEO_ID --copy --save --title "Mon titre" --tags ai,tutorial
```

### Options avancées
```bash
# Spécifier les langues préférées
yt VIDEO_ID --languages fr,en

# Utiliser un vault Obsidian différent
yt VIDEO_ID --save --obsidian-path ~/mon-vault
```

## Structure Obsidian

Les transcriptions sont sauvegardées dans :
```
SecondBrain/content/videos/[titre-VIDEO_ID].md
```

Chaque fichier contient :
```yaml
---
title: "Titre de la vidéo"
video_id: VIDEO_ID
date: 2025-12-01
url: https://youtube.com/watch?v=VIDEO_ID
tags: [dev, python]
---

[Transcription complète]
```

## Exemples

```bash
# Cas d'usage simple : copier une transcription
yt dQw4w9WgXcQ --copy

# Cas d'usage complet : sauvegarder avec métadonnées
yt dQw4w9WgXcQ \
  --save \
  --title "Never Gonna Give You Up" \
  --tags music,80s,rickroll

# Juste afficher pour lire rapidement
yt dQw4w9WgXcQ
```

## Troubleshooting

**Erreur : "Transcriptions désactivées"**
- La vidéo n'a pas de sous-titres disponibles

**Erreur : "Module non installé"**
```bash
pip install youtube-transcript-api
```

**Le script n'est pas dans le PATH**
```bash
# Vérifier
echo $PATH | grep .local/bin

# Si absent, ajouter dans ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

## Intégration avec Claude

Workflow recommandé :
1. `yt VIDEO_ID --save --title "..." --tags ...`
2. Demander à Claude d'analyser : "Analyse la dernière vidéo que j'ai ajoutée"
3. Claude lit le fichier dans `SecondBrain/content/videos/`

## Licence

Libre d'utilisation personnelle.
