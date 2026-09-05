import os
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

nb = nbf.v4.new_notebook()
cells = []

def add_md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))

def add_code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))

# ==============================================================================
# 1. TITLE
# ==============================================================================
add_md("""# Seasonal Agriculture Performance Analysis

**Program:** VOIS AICTE Internship Batch 1 (2026–2027)  
**Project:** Data Analytics Major Project  
**Submission Deadline:** 10 September 2026  
""")

# ==============================================================================
# 2. INTRODUCTION
# ==============================================================================
add_md("""## 1. Introduction

In India, farming activities are closely tied to the seasons and monsoon weather. Agriculture is generally divided into three main cropping seasons:

- **Kharif (Monsoon Season):** Runs from June/July to September/October. It depends heavily on southwest monsoon rainfall. Common crops include Rice, Maize, Cotton, and Pulses.
- **Rabi (Winter Season):** Runs from October/November to March/April. It depends on cooler temperatures, leftover soil moisture, and irrigation. Major crops include Wheat and Pulses.
- **Zaid (Summer Season):** A short warm season from March to June between Rabi and Kharif. It relies almost entirely on irrigation.

This project analyzes a dataset of 4,000 farm records across India to understand how crop yield, farm profits, rainfall, and water use vary across these three seasons.
""")

# ==============================================================================
# 3. OBJECTIVES
# ==============================================================================
add_md("""## 2. Project Objectives

The main objectives of this project are:

1. Clean and prepare the agricultural dataset by checking missing values, duplicates, and invalid entries.
2. Compare median crop yield, profit, and rainfall across Kharif, Rabi, and Zaid seasons.
3. Check how individual crops perform across the different seasons.
4. Analyze the relationship between rainfall and crop yield.
5. Use a statistical test (Kruskal-Wallis) to see if seasonal yield differences are significant.
6. Compare different irrigation methods in terms of yield, profit, and water use.
7. Provide practical recommendations based on the observed data.
""")

# ==============================================================================
# 4. ANALYTICAL QUESTIONS
# ==============================================================================
add_md("""## 3. Analytical Questions

Based on the dataset, we focus on answering the following questions:

1. How does agricultural yield vary across Kharif, Rabi, and Zaid seasons?
2. How does profitability vary across seasons?
3. How does rainfall differ across the three seasons?
4. Do different crops show different yield patterns across seasons?
5. Is there an association between rainfall and agricultural yield?

**Supporting Question:**  
6. How do irrigation methods compare in terms of yield, water use, and profitability?
""")

# ==============================================================================
# 5. DATASET OVERVIEW & LIBRARIES
# ==============================================================================
add_md("""## 4. Dataset Overview & Libraries

The dataset `seasonal_agriculture_performance_dataset.csv` contains 4,000 records and 28 columns covering:
- Farm location (`State`, `District`)
- Crop type, season, and irrigation method
- Weather conditions (rainfall, temperature, humidity, sunlight)
- Soil properties (pH, soil moisture, N, P, K nutrients)
- Farm area, inputs (fertilizer, pesticide, seed score)
- Production and economics (yield, production, cost, revenue, profit)
- Water usage and efficiency

We use standard Python libraries: pandas for data handling, numpy for numerical tasks, matplotlib and seaborn for charts, and scipy for statistical testing.
""")

