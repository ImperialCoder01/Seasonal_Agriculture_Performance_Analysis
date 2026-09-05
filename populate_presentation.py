import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

prs = Presentation('VOIS_Major_Project_PPT_Submission_Template.pptx')

# Helper function to add a title and bullet box
def add_bullet_text(slide, left, top, width, height, title_text, bullets):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.1)
    tf.margin_bottom = Inches(0.1)
    
    # Subtitle / Header
    p0 = tf.paragraphs[0]
    p0.text = title_text
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(27, 54, 93)
    p0.space_after = Pt(12)
    
    # Bullets
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_after = Pt(8)

# ==============================================================================
# SLIDE 1: TITLE
# ==============================================================================
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame:
        txt = shape.text.strip()
        if "Project Title" in txt or "Seasonal Agriculture" in txt:
            shape.text_frame.text = "Seasonal Agriculture Performance Analysis"
            for p in shape.text_frame.paragraphs:
                p.font.bold = True
                p.font.size = Pt(22)
                p.font.color.rgb = RGBColor(27, 54, 93)
        elif "[Student Name" in txt or "VOIS AICTE Batch 1" in txt:
            shape.text_frame.text = "[Student Name]\n[College Name]\nVOIS AICTE Batch 1 (2026–2027)"
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(60, 60, 60)
        elif "AICTE STU ID" in txt:
            shape.text_frame.text = "AICTE STU ID: [Enter AICTE Student ID]"
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(13)
                p.font.color.rgb = RGBColor(90, 90, 90)

# ==============================================================================
# SLIDE 2: PROBLEM STATEMENT
# ==============================================================================
slide2 = prs.slides[1]
for shape in slide2.shapes:
    if shape.has_text_frame and shape.left < Inches(8) and shape.top > Inches(1.5):
        tf = shape.text_frame
        tf.clear()
        bullets = [
            "Agricultural productivity varies substantially across seasons due to changing rainfall, temperatures, soil moisture, and farming inputs.",
            "Raw observational farm data lacks clear structure, containing missing values and skewed distributions that complicate decision-making.",
            "Objective: Analyze empirical farm records to investigate seasonal variations in yield, economic margins, and environmental factors across Kharif, Rabi, and Zaid.",
            "Focus on empirical evidence and robust non-parametric analysis without assuming unproven causal relationships."
        ]
        for i, b in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(14)
            p.space_after = Pt(10)
            p.font.color.rgb = RGBColor(40, 40, 40)

# ==============================================================================
# SLIDE 3: PROJECT DESCRIPTION
# ==============================================================================
slide3 = prs.slides[2]
# Adjust shape 0
shape0 = slide3.shapes[0]
if shape0.has_text_frame:
    shape0.text_frame.text = "Project Description"
    for p in shape0.text_frame.paragraphs:
        p.font.bold = True
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(27, 54, 93)

# Clear existing text boxes added previously if any, or update
for shape in list(slide3.shapes):
    if shape.has_text_frame and shape != shape0 and shape.top > Inches(1.5):
        sp_id = shape.shape_id
        # slide3.shapes._spTree.remove(shape._element)
        shape.text_frame.clear()

desc_box = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.8))
tf = desc_box.text_frame
tf.word_wrap = True
bullets = [
    "Empirical Study: Comprehensive data analytics study analyzing 4,000 agricultural farm operations across diverse Indian agro-climatic zones.",
    "Multi-Dimensional Dataset: Evaluated 28 variables spanning soil nutrients (N, P, K, pH), weather metrics, crop types, irrigation methods, and financial outcomes.",
    "Rigorous Data Cleaning: Handled missing values through season-wise median imputation (Rainfall, Soil Moisture) and exact deterministic calculation for Yield (Yield_Tonnes_Ha = Production_Tonnes / Farm_Area_Hectares).",
    "Non-Parametric Approach: Prioritized median-based summaries over means to prevent distortion from high-yielding crops like Sugarcane.",
    "Statistical Validation: Applied Kruskal-Wallis non-parametric hypothesis testing and Spearman rank correlation to establish rigorous, non-causal associations."
]
for i, b in enumerate(bullets):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(15)
    p.space_after = Pt(12)
    p.font.color.rgb = RGBColor(40, 40, 40)

