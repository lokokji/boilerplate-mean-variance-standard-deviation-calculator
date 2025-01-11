import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('medical_examination.csv')

df['BMI'] = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (df['BMI'] > 25).astype(int)

df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else (1 if x == 2 else x))
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else (1 if x == 2 else x))

def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="count")
    df_cat = df_cat.dropna(subset=["variable", "value", "count"])
    fig = sns.catplot(data=df_cat, x="variable", hue="value", col="cardio", kind="count", height=5)
    plt.show()

def draw_heat_map():
    df_heat = df.dropna(subset=['ap_lo', 'ap_hi', 'height', 'weight'])
    df_heat = df_heat[(df_heat['ap_lo'] <= df_heat['ap_hi']) &
                      (df_heat['height'] >= df_heat['height'].quantile(0.025)) &
                      (df_heat['height'] <= df_heat['height'].quantile(0.975)) &
                      (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) &
                      (df_heat['weight'] <= df_heat['weight'].quantile(0.975))]

    corr = df_heat.corr()
    mask = np.triu(corr)
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap="coolwarm", vmin=-1, vmax=1)
    plt.show()

draw_cat_plot()
draw_heat_map()

