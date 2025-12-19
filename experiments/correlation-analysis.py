import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from sklearn.decomposition import PCA

# ========= PARAMÈTRES =========
DATA_FILE = "pose_dataset.json"
PCA_COMPONENTS = 2  # pour le cercle de corrélations
# ==============================

# 1. Charger le dataset
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraire X et y
features = []
labels = []

for entry in data:
    pose = entry["pose"]
    features.append([
        pose["x"], pose["y"], pose["z"],
        pose["roll"], pose["pitch"], pose["yaw"],
        pose["body_yaw"], pose["antennas"][0], pose["antennas"][1]
    ])
    labels.append(entry["label"])

X = np.array(features)
y = np.array(labels)
cols = ["x","y","z","roll","pitch","yaw","body_yaw","ant1","ant2"]
n_features = len(cols)

# 2. Histogrammes regroupés sur une seule figure
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()
for i, ax in enumerate(axes):
    sns.histplot(X[y==1, i], color='green', label='OK', kde=False, bins=15, ax=ax)
    sns.histplot(X[y==0, i], color='red', label='NOK', kde=False, bins=15, ax=ax)
    ax.set_title(cols[i])
    if i == 0:
        ax.legend()
plt.tight_layout()
plt.show()

# 3. Scatter plots 2D regroupés
pairs = list(combinations(range(n_features), 2))
n_plots = len(pairs)
cols_grid = 4
rows_grid = int(np.ceil(n_plots / cols_grid))

fig, axes = plt.subplots(rows_grid, cols_grid, figsize=(20, rows_grid*4))
axes = axes.flatten()
for idx, (i,j) in enumerate(pairs):
    axes[idx].scatter(X[y==1,i], X[y==1,j], color='green', label='OK', alpha=0.6)
    axes[idx].scatter(X[y==0,i], X[y==0,j], color='red', label='NOK', alpha=0.6)
    axes[idx].set_xlabel(cols[i])
    axes[idx].set_ylabel(cols[j])
plt.tight_layout()
plt.show()

# 4. ACP et cercle de corrélation (biplot)
pca = PCA(n_components=PCA_COMPONENTS)
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)  # standardisation
X_pca = pca.fit_transform(X_scaled)

# Cercle de corrélation
fig, ax = plt.subplots(figsize=(8,8))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
circle = plt.Circle((0,0), 1, color='grey', fill=False, linestyle='--') # pyright: ignore[reportPrivateImportUsage]
ax.add_artist(circle)

# vecteurs des variables
for i, col_name in enumerate(cols):
    x_vec = pca.components_[0, i]
    y_vec = pca.components_[1, i]
    ax.arrow(0, 0, x_vec, y_vec, color='r', alpha=0.8,
             head_width=0.03, head_length=0.03)
    ax.text(x_vec*1.1, y_vec*1.1, col_name, color='b', ha='center', va='center')

ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("Cercle des corrélations")
ax.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.show()

print("Variance expliquée par PC1 et PC2 :", pca.explained_variance_ratio_)