# ==============================================================================
# SLIDE 4: WHO ARE THE END USERS?
# ==============================================================================
slide4 = prs.slides[3]
for shape in slide4.shapes:
    if shape.has_text_frame and shape.top > Inches(1.8):
        tf = shape.text_frame
        tf.clear()
        users = [
            ("Farmers: ", "Understand seasonal yield and cost dynamics; select suitable crops and evaluate efficient irrigation methods (e.g., drip) to manage seasonal risks during periods like Zaid."),
            ("Agricultural Planners: ", "Optimize seasonal seed and fertilizer supply allocations and schedule canal water releases based on empirical seasonal rainfall patterns."),
            ("Agricultural Analysts: ", "Benchmark seasonal productivity patterns, evaluate resource efficiency ratios, and conduct sound observational modeling without misleading causal claims."),
            ("Policymakers: ", "Formulate targeted seasonal credit support, design drought/heatwave insurance schemes for summer crops, and prioritize micro-irrigation infrastructure investments.")
        ]
        for i, (title, desc) in enumerate(users):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(10)
            run1 = p.add_run()
            run1.text = "• " + title
            run1.font.bold = True
            run1.font.size = Pt(14)
            run1.font.color.rgb = RGBColor(27, 54, 93)
            run2 = p.add_run()
            run2.text = desc
            run2.font.size = Pt(13)
            run2.font.color.rgb = RGBColor(50, 50, 50)

