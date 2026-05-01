#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:51:55 2026

@author: camilletuncq
"""

import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_excel("US Cocoa Futures Historical Data.xlsx")
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)
df = df.sort_values("Date").reset_index(drop=True)
df = df[df["Date"] <= "2026-03-31"]


df["Price"] = df["Price"].str.replace(",", "").astype(float)
df["Returns"] = df["Price"].pct_change()
df["Volatility_21d"] = df["Returns"].rolling(21).std() * np.sqrt(252) * 100
df.head(35)

df["MA_200"] = df["Price"].rolling(200).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Price"], mode="lines", name="Prix journalier"))
fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_200"], mode="lines", name="Moyenne mobile 200 jours"))

fig.update_layout(
    title="Niveau des prix du Cacao entre janvier 2010 et mars 2026", 
    xaxis_title="Date", 
    yaxis_title="Prix (US$/tonne)")

#fig.write_html("cacao_prix.html", auto_open=True)
fig.write_image("annexe1_prix.png", width=1200, height=600)



fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["Date"], y=df["Volatility_21d"], mode="lines", name="Volatilité"))

fig2.update_layout(
    title="Volatilité du Cacao entre janvier 2010 et mars 2026",
    xaxis_title="Date",
    yaxis_title="Volatilité sur 21 jours")

#fig2.write_html("cacao_volatilité.html", auto_open=True)
fig2.write_image("annexe2_volatilite.png", width=1200, height=600)

#----------------# Création d'un subplot entre le grap 1 et 2


fig_combined = make_subplots(rows=2, cols=1, shared_xaxes=True,
                              subplot_titles=("Niveau des prix du cacao", "Volatilité du cacao"))

fig_combined.add_trace(go.Scatter(x=df["Date"], y=df["Price"], 
                                   mode="lines", name="Prix journalier"), row=1, col=1)

fig_combined.add_trace(go.Scatter(x=df["Date"], y=df["MA_200"], 
                                   mode="lines", name="Moyenne mobile 200j"), row=1, col=1)

fig_combined.add_trace(go.Scatter(x=df["Date"], y=df["Volatility_21d"], 
                                   mode="lines", name="Volatilité 21j"), row=2, col=1)

fig_combined.update_layout(
    title="Prix et volatilité du cacao (2010-2026)",
    yaxis_title="Prix (US$/tonne)",
    yaxis2_title="Volatilité annualisée (%)"
)

#fig_combined.write_html("cacao_combined.html", auto_open=True)
fig_combined.write_image("annexe3_combined.png", width=1200, height=600)

#-----------------# On définit deux périodes distinctes avant la crise de 2023 et de 2023 à 2026

df_avant = df[df["Date"]<"2023-01-01"]
df_crise = df[df["Date"] >= "2023-01-01"]

#print(df_avant["Price"].describe())
#print(df_crise["Price"].describe())

#print(df_avant["Volatility_30d"].describe())
#print(df_crise["Volatility_30d"].describe())

#-----------------# On va créer un tableau pour y entrer nos valeurs et ainsi les comparer plus facilement

tableau = pd.concat([
    df_avant[["Price", "Volatility_21d"]].describe(),
    df_crise[["Price", "Volatility_21d"]].describe()
    ], keys=["Avant 2023", "Depuis 2023"], axis=1)
print(tableau)
tableau.to_excel("stats_descriptives.xlsx")

#----------------# Création d'un boxplot année par année

df["Annee"] = df["Date"].dt.year

df["Annee"].head()

fig3 = go.Figure()

fig3.add_trace(go.Box(x=df["Annee"], y=df["Price"], name="Prix"))

fig3.update_layout(
    title="Distribution des prix du cacao par année",
    xaxis_title="Année",
    yaxis_title="Prix (US$/tonne)"
)

#fig3.write_html("cacao_boxplot.html", auto_open=True)
fig3.write_image("annexe4_boxplot.png", width=1200, height=600)

#----------------# Création du DataFrame pour le BDI 

df_bdi = pd.read_excel("Baltic Dry Index Historical Data.xlsx")

#print(df_bdi.head())

df_bdi["Date"] = pd.to_datetime(df_bdi["Date"], format="mixed", dayfirst=False)
df_bdi = df_bdi.sort_values("Date").reset_index(drop=True)
df_bdi = df_bdi[df_bdi["Date"] <= "2026-03-31"]


df_bdi["Price"] = df_bdi["Price"].str.replace(",", "").astype(float)

#print(df_bdi.head())
#print(df_bdi.tail())


#-----------------# Création d'un DataFrame avec nos deux DataFrame

df_merge = pd.merge(df[["Date", "Price", "Volatility_21d"]], 
                    df_bdi[["Date", "Price"]], 
                    on="Date", 
                    suffixes=("_cacao", "_bdi"))

#print(df_merge.head())



#------------------# Création de moyenne mobile pour rendre le graphique plus lisible 

df_merge["MA_cacao"] = df_merge["Price_cacao"].rolling(200).mean()
df_merge["MA_bdi"] = df_merge["Price_bdi"].rolling(200).mean()


#----------------# Création d'un graphique à partir de notre DataFrame concaténé 

fig4 = go.Figure()

fig4.add_trace(go.Scatter(x=df_merge["Date"], y=df_merge["Price_cacao"], 
                          name="Prix cacao", mode="lines", opacity=0.2))

fig4.add_trace(go.Scatter(x=df_merge["Date"], y=df_merge["Price_bdi"], 
                          name="BDI", mode="lines", yaxis="y2", opacity=0.2))

fig4.add_trace(go.Scatter(x=df_merge["Date"], y=df_merge["MA_cacao"], 
                          name="Moyenne mobile Cacao", mode="lines"))

fig4.add_trace(go.Scatter(x=df_merge["Date"], y=df_merge["MA_bdi"], 
                          name="Moyenne mobile BDI", mode="lines", yaxis="y2"))

fig4.update_layout(
    title="Prix du cacao vs Baltic Dry Index (2010-2026)",
    yaxis=dict(title="Prix cacao (US$/tonne)"),
    yaxis2=dict(title="BDI", overlaying="y", side="right")
)

#fig4.write_html("cacao_vs_bdi.html", auto_open=True)
fig4.write_image("annexe5_bdi.png", width=1200, height=600)

#---------------# On fait une corrélation entre le cacao et le bdi

correlation = df_merge["Price_cacao"].corr(df_merge["Price_bdi"])
print(correlation)

#---------------# On créer un sous DataFrame dans df_merge

df_periode = df_merge[df_merge["Date"]>="2023-01-01"]

correlation2 = df_periode["Price_cacao"].corr(df_periode["Price_bdi"])
print(correlation2)

#----------------# On fait la corrélation entre la volatilité et le BDI 

correlation3 = df_merge["Volatility_21d"].corr(df_merge["Price_bdi"])
print(correlation3)