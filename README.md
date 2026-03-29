# Prédiction de la Qualité et du Site d'Extraction des Phosphates

## Description

Cette application utilise un modèle de machine learning basé sur les **Support Vector Machines (SVM)** pour prédire :
- 🎯 **Le site d'extraction** des phosphates (Sidi Chennane ou Sidi Daoui)
- ⭐ **La qualité des phosphates** (Faible, Moyenne, Haute)

L'application offre une précision de **90% pour l'identification des sites** et **99% pour l'évaluation de la qualité** des phosphates de l'OCP Khouribga.

### Spécifications
- **Organisation** : OCP (Office Chérifien des Phosphates)
- **Site** : Khouribga
- **Type de modèle** : Support Vector Machine (SVM)
- **Interface** : Gradio (web-based UI)

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le repository** :
```bash
git clone <votre-url-repository>
cd predicteur_phosphate_ocp
```

2. **Créer un environnement virtuel** (recommandé) :
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel** :
- **Windows** :
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux** :
  ```bash
  source venv/bin/activate
  ```

4. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

### Lancer l'application

```bash
python app.py
```

L'application se lancera sur `http://localhost:7860` par défaut.

---

## Paramètres d'Entrée

L'application accepte les 5 paramètres de composition du phosphate :

| Paramètre | Unité | Description |
|-----------|-------|-------------|
| **Teneur en P2O5** | % | Concentration d'oxyde de phosphore pentoxyde |
| **Teneur en CaO** | % | Concentration d'oxyde de calcium |
| **Teneur en SiO2** | % | Concentration de dioxyde de silicium |
| **Humidité** | % | Taux d'humidité du phosphate |
| **Granulométrie** | mm | Taille des particules |

---

## 📁 Structure du Projet

```
predicteur_phosphate_ocp/
├── app.py                      # Application principale
├── requirements.txt            # Dépendances Python
├── .gitignore                  # Configuration Git
├── README.md                   # Ce fichier
├── Donnees_Phosphate.csv       # Données d'entraînement
├── modele_site.pkl             # Modèle prédiction site
├── modele_qualite.pkl          # Modèle prédiction qualité
├── scaler.pkl22                # Scaler pour normalisation
└── logo_ocp.png                # Logo OCP
```

---

## 🔧 Dépendances

- **gradio** : Interface web interactive
- **pandas** : Manipulation de données
- **numpy** : Calculs numériques
- **scikit-learn** : Machine Learning (SVM, StandardScaler)
- **joblib** : Sérialisation des modèles

Voir `requirements.txt` pour les versions spécifiques.

---

##  Utilisation

### Via l'Interface Web

1. Lancez l'application : `python app.py`
2. Ouvrez votre navigateur à `http://localhost:7860`
3. Entrez les 5 paramètres de composition
4. Cliquez sur **Submit** pour obtenir la prédiction
5. Consultez les résultats :
   - Site d'extraction prédit
   - Qualité du phosphate prédite


## 🎨 Personnalisation

### Modifier l'apparence

L'application utilise Gradio avec un thème personnalisé. Pour modifier :

1. **Couleurs** : Modifiez `primary_hue` dans `app.py`
2. **CSS** : Personnalisez la section `css=` pour l'apparence
3. **Logo** : Remplacez l'URL du logo OCP

### Modifier les sites et qualités

Dans `app.py`, modifiez :

```python
site_encoding = {'Sidi Chennane': 0, 'Sidi Daoui': 1}
quality_encoding = {'Faible': 0, 'Haute': 1, 'Moyenne': 2}
```

---

## Performance du Modèle

| Métrique | Performance |
|----------|-------------|
| **Précision Site** | 90% |
| **Précision Qualité** | 99% |
| **Type d'algorithme** | Support Vector Machine (SVM) |
| **Normalisation** | StandardScaler |

---

## Dépannage

### Erreur : "Fichiers not found"
- Vérifiez que tous les fichiers `.pkl*` et `.csv` sont dans le même répertoire que `app.py`

### Erreur : "Port already in use"
- Lancez l'application avec un port différent :
  ```bash
  python -c "from app import interface; interface.launch(server_name='0.0.0.0', server_port=8000)"
  ```

### Performance lente
- Vérifiez que les modèles SVM sont correctement chargés
- Vérifiez votre connexion réseau si accès distant

---


##  Support

Pour les questions ou problèmes, veuillez consulter la documentation officielle :
- [Gradio Documentation](https://www.gradio.app/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

---