# ==============================================================================
# SLIDE 5: TECHNOLOGY USED
# ==============================================================================
slide5 = prs.slides[4]
for shape in slide5.shapes:
    if shape.has_text_frame and shape.top > Inches(1.2):
        tf = shape.text_frame
        tf.clear()
        tech_items = [
            ("Python: ", "Core programming language for end-to-end data analytics, data cleaning, and statistical modeling."),
            ("Pandas: ", "Data ingestion, structural auditing, season-wise median imputation, and tabular aggregation."),
            ("NumPy: ", "Numerical transformations and vectorized conditional logic (e.g., Profit_Status classification)."),
            ("Matplotlib & Seaborn: ", "Academic-quality visualization for bar charts, cross-tabulated heatmaps, and scatter plots."),
            ("SciPy (scipy.stats): ", "Rigorous non-parametric inference: Kruskal-Wallis H-test and Spearman rank correlation."),
            ("Google Colab / Jupyter Notebook: ", "Interactive reproducible environment containing all code, outputs, and interpretations."),
            ("GitHub: ", "Version-controlled project repository, file management, and documentation hosting."),
            ("Microsoft PowerPoint: ", "Executive presentation deck reporting.")
        ]
        for i, (title, desc) in enumerate(tech_items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            run1 = p.add_run()
            run1.text = "• " + title
            run1.font.bold = True
            run1.font.size = Pt(14)
            run1.font.color.rgb = RGBColor(27, 54, 93)
            run2 = p.add_run()
            run2.text = desc
            run2.font.size = Pt(13)
            run2.font.color.rgb = RGBColor(50, 50, 50)

# ==============================================================================
# SLIDES 6 TO 10: EXACT 5 MAIN RESULT CHARTS
# ==============================================================================
results_data = [
    {
        "slide_idx": 5, # Slide 6
        "chart_file": "chart1_seasonal_yield.png",
        "header_title": "Seasonal Yield Performance",
        "subtitle": "Median Agricultural Yield by Season",
        "bullets": [
            "Kharif recorded the highest median yield at 1.94 Tonnes/Ha (Mean: 5.63 t/ha).",
            "Zaid recorded the lowest median yield at 1.45 Tonnes/Ha (Mean: 4.63 t/ha), while Rabi produced 1.66 Tonnes/Ha.",
            "Observed difference: Kharif median yield is approximately 0.49 Tonnes/Ha (~33.8%) higher than Zaid.",
            "Non-Causal Guardrail: Differences indicate seasonal variation and do not imply that season alone drives yield variation."
        ]
    },
    {
        "slide_idx": 6, # Slide 7
        "chart_file": "chart2_seasonal_profit.png",
        "header_title": "Seasonal Economic Performance",
        "subtitle": "Median Profit by Season",
        "bullets": [
            "Kharif is the only season demonstrating positive median profit at INR 38,808 per farm.",
            "Zaid recorded substantially lower median profitability (-INR 62,144), while Rabi records a slight median deficit (-INR 3,187).",
            "Cost and resource-use patterns may contribute to the observed profitability differences, but this analysis does not establish causation.",
            "Decision Impact: Underscores greater economic risk during the summer season and the need for risk buffers."
        ]
    },
    {
        "slide_idx": 7, # Slide 8
        "chart_file": "chart3_seasonal_rainfall.png",
        "header_title": "Seasonal Environmental Conditions",
        "subtitle": "Median Rainfall by Season",
        "bullets": [
            "Kharif received the highest median precipitation at 854.75 mm (Mean: 852.11 mm).",
            "Zaid received the lowest median rainfall at 283.30 mm, while Rabi received 430.30 mm.",
            "Lower observed rainfall in Rabi and Zaid indicates potentially greater reliance on irrigation compared with Kharif (~3.0x difference).",
            "Rainfall variation characterizes seasonal environments but operates alongside other agronomic factors."
        ]
    },
    {
        "slide_idx": 8, # Slide 9
        "chart_file": "chart4_crop_season_heatmap.png",
        "header_title": "Crop Performance Across Seasons",
        "subtitle": "Median Crop Yield Across Seasons",
        "bullets": [
            "Sugarcane recorded the highest median yield among the crops analyzed across all seasons (56.65 t/ha in Kharif, 45.46 t/ha in Rabi, 38.78 t/ha in Zaid).",
            "Food grains showed solid observed yields: Maize (2.255–3.12 t/ha), Rice (1.935–2.88 t/ha), and Wheat (1.84–2.36 t/ha).",
            "Pulses (0.655–1.09 t/ha) and Cotton (0.955–1.44 t/ha) recorded lower median yields across all three seasons.",
            "Observed Pattern: All 8 crops achieved their highest median yields in Kharif and lowest in Zaid."
        ]
    },
    {
        "slide_idx": 9, # Slide 10
        "chart_file": "chart5_rainfall_yield_scatter.png",
        "header_title": "Rainfall and Yield Relationship",
        "subtitle": "Relationship Between Rainfall and Agricultural Yield",
        "bullets": [
            "Spearman rank correlation: rho = 0.1295, p = 1.99e-16 across N = 4,000 farms.",
            "The analysis indicates a statistically significant, weak positive association between rainfall and yield.",
            "Caution: Correlation does not establish causation; higher rainfall does not singularly cause higher yields.",
            "Multiple agronomic inputs (irrigation, fertilization, soil quality, temperature) operate simultaneously."
        ]
    }
]

for item in results_data:
    slide = prs.slides[item["slide_idx"]]
    
    # Update header title to exact requested title
    for shape in slide.shapes:
        if shape.has_text_frame and shape.top < Inches(1.5) and shape.left < Inches(6):
            shape.text_frame.text = item["header_title"]
            for p in shape.text_frame.paragraphs:
                p.font.bold = True
                p.font.size = Pt(22)
                p.font.color.rgb = RGBColor(27, 54, 93)
        elif shape.has_text_frame and "[Add screen shots" in shape.text:
            shape.text_frame.clear()
            shape.left = Inches(20)
    
    # Remove older added textboxes/pictures on this slide if any
    for shape in list(slide.shapes):
        if shape.has_text_frame and shape.top > Inches(1.5) and shape.left > Inches(6.5):
            shape.text_frame.clear()
        elif shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE and shape.left < Inches(7) and shape.top < Inches(6.5) and shape.top > Inches(1.0):
            # This is the chart picture
            pass
            
    # Add/ensure chart picture on left
    chart_path = item["chart_file"]
    # Check if picture already there
    has_pic = any(s.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE and s.top > Inches(1.2) and s.top < Inches(6.5) for s in slide.shapes)
    if not has_pic:
        slide.shapes.add_picture(chart_path, Inches(0.8), Inches(1.6), width=Inches(6.0))
    
    # Add text box on right
    add_bullet_text(slide, Inches(7.1), Inches(1.6), Inches(5.6), Inches(4.8), item["subtitle"], item["bullets"])

# ==============================================================================
# SLIDE 11: FUTURE SCOPE
# ==============================================================================
slide11 = prs.slides[10]
for shape in list(slide11.shapes):
    if shape.has_text_frame and shape.top > Inches(1.5):
        shape.text_frame.clear()

scope_box = slide11.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.8))
tf = scope_box.text_frame
tf.word_wrap = True
scopes = [
    ("Predictive Machine Learning Forecasting: ", "Develop regression and ensemble models to forecast crop yield from multi-variable environmental inputs."),
    ("Weather-Driven Early Warning Systems: ", "Integrate real-time meteorological forecasts to anticipate drought, unseasonal rains, and heatwave impacts on seasonal crops."),
    ("Interactive Farm Analytics Dashboard: ", "Build an interactive web application allowing farmers to simulate seasonal crop choices, water requirements, and net profit margins."),
    ("Multi-Year Longitudinal Analysis: ", "Expand the dataset across multi-year cycles to evaluate long-term climate change impacts and seasonal variability trends."),
    ("Automated Crop Recommendation Engine: ", "Implement prescriptive models to recommend optimal crop-season-irrigation pairings tailored to soil chemistry and water availability."),
    ("Note on Scope: ", "The above enhancements represent proposed future capabilities and were not implemented in the current baseline exploratory project.")
]
for i, (title, desc) in enumerate(scopes):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(8)
    run1 = p.add_run()
    run1.text = "• " + title
    run1.font.bold = True
    run1.font.size = Pt(13)
    run1.font.color.rgb = RGBColor(27, 54, 93)
    run2 = p.add_run()
    run2.text = desc
    run2.font.size = Pt(12)
    run2.font.color.rgb = RGBColor(50, 50, 50)

