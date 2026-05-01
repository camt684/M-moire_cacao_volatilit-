#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:20:31 2026

@author: camilletuncq

Objectif : Test de l'hypothèse H1 - Volatilité des prix du cacao et volumes exportés

"""


import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------# Chargement des données

df_volumes = pd.read_excel("FAOSTAT_data_en_4-2-2026.xlsx")

df = pd.read_excel("US Cocoa Futures Historical Data.xlsx")
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)
df = df.sort_values("Date").reset_index(drop=True)
df = df[df["Date"] <= "2026-03-31"]


df["Price"] = df["Price"].str.replace(",", "").astype(float)
df["Annee"] = df["Date"].dt.year
df["Returns"] = df["Price"].pct_change()

# ----------------# Calcul de la volatilité annuelle

df_vol_annuelle = df.groupby("Annee")["Returns"].std() * np.sqrt(252) * 100
df_vol_annuelle = df_vol_annuelle.reset_index()
df_vol_annuelle.columns = ["Year", "Volatilite_annuelle"]

print("=== Volatilité annuelle du cacao ===")
print(df_vol_annuelle)

# ----------------# Calcul du prix moyen annuel

df_prix_annuel = df.groupby("Annee")["Price"].mean().reset_index()
df_prix_annuel.columns = ["Year", "Prix_moyen"]

# ----------------# Fusion avec les volumes exportés

df_merge_h1 = pd.merge(df_vol_annuelle, df_volumes, on="Year")

print("\n=== DataFrame fusionné (volatilité + volumes) ===")
print(df_merge_h1)

# ----------------# Corrélation H1 sur toute la période

correlation_h1 = df_merge_h1["Volatilite_annuelle"].corr(df_merge_h1["Export volume"])
print(f"\nCorrélation H1 globale (2010-2024) : {correlation_h1:.4f}")

# ----------------# Corrélation H1 sur la sous-période 2023-2024

df_crise_h1 = df_merge_h1[df_merge_h1["Year"] >= 2023]
correlation_h1_crise = df_crise_h1["Volatilite_annuelle"].corr(df_crise_h1["Export volume"])
print(f"Corrélation H1 période crise (2023-2024) : {correlation_h1_crise:.4f}")

# ----------------# Export tableau statistiques

tableau_h1 = pd.merge(df_vol_annuelle, df_merge_h1[["Year", "Export volume"]], on="Year")
tableau_h1 = pd.merge(tableau_h1, df_prix_annuel, on="Year")
print("\n=== Tableau complet volatilité / volumes / prix moyens ===")
print(tableau_h1)
tableau_h1.to_excel("stats_h1.xlsx", index=False)
print("Tableau exporté : stats_h1.xlsx")

# ----------------# Graphique volatilité annuelle vs volumes exportés

fig_h1 = go.Figure()

fig_h1.add_trace(go.Scatter(
    x=df_merge_h1["Year"], 
    y=df_merge_h1["Volatilite_annuelle"],
    mode="lines+markers", 
    name="Volatilité annuelle"
))

fig_h1.add_trace(go.Scatter(
    x=df_merge_h1["Year"], 
    y=df_merge_h1["Export volume"],
    mode="lines+markers", 
    name="Volumes exportés", 
    yaxis="y2"
))

fig_h1.update_layout(
    title="Volatilité annuelle du cacao vs Volumes exportés (2010-2024)",
    xaxis_title="Année",
    yaxis=dict(title="Volatilité annualisée (%)"),
    yaxis2=dict(title="Volumes exportés (tonnes)", overlaying="y", side="right")
)

#fig_h1.write_html("cacao_h1.html", auto_open=True)
fig_h1.write_image("annexe6_h1.png", width=1200, height=600)
print("Graphique exporté : annexe6_h1.png")