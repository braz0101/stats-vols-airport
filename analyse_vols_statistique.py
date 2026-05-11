import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, gamma, burr, lognorm, beta, chi2
from sklearn.metrics import mean_squared_error
import warnings

# Charger le fichier CSV
df = pd.read_csv('airport.csv', sep=';', index_col=0)

# Désactiver les avertissements pour éviter les interruptions
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Question 1 : Afficher les aéroports d’origine des vols
print("# Question 1")
origins = np.unique(df['origin'])
print(origins)

# Question 2 : Calcul du nombre de vols par aéroport d’origine et diagramme en bar
print("# Question 2")
nb_vols = {}
for origin in origins:
    nb_vols[origin] = np.nansum(np.where(df['origin'] == origin, 1, 0))

plt.figure(figsize=(12, 6))
plt.bar(nb_vols.keys(), nb_vols.values())
plt.title('Nombre de vols par aéroport d\'origine')
plt.xlabel('Aéroport')
plt.ylabel('Nombre de vols')
plt.xticks(rotation=45)
plt.show()

# Question 3 : Distance moyenne par aéroport et diagramme en bar
print("# Question 3")
distances_moy = {}
for origin in origins:
    mask = np.where(df['origin'] == origin, True, False)
    distances_moy[origin] = np.nanmean(np.where(mask, df['distance'], np.nan))

plt.figure(figsize=(12, 6))
plt.bar(distances_moy.keys(), distances_moy.values())
plt.title('Distance moyenne par aéroport d\'origine')
plt.xlabel('Aéroport')
plt.ylabel('Distance moyenne (km)')
plt.xticks(rotation=45)
plt.show()

# Question 4 : Durée moyenne des vols par aéroport et diagramme en bar
print("# Question 4")
duree_moy = {}
for origin in origins:
    mask = np.where(df['origin'] == origin, True, False)
    duree_moy[origin] = np.nanmean(np.where(mask, df['air_time'], np.nan))

plt.figure(figsize=(12, 6))
plt.bar(duree_moy.keys(), duree_moy.values())
plt.title('Durée moyenne des vols par aéroport d\'origine')
plt.xlabel('Aéroport')
plt.ylabel('Durée moyenne (minutes)')
plt.xticks(rotation=45)
plt.show()

# Question 5 : Destination privilégiée pour chaque aéroport
print("# Question 5")
dest_pref = {}
for origin in origins:
    destinations = df.loc[df['origin'] == origin, 'dest']
    dest_pref[origin] = destinations.value_counts().idxmax()
print(dest_pref)

# Question 6 : Aéroport avec la destination la plus diversifiée + diagramme
print("# Question 6")
diversite = {}
for origin in origins:
    diversite[origin] = len(np.unique(df.loc[df['origin'] == origin, 'dest']))

plt.figure(figsize=(12, 6))
plt.bar(diversite.keys(), diversite.values())
plt.title('Nombre de destinations par aéroport d\'origine')
plt.xlabel('Aéroport')
plt.ylabel('Nombre de destinations différentes')
plt.xticks(rotation=45)
plt.show()

# Question 7 : Distribution de la distance des vols (densité) pour chaque aéroport (3 graphiques)
print("# Question 7")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for i, origin in enumerate(origins[:3]):
    mask = np.where(df['origin'] == origin, True, False)
    data = df['distance'][mask]
    sns.kdeplot(data, ax=axes[i])
    axes[i].set_title(f'Densité des distances - {origin}')
plt.tight_layout()
plt.show()

# Question 8 : Modèle le plus performant pour chaque aéroport
print("# Question 8")
distributions = {'gauss': norm, 'gamma': gamma, 'burr': burr, 'lognorm': lognorm, 'beta': beta, 'chi2': chi2}
best_models = {}

def fit_and_rmse(data, dist):
    try:
        params = dist.fit(data)
        hist, bin_edges = np.histogram(data, bins=30, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        fitted_data = dist.pdf(bin_centers, *params)  
        return mean_squared_error(hist, fitted_data)
    except Exception as e:
        print(f"Erreur lors de l'ajustement pour {dist.name}: {e}")
        return np.nan

for origin in origins:
    mask = np.where(df['origin'] == origin, True, False)
    data = df['distance'][mask].dropna()
    rmse = {}
    for name, distribution in distributions.items():
        rmse[name] = fit_and_rmse(data, distribution)
    best_models[origin] = min(rmse, key=rmse.get)
print(best_models)

# Question 9 : Superposer modèle et distribution brute (3 graphiques)
print("# Question 9")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for i, origin in enumerate(origins[:3]):
    mask = np.where(df['origin'] == origin, True, False)
    data = df['distance'][mask].dropna()
    sns.histplot(data, kde=False, ax=axes[i], stat='density', bins=30)
    best_dist = distributions[best_models[origin]]
    params = best_dist.fit(data)
    x = np.linspace(min(data), max(data), 100)
    axes[i].plot(x, best_dist.pdf(x, *params), label=best_models[origin])
    axes[i].set_title(f'Distribution - {origin}')
    axes[i].legend()
plt.tight_layout()
plt.show()

# Question 10 : Diagramme en bar des RMSE pour chaque aéroport
print("# Question 10")
rmse_final = {}
for origin in origins:
    mask = np.where(df['origin'] == origin, True, False)
    data = df['distance'][mask].dropna()
    best_dist = distributions[best_models[origin]]
    rmse_final[origin] = fit_and_rmse(data, best_dist)

plt.figure(figsize=(12, 6))
plt.bar(rmse_final.keys(), rmse_final.values())
plt.title('RMSE du meilleur modèle par aéroport')
plt.xlabel('Aéroport')
plt.ylabel('RMSE')
plt.xticks(rotation=45)
plt.show()
