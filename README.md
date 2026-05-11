# ✈️ Analyse Statistique de Données de Vols

Projet de statistiques et analyse de données portant sur un jeu de données de vols aéroportuaires.

---

## 📋 Contenu du projet

Le script répond à 10 questions d'analyse :

| # | Question |
|---|----------|
| 1 | Aéroports d'origine présents dans le dataset |
| 2 | Nombre de vols par aéroport d'origine (diagramme en bar) |
| 3 | Distance moyenne des vols par aéroport (diagramme en bar) |
| 4 | Durée moyenne des vols par aéroport (diagramme en bar) |
| 5 | Destination la plus fréquente pour chaque aéroport |
| 6 | Diversité des destinations par aéroport |
| 7 | Distribution (densité) des distances par aéroport — 3 graphiques KDE |
| 8 | Meilleur modèle statistique par aéroport (Gauss, Gamma, Burr, LogNorm, Beta, Chi²) via RMSE |
| 9 | Superposition modèle ajusté / distribution brute — 3 graphiques |
| 10 | Diagramme comparatif des RMSE par aéroport |

---

## 🚀 Utilisation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Placer le fichier de données

Place ton fichier `airport.csv` (séparateur `;`) à la racine du projet.

### 3. Lancer l'analyse

```bash
python analyse_vols.py
```

---

## 📦 Dépendances

```
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn
```

---

## 📁 Structure du dépôt

```
stats-airport/
├── analyse_vols.py             # Script principal (10 questions)
├── analyse_vols_statistique.py # Variante du script
├── requirements.txt
└── README.md
```

---

## 👤 Auteur

**IFALL**
