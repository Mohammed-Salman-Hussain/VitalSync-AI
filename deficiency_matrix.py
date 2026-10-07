"""
deficiency_matrix.py - Bidirectional Micronutrient Deficiency Knowledge Base

Implements evidence-grounded nutritional biochemistry:
- Maps everyday functional symptoms to probable micronutrient shortfalls
- Prioritizes bioavailable whole-food dietary sources
- Specifies crucial biological absorption cofactors and inhibitors
- Formats actionable, non-alarmist lifestyle levers
"""

from typing import List, Dict, Any
from schemas import (
    UserHealthProfile,
    MicronutrientMatch,
    NutrientDeficiencyAnalysis
)

# ---------------------------------------------------------------------------
# Biological Knowledge Graph: Nutrients, Symptoms, Food Sources & Biochemistry
# ---------------------------------------------------------------------------

MICRONUTRIENT_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "Magnesium": {
        "symptoms": [
            "eyelid_twitch",
            "night_calf_cramps",
            "muscle_spasms",
            "restless_legs",
            "heart_flutter_post_coffee",
            "difficulty_switching_off_brain",
            "tension_headaches"
        ],
        "biological_function": (
            "Acts as an essential cofactor in over 300 enzymatic reactions. "
            "Regulates neuromuscular transmission, muscle relaxation, and GABAergic calming pathways in the central nervous system."
        ),
        "top_whole_food_sources": [
            "Pumpkin seeds (150 mg / oz)",
            "Spinach & Swiss chard (157 mg / cooked cup)",
            "Dark chocolate 85%+ (65 mg / oz)",
            "Black beans & lentils (120 mg / cup)",
            "Avocados & almonds"
        ],
        "absorption_cofactors": [
            "Vitamin B6 (enhances cellular magnesium uptake)",
            "Vitamin D3 (works synergistically in metabolic pathways)"
        ],
        "absorption_inhibitors": [
            "Excessive caffeine and alcohol (accelerate renal excretion of magnesium)",
            "High phytate unsoaked grains (modestly bind magnesium in the gut)"
        ],
        "safety_supplement_note": (
            "If dietary sources are insufficient, highly bioavailable forms like Magnesium Glycinate (for sleep/anxiety) "
            "or Magnesium Malate (for daytime energy/muscle soreness) are generally well tolerated. Avoid high doses of Magnesium Oxide due to poor absorption and laxative effects."
        )
    },
    "Vitamin D3": {
        "symptoms": [
            "chronic_fatigue",
            "brain_fog",
            "low_mood_winter",
            "frequent_minor_illnesses",
            "muscle_weakness",
            "poor_sleep_quality"
        ],
        "biological_function": (
            "Functions as a neuro-steroid hormone regulating hundreds of genes, calcium homeostasis, "
            "innate immune response, serotonin synthesis, and circadian rhythm entrainment."
        ),
        "top_whole_food_sources": [
            "Wild-caught sockeye salmon (600-800 IU / 3 oz)",
            "Sardines & mackerel (300-400 IU / 3 oz)",
            "Pasture-raised egg yolks (40-60 IU / yolk)",
            "UV-exposed mushrooms",
            "Fortified dairy or plant milks"
        ],
        "absorption_cofactors": [
            "Dietary healthy fats (essential: Vitamin D is fat-soluble)",
            "Vitamin K2 (MK-7) (ensures absorbed calcium is directed to bones and teeth rather than arterial walls)",
            "Magnesium (required for converting D3 into active 25-hydroxyvitamin D)"
        ],
        "absorption_inhibitors": [
            "Severe fat malabsorption",
            "Lack of midday sun exposure (UVB rays below latitude 37° in winter)"
        ],
        "safety_supplement_note": (
            "A routine annual 25(OH)D blood test is recommended to calibrate optimal intake (target 40-60 ng/mL). "
            "Standard lifestyle supplemental ranges are 1,000 to 2,000 IU/day with breakfast."
        )
    },
    "Iron & Ferritin": {
        "symptoms": [
            "cold_hands_feet",
            "chronic_fatigue",
            "brain_fog",
            "brittle_nails",
            "hair_thinning",
            "shortness_of_breath_stairs",
            "pale_skin"
        ],
        "biological_function": (
            "Core component of hemoglobin and myoglobin, responsible for oxygen transport to muscles and brain. "
            "Essential for cellular mitochondrial ATP energy production."
        ),
        "top_whole_food_sources": [
            "Grass-fed beef & organ meats (Heme iron - highly bioavailable)",
            "Lentils, chickpeas & kidney beans (Non-heme iron)",
            "Cooked spinach & Swiss chard",
            "Blackstrap molasses & pumpkin seeds"
        ],
        "absorption_cofactors": [
            "Vitamin C (ascorbic acid: doubles or triples non-heme plant iron absorption when eaten together)",
            "Fermented foods / sourdough preparation (reduces phytates)"
        ],
        "absorption_inhibitors": [
            "Tannins and polyphenols in coffee & tea (inhibit iron absorption by up to 60-70% if consumed within 1 hour of meals)",
            "High calcium intake taken simultaneously (competes for intestinal receptors)"
        ],
        "safety_supplement_note": (
            "Never take high-dose iron supplements without confirmed low Ferritin blood labs, as excess iron can cause oxidative tissue stress. "
            "Prioritize food pairings (e.g. lentils with lemon juice or bell peppers)."
        )
    },
    "Vitamin B12 (Cobalamin)": {
        "symptoms": [
            "brain_fog",
            "mental_sluggishness",
            "tingling_fingers_toes",
            "chronic_fatigue",
            "unsteady_balance",
            "smooth_inflamed_tongue"
        ],
        "biological_function": (
            "Required for myelin sheath maintenance around nerve fibers, DNA synthesis, "
            "and red blood cell maturation. Critical for homocysteine recycling."
        ),
        "top_whole_food_sources": [
            "Clams, oysters & sardines",
            "Beef liver & grass-fed beef",
            "Pasture-raised eggs & dairy",
            "Fortified nutritional yeast (essential for vegans)"
        ],
        "absorption_cofactors": [
            "Adequate stomach acid (HCl) and intrinsic factor secreted by gastric parietal cells"
        ],
        "absorption_inhibitors": [
            "Long-term use of proton pump inhibitors (PPIs/antacids)",
            "Metformin medication use",
            "Strict vegan diet without supplementation"
        ],
        "safety_supplement_note": (
            "Methylcobalamin or Adenosylcobalamin are bio-identical sublingual forms that bypass potential stomach acid absorption bottlenecks."
        )
    },
    "Zinc": {
        "symptoms": [
            "frequent_minor_illnesses",
            "white_spots_on_nails",
            "slow_wound_healing",
            "hair_thinning",
            "reduced_taste_smell",
            "acne_skin_breakouts"
        ],
        "biological_function": (
            "Catalyst for nearly 100 enzymes; vital for DNA replication, testosterone synthesis, "
            "thyroid hormone conversion (T4 to T3), and mucosal immune barrier defense."
        ),
        "top_whole_food_sources": [
            "Oysters (richest natural source)",
            "Grass-fed beef & poultry",
            "Pumpkin seeds & hemp seeds",
            "Cashews & lentils"
        ],
        "absorption_cofactors": [
            "Animal protein (forms soluble zinc-amino acid complexes that enhance absorption)"
        ],
        "absorption_inhibitors": [
            "High phytate unsprouted grains",
            "Excessive copper or high-dose iron taken at the exact same moment"
        ],
        "safety_supplement_note": (
            "Zinc Picolinate or Zinc Bisglycinate (15-25 mg) are well absorbed. Always take zinc with a meal to avoid nausea."
        )
    },
    "Potassium & Electrolytes": {
        "symptoms": [
            "night_calf_cramps",
            "muscle_weakness",
            "heart_flutter_post_coffee",
            "afternoon_crash",
            "high_blood_pressure_tendency"
        ],
        "biological_function": (
            "Primary intracellular electrolyte. Drives the sodium-potassium pump ($Na^+/K^+\\text{-ATPase}$), "
            "regulates arterial vasodilation, blood pressure, and cellular hydration."
        ),
        "top_whole_food_sources": [
            "Cooked potatoes with skin (900 mg / medium potato)",
            "Avocados (700 mg / medium avocado)",
            "Coconut water (600 mg / cup)",
            "Bananas, kiwi & cantaloupe",
            "Spinach & acorn squash"
        ],
        "absorption_cofactors": [
            "Adequate magnesium (magnesium is required for the sodium-potassium pump to function properly)"
        ],
        "absorption_inhibitors": [
            "Very high sodium intake without potassium balance",
            "Heavy perspiration without electrolyte replacement"
        ],
        "safety_supplement_note": (
            "Always obtain potassium primarily from whole foods (potatoes, squash, avocados, coconut water) "
            "rather than high-dose supplements, to maintain safe cardiac conduction."
        )
    }
}