# ==============================================================================
# SLIDE 12: GITHUB LINK
# ==============================================================================
slide12 = prs.slides[11]
for shape in list(slide12.shapes):
    if shape.has_text_frame and shape.top > Inches(1.5):
        shape.text_frame.clear()

git_box = slide12.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.8))
tf = git_box.text_frame
tf.word_wrap = True

p0 = tf.paragraphs[0]
p0.text = "Project Repository & Deliverables"
p0.font.bold = True
p0.font.size = Pt(18)
p0.font.color.rgb = RGBColor(27, 54, 93)
p0.space_after = Pt(14)

git_bullets = [
    "Repository Name: Seasonal-Agriculture-Performance-Analysis",
    "Repository URL: https://github.com/ImperialCoder01/Seasonal_Agriculture_Performance_Analysis",
    "Repository Files Included:",
    "   1. Seasonal_Agriculture_Performance_Analysis.ipynb  (Complete executed Jupyter Notebook with 49 cells and embedded charts)",
    "   2. seasonal_agriculture_performance_cleaned.csv     (Fully cleaned dataset with 4,000 records and zero missing values)",
    "   3. README.md                                        (Academic documentation with verified findings, tables, and defense notes)",
    "   4. Result Charts (chart1 to chart5 PNG files)       (High-resolution 300 DPI visualizations)",
    "Action Required: Upload the workspace files to your GitHub account and replace the placeholder above with your live link."
]
for b in git_bullets:
    p = tf.add_paragraph()
    p.text = "• " + b if not b.startswith("   ") else b
    p.font.size = Pt(13)
    p.space_after = Pt(6)
    p.font.color.rgb = RGBColor(40, 40, 40)

# ==============================================================================
# SLIDE 13: VOIS CERTIFICATE
# ==============================================================================
slide13 = prs.slides[12]
for shape in list(slide13.shapes):
    if shape.has_text_frame and shape.top > Inches(1.5):
        shape.text_frame.clear()

cert_box = slide13.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(4.2))
tf = cert_box.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "Course: Data Visualization — VOIS Internship Program"
p0.font.bold = True
p0.font.size = Pt(18)
p0.font.color.rgb = RGBColor(27, 54, 93)
p0.space_after = Pt(14)

cert_notes = [
    "Instructions for Certificate Insertion:",
    "1. Complete the mandatory Data Visualization course under the VOIS program.",
    "2. Download your Course Completion Certificate in image (PNG/JPG) or PDF format.",
    "3. Paste your certificate screenshot in the space provided on this slide.",
    "4. Ensure your Name, Certificate ID, and Course Name are clearly legible for academic evaluation."
]
for n in cert_notes:
    p = tf.add_paragraph()
    p.text = "• " + n
    p.font.size = Pt(14)
    p.space_after = Pt(8)
    p.font.color.rgb = RGBColor(60, 60, 60)

# ==============================================================================
# SLIDE 14: THANK YOU
# ==============================================================================
slide14 = prs.slides[13]
for shape in list(slide14.shapes):
    if shape.has_text_frame and shape.top > Inches(1.5):
        shape.text_frame.clear()

ty_box = slide14.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(3.5))
tf = ty_box.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "Thank You for Your Time and Consideration"
p0.font.bold = True
p0.font.size = Pt(22)
p0.font.color.rgb = RGBColor(27, 54, 93)
p0.space_after = Pt(14)

p1 = tf.add_paragraph()
p1.text = "Seasonal Agriculture Performance Analysis\nVOIS AICTE Internship Batch 1 (2026–2027)\nFinal Submission Deadline: 10 September 2026\n\nStudent Name: [Your Name]\nCollege: [Your College / University]\nAICTE Student ID: [Your AICTE ID]"
p1.font.size = Pt(15)
p1.font.color.rgb = RGBColor(50, 50, 50)

# Save presentation
output_ppt_name = 'VOIS_Major_Project_PPT_Submission_Template.pptx'
prs.save(output_ppt_name)
print(f"Presentation successfully updated and saved to {output_ppt_name}!")
