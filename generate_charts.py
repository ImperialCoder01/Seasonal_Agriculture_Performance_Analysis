import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# Load raw data
raw_df = pd.read_csv('seasonal_agriculture_performance_dataset.csv')
clean_df = raw_df.copy()

# Step 1: Impute Rainfall_mm by Season median
clean_df['Rainfall_mm'] = clean_df['Rainfall_mm'].fillna(
    clean_df.groupby('Season')['Rainfall_mm'].transform('median')
)

# Step 2: Impute Soil_Moisture_pct by Season median
clean_df['Soil_Moisture_pct'] = clean_df['Soil_Moisture_pct'].fillna(
    clean_df.groupby('Season')['Soil_Moisture_pct'].transform('median')
)

# Step 3: Impute Yield_Tonnes_Ha from Production / Area
clean_df['Yield_Tonnes_Ha'] = clean_df['Yield_Tonnes_Ha'].fillna(
    (clean_df['Production_Tonnes'] / clean_df['Farm_Area_Hectares']).round(2)
)

# Add Profit_Status
clean_df['Profit_Status'] = np.where(clean_df['Profit_INR'] > 0, 'Profitable', 'Loss')

# Save cleaned dataset
clean_df.to_csv('seasonal_agriculture_performance_cleaned.csv', index=False)
print("Cleaned dataset saved: seasonal_agriculture_performance_cleaned.csv")
print(f"Shape: {clean_df.shape}, Nulls remaining: {clean_df.isnull().sum().sum()}")

season_order = ['Kharif', 'Rabi', 'Zaid']
palette = {'Kharif': '#2b5c8f', 'Rabi': '#2ca02c', 'Zaid': '#d95f02'}

# -------------------------------------------------------------
# CHART 1 — SEASONAL YIELD PERFORMANCE
# -------------------------------------------------------------
yield_series = clean_df.groupby('Season')['Yield_Tonnes_Ha'].median().reindex(season_order)

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(yield_series.index, yield_series.values, color=[palette[s] for s in season_order], width=0.55, edgecolor='black', linewidth=0.8)
ax.set_title('Median Agricultural Yield by Season', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Season', fontsize=12, labelpad=10)
ax.set_ylabel('Median Yield (Tonnes/Ha)', fontsize=12, labelpad=10)
ax.set_ylim(0, max(yield_series.values) * 1.25)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.06, f'{yval:.2f} t/ha', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('chart1_seasonal_yield.png', dpi=300)
plt.close()
print("Chart 1 saved.")

# -------------------------------------------------------------
# CHART 2 — SEASONAL ECONOMIC PERFORMANCE
# -------------------------------------------------------------
profit_series = clean_df.groupby('Season')['Profit_INR'].median().reindex(season_order)

fig, ax = plt.subplots(figsize=(7, 4.5))
colors = ['#2ca02c' if v >= 0 else '#d62728' for v in profit_series.values]
bars = ax.bar(profit_series.index, profit_series.values, color=colors, width=0.55, edgecolor='black', linewidth=0.8)
ax.axhline(0, color='black', linewidth=1, linestyle='--')
ax.set_title('Median Profit by Season', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Season', fontsize=12, labelpad=10)
ax.set_ylabel('Median Profit (INR)', fontsize=12, labelpad=10)
y_min = min(profit_series.values) * 1.3
y_max = max(profit_series.values) * 1.35
ax.set_ylim(y_min, y_max)
for bar in bars:
    yval = bar.get_height()
    va = 'bottom' if yval >= 0 else 'top'
    offset = 2500 if yval >= 0 else -6000
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + offset, f'INR {yval:,.0f}', ha='center', va=va, fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('chart2_seasonal_profit.png', dpi=300)
plt.close()
print("Chart 2 saved.")

# -------------------------------------------------------------
# CHART 3 — SEASONAL ENVIRONMENTAL CONDITIONS
# -------------------------------------------------------------
rainfall_series = clean_df.groupby('Season')['Rainfall_mm'].median().reindex(season_order)

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(rainfall_series.index, rainfall_series.values, color=['#1f77b4', '#41b6c4', '#a1dab4'], width=0.55, edgecolor='black', linewidth=0.8)
ax.set_title('Median Rainfall by Season', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Season', fontsize=12, labelpad=10)
ax.set_ylabel('Median Rainfall (mm)', fontsize=12, labelpad=10)
ax.set_ylim(0, max(rainfall_series.values) * 1.22)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f'{yval:.2f} mm', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('chart3_seasonal_rainfall.png', dpi=300)
plt.close()
print("Chart 3 saved.")

# -------------------------------------------------------------
# CHART 4 — CROP PERFORMANCE ACROSS SEASONS
# -------------------------------------------------------------
crop_pivot = clean_df.pivot_table(index='Crop', columns='Season', values='Yield_Tonnes_Ha', aggfunc='median')[season_order]

fig, ax = plt.subplots(figsize=(7.5, 5))
sns.heatmap(crop_pivot, annot=True, fmt='.2f', cmap='YlGnBu', cbar_kws={'label': 'Median Yield (Tonnes/Ha)'}, ax=ax, linewidths=0.5, linecolor='white')
ax.set_title('Median Crop Yield Across Seasons', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Season', fontsize=12, labelpad=10)
ax.set_ylabel('Crop', fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig('chart4_crop_season_heatmap.png', dpi=300)
plt.close()
print("Chart 4 saved.")

# -------------------------------------------------------------
# CHART 5 — RAINFALL AND YIELD RELATIONSHIP
# -------------------------------------------------------------
rho, p_val = stats.spearmanr(clean_df['Rainfall_mm'], clean_df['Yield_Tonnes_Ha'])

fig, ax = plt.subplots(figsize=(7.5, 5))
sns.scatterplot(
    data=clean_df,
    x='Rainfall_mm',
    y='Yield_Tonnes_Ha',
    hue='Season',
    hue_order=season_order,
    palette=palette,
    alpha=0.6,
    s=35,
    edgecolor='none',
    ax=ax
)
ax.set_title('Relationship Between Rainfall and Agricultural Yield', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Rainfall (mm)', fontsize=12, labelpad=10)
ax.set_ylabel('Yield (Tonnes/Ha)', fontsize=12, labelpad=10)
ax.legend(title='Season', frameon=True, facecolor='white', framealpha=0.9)

# Annotation box with Spearman statistics
stats_text = f'Spearman Correlation:\nrho = {rho:.4f}\np = {p_val:.2e}\n(Statistically significant,\nweak positive association)'
ax.text(0.97, 0.95, stats_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f7f7f7', edgecolor='#999999', alpha=0.95), fontsize=10)

plt.tight_layout()
plt.savefig('chart5_rainfall_yield_scatter.png', dpi=300)
plt.close()
print("Chart 5 saved.")
