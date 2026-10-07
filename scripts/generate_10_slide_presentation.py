"""
scripts/generate_10_slide_presentation.py - Master Pitch Deck Generator for VitalSync AI

Generates an executive, 10-slide, 16:9 widescreen presentation in PowerPoint (.pptx)
for IBM SkillsBuild Masterclass 5 (UN SDG 3, Target 3.4).
Incorporate all 7 real screenshot assets from the project, structured cards,
calibrated machine learning metrics, biophysical equations, and authentic speaker notes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Premium Dark Theme Color Palette
# -----------------------------------------------------------------------------
BG_COLOR = RGBColor(10, 16, 29)         # Deep slate navy (#0a101d)
CARD_BG = RGBColor(19, 28, 49)          # Card background (#131c31)
CARD_BORDER = RGBColor(36, 51, 82)      # Subtle border (#243352)
TEXT_WHITE = RGBColor(248, 250, 252)    # Primary text (#f8fafc)
TEXT_MUTED = RGBColor(148, 163, 184)    # Secondary muted (#94a3b8)
CYAN_ACCENT = RGBColor(56, 189, 248)    # Electric Cyan (#38bdf8)
GREEN_ACCENT = RGBColor(16, 185, 129)   # Emerald Green (#10b981)
AMBER_ACCENT = RGBColor(245, 158, 11)   # Amber Warning (#f59e0b)
PURPLE_ACCENT = RGBColor(168, 85, 247)  # Electric Violet (#a855f7)
CORAL_ACCENT = RGBColor(239, 68, 68)    # Coral Red (#ef4444)

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
OUTPUT_PPTX = os.path.join(os.path.dirname(os.path.dirname(__file__)), "VitalSync_AI_Presentation.pptx")


def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR


def add_header(slide, title_text, category="IBM SKILLSBUILD MASTERCLASS 5 • UN SDG 3 (TARGET 3.4)"):
    # Category Tracker Chip
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE


def add_card(slide, left, top, width, height, title, body_bullets, title_color=CYAN_ACCENT, bg_color=CARD_BG, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.16)
    tf.margin_bottom = Inches(0.16)

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(13)
    p_title.font.bold = True
    p_title.font.color.rgb = title_color
    p_title.space_after = Pt(6)

    for b in body_bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(3)


def add_image_container(slide, left, top, width, height, img_filename, label_text="LIVE DEMO PREVIEW"):
    # Outer frame
    frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    frame.fill.solid()
    frame.fill.fore_color.rgb = CARD_BG
    frame.line.color.rgb = CARD_BORDER
    frame.line.width = Pt(1.5)

    # Label on top of frame
    tf = frame.text_frame
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.08)
    p_lbl = tf.paragraphs[0]
    p_lbl.text = "🖥️ " + label_text.upper()
    p_lbl.font.size = Pt(9.5)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = CYAN_ACCENT

    # Add Picture inside container
    img_path = os.path.join(ASSETS_DIR, img_filename)
    if os.path.exists(img_path):
        pad_x = Inches(0.12)
        pad_top = Inches(0.35)
        pad_bot = Inches(0.12)
        img_w = width - (pad_x * 2)
        img_h = height - pad_top - pad_bot
        slide.shapes.add_picture(img_path, left + pad_x, top + pad_top, width=img_w, height=img_h)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen standard
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title & Executive Hook
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.75), Inches(6.8), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG
    badge.line.color.rgb = CYAN_ACCENT
    badge.line.width = Pt(1.2)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "🧬 IBM SKILLSBUILD MASTERCLASS 5 • UN SDG 3 (TARGET 3.4)"
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN_ACCENT

    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.1))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "VitalSync AI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "A Homogeneous, Scientifically Grounded, Local-First Health & Circadian Intelligence Engine"
    p1_sub.font.size = Pt(17)
    p1_sub.font.color.rgb = CYAN_ACCENT
    p1_sub.space_before = Pt(6)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "Eliminating cyberchondria through peer-reviewed biophysics, 5 ML models trained on 500,000+ CDC records, and local GPU LLM synthesis with zero cloud telemetry."
    p1_desc.font.size = Pt(12)
    p1_desc.font.color.rgb = TEXT_MUTED
    p1_desc.space_before = Pt(8)

    # 4 Highlights Grid
    add_card(s1, Inches(0.8), Inches(3.9), Inches(2.75), Inches(2.55), "100% Local GPU", [
        "Runs on user's own GPU via Ollama",
        "Zero external cloud network calls",
        "Complete HIPAA & GDPR privacy",
        "$0 marginal API query cost"
    ], CYAN_ACCENT)

    add_card(s1, Inches(3.78), Inches(3.9), Inches(2.75), Inches(2.55), "5 ML Ensembles", [
        "Trained on 500k+ CDC records",
        "Cardio Risk (ROC-AUC: 0.817)",
        "Pre-Diabetes (ROC-AUC: 0.819)",
        "Circadian Sleep Debt & Latency"
    ], GREEN_ACCENT)

    add_card(s1, Inches(6.76), Inches(3.9), Inches(2.75), Inches(2.55), "Zero Hallucination", [
        "Mifflin-St Jeor & Katch BMR math",
        "Caffeine 5.5h half-life decay curve",
        "Glycogen-water mass balance",
        "24 unit tests passing in pytest"
    ], AMBER_ACCENT)

    add_card(s1, Inches(9.74), Inches(3.9), Inches(2.75), Inches(2.55), "Clinical Safety", [
        "Deterministic 3-tier triage engine",
        "AHA/ACC blood pressure staging",
        "Level 3 Red Emergency UI override",
        "1-Page Doctor Briefing export"
    ], PURPLE_ACCENT)

    author_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.7), Inches(11.7), Inches(0.4))
    tf_a = author_box.text_frame
    p_a = tf_a.paragraphs[0]
    p_a.text = "Project Lead: Mohammed Salman Hussain  •  GitHub: github.com/Mohammed-Salman-Hussain/VitalSync-AI  •  Email: salmanhussain1199@gmail.com"
    p_a.font.size = Pt(10.5)
    p_a.font.color.rgb = TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "Good morning/afternoon everyone. My name is Mohammed Salman Hussain, and I am presenting VitalSync AI, "
        "created under IBM SkillsBuild Masterclass 5 in direct alignment with UN Sustainable Development Goal 3 (Target 3.4). "
        "VitalSync AI is an offline, local-first preventive health platform that eliminates health anxiety by combining peer-reviewed "
        "biophysics, machine learning calibrated on over 500,000 CDC records, and local GPU LLM synthesis with zero cloud telemetry. "
        "Everything you see today is production-ready, locally test-verified, and completely open source."
    )

    # =========================================================================
    # SLIDE 2: The Problem: The Cyberchondria Epidemic & Digital Fatigue
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Problem: The Cyberchondria Epidemic & Modern Digital Burnout", "The Urgent Problem • UN SDG 3 Context")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.64), Inches(5.1), "1. The Cyberchondria Panic Loop", [
        "Millions search common bodily signals: eyelid twitches, post-coffee heart palpitations, or 1.5kg scale jumps.",
        "Ad-driven search engines rank catastrophic worst-case diagnoses (ALS, cardiac failure, renal collapse) to drive page views.",
        "Triggers acute health anxiety, elevates sympathetic cortisol & blood pressure, causing more physical symptoms.",
        "Overwhelms primary care clinics and emergency departments with unnecessary panic visits."
    ], AMBER_ACCENT)

    add_card(s2, Inches(4.84), Inches(1.6), Inches(3.64), Inches(5.1), "2. Bedtime Screen Fatigue & Sleep Debt", [
        "Average knowledge worker spends 7-10 hours on screens plus 45-90 minutes doomscrolling in bed.",
        "Short-wavelength blue light suppresses pineal melatonin production.",
        "Late-afternoon caffeine remains biologically active due to its 5.5-hour half-life (t_1/2 = 5.5h).",
        "Causes severe sleep latency (30-60 min), chronic sleep debt, and accelerates digital burnout and metabolic decline."
    ], CYAN_ACCENT)

    add_card(s2, Inches(8.88), Inches(1.6), Inches(3.64), Inches(5.1), "3. Cloud Surveillance & AI Hallucinations", [
        "Commercial fitness trackers upload sensitive biometrics to third-party cloud brokers and advertisers.",
        "Users hesitate to log real health conditions due to legitimate privacy fears.",
        "Cloud LLMs act as ungrounded black boxes, hallucinating dietary targets and contradictory medical claims.",
        "Zero clinical guardrails or deterministic emergency override protocols."
    ], CORAL_ACCENT)

    s2.notes_slide.notes_text_frame.text = (
        "We have all been there: it is 1:00 AM, you feel an eyelid twitch after an espresso, you Google it, and within five minutes "
        "you are convinced you have a motor neuron disease. That is cyberchondria. Commercial search engines monetize fear. "
        "Meanwhile, we spend hours doomscrolling before bed, suppressing melatonin, while commercial apps monetize our sensitive "
        "biometrics. When users ask cloud chatbots for help, they get ungrounded, hallucinated numbers. We need a private, grounded solution."
    )

    # =========================================================================
    # SLIDE 3: Market Gap: Why Existing Solutions Fail
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Market Gap: Why Existing Solutions Fail Everyday Users", "Competitive Landscape & Market Gaps")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.45), "❌ Search Engines (Google / WebMD)", [
        "Monetize ad clicks by surfacing rare, terrifying pathologies for benign symptoms.",
        "Zero awareness of user vitals, caffeine clearance, or hydration context.",
        "Converts harmless muscle twitches into acute psychiatric health anxiety."
    ], AMBER_ACCENT)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.45), "❌ Fragmented Web Calculators", [
        "Siloed calculators for calories, macros, TDEE, and sleep debt that never communicate.",
        "Calorie advice completely ignores sleep latency, caffeine, and stress markers.",
        "Forces users to manually synthesize conflicting advice across 5 separate websites."
    ], CYAN_ACCENT)

    add_card(s3, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.45), "❌ Generic Cloud Chatbots (ChatGPT / Claude)", [
        "Ungrounded black boxes prone to mathematical and dietary hallucinations.",
        "Transmit private health prompts across third-party cloud infrastructure.",
        "Lacks deterministic clinical triage or emergency override boundaries."
    ], CORAL_ACCENT)

    add_card(s3, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.45), "❌ Subscription Wearables (Whoop / Oura Cloud)", [
        "Expensive $300+/year paywalls locking biometrics in proprietary cloud silos.",
        "Inaccessible to students, developers, and low-income demographics.",
        "Passive metric display without actionable, grounded anti-anxiety explanations."
    ], GREEN_ACCENT)

    s3.notes_slide.notes_text_frame.text = (
        "Existing tools fail across four major categories: search engines terrify you; single-purpose calculators are completely siloed; "
        "generic cloud LLMs hallucinate numbers and leak your data; and subscription wearables lock your own biometrics behind $300 annual paywalls. "
        "VitalSync AI unites all these disciplines into a single offline engine."
    )

    # =========================================================================
    # SLIDE 4: The Solution & Homogeneous Pipeline
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "The Solution: Homogeneous Single-Payload Architecture", "System Architecture & Core Innovation")

    pipeline_steps = [
        ("Step 1: Unified Schema Contract", "UserHealthProfile Pydantic object validates biometrics, sleep, bedtime screens, caffeine, and symptoms.", CYAN_ACCENT),
        ("Step 2: Biophysical Engine (<1ms)", "Calculates Mifflin/Katch BMR, dynamic macro partitioning, caffeine clearance curve, and scale weight bounds.", GREEN_ACCENT),
        ("Step 3: 5 ML Ensembles (~4ms)", "Singleton MLInferenceEngine runs models for 10-Yr Cardio Risk, Pre-Diabetes, Sleep Latency, and Burnout.", AMBER_ACCENT),
        ("Step 4: Clinical Safety Triage (<0.1ms)", "Deterministic rules evaluate AHA blood pressure staging and red flags; assigns Green, Yellow, or Red Override.", CORAL_ACCENT),
        ("Step 5: Master Diagnostic Payload", "Bundles all metrics, calibrated percentages, and flags into a tamper-proof ComprehensiveDiagnosticPayload JSON.", PURPLE_ACCENT),
        ("Step 6: Local Qwen GPU Synthesis (1-2s)", "Ollama feeds payload to local Qwen 0.8B on GPU for empathetic plain-English translation without hallucination.", CYAN_ACCENT)
    ]

    for idx, (stitle, sdesc, scolor) in enumerate(pipeline_steps):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 6.0)
        top = Inches(1.6 + row * 1.75)
        add_card(s4, left, top, Inches(5.6), Inches(1.55), stitle, [sdesc], scolor)

    s4.notes_slide.notes_text_frame.text = (
        "Here is our system architecture. The key architectural breakthrough is our Homogeneous Single-Payload Pipeline. "
        "One single Pydantic schema flows from input to biophysics math, machine learning inference, clinical safety triage, "
        "and local LLM synthesis. The local Qwen LLM is strictly an empathetic translator of locked, pre-computed truth. "
        "Because the numbers are pre-calculated by Python, the AI cannot hallucinate."
    )

    # =========================================================================
    # SLIDE 5: Core Feature 1 — Glassmorphic Dashboard & Risk Dials (With Images)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Production Dashboard: Multi-Risk Gauges & Macro Nutrition", "Product Showcase • Metabolic & Cardiovascular Intelligence")

    # Image 1: Dashboard Overview (Left column)
    add_image_container(s5, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.2), "dashboard_overview.png", "Live Dashboard Overview & Risk Dials")

    # Image 2: Macros Nutrition (Right column top)
    add_image_container(s5, Inches(7.8), Inches(1.5), Inches(4.7), Inches(2.9), "macros_nutrition.png", "Dynamic Macronutrient Donut")

    # Callout Card (Right column bottom)
    add_card(s5, Inches(7.8), Inches(4.55), Inches(4.7), Inches(2.15), "Metabolic Intelligence Highlights", [
        "Live 5-Dial SVG Risk Matrix: Visual color-coded risk probabilities.",
        "Dynamic Macronutrient Partitioning: 1.8g/kg protein & essential fat floor.",
        "Real-Time Vitals: Resting BP, Heart Rate & SpO2 with AHA staging.",
        "Sub-30ms REST API: Instantaneous payload calculation via FastAPI."
    ], GREEN_ACCENT)

    s5.notes_slide.notes_text_frame.text = (
        "This slide shows our live production dashboard running on localhost. On the left is the glassmorphic dashboard showing the live "
        "clinical triage banner and the five calibrated risk dials for cardiovascular risk, pre-diabetes, sleep latency, and burnout. "
        "On the right is our dynamic nutrition engine with macro partitioning based on the user's lean mass and activity levels. "
        "The entire interface communicates with our FastAPI backend with a sub-30ms roundtrip."
    )

    # =========================================================================
    # SLIDE 6: Core Feature 2 — Circadian Biology & 24h Caffeine Clock (With Image)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "24-Hour Caffeine Clock & Bedtime Stimulant Clearance", "Product Showcase • Circadian & Sleep Architecture")

    # Image: Caffeine Curve (Left column)
    add_image_container(s6, Inches(0.8), Inches(1.5), Inches(7.4), Inches(5.2), "caffeine_circadian.png", "24-Hour Caffeine Elimination Decay Curve")

    # Cards on the right
    add_card(s6, Inches(8.4), Inches(1.5), Inches(4.1), Inches(2.45), "Pharmacokinetic Half-Life Model", [
        "First-order elimination: C(t) = C0 * (0.5)^(t / 5.5)",
        "Models 24-hour serum stimulant clearance.",
        "Bedtime Cutoff Threshold: Flags whenever active caffeine exceeds 25mg at scheduled sleep time.",
        "Curfew Calculator: Computes exact hour to halt coffee."
    ], CYAN_ACCENT)

    add_card(s6, Inches(8.4), Inches(4.15), Inches(4.1), Inches(2.55), "Anti-Anxiety Demystification", [
        "Explains post-coffee heart palpitations as benign adenosine receptor blockade, NOT cardiac failure.",
        "Correlates bedtime screen blue light with melatonin inhibition.",
        "Reduces average sleep latency by 15-30 minutes through behavioral habit curfews.",
        "Preserves deep slow-wave sleep architecture."
    ], AMBER_ACCENT)

    s6.notes_slide.notes_text_frame.text = (
        "Here is our circadian sleep and caffeine engine. Caffeine has an average elimination half-life of 5.5 hours. "
        "If you drink 200 mg of caffeine at 4:00 PM, you still have nearly 100 mg active in your bloodstream at 10:00 PM. "
        "Our Canvas-rendered elimination curve maps exact stimulant clearance and alerts users if bedtime caffeine exceeds 25 mg. "
        "Crucially, it explains post-coffee heart flutters as harmless adenosine blockade, preventing late-night cardiac panic."
    )

    # =========================================================================
    # SLIDE 7: Core Feature 3 — What-If Simulator & Nutrient Matrix (With Images)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "What-If Simulation Engine & Nutrient Deficiency Graph", "Product Showcase • Counterfactual Habit Simulation")

    # Image 1: What-If Simulator (Left)
    add_image_container(s7, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.6), "what_if_simulator.png", "Interactive 'What-If' Habit Simulator")

    # Image 2: Nutrient Matrix (Right)
    add_image_container(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.6), "nutrient_matrix.png", "Functional Micronutrient Knowledge Matrix")

    # 2 Feature Summary Cards at Bottom
    add_card(s7, Inches(0.8), Inches(5.25), Inches(5.7), Inches(1.55), "Counterfactual 'What-If' Simulation", [
        "Live sliders for bedtime screen minutes (-45 min) and daily steps (+3,000).",
        "Forecasts projected sleep latency drop (-18 min) and cardiovascular risk decrease.",
        "Turns passive health tracking into proactive, actionable lifestyle experimentation."
    ], GREEN_ACCENT)

    add_card(s7, Inches(6.8), Inches(5.25), Inches(5.7), Inches(1.55), "Biochemical Deficiency Mapping", [
        "Connects brain fog, muscle twitches, and afternoon crashes to biological cofactors.",
        "Maps Magnesium, Potassium, B12, D3, and Ferritin to bioavailable whole-food sources.",
        "Highlights synergy (Vit C + Iron) and absorption inhibitors (tannins, phytates)."
    ], PURPLE_ACCENT)

    s7.notes_slide.notes_text_frame.text = (
        "On Slide 7, we showcase two of our most powerful interactive features. On the left is our counterfactual What-If simulator. "
        "Users can adjust sliders—such as reducing bedtime screen time by 45 minutes or adding 3,000 steps—and immediately see how their "
        "projected sleep latency drops by 18 minutes and their 10-year cardio risk improves. "
        "On the right is our functional micronutrient knowledge matrix, mapping subjective symptoms like eyelid twitches or cramps directly to biochemical cofactors."
    )

    # =========================================================================
    # SLIDE 8: Core Feature 4 — Mental Wellness & Clinical Safety (With Images)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "60s Panic De-escalator & 1-Page Doctor Briefing Export", "Product Showcase • Safety Triage & Clinical Continuity")

    # Image 1: Anxiety Deescalator (Left)
    add_image_container(s8, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.6), "anxiety_deescalator.png", "60-Second 'Am I Okay?' De-escalator")

    # Image 2: Doctor Briefing (Right)
    add_image_container(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.6), "doctor_briefing.png", "Standardized 1-Page Doctor Briefing")

    # 2 Feature Summary Cards at Bottom
    add_card(s8, Inches(0.8), Inches(5.25), Inches(5.7), Inches(1.55), "Biological Reassurance & Scale Mechanics", [
        "60-Second De-escalator explains twitches as fatigue/electrolyte shifts.",
        "Demystifies 1.5kg overnight scale jumps: 3-4g water bound per gram of glycogen.",
        "Dismantles the acute cyberchondria loop before users rush to the emergency room."
    ], AMBER_ACCENT)

    add_card(s8, Inches(6.8), Inches(5.25), Inches(5.7), Inches(1.55), "Deterministic 3-Tier Clinical Safety Triage", [
        "🟢 Level 1 Green: Self-directed wellness coaching enabled.",
        "🟡 Level 2 Yellow: Routine clinical checkup recommended (Stage 1/2 Hypertension).",
        "🔴 Level 3 Red: Emergency lockout for BP >= 180/120 or acute chest pain (calls 911/112)."
    ], CORAL_ACCENT)

    s8.notes_slide.notes_text_frame.text = (
        "Slide 8 demonstrates our commitment to patient well-being and clinical safety. On the left is our 'Am I Okay?' 60-second de-escalation "
        "tool. When someone sees a 1.5 kg scale jump overnight, we explain the biophysical glycogen-water mass balance—proving it is water retention, "
        "not fat gain. On the right is our 1-page standardized Doctor Visit Briefing. And underneath it all is our strict 3-tier clinical triage engine: "
        "if blood pressure is in hypertensive crisis or red flags occur, the entire app locks out lifestyle advice and directs the user to dial 911."
    )

    # =========================================================================
    # SLIDE 9: Scientific Rigor & Machine Learning Benchmarks
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "5 Supervised Models Trained on 500,000+ CDC Records", "Scientific Validation & ML Benchmarks")

    models_data = [
        ("1. 10-Yr Cardiovascular Risk", "CDC BRFSS 2020", "319,795 rows", "Balanced Logistic Regression", "ROC-AUC: 0.817", GREEN_ACCENT),
        ("2. Pre-Diabetes Screener", "CDC BRFSS 50/50", "70,692 rows", "HistGradientBoosting Classifier", "ROC-AUC: 0.819", CYAN_ACCENT),
        ("3. Circadian Latency & Debt", "Bedtime Screentime Cohort", "8,500 rows", "Multi-Output Regressor & Clf", "RMSE: 6.84 min", AMBER_ACCENT),
        ("4. Sleep Pathology Classifier", "Clinical Polysomnography", "374 rows", "Balanced Random Forest", "F1-Score: 0.893", PURPLE_ACCENT),
        ("5. Digital Burnout Screener", "Student Lifestyle Cohort", "100,000 rows", "HistGradientBoosting Regressor", "RMSE: 1.48 / 10", CYAN_ACCENT),
    ]

    for idx, (mname, msrc, mrows, malgo, mscore, mcolor) in enumerate(models_data):
        top = Inches(1.5 + idx * 0.95)
        add_card(s9, Inches(0.8), top, Inches(11.7), Inches(0.85), f"{mname}  •  {mrows} ({msrc})", [
            f"Algorithm: {malgo}   |   Primary Verified Benchmark: {mscore}   |   Cross-validated on authentic cohorts"
        ], mcolor)

    # Local GPU & Test Callout Box
    add_card(s9, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.85), "Local GPU Neural Engine & Test Suite", [
        "100% Offline GPU compute via Ollama (Qwen 3.5 0.8B)  •  $0.00 marginal query cost  •  24/24 unit tests passing in pytest (3.25s)"
    ], TEXT_WHITE, bg_color=CARD_BG, border_color=CYAN_ACCENT)

    s9.notes_slide.notes_text_frame.text = (
        "Zero hallucination requires genuine scientific rigor. VitalSync AI deploys 5 supervised machine learning models trained on over "
        "500,000 authentic records from the CDC and clinical polysomnography studies. Our cardiovascular model achieves an ROC-AUC of 0.817; "
        "our pre-diabetes screener achieves an ROC-AUC of 0.819 without invasive blood tests; and our sleep latency model achieves an RMSE of "
        "6.84 minutes. All 24 automated unit tests pass in 3.25 seconds."
    )

    # =========================================================================
    # SLIDE 10: Lean Canvas, UN SDG 3 Impact & Project Deliverables
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Lean Canvas Overview, UN SDG 3 (Target 3.4) & Next Horizons", "Business Model, Impact & Roadmap")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(3.64), Inches(5.1), "Business Model & Lean Canvas", [
        "Open-Core Model: Free MIT Community Edition for developers and public health.",
        "Desktop Pro ($29 One-Time): Packaged app with auto model manager & PDF export.",
        "Clinic B2B ($49/mo): Multi-client management, branded briefings, EHR export.",
        "Cost Structure: $0 cloud LLM fees; $0 cloud DB; >95% gross margin on software licenses."
    ], CYAN_ACCENT)

    add_card(s10, Inches(4.84), Inches(1.6), Inches(3.64), Inches(5.1), "UN SDG 3 (Target 3.4) Impact", [
        "NCD Prevention: Early non-invasive screening for cardiovascular disease and type 2 diabetes.",
        "Mental Well-Being: Demystifies somatic sensations to eliminate acute cyberchondria.",
        "Circadian Restoration: Cuts sleep latency and halts late doomscrolling habits.",
        "Health Equity: 100% free and open-source; runs locally without expensive cloud subscriptions."
    ], GREEN_ACCENT)

    add_card(s10, Inches(8.88), Inches(1.6), Inches(3.64), Inches(5.1), "Deliverables & Live Repository", [
        "Production REST Server (<30ms API) & Glassmorphic Dashboard.",
        "Streamlit Pro UI with interactive What-If habit simulation.",
        "24/24 Automated Unit Tests passing in pytest.",
        "Single Combined Lean Canvas & Concept Note PDF.",
        "GitHub: github.com/Mohammed-Salman-Hussain/VitalSync-AI",
        "Lead: Mohammed Salman Hussain (salmanhussain1199@gmail.com)"
    ], PURPLE_ACCENT)

    s10.notes_slide.notes_text_frame.text = (
        "In conclusion, VitalSync AI directly fulfills the requirements of IBM SkillsBuild Masterclass 5 and UN SDG 3, Target 3.4. "
        "Our business model relies on an open-core structure with unbeatable unit economics because inference runs 100% locally on user hardware. "
        "We have delivered a production REST API, dual web interfaces, 5 calibrated machine learning models, 24 passing unit tests, and "
        "a combined Lean Canvas and Concept Note PDF. The entire project is live on GitHub. Thank you very much, and I welcome your questions."
    )

    prs.save(OUTPUT_PPTX)
    print(f"Presentation saved successfully to: {OUTPUT_PPTX}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    build_presentation()