def analyze_symptom_deficiencies(profile: UserHealthProfile) -> NutrientDeficiencyAnalysis:
    """
    Evaluates the user's active symptoms against the biological knowledge graph.
    Computes a confidence score for each nutrient and generates prioritized, safe lifestyle levers.
    """
    user_symptoms = set(profile.symptoms)
    flagged: List[MicronutrientMatch] = []
    
    # Also infer implicit metabolic context
    if profile.daily_caffeine_mg >= 300:
        user_symptoms.add("caffeine_depletion_risk")
    if profile.fruit_veg_servings < 2:
        user_symptoms.add("low_produce_intake")
    if profile.daily_water_liters < 1.5:
        user_symptoms.add("mild_dehydration")

    for nutrient, data in MICRONUTRIENT_KNOWLEDGE_BASE.items():
        nutrient_symptoms = set(data["symptoms"])
        matches = list(user_symptoms.intersection(nutrient_symptoms))
        
        if matches:
            # Confidence score based on proportion of matched hallmark symptoms
            confidence = round(min(len(matches) / max(len(nutrient_symptoms) * 0.4, 1.0), 1.0), 2)
            
            flagged.append(
                MicronutrientMatch(
                    nutrient_name=nutrient,
                    confidence_score=confidence,
                    matched_symptoms=matches,
                    biological_function=data["biological_function"],
                    top_whole_food_sources=data["top_whole_food_sources"],
                    absorption_cofactors=data["absorption_cofactors"],
                    absorption_inhibitors=data["absorption_inhibitors"],
                    safety_supplement_note=data["safety_supplement_note"]
                )
            )

    # Sort flagged nutrients by confidence score descending
    flagged.sort(key=lambda x: x.confidence_score, reverse=True)

    # Formulate prioritized lifestyle action levers
    levers: List[str] = []
    if any(m.nutrient_name == "Magnesium" for m in flagged):
        levers.append("Add 1 oz pumpkin seeds or 1 cup cooked spinach to dinner to support neuromuscular calming.")
    if any(m.nutrient_name == "Vitamin D3" for m in flagged):
        levers.append("Get 15-20 min of morning natural sunlight; include egg yolks or wild salmon in weekly meals.")
    if any(m.nutrient_name == "Iron & Ferritin" for m in flagged):
        levers.append("Avoid coffee/tea within 1 hour of iron-rich meals; pair plant iron (lentils/spinach) with Vitamin C.")
    if profile.fruit_veg_servings < 3:
        levers.append("Increase colorful fruit & vegetable servings to at least 4 daily to naturally cover potassium & trace minerals.")
    if not levers:
        levers.append("Maintain your balanced micronutrient profile by eating diverse, colorful whole foods.")

    return NutrientDeficiencyAnalysis(
        flagged_deficiencies=flagged,
        total_symptoms_evaluated=len(profile.symptoms),
        primary_lifestyle_levers=levers
    )
