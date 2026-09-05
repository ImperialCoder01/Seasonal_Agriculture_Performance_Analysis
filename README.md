# Seasonal Agriculture Performance Analysis

**VOIS AICTE Internship Batch 1 (2026–2027) — Major Project**  
**Submission Deadline:** 10 September 2026  
**Project Track:** Data Analytics & Academic Research  

---

## Project Overview
Agriculture is intrinsically dependent on seasonal rhythms, climatic conditions, resource accessibility, and crop management practices. In India, agricultural activities are categorized across three major cropping seasons:
- **Kharif (Monsoon Season):** Sown during the onset of the southwest monsoon (June–July) and harvested in autumn (September–October).
- **Rabi (Winter Season):** Sown post-monsoon in winter (October–December) and harvested in spring (March–April).
- **Zaid (Summer Season):** A transitional summer cropping season (March–June) characterized by high temperatures and reliance on irrigation.

This study performs an empirical, non-parametric data analysis of **4,000 agricultural farm records** across diverse Indian states to investigate seasonal performance across productivity, farm economics, and environmental factors.

---

## Problem Statement
Agricultural productivity and economic viability fluctuate across cropping seasons due to variations in precipitation, ambient temperature, soil moisture, and farming inputs. However, raw farm observational data contains missing observations, noise, and substantial positive skewness (e.g., high-yielding crops like Sugarcane).

Without structured empirical analysis, agricultural stakeholders face uncertainty regarding seasonal yield reliability, profitability risks, and resource management. The objective of this project is to analyze the agricultural dataset, test for statistically significant seasonal variations, and uncover actionable patterns without making unverified causal claims.

---

## Objectives
1. **Data Audit & Cleaning:** Audit data integrity, check for invalid negative values, and impute missing records using seasonal median imputation and deterministic calculation based on actual dataset relations.
2. **Seasonal Comparative Analysis:** Quantify and contrast median yield, net farm profit, and precipitation across Kharif, Rabi, and Zaid seasons.
3. **Crop-Season Interactions:** Examine crop-specific yield dynamics across seasons via cross-tabulated heatmap visualization.
4. **Environmental Association:** Analyze the statistical association between rainfall and agricultural yield using non-parametric correlation.
5. **Statistical Hypothesis Testing:** Conduct a Kruskal-Wallis test to determine whether seasonal yield distributions differ significantly.
6. **Supporting Evaluations:** Tabulate irrigation method efficiencies and calculate farm profitability proportions across seasons.
7. **Actionable Recommendations:** Provide evidence-based recommendations for farmers, agricultural planners, analysts, and policymakers based strictly on observed associations.

---

## Dataset Description
The dataset `seasonal_agriculture_performance_dataset.csv` contains 4,000 farm operations and 28 features:
- **Identifiers & Geography:** `Farm_ID`, `State`, `District`
- **Farming Classification:** `Crop` (8 crops: Rice, Wheat, Maize, Cotton, Pulses, Groundnut, Chilli, Sugarcane), `Season` (Kharif, Rabi, Zaid), `Irrigation_Method` (Drip, Flood, Rainfed, Sprinkler)
- **Land & Weather Parameters:** `Farm_Area_Hectares`, `Rainfall_mm`, `Avg_Temperature_C`, `Humidity_pct`, `Sunlight_Hours_Day`, `Soil_pH`, `Soil_Moisture_pct`
- **Soil Nutrients & Chemical Inputs:** `Nitrogen_kg_ha`, `Phosphorus_kg_ha`, `Potassium_kg_ha`, `Fertilizer_kg_ha`, `Pesticide_Litre_ha`, `Seed_Quality_Score`
- **Production & Financial Metrics:** `Yield_Tonnes_Ha`, `Production_Tonnes`, `Market_Price_INR_Tonne`, `Total_Cost_INR`, `Revenue_INR`, `Profit_INR`
- **Water Utilization & Agronomic Risk:** `Water_Used_m3`, `Water_Efficiency_t_per_1000m3`, `Disease_Pest_Risk_pct`

---

## Technologies Used
- **Python:** Core programming environment for data analysis and modeling.
- **Pandas:** Tabular data ingestion, missing value imputation, and group-wise aggregations.
- **NumPy:** Vectorized mathematical transformations and conditional indexing.
- **Matplotlib & Seaborn:** Academic-grade statistical visualizations and high-resolution chart generation.
- **SciPy (`scipy.stats`):** Non-parametric statistical inference (Kruskal-Wallis $H$-test) and Spearman rank correlation.
- **Google Colab / Jupyter Notebook:** Interactive reproducible analytical notebook.
- **Git & GitHub:** Version control and public repository hosting.
- **Microsoft PowerPoint:** Presentation deck reporting.