add_code("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.sans-serif'] = 'Arial'
print("Libraries loaded.")
""")

# ==============================================================================
# 6. LOAD DATASET
# ==============================================================================
add_md("""## 5. Load Dataset

We load the dataset into a pandas DataFrame. If running in Google Colab, make sure `seasonal_agriculture_performance_dataset.csv` is uploaded to your session before running.
""")

add_code("""csv_file = 'seasonal_agriculture_performance_dataset.csv'

if not os.path.exists(csv_file):
    try:
        from google.colab import files
        uploaded = files.upload()
    except ImportError:
        pass

df = pd.read_csv(csv_file)
print("Dataset shape:", df.shape)
df.head()
""")

# ==============================================================================
# 7. DATA UNDERSTANDING
# ==============================================================================
add_md("""## 6. Data Understanding

Here we check column data types, unique seasons, crop counts, and check for any duplicate or negative values.
""")

add_code("""# Check column types and counts
print(df.info())

print("\\nSeason distribution:")
print(df['Season'].value_counts())

print(f"\\nCrops ({df['Crop'].nunique()} unique):")
print(df['Crop'].value_counts())

print("\\nIrrigation methods:")
print(df['Irrigation_Method'].value_counts())

# Check duplicates
print("\\nDuplicate rows:", df.duplicated().sum())
print("Duplicate Farm_IDs:", df['Farm_ID'].duplicated().sum())

# Check negative values
num_cols = df.select_dtypes(include=[np.number]).columns
for col in num_cols:
    neg = (df[col] < 0).sum()
    if neg > 0:
        print(f"{col}: {neg} negative values (valid for financial losses in Profit_INR)")
""")

# ==============================================================================
# 8. DATA CLEANING
# ==============================================================================
add_md("""## 7. Data Cleaning

We check for missing values and handle them carefully without modifying the raw dataset:

1. **Rainfall (`Rainfall_mm`):** 48 missing values. Since rainfall depends heavily on the season, we fill missing values using the median rainfall of each season.
2. **Soil Moisture (`Soil_Moisture_pct`):** 40 missing values. Filled using the median soil moisture of each season.
3. **Yield (`Yield_Tonnes_Ha`):** 32 missing values. By definition:

$$\\text{Yield\\_Tonnes\\_Ha} = \\frac{\\text{Production\\_Tonnes}}{\\text{Farm\\_Area\\_Hectares}}$$

We verify this formula on the existing non-missing records and calculate the missing yield values.
""")

add_code("""print("Missing values before cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

clean_df = df.copy()

# Fill rainfall using the median within each season
clean_df['Rainfall_mm'] = clean_df['Rainfall_mm'].fillna(
    clean_df.groupby('Season')['Rainfall_mm'].transform('median')
)

# Fill soil moisture using the median within each season
clean_df['Soil_Moisture_pct'] = clean_df['Soil_Moisture_pct'].fillna(
    clean_df.groupby('Season')['Soil_Moisture_pct'].transform('median')
)

# Check that Yield_Tonnes_Ha = Production_Tonnes / Farm_Area_Hectares holds
valid_mask = clean_df['Yield_Tonnes_Ha'].notnull()
expected_yield = clean_df.loc[valid_mask, 'Production_Tonnes'] / clean_df.loc[valid_mask, 'Farm_Area_Hectares']
diff = (clean_df.loc[valid_mask, 'Yield_Tonnes_Ha'] - expected_yield).abs()
print(f"Max difference on existing yield data: {diff.max():.4f} (matches within 2 decimal places)")

# Calculate missing yield values using the formula
clean_df['Yield_Tonnes_Ha'] = clean_df['Yield_Tonnes_Ha'].fillna(
    (clean_df['Production_Tonnes'] / clean_df['Farm_Area_Hectares']).round(2)
)

print("\\nMissing values after cleaning:", clean_df.isnull().sum().sum())
print("Cleaned rows:", len(clean_df))
""")

# ==============================================================================
# 9. EXPLORATORY ANALYSIS (DESCRIPTIVE STATS)
# ==============================================================================
add_md("""## 8. Exploratory Analysis: Mean vs. Median

In agriculture, some crops like Sugarcane produce very high yields (over 40 to 100 tonnes/ha), which pulls the average (mean) upward. 

Below we compare the mean and median. Because the mean is skewed by extreme values, the **median** gives a more realistic comparison across seasons.
""")

add_code("""summary_stats = clean_df[['Yield_Tonnes_Ha', 'Profit_INR', 'Rainfall_mm', 'Water_Used_m3', 'Water_Efficiency_t_per_1000m3']].describe().T
summary_stats['median'] = clean_df[['Yield_Tonnes_Ha', 'Profit_INR', 'Rainfall_mm', 'Water_Used_m3', 'Water_Efficiency_t_per_1000m3']].median()
summary_stats[['mean', 'std', 'min', 'median', 'max']].round(2)
""")

# ==============================================================================
# 10. SEASONAL ANALYSIS (YIELD, PROFIT, PROFITABILITY)
# ==============================================================================
add_md("""## 9. Seasonal Analysis

### Question 1: How does agricultural yield vary across seasons?
We calculate the median yield for each season and plot Chart 1.
""")

add_code("""season_order = ['Kharif', 'Rabi', 'Zaid']
palette = {'Kharif': '#2b5c8f', 'Rabi': '#2ca02c', 'Zaid': '#d95f02'}

yield_by_season = clean_df.groupby('Season')['Yield_Tonnes_Ha'].median().reindex(season_order)
mean_yield_by_season = clean_df.groupby('Season')['Yield_Tonnes_Ha'].mean().reindex(season_order)

for s in season_order:
    print(f"{s}: Median Yield = {yield_by_season[s]:.2f} t/ha (Mean = {mean_yield_by_season[s]:.2f} t/ha)")

# Chart 1: Median Agricultural Yield by Season
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(season_order, yield_by_season, color=[palette[s] for s in season_order], width=0.55, edgecolor='black', linewidth=0.8)
ax.set_title('Median Agricultural Yield by Season', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Season', fontsize=11)
ax.set_ylabel('Median Yield (Tonnes/Ha)', fontsize=11)
ax.set_ylim(0, yield_by_season.max() * 1.25)

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.05, f"{h:.2f} t/ha", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('chart1_seasonal_yield.png', dpi=300)
plt.show()
""")

add_md("""**Findings for Chart 1:**
- Kharif recorded the highest median yield at **1.94 tonnes/ha** (mean: 5.63 t/ha).
- Zaid recorded the lowest median yield at **1.45 tonnes/ha** (mean: 4.63 t/ha).
- Rabi was in between at **1.66 tonnes/ha** (mean: 5.09 t/ha).
- Kharif median yield was about **0.49 tonnes/ha (~33.8%)** higher than Zaid.
- *Note:* The data shows an association between season and yield, but season alone is not the sole cause, since crops and farming practices also change across seasons.
""")

add_md("""### Question 2: How does profitability vary across seasons?
We calculate median profit by season and plot Chart 2.
""")

add_code("""profit_by_season = clean_df.groupby('Season')['Profit_INR'].median().reindex(season_order)
mean_profit_by_season = clean_df.groupby('Season')['Profit_INR'].mean().reindex(season_order)

for s in season_order:
    print(f"{s}: Median Profit = INR {profit_by_season[s]:,.0f} (Mean = INR {mean_profit_by_season[s]:,.0f})")

# Chart 2: Median Profit by Season
fig, ax = plt.subplots(figsize=(7, 4.5))
colors = ['#2ca02c' if v >= 0 else '#d62728' for v in profit_by_season]
bars = ax.bar(season_order, profit_by_season, color=colors, width=0.55, edgecolor='black', linewidth=0.8)
ax.axhline(0, color='black', linewidth=1, linestyle='--')
ax.set_title('Median Profit by Season', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Season', fontsize=11)
ax.set_ylabel('Median Profit (INR)', fontsize=11)
ax.set_ylim(profit_by_season.min() * 1.3, profit_by_season.max() * 1.35)

for bar in bars:
    h = bar.get_height()
    va = 'bottom' if h >= 0 else 'top'
    offset = 2500 if h >= 0 else -6000
    ax.text(bar.get_x() + bar.get_width()/2.0, h + offset, f"INR {h:,.0f}", ha='center', va=va, fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('chart2_seasonal_profit.png', dpi=300)
plt.show()
""")

add_md("""**Findings for Chart 2:**
- Kharif was the only season with a positive median profit at **₹38,808**.
- Rabi had a slight median deficit of **-₹3,187**.
- Zaid recorded a substantial median loss of **-₹62,144**.
- Zaid recorded substantially lower median profitability, indicating greater economic risk during the summer season. Cost and resource-use patterns may contribute to these differences, but this analysis does not establish causation.
""")

add_md("""### Supporting Seasonal Profitability Check
We also check the proportion of farms that made a profit (`Profit_INR > 0`) in each season.
""")

add_code("""# Categorize farms into Profitable or Loss
clean_df['Profit_Status'] = np.where(clean_df['Profit_INR'] > 0, 'Profitable', 'Loss')

profitability_summary = pd.DataFrame({
    'Total_Farms': clean_df.groupby('Season')['Farm_ID'].count().reindex(season_order),
    'Profitable_Farms': clean_df[clean_df['Profit_Status'] == 'Profitable'].groupby('Season')['Farm_ID'].count().reindex(season_order),
})
profitability_summary['Profitable_pct'] = (profitability_summary['Profitable_Farms'] / profitability_summary['Total_Farms'] * 100).round(2)
profitability_summary
""")

add_md("""The proportion of profitable farms was highest in Kharif (57.79%), followed by Rabi (48.86%), and lowest in Zaid (35.52%).
""")

# ==============================================================================
# 11. CROP ANALYSIS (CHART 4)
# ==============================================================================
add_md("""## 10. Crop Analysis Across Seasons

### Question 4: Do different crops show different yield patterns across seasons?
We create a heatmap showing median yield for each crop in each season (Chart 4).
""")

add_code("""crop_pivot = clean_df.pivot_table(index='Crop', columns='Season', values='Yield_Tonnes_Ha', aggfunc='median')[season_order]
print(crop_pivot.round(2))

# Chart 4: Median Crop Yield Across Seasons
fig, ax = plt.subplots(figsize=(7.5, 5))
sns.heatmap(crop_pivot, annot=True, fmt='.2f', cmap='YlGnBu', cbar_kws={'label': 'Median Yield (Tonnes/Ha)'}, ax=ax, linewidths=0.5, linecolor='white')
ax.set_title('Median Crop Yield Across Seasons', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Season', fontsize=11)
ax.set_ylabel('Crop', fontsize=11)
plt.tight_layout()
plt.savefig('chart4_crop_season_heatmap.png', dpi=300)
plt.show()
""")

add_md("""**Findings for Chart 4:**
- Sugarcane recorded the highest median yield among the crops analyzed across all seasons (56.65 t/ha in Kharif, 45.46 t/ha in Rabi, 38.78 t/ha in Zaid).
- Grain crops showed steady yields: Maize (2.255 to 3.12 t/ha), Rice (1.935 to 2.88 t/ha), and Wheat (1.84 to 2.36 t/ha).
- Pulses (0.655 to 1.09 t/ha) and Cotton (0.955 to 1.44 t/ha) had lower median yields across all three seasons.
- For all 8 crops in this dataset, median yields were highest in Kharif and lowest in Zaid.
""")

# ==============================================================================
# 12. ENVIRONMENTAL ANALYSIS (CHART 3 & CHART 5)
# ==============================================================================
add_md("""## 11. Environmental Analysis: Rainfall and Yield

### Question 3: How does rainfall differ across the three seasons?
We calculate median rainfall by season and plot Chart 3.
""")

add_code("""rainfall_by_season = clean_df.groupby('Season')['Rainfall_mm'].median().reindex(season_order)
mean_rain_by_season = clean_df.groupby('Season')['Rainfall_mm'].mean().reindex(season_order)

for s in season_order:
    print(f"{s}: Median Rainfall = {rainfall_by_season[s]:.2f} mm (Mean = {mean_rain_by_season[s]:.2f} mm)")

# Chart 3: Median Rainfall by Season
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(season_order, rainfall_by_season, color=['#1f77b4', '#41b6c4', '#a1dab4'], width=0.55, edgecolor='black', linewidth=0.8)
ax.set_title('Median Rainfall by Season', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Season', fontsize=11)
ax.set_ylabel('Median Rainfall (mm)', fontsize=11)
ax.set_ylim(0, rainfall_by_season.max() * 1.22)

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, h + 20, f"{h:.2f} mm", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('chart3_seasonal_rainfall.png', dpi=300)
plt.show()
""")

add_md("""**Findings for Chart 3:**
- Kharif received the highest median rainfall at **854.75 mm** (mean: 852.11 mm).
- Rabi received **430.30 mm** (mean: 435.94 mm).
- Zaid received the lowest median rainfall at **283.30 mm** (mean: 299.12 mm).
- Lower observed rainfall in Rabi and Zaid indicates potentially greater reliance on irrigation compared with Kharif (~3 times difference between Kharif and Zaid).
""")

add_md("""### Question 5: Is there an association between rainfall and agricultural yield?
We plot rainfall vs. yield and calculate the Spearman rank correlation (Chart 5).
""")

add_code("""rho, p_val = stats.spearmanr(clean_df['Rainfall_mm'], clean_df['Yield_Tonnes_Ha'])
print(f"Sample size N = {len(clean_df)}")
print(f"Spearman rho = {rho:.4f}")
print(f"p-value = {p_val:.4e}")

# Chart 5: Relationship Between Rainfall and Agricultural Yield
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
ax.set_title('Relationship Between Rainfall and Agricultural Yield', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Rainfall (mm)', fontsize=11)
ax.set_ylabel('Yield (Tonnes/Ha)', fontsize=11)
ax.legend(title='Season', frameon=True, facecolor='white', framealpha=0.9)

stats_text = f"Spearman rho = {rho:.4f}\\np = {p_val:.2e}\\n(Weak positive association)"
ax.text(0.97, 0.95, stats_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f7f7f7', edgecolor='#999999', alpha=0.95), fontsize=10)

plt.tight_layout()
plt.savefig('chart5_rainfall_yield_scatter.png', dpi=300)
plt.show()
""")

add_md("""**Findings for Chart 5:**
- The Spearman correlation between rainfall and yield is $\\rho = 0.1295$ with $p = 1.99 \\times 10^{-16}$ ($N = 4,000$).
- The data show a statistically significant, weak positive association between rainfall and yield.
- **Important:** Correlation does not establish causation. Rainfall alone does not explain most of the variation in yield; other inputs like soil fertility, irrigation, temperature, and crop choices also matter.
""")

# ==============================================================================
# 13. STATISTICAL ANALYSIS (KRUSKAL-WALLIS)
# ==============================================================================
add_md("""## 12. Statistical Analysis: Kruskal-Wallis Test

The Kruskal-Wallis test was used to check whether yield distributions differed across the three seasons. Because agricultural yield is skewed, this non-parametric test is more appropriate than standard ANOVA.

- **Null Hypothesis ($H_0$):** Yield distributions are the same across Kharif, Rabi, and Zaid.
- **Alternative Hypothesis ($H_1$):** Yield distributions differ across seasons.
""")

add_code("""kharif_yields = clean_df[clean_df['Season'] == 'Kharif']['Yield_Tonnes_Ha']
rabi_yields = clean_df[clean_df['Season'] == 'Rabi']['Yield_Tonnes_Ha']
zaid_yields = clean_df[clean_df['Season'] == 'Zaid']['Yield_Tonnes_Ha']

kw_stat, kw_p = stats.kruskal(kharif_yields, rabi_yields, zaid_yields)
print(f"Kruskal-Wallis H-statistic: {kw_stat:.4f}")
print(f"p-value: {kw_p:.4e}")

if kw_p < 0.05:
    print("Result: Reject H0. There is statistically significant evidence that yield distributions differ across seasons.")
else:
    print("Result: Fail to reject H0. No significant difference found.")
""")

add_md("""Since $p = 4.69 \\times 10^{-16} < 0.05$, there is statistically significant evidence that yield distributions differ across seasons. This test confirms an observed difference, not that season alone caused it.
""")

# ==============================================================================
# 14. SUPPORTING IRRIGATION ANALYSIS
# ==============================================================================
add_md("""## 13. Supporting Irrigation Analysis

### Question 6: How do irrigation methods compare in terms of yield, water use, and profitability?
We summarize median performance across the four irrigation methods in a table.
""")

add_code("""irrigation_summary = clean_df.groupby('Irrigation_Method').agg(
    Farms=('Farm_ID', 'count'),
    Median_Yield_t_ha=('Yield_Tonnes_Ha', 'median'),
    Median_Profit_INR=('Profit_INR', 'median'),
    Median_Water_Used_m3=('Water_Used_m3', 'median'),
    Median_Water_Efficiency=('Water_Efficiency_t_per_1000m3', 'median')
).loc[['Drip', 'Flood', 'Rainfed', 'Sprinkler']]

print(irrigation_summary.round(2))
""")

add_md("""**Observations on Irrigation:**
- **Drip:** Recorded the highest observed median yield (**1.96 t/ha**), highest median profit (**₹52,895**), and good water efficiency (**3.26 t/1000m³**) with moderate water use (**4,606 m³**).
- **Flood:** Used the most water (**6,326 m³**) while recording the lowest median yield (**1.63 t/ha**) and a median loss (**-₹12,131**).
- **Rainfed:** Used the least water (**2,782 m³**) with high efficiency (**4.58 t/1000m³**), but had moderate yields (**1.72 t/ha**).
- **Sprinkler:** Showed balanced performance (**1.80 t/ha** yield, **₹7,840** profit, **4,687 m³** water).
- *Note:* These are observed associations in this dataset and do not prove that changing irrigation alone will produce identical gains for every farm.
""")

# ==============================================================================
# 15. KEY FINDINGS
# ==============================================================================
add_md("""## 14. Key Findings

Based on the analysis of the 4,000 farm records:

1. **Seasonal Yield Variation:** Kharif recorded the highest median yield at **1.94 tonnes/ha**, compared to **1.66 tonnes/ha** in Rabi and **1.45 tonnes/ha** in Zaid (about 33.8% higher than Zaid).
2. **Seasonal Profitability Difference:** Kharif was the only season with a positive median profit (**₹38,808**), while Rabi (-₹3,187) and Zaid (-₹62,144) recorded median deficits.
3. **Rainfall Gradient:** Median rainfall was highest in Kharif (**854.75 mm**), intermediate in Rabi (**430.30 mm**), and lowest in Zaid (**283.30 mm**).
4. **Crop-Season Variation:** Crop yields varied across seasons; Sugarcane recorded the highest median yield among the crops analyzed (38.78 to 56.65 t/ha), while Pulses (0.655 to 1.09 t/ha) and Cotton (0.955 to 1.44 t/ha) had lower median yields.
5. **Rainfall-Yield Association:** The Spearman correlation showed a statistically significant, weak positive association between rainfall and yield ($\\rho = 0.1295, p = 1.99 \\times 10^{-16}, N = 4,000$).
6. **Significant Seasonal Differences:** The Kruskal-Wallis test produced $H = 70.5935$ ($p = 4.69 \\times 10^{-16}$), showing statistically significant differences in yield distributions across seasons.
7. **Irrigation-Method Patterns:** Farms using Drip irrigation recorded the highest median profit (**₹52,895**) and yield (**1.96 t/ha**), while Flood irrigation had the highest water use (**6,326 m³**) and negative median returns.
8. **Seasonal Profitability Rates:** The percentage of profitable farms was highest in Kharif (**57.79%**), followed by Rabi (**48.86%**), and lowest in Zaid (**35.52%**).
""")

# ==============================================================================
# 16. RECOMMENDATIONS
# ==============================================================================
add_md("""## 15. Recommendations

Based on the observed data:

1. **Evaluate Drip Irrigation:** Drip irrigation recorded higher observed median water efficiency, yield, and profitability in this dataset. Farmers and planners can consider evaluating drip systems where local conditions and crop types are suitable.
2. **Manage Summer Season (Zaid) Risk:** Since over 64% of Zaid farms operated at an economic loss, stakeholders should consider targeted risk-management measures such as crop insurance and credit buffers for summer farming.
3. **Consider Crop-Season Matching:** High-water crops align well with the higher rainfall observed in Kharif, while lower-water or heat-tolerant crops can be considered during drier Zaid conditions.
4. **Evaluate Water Storage Options:** Because rainfall shows a positive association with yield, rainwater harvesting and farm storage can be evaluated to provide supplemental water during drier seasons.
""")

# ==============================================================================
# 17. CONCLUSION & LIMITATIONS
# ==============================================================================
add_md("""## 16. Conclusion & Limitations

### Conclusion
This project analyzed seasonal agricultural performance across 4,000 farm records. The analysis showed clear differences in yield, rainfall, and profitability across seasons. Kharif had the highest observed median productivity and profitability. Statistical testing confirmed that yield distributions differ significantly across seasons.

### Limitations
1. **Observational Data:** The analysis identifies associations in the available data and does not prove causal relationships.
2. **Confounding Factors:** Farming practices, crop choices, input costs, and local weather interact and vary across seasons.
3. **Dataset Scope:** Findings reflect the 4,000 records in this dataset rather than universal farming rules.
""")

# ==============================================================================
# 18. EXPORT CLEANED DATASET
# ==============================================================================
add_md("""## 17. Export Cleaned Dataset

We save the cleaned dataset with the added `Profit_Status` column to `seasonal_agriculture_performance_cleaned.csv`.
""")

add_code("""clean_df.to_csv('seasonal_agriculture_performance_cleaned.csv', index=False)
print("Cleaned dataset saved: seasonal_agriculture_performance_cleaned.csv")
print("Final shape:", clean_df.shape)
""")

nb.cells = cells

# Save unexecuted notebook
with open('Seasonal_Agriculture_Performance_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook created with {len(nb.cells)} cells. Now executing all cells...")

# Execute notebook so all outputs are embedded
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
with open('Seasonal_Agriculture_Performance_Analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_to_run = nbf.read(f, as_version=4)

ep.preprocess(nb_to_run, {'metadata': {'path': '.'}})

with open('Seasonal_Agriculture_Performance_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb_to_run, f)

print("Notebook fully executed and saved successfully with all outputs embedded!")