---

## Analytical Questions
- **Q1:** How does agricultural yield vary across Kharif, Rabi, and Zaid seasons?
- **Q2:** How does profitability vary across agricultural seasons?
- **Q3:** How do environmental conditions, particularly rainfall, differ across seasons?
- **Q4:** Do different crops show different yield patterns across seasons?
- **Q5:** Is there a relationship between rainfall and agricultural yield?
- **Q6 (Supporting):** How does irrigation method relate to yield, profitability, water usage, and water efficiency?
- **Q7 (Supporting):** Are the differences in yield across seasons statistically significant?

---

## Data Cleaning Methodology
All cleaning was executed on a copy of the dataset (`clean_df`) preserving the original raw CSV:
1. **Rainfall Imputation:** Missing values in `Rainfall_mm` ($N = 48$) were imputed using season-wise median values:
   - Kharif Median: **854.75 mm**
   - Rabi Median: **430.30 mm**
   - Zaid Median: **283.30 mm**
2. **Soil Moisture Imputation:** Missing values in `Soil_Moisture_pct` ($N = 40$) were imputed using season-wise median values:
   - Kharif Median: **30.50%**
   - Rabi Median: **24.50%**
   - Zaid Median: **19.80%**
3. **Deterministic Yield Imputation:** Missing values in `Yield_Tonnes_Ha` ($N = 32$) were validated against the deterministic formula:

$$\text{Yield\_Tonnes\_Ha} = \frac{\text{Production\_Tonnes}}{\text{Farm\_Area\_Hectares}}$$

The formula `Yield_Tonnes_Ha = Production_Tonnes / Farm_Area_Hectares` was confirmed across all 3,968 non-missing rows (maximum discrepancy $< 0.01$ due to 2-decimal rounding) and used to deterministically calculate the 32 missing values.
4. **Integrity Checks:** Verified that no invalid negative values exist in land area, rainfall, soil moisture, or inputs. Negative values in `Profit_INR` ($N = 1,966$) were confirmed as valid economic operating losses.
5. **Post-Cleaning Verification:** The cleaned dataset retains all **4,000 rows**, 0 duplicate rows, 0 duplicate `Farm_ID` values, and **0 remaining missing values** across 29 columns (after adding `Profit_Status`).

---

## Five Main Result Visualizations

### 1. Seasonal Yield Performance (Main Result Chart 1)
- **Title:** `Median Agricultural Yield by Season`
- **File:** `chart1_seasonal_yield.png`
- **Kharif:** Median Yield = **1.94 Tonnes/Ha** (Mean: 5.63 Tonnes/Ha)
- **Rabi:** Median Yield = **1.66 Tonnes/Ha** (Mean: 5.09 Tonnes/Ha)
- **Zaid:** Median Yield = **1.45 Tonnes/Ha** (Mean: 4.63 Tonnes/Ha)
- **Observed Difference:** Kharif recorded an observed median yield **0.49 Tonnes/Ha (~33.8%)** higher than Zaid. Differences reflect seasonal variation and do not imply that season alone drives the variation.

### 2. Seasonal Economic Performance (Main Result Chart 2)
- **Title:** `Median Profit by Season`
- **File:** `chart2_seasonal_profit.png`
- **Kharif:** Median Profit = **INR 38,808** (Mean: INR 178,915)
- **Rabi:** Median Profit = **-INR 3,187** (Mean: INR 87,689)
- **Zaid:** Median Profit = **-INR 62,144** (Mean: -INR 24,805)
- **Economic Insight:** Kharif was the sole season with positive median profitability. Zaid recorded substantially lower median profitability, indicating greater economic risk during the summer season.

### 3. Seasonal Environmental Conditions (Main Result Chart 3)
- **Title:** `Median Rainfall by Season`
- **File:** `chart3_seasonal_rainfall.png`
- **Kharif:** Median Rainfall = **854.75 mm** (Mean: 852.11 mm)
- **Rabi:** Median Rainfall = **430.30 mm** (Mean: 435.94 mm)
- **Zaid:** Median Rainfall = **283.30 mm** (Mean: 299.12 mm)
- **Environmental Context:** Kharif received ~3.0 times the median precipitation of Zaid and ~2.0 times that of Rabi. Lower observed rainfall in Rabi and Zaid indicates potentially greater reliance on irrigation compared with Kharif.

### 4. Crop Performance Across Seasons (Main Result Chart 4 Heatmap)
- **Title:** `Median Crop Yield Across Seasons`
- **File:** `chart4_crop_season_heatmap.png`
- Median crop yield cross-tabulation (Tonnes/Ha):

| Crop | Kharif | Rabi | Zaid |
| :--- | :---: | :---: | :---: |
| **Sugarcane** | 56.65 | 45.46 | 38.78 |
| **Maize** | 3.12 | 2.82 | 2.255 |
| **Rice** | 2.88 | 2.38 | 1.935 |
| **Wheat** | 2.36 | 2.22 | 1.84 |
| **Chilli** | 1.77 | 1.56 | 1.235 |
| **Groundnut** | 1.52 | 1.30 | 1.095 |
| **Cotton** | 1.44 | 1.21 | 0.955 |
| **Pulses** | 1.09 | 0.90 | 0.655 |

- **Observed Pattern:** Sugarcane recorded the highest median yield among the crops analyzed across all seasons. Food grains (Maize, Rice, Wheat) produced intermediate stable yields. Pulses and Cotton recorded lower median yields. All 8 crops achieved their highest observed median yields during Kharif and lowest in Zaid.

### 5. Rainfall and Yield Relationship (Main Result Chart 5 Scatter)
- **Title:** `Relationship Between Rainfall and Agricultural Yield`
- **File:** `chart5_rainfall_yield_scatter.png`
- **Spearman Rank Correlation:** $\rho = \mathbf{0.1295}$
- **p-value:** $p = \mathbf{1.9896 \times 10^{-16}} < 0.05$
- **Sample Size:** $N = 4,000$ farm records
- **Interpretation:** The analysis indicates a statistically significant, weak positive association between rainfall and yield.
- **Causation Guardrail:** **Correlation does not establish causation.** Higher rainfall does not singularly cause higher yields; multiple agronomic factors operate concurrently.

---

## Statistical Methods

### Kruskal-Wallis Non-Parametric Hypothesis Test
Because agricultural yield distributions are non-normal and positively skewed, a one-way ANOVA would violate normality assumptions. A non-parametric **Kruskal-Wallis $H$-test** was conducted:
- **Null Hypothesis ($H_0$):** Median yield distributions are identical across Kharif, Rabi, and Zaid seasons.
- **Alternative Hypothesis ($H_1$):** At least one season has a yield distribution that differs from the others.
- **Results:**
  - $H\text{-Statistic} = \mathbf{70.5935}$
  - $p\text{-value} = \mathbf{4.6860 \times 10^{-16}} < 0.05$
- **Conclusion:** There is statistically significant evidence that agricultural yield distributions differ across seasons.

### Supporting Irrigation Analysis (Tabular)
Tabular summary across irrigation methods:

| Irrigation Method | Farm Count | Median Yield (t/ha) | Median Profit (INR) | Median Water Used ($m^3$) | Median Water Efficiency ($t/1000m^3$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Drip** | 915 | **1.96** | **INR 52,895** | 4,606 | 3.2580 |
| **Sprinkler** | 734 | 1.80 | INR 7,840 | 4,687 | 2.6520 |
| **Rainfed** | 1,041 | 1.72 | -INR 9,650 | **2,782** | **4.5810** |
| **Flood** | 1,310 | 1.63 | -INR 12,131 | 6,326 | 1.9505 |

### Seasonal Profitability Proportions
Farms were categorized into operational status (`Profitable` if $\text{Profit\_INR} > 0$, else `Loss`):
- **Kharif:** **57.79%** Profitable ($1,028 / 1,779$ farms)
- **Rabi:** **48.86%** Profitable ($795 / 1,627$ farms)
- **Zaid:** **35.52%** Profitable ($211 / 594$ farms)

---

## Key Findings
1. **Seasonal Yield Variation:** Kharif recorded the highest median agricultural yield at **1.94 Tonnes/Ha**, compared to **1.66 Tonnes/Ha** in Rabi and **1.45 Tonnes/Ha** in Zaid (an observed difference of approximately 0.49 Tonnes/Ha or 33.8% over Zaid).
2. **Seasonal Profitability Differences:** Kharif was the sole season with a positive median net profit (**INR 38,808**), whereas Rabi (-INR 3,187) and Zaid (-INR 62,144) exhibited negative median operating margins in this dataset.
3. **Rainfall Gradient:** Median rainfall during Kharif was **854.75 mm**, approximately 2.0 times that of Rabi (**430.30 mm**) and 3.0 times that of Zaid (**283.30 mm**).
4. **Crop-Season Variation:** Crop yields varied across seasons; Sugarcane recorded the highest median yield among the crops analyzed (38.78–56.65 t/ha), while Pulses (0.655–1.09 t/ha) and Cotton (0.955–1.44 t/ha) recorded lower median yields.
5. **Rainfall-Yield Association:** Non-parametric Spearman correlation demonstrated a statistically significant, weak positive association between rainfall and yield ($\rho = 0.1295, p = 1.99 \times 10^{-16}, N = 4,000$).
6. **Statistically Significant Seasonal Differences:** The Kruskal-Wallis test produced $H = 70.5935$ ($p = 4.69 \times 10^{-16} < 0.05$), confirming statistically significant evidence that yield distributions differ across seasons.
7. **Irrigation-Method Association:** Farms utilizing Drip irrigation recorded the highest median profit (**INR 52,895**) and yield (**1.96 t/ha**), whereas Flood irrigation was associated with the highest water consumption (**6,326 m³**) and negative median returns (-INR 12,131).
8. **Seasonal Profitability Rates:** The proportion of profitable farms was highest in Kharif (**57.79%**), followed by Rabi (**48.86%**), and lowest in Zaid (**35.52%**).

---

## Practical Recommendations
1. **Evaluate and Promote Precision Irrigation:** Promote evaluation and adoption of drip irrigation where suitable, based on its higher observed median water efficiency (3.26 t/1000m³), yield (1.96 t/ha), and profitability (INR 52,895) in this dataset. The analysis identifies an observed association and does not prove that switching irrigation methods will produce identical gains for all farms.
2. **Develop Targeted Risk-Management Support for Zaid:** Because Zaid farming operations exhibited substantial economic deficits (with 64.48% running at an operational loss), institutions should explore targeted summer crop insurance, localized micro-credit, and drought-resilient packages.
3. **Consider Crop-Season Matching:** Agricultural planners should consider aligning water-demanding crops with the high-rainfall Kharif window and evaluating heat-resilient, lower-water crops during dry Zaid conditions.
4. **Consider Rainwater Harvesting and Supplemental Water Strategies:** Because rainfall exhibits a positive association with yield, rainwater harvesting and local storage should be evaluated where appropriate to buffer against water deficits in post-monsoon seasons.

---

## Limitations
1. **Observational Nature:** The analysis identifies associations and patterns in the available dataset and does not establish causal relationships.
2. **Confounding Factors:** Crop selections, farming techniques, input costs, and local micro-climates vary by season and interact dynamically.
3. **Generalizability:** The analysis covers the available observational dataset rather than establishing universal agricultural rules.

---

## How to Run in Google Colab
1. Open Google Colab ([colab.research.google.com](https://colab.research.google.com)).
2. Upload `Seasonal_Agriculture_Performance_Analysis.ipynb`.
3. In the Colab file explorer (left sidebar), upload `seasonal_agriculture_performance_dataset.csv`.
4. Click **Runtime → Run all** (or `Ctrl+F9`).
5. All cells will execute sequentially, generating data tables and inline visualizations automatically.

---

## Project Files
```
Seasonal-Agriculture-Performance-Analysis/
│
├── Seasonal_Agriculture_Performance_Analysis.ipynb    # Fully executed 25-section Jupyter Notebook (Colab compatible)
├── seasonal_agriculture_performance_cleaned.csv       # Cleaned dataset (4,000 rows, 29 cols, 0 nulls)
├── seasonal_agriculture_performance_dataset.csv       # Original raw dataset
├── VOIS_Major_Project_PPT_Submission_Template.pptx   # Updated 14-slide presentation deck
├── Major Project_Seasonal Agriculture Performance...  # Problem statement PDF
├── README.md                                          # Academic project documentation
│
├── chart1_seasonal_yield.png                          # Chart 1: Median Agricultural Yield by Season
├── chart2_seasonal_profit.png                         # Chart 2: Median Profit by Season
├── chart3_seasonal_rainfall.png                       # Chart 3: Median Rainfall by Season
├── chart4_crop_season_heatmap.png                     # Chart 4: Median Crop Yield Across Seasons
└── chart5_rainfall_yield_scatter.png                  # Chart 5: Rainfall vs Yield Scatter Plot
```

---

## Academic Viva / Defense Preparation Tips
1. **Why Median instead of Mean?**  
   Agricultural data contains heavy positive skewness due to high-yielding crops like Sugarcane (which reaches 101.44 t/ha), pulling the mean yield to 5.27 t/ha while the median is only 1.74 t/ha. The median provides an honest, robust representation of central tendency unaffected by outliers.
2. **Why Kruskal-Wallis instead of ANOVA?**  
   One-way ANOVA requires normally distributed residuals and homogeneity of variances. The skewed nature of agricultural yield violates these assumptions, making the non-parametric Kruskal-Wallis test statistically appropriate.
3. **Why Spearman instead of Pearson?**  
   Spearman rank correlation evaluates monotonic relationships without assuming linear bivariate normality.
4. **Association vs. Causation:**  
   Always emphasize that seasonal differences and rainfall correlations are observational associations. Confounding variables (temperature, pest pressure, soil nutrients, irrigation method) operate simultaneously.
