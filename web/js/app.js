/**
 * app.js - Master Frontend Controller (VitalSync AI)
 * 
 * Orchestrates:
 * 1. 1-Click Patient Personas (Demo Mode for College Viva)
 * 2. Quick vs. Deep Intake mode toggling & dynamic accordion
 * 3. High-speed AJAX communication with FastAPI (/api/analyze, /api/consultation)
 * 4. 60fps Canvas & SVG visualization rendering via charts.js
 * 5. Interactive live What-If counterfactual habit simulation
 * 6. Rich formatted glassmorphic Dr. Qwen AI consultation cards
 * 7. Triage banner state machine & hospital-grade print engine
 */

import { updateRadialGauge, drawCaffeineCurve, drawMacroDonut, animateNumber } from './charts.js';

let currentPayload = null;

// Preset Clinical Personas for 1-Click College Presentation
const PRESET_PERSONAS = {
    student: {
        age: 21,
        sex: "male",
        weight_kg: 74,
        height_cm: 176,
        systolic_bp: 122,
        diastolic_bp: 78,
        resting_hr_bpm: 72,
        actual_sleep_hours: 5.5,
        bedtime_phone_minutes: 75,
        bedtime_app: "short_form_video",
        blue_light_filter_active: false,
        snoring_frequent: false,
        daily_caffeine_mg: 280,
        hours_caffeine_before_bed: 4.0,
        daily_steps: 5500,
        goal_type: "fat_loss_moderate",
        symptoms: ["afternoon_crash", "eyelid_twitch"],
        waist_cm: null,
        body_fat_pct: null,
        daily_water_liters: 1.8,
        fruit_veg_servings: 2,
        fast_food_meals_per_week: 3,
        stress_level_1_to_10: 7,
        resistance_training_days_per_week: 2,
        cardio_sessions_per_week: 1
    },
    crisis: {
        age: 54,
        sex: "male",
        weight_kg: 92,
        height_cm: 175,
        systolic_bp: 186,  // Hypertensive Crisis Threshold (>=180)
        diastolic_bp: 124,  // Crisis Threshold (>=120)
        resting_hr_bpm: 96,
        actual_sleep_hours: 5.0,
        bedtime_phone_minutes: 40,
        bedtime_app: "messaging",
        blue_light_filter_active: false,
        snoring_frequent: true,
        daily_caffeine_mg: 350,
        hours_caffeine_before_bed: 2.0,
        daily_steps: 2800,
        goal_type: "maintenance_recomp",
        symptoms: ["chest_pain_radiating", "heart_flutter_post_coffee"],
        waist_cm: 104,
        body_fat_pct: 32.0,
        daily_water_liters: 1.4,
        fruit_veg_servings: 1,
        fast_food_meals_per_week: 5,
        stress_level_1_to_10: 9,
        resistance_training_days_per_week: 0,
        cardio_sessions_per_week: 0
    },
    worker: {
        age: 48,
        sex: "male",
        weight_kg: 96,
        height_cm: 172,
        systolic_bp: 138,
        diastolic_bp: 88,
        resting_hr_bpm: 78,
        actual_sleep_hours: 6.0,
        bedtime_phone_minutes: 60,
        bedtime_app: "short_form_video",
        blue_light_filter_active: false,
        snoring_frequent: true,
        daily_caffeine_mg: 250,
        hours_caffeine_before_bed: 4.5,
        daily_steps: 3200,
        goal_type: "fat_loss_moderate",
        symptoms: ["brain_fog", "afternoon_crash"],
        waist_cm: 98,
        body_fat_pct: 29.5,
        daily_water_liters: 1.5,
        fruit_veg_servings: 1,
        fast_food_meals_per_week: 4,
        stress_level_1_to_10: 7,
        resistance_training_days_per_week: 1,
        cardio_sessions_per_week: 0
    },
    athlete: {
        age: 26,
        sex: "male",
        weight_kg: 82,
        height_cm: 182,
        systolic_bp: 116,
        diastolic_bp: 74,
        resting_hr_bpm: 54,
        actual_sleep_hours: 8.0,
        bedtime_phone_minutes: 15,
        bedtime_app: "reading_audio",
        blue_light_filter_active: true,
        snoring_frequent: false,
        daily_caffeine_mg: 150,
        hours_caffeine_before_bed: 8.0,
        daily_steps: 11500,
        goal_type: "maintenance_recomp",
        symptoms: [],
        waist_cm: 80,
        body_fat_pct: 13.5,  // Activates Katch-McArdle Formula!
        daily_water_liters: 3.6,
        fruit_veg_servings: 5,
        fast_food_meals_per_week: 0,
        stress_level_1_to_10: 3,
        resistance_training_days_per_week: 4,
        cardio_sessions_per_week: 3
    }
};

// ---------------------------------------------------------------------------
// 1. Initial State & DOM Element Caching
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSliders();
    initSymptomPills();
    initPersonas();
    initModeToggle();
    initFormSubmit();
    initAiHandlers();
    initSimulatorSliders();
    initAnxietyModalHandlers();
    initWindowResizeHandler();

    // Trigger initial calculation with default persona
    executeDiagnosticAnalysis();
});

// ---------------------------------------------------------------------------
// 2. Tab Navigation
// ---------------------------------------------------------------------------
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');

                // Re-render canvas if tab becomes visible
                if (targetId === 'tab-nutrition' && currentPayload) {
                    const m = currentPayload.math_metrics;
                    drawMacroDonut(document.getElementById('canvasMacroDonut'), m.target_protein_g, m.target_fat_g, m.target_carbs_g, m.target_calories_kcal);
                } else if (targetId === 'tab-circadian' && currentPayload) {
                    const p = currentPayload.profile;
                    drawCaffeineCurve(document.getElementById('canvasCaffeineCurve'), p.daily_caffeine_mg, p.hours_caffeine_before_bed);
                }
            }
        });
    });

    const activateFromHash = () => {
        if (window.location.hash) {
            const hashTab = window.location.hash.substring(1);
            const matchingBtn = document.querySelector(`.tab-btn[data-tab="${hashTab}"]`);
            if (matchingBtn) {
                matchingBtn.click();
                setTimeout(() => window.scrollTo(0, 0), 10);
            }
        }
    };

    activateFromHash();
    window.addEventListener('hashchange', activateFromHash);
}

// ---------------------------------------------------------------------------
// 3. Slider Live Value Badges
// ---------------------------------------------------------------------------
function initSliders() {
    const sliders = [
        { id: 'inputHR', tag: 'valHR', format: v => `${v} BPM` },
        { id: 'inputSleep', tag: 'valSleep', format: v => `${v} hrs` },
        { id: 'inputPhone', tag: 'valPhone', format: v => `${v} min` },
        { id: 'inputCaffeine', tag: 'valCaffeine', format: v => `${v} mg` },
        { id: 'inputCaffHours', tag: 'valCaffHours', format: v => `${v} hrs` },
        { id: 'inputSteps', tag: 'valSteps', format: v => `${parseInt(v).toLocaleString()}` },
        { id: 'inputWater', tag: 'valWater', format: v => `${parseFloat(v).toFixed(1)} L` },
        { id: 'inputStress', tag: 'valStress', format: v => `${v} / 10` },
    ];

    sliders.forEach(s => {
        const input = document.getElementById(s.id);
        const tag = document.getElementById(s.tag);
        if (input && tag) {
            input.addEventListener('input', () => {
                tag.innerText = s.format(input.value);
            });
        }
    });
}

// ---------------------------------------------------------------------------
// 4. 1-Click Patient Personas (Demo Mode for College Viva)
// ---------------------------------------------------------------------------
function initPersonas() {
    const buttons = document.querySelectorAll('.persona-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const key = btn.getAttribute('data-persona');
            const data = PRESET_PERSONAS[key];
            if (!data) return;

            // Populate DOM fields
            document.getElementById('inputAge').value = data.age;
            document.getElementById('inputSex').value = data.sex;
            document.getElementById('inputWeight').value = data.weight_kg;
            document.getElementById('inputHeight').value = data.height_cm;
            document.getElementById('inputSysBP').value = data.systolic_bp;
            document.getElementById('inputDiaBP').value = data.diastolic_bp;
            document.getElementById('inputHR').value = data.resting_hr_bpm;
            document.getElementById('valHR').innerText = `${data.resting_hr_bpm} BPM`;

            document.getElementById('inputSleep').value = data.actual_sleep_hours;
            document.getElementById('valSleep').innerText = `${data.actual_sleep_hours} hrs`;
            document.getElementById('inputPhone').value = data.bedtime_phone_minutes;
            document.getElementById('valPhone').innerText = `${data.bedtime_phone_minutes} min`;
            document.getElementById('inputApp').value = data.bedtime_app;
            document.getElementById('inputBlueLight').checked = data.blue_light_filter_active;
            document.getElementById('inputSnoring').checked = data.snoring_frequent;

            document.getElementById('inputCaffeine').value = data.daily_caffeine_mg;
            document.getElementById('valCaffeine').innerText = `${data.daily_caffeine_mg} mg`;
            document.getElementById('inputCaffHours').value = data.hours_caffeine_before_bed;
            document.getElementById('valCaffHours').innerText = `${data.hours_caffeine_before_bed} hrs`;
            document.getElementById('inputSteps').value = data.daily_steps;
            document.getElementById('valSteps').innerText = `${data.daily_steps.toLocaleString()}`;
            document.getElementById('inputGoal').value = data.goal_type;

            // Deep fields
            if (document.getElementById('inputWaist')) document.getElementById('inputWaist').value = data.waist_cm || '';
            if (document.getElementById('inputBodyFat')) document.getElementById('inputBodyFat').value = data.body_fat_pct || '';
            if (document.getElementById('inputWater')) {
                document.getElementById('inputWater').value = data.daily_water_liters;
                document.getElementById('valWater').innerText = `${data.daily_water_liters} L`;
            }
            if (document.getElementById('inputProduce')) document.getElementById('inputProduce').value = data.fruit_veg_servings;
            if (document.getElementById('inputFastFood')) document.getElementById('inputFastFood').value = data.fast_food_meals_per_week;
            if (document.getElementById('inputAlcohol')) document.getElementById('inputAlcohol').value = 2;
            if (document.getElementById('inputResistance')) document.getElementById('inputResistance').value = data.resistance_training_days_per_week;
            if (document.getElementById('inputCardio')) document.getElementById('inputCardio').value = data.cardio_sessions_per_week;
            if (document.getElementById('inputStress')) {
                document.getElementById('inputStress').value = data.stress_level_1_to_10;
                document.getElementById('valStress').innerText = `${data.stress_level_1_to_10} / 10`;
            }

            // Sync symptom pills
            const pills = document.querySelectorAll('.symptom-pill');
            const chestPill = document.getElementById('pillChestEmergency');
            pills.forEach(p => {
                const code = p.getAttribute('data-code');
                if (data.symptoms.includes(code)) {
                    p.classList.add('selected');
                    if (code === 'chest_pain_radiating' && chestPill) chestPill.style.display = 'inline-block';
                } else {
                    p.classList.remove('selected');
                    if (code === 'chest_pain_radiating' && chestPill && !data.symptoms.includes(code)) {
                        chestPill.style.display = 'none';
                    }
                }
            });

            // Automatically trigger analysis
            executeDiagnosticAnalysis();
        });
    });
}

// ---------------------------------------------------------------------------
// 5. Quick vs Deep Intake Mode Toggle
// ---------------------------------------------------------------------------
function initModeToggle() {
    const btnQuick = document.getElementById('toggleQuick');
    const btnDeep = document.getElementById('toggleDeep');
    const deepSection = document.getElementById('deepIntakeSection');

    if (btnQuick && btnDeep && deepSection) {
        btnQuick.addEventListener('click', () => {
            btnQuick.classList.add('active');
            btnDeep.classList.remove('active');
            deepSection.style.display = 'none';
        });

        btnDeep.addEventListener('click', () => {
            btnDeep.classList.add('active');
            btnQuick.classList.remove('active');
            deepSection.style.display = 'flex';
        });
    }
}

// ---------------------------------------------------------------------------
// 6. Symptom Pill Selection
// ---------------------------------------------------------------------------
function initSymptomPills() {
    const pills = document.querySelectorAll('.symptom-pill');
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pill.classList.toggle('selected');
        });
    });
}

function getSelectedSymptoms() {
    const pills = document.querySelectorAll('.symptom-pill.selected');
    return Array.from(pills).map(p => p.getAttribute('data-code'));
}

// ---------------------------------------------------------------------------
// 7. Form Collection & Diagnostic Execution
// ---------------------------------------------------------------------------
function collectProfileFromDOM() {
    const waistVal = document.getElementById('inputWaist') ? parseFloat(document.getElementById('inputWaist').value) : null;
    const bodyFatVal = document.getElementById('inputBodyFat') ? parseFloat(document.getElementById('inputBodyFat').value) : null;
    const waterVal = document.getElementById('inputWater') ? parseFloat(document.getElementById('inputWater').value) : 2.0;
    const produceVal = document.getElementById('inputProduce') ? parseInt(document.getElementById('inputProduce').value) : 2;
    const fastFoodVal = document.getElementById('inputFastFood') ? parseInt(document.getElementById('inputFastFood').value) : 2;
    const alcoholVal = document.getElementById('inputAlcohol') ? parseInt(document.getElementById('inputAlcohol').value) : 2;
    const resistanceVal = document.getElementById('inputResistance') ? parseInt(document.getElementById('inputResistance').value) : 2;
    const cardioVal = document.getElementById('inputCardio') ? parseInt(document.getElementById('inputCardio').value) : 1;
    const stressVal = document.getElementById('inputStress') ? parseInt(document.getElementById('inputStress').value) : 6;

    return {
        age: parseInt(document.getElementById('inputAge').value) || 21,
        sex: document.getElementById('inputSex').value,
        height_cm: parseFloat(document.getElementById('inputHeight').value) || 176.0,
        weight_kg: parseFloat(document.getElementById('inputWeight').value) || 74.0,
        waist_cm: (!isNaN(waistVal) && waistVal > 0) ? waistVal : null,
        body_fat_pct: (!isNaN(bodyFatVal) && bodyFatVal > 0) ? bodyFatVal : null,
        systolic_bp: parseInt(document.getElementById('inputSysBP').value) || 122,
        diastolic_bp: parseInt(document.getElementById('inputDiaBP').value) || 78,
        resting_hr_bpm: parseInt(document.getElementById('inputHR').value) || 72,
        bedtime_hour: 23.5,
        wake_hour: 7.5,
        actual_sleep_hours: parseFloat(document.getElementById('inputSleep').value) || 5.5,
        chronotype: "intermediate",
        snooze_count: 1,
        snoring_frequent: document.getElementById('inputSnoring').checked,
        gasping_choking_nocturnal: false,
        total_screen_time_hours: 6.0,
        social_media_hours: 2.5,
        bedtime_phone_minutes: parseInt(document.getElementById('inputPhone').value) || 75,
        bedtime_app: document.getElementById('inputApp').value,
        screen_brightness_pct: 60,
        blue_light_filter_active: document.getElementById('inputBlueLight').checked,
        daily_water_liters: isNaN(waterVal) ? 2.0 : waterVal,
        fruit_veg_servings: isNaN(produceVal) ? 2 : produceVal,
        fast_food_meals_per_week: isNaN(fastFoodVal) ? 2 : fastFoodVal,
        hours_last_meal_to_bed: 2.0,
        daily_caffeine_mg: parseInt(document.getElementById('inputCaffeine').value) || 280,
        hours_caffeine_before_bed: parseFloat(document.getElementById('inputCaffHours').value) || 4.0,
        alcohol_drinks_per_week: isNaN(alcoholVal) ? 2 : alcoholVal,
        alcohol_near_bedtime: false,
        smoker_or_vaper: false,
        daily_steps: parseInt(document.getElementById('inputSteps').value) || 5500,
        resistance_training_days_per_week: isNaN(resistanceVal) ? 2 : resistanceVal,
        cardio_sessions_per_week: isNaN(cardioVal) ? 1 : cardioVal,
        desk_job_sedentary: true,
        symptoms: getSelectedSymptoms(),
        goal_type: document.getElementById('inputGoal').value,
        stress_level_1_to_10: isNaN(stressVal) ? 6 : stressVal
    };
}

function initFormSubmit() {
    const form = document.getElementById('healthForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        executeDiagnosticAnalysis();
    });
}

async function executeDiagnosticAnalysis() {
    const profile = collectProfileFromDOM();
    const btn = document.getElementById('btnAnalyze');
    if (btn) btn.innerHTML = '<span>⏳ Calculating Pipeline...</span>';

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });

        if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
        const payload = await res.json();
        currentPayload = payload;

        updateDashboardUI(payload);
    } catch (err) {
        console.error('Analysis error:', err);
    } finally {
        if (btn) btn.innerHTML = '<span>⚡ Run Diagnostic Pipeline</span>';
    }
}

// ---------------------------------------------------------------------------
// 8. UI Update Engine
// ---------------------------------------------------------------------------
function updateDashboardUI(payload) {
    const p = payload.profile;
    const m = payload.math_metrics;
    const ml = payload.ml_metrics;
    const t = payload.triage;

    // 1. Triage Banner
    const triageBanner = document.getElementById('triageBanner');
    const triageIcon = document.getElementById('triageBadgeIcon');
    const triageText = document.getElementById('triageBadgeText');
    if (triageBanner) {
        triageBanner.className = `triage-indicator ${t.level}`;
        triageIcon.innerText = t.level === 'red' ? '🚨' : (t.level === 'yellow' ? '⚠️' : '✅');
        triageText.innerHTML = `<strong>${t.badge_title}</strong>: ${t.banner_message}`;
    }

    // 2. BMI & Primary Vitals
    const calculatedBMI = (p.bmi !== undefined && p.bmi !== null) ? p.bmi : (p.weight_kg / Math.pow(p.height_cm / 100, 2)).toFixed(1);
    document.getElementById('valBMI').innerText = `${calculatedBMI}`;
    document.getElementById('valBP').innerText = `${p.systolic_bp} / ${p.diastolic_bp}`;
    document.getElementById('valBPCat').innerText = m.bp_category;
    document.getElementById('valBMR').innerText = `${Math.round(m.bmr_kcal).toLocaleString()}`;
    document.getElementById('valBMRFormula').innerText = m.bmr_formula_used;
    document.getElementById('valTDEE').innerText = `${Math.round(m.tdee_kcal).toLocaleString()}`;
    document.getElementById('valTargetCal').innerText = `Target: ${Math.round(m.target_calories_kcal).toLocaleString()} kcal`;

    // 3. Radial ML Gauges
    updateRadialGauge(
        document.getElementById('gaugeCardioCircle'),
        document.getElementById('gaugeCardioVal'),
        ml.cardiovascular_10yr_risk_pct,
        50, '%', true
    );
    updateRadialGauge(
        document.getElementById('gaugeDiabCircle'),
        document.getElementById('gaugeDiabVal'),
        ml.prediabetes_risk_pct,
        60, '%', true
    );
    updateRadialGauge(
        document.getElementById('gaugeSleepCircle'),
        document.getElementById('gaugeSleepVal'),
        ml.predicted_sleep_latency_min,
        80, 'm', true
    );
    document.getElementById('valDebtCategory').innerText = ml.sleep_debt_category;

    updateRadialGauge(
        document.getElementById('gaugeApneaCircle'),
        document.getElementById('gaugeApneaVal'),
        ml.sleep_apnea_probability_pct,
        60, '%', true
    );

    // 4. Macro Donut Chart & Cards
    drawMacroDonut(
        document.getElementById('canvasMacroDonut'),
        m.target_protein_g,
        m.target_fat_g,
        m.target_carbs_g,
        m.target_calories_kcal
    );
    document.getElementById('macroProteinVal').innerText = `${m.target_protein_g}g`;
    document.getElementById('macroFatVal').innerText = `${m.target_fat_g}g`;
    document.getElementById('macroCarbsVal').innerText = `${m.target_carbs_g}g`;
    document.getElementById('valDeficitPill').innerText = `${m.deficit_or_surplus_kcal} kcal Deficit/Surplus`;

    // Scale Water Bounds
    document.getElementById('scaleSwingRange').innerText = `±${m.expected_daily_scale_swing_min_kg} to ${m.expected_daily_scale_swing_max_kg} kg`;
    document.getElementById('glycogenWaterVal').innerText = `${(m.glycogen_water_bound_g / 1000).toFixed(1)} Liters`;

    // 5. Caffeine Elimination Curve
    drawCaffeineCurve(
        document.getElementById('canvasCaffeineCurve'),
        p.daily_caffeine_mg,
        p.hours_caffeine_before_bed
    );
    document.getElementById('caffActiveVal').innerText = `${m.caffeine_active_at_bedtime_mg} mg`;
    document.getElementById('caffHoursClearVal').innerText = `${m.caffeine_clearance_hours_needed} hrs`;
    const caffBadge = document.getElementById('caffeineStatusBadge');
    if (caffBadge) {
        if (m.caffeine_sleep_disruption_flag) {
            caffBadge.style.color = '#ef4444';
            caffBadge.style.borderColor = '#ef4444';
            caffBadge.innerText = 'High Sleep Disruption Risk (>25mg)';
        } else {
            caffBadge.style.color = '#10b981';
            caffBadge.style.borderColor = '#10b981';
            caffBadge.innerText = 'Optimal Clearance (<25mg)';
        }
    }

    // 6. Nutrient Deficiency Cards
    renderDeficiencyCards(payload.deficiency_analysis);

    // 7. Counterfactual Simulation Update
    updateSimulatorOutputs();

    // 8. Doctor Briefing Preview
    generateDoctorBriefingPreview(payload);

    // 9. Re-render charts for currently active tab
    const activeTab = document.querySelector('.tab-pane.active');
    if (activeTab) {
        if (activeTab.id === 'tab-nutrition') {
            drawMacroDonut(document.getElementById('canvasMacroDonut'), m.target_protein_g, m.target_fat_g, m.target_carbs_g, m.target_calories_kcal);
        } else if (activeTab.id === 'tab-circadian') {
            drawCaffeineCurve(document.getElementById('canvasCaffeineCurve'), p.daily_caffeine_mg, p.hours_caffeine_before_bed);
        }
    }
}

// ---------------------------------------------------------------------------
// 9. Interactive Live What-If Counterfactual Simulator (Tab 5)
// ---------------------------------------------------------------------------
function initSimulatorSliders() {
    const sPhone = document.getElementById('simPhoneSlider');
    const sSteps = document.getElementById('simStepsSlider');
    const sCaff = document.getElementById('simCaffSlider');

    const updateSimLabels = () => {
        if (sPhone) document.getElementById('lblSimPhone').innerText = `-${sPhone.value} min`;
        if (sSteps) document.getElementById('lblSimSteps').innerText = `+${parseInt(sSteps.value).toLocaleString()}`;
        if (sCaff) document.getElementById('lblSimCaffeine').innerText = `+${parseFloat(sCaff.value).toFixed(1)} hrs`;
        updateSimulatorOutputs();
    };

    [sPhone, sSteps, sCaff].forEach(s => {
        if (s) s.addEventListener('input', updateSimLabels);
    });
}

// Re-runs the real trained models on the server (POST /api/what-if).
// Debounced so dragging a slider doesn't flood the server with requests.
let simTimer = null;
function updateSimulatorOutputs() {
    if (!currentPayload) return;
    clearTimeout(simTimer);
    simTimer = setTimeout(runWhatIfOnServer, 200);
}

async function runWhatIfOnServer() {
    const sPhone = document.getElementById('simPhoneSlider');
    const sSteps = document.getElementById('simStepsSlider');
    const sCaff = document.getElementById('simCaffSlider');

    const body = {
        profile: currentPayload.profile,
        phone_reduction_min: sPhone ? parseInt(sPhone.value) : 30,
        extra_steps: sSteps ? parseInt(sSteps.value) : 3000,
        caffeine_cutoff_earlier_hours: sCaff ? parseFloat(sCaff.value) : 3.0
    };

    let r;
    try {
        const res = await fetch('/api/what-if', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
        r = await res.json();
    } catch (err) {
        console.error('What-if error:', err);
        return;
    }

    const latencyDrop = r.latency_reduction_minutes;
    const projectedLat = r.projected_latency_minutes;
    const fatigueDrop = r.fatigue_score_reduction;
    const projectedFat = r.projected_fatigue_score;
    const cardioDrop = r.cardio_risk_reduction_pct;
    const projectedCardio = r.projected_cardio_risk_pct;

    // Update DOM
    const dropLatEl = document.getElementById('cfLatencyDrop');
    const newLatEl = document.getElementById('cfNewLatency');
    const dropFatEl = document.getElementById('cfFatigueDrop');
    const newFatEl = document.getElementById('cfNewFatigue');
    const dropCardioEl = document.getElementById('cfCardioDrop');
    const newCardioEl = document.getElementById('cfNewCardio');

    if (dropLatEl) dropLatEl.innerText = `-${latencyDrop} min`;
    if (newLatEl) newLatEl.innerText = `Projected Onset: ~${projectedLat} min`;
    if (dropFatEl) dropFatEl.innerText = `-${fatigueDrop} pts`;
    if (newFatEl) newFatEl.innerText = `Projected Fatigue: ${projectedFat} / 10`;
    if (dropCardioEl) dropCardioEl.innerText = `-${cardioDrop}%`;
    if (newCardioEl) newCardioEl.innerText = `Projected Odds: ${projectedCardio}%`;
}

// ---------------------------------------------------------------------------
// 10. Deficiency Card Ingestion
// ---------------------------------------------------------------------------
function renderDeficiencyCards(analysis) {
    const container = document.getElementById('deficiencyCardsContainer');
    if (!container) return;

    if (!analysis.flagged_deficiencies || analysis.flagged_deficiencies.length === 0) {
        container.innerHTML = '<div style="color:#10b981; padding:16px;">✅ No significant micronutrient shortfalls identified!</div>';
        return;
    }

    container.innerHTML = analysis.flagged_deficiencies.map(d => `
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <h4 style="color:#38bdf8; font-size:1.05rem;">🔍 ${d.nutrient_name}</h4>
                <span class="status-pill" style="color:#a855f7; border-color:#a855f7;">Confidence: ${Math.round(d.confidence_score * 100)}%</span>
            </div>
            <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:10px;">${d.biological_function}</p>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:0.82rem;">
                <div>
                    <strong style="color:#ffffff;">Top Whole Foods:</strong>
                    <ul style="margin-left:16px; color:#cbd5e1; margin-top:4px;">
                        ${d.top_whole_food_sources.map(f => `<li>${f}</li>`).join('')}
                    </ul>
                </div>
                <div>
                    <strong style="color:#ffffff;">Absorption Rules:</strong>
                    <p style="color:#cbd5e1; margin-top:4px;">Cofactors: ${d.absorption_cofactors.join(', ')}</p>
                    <p style="color:#cbd5e1;">Inhibitors: ${d.absorption_inhibitors.join(', ')}</p>
                </div>
            </div>
        </div>
    `).join('');
}

// ---------------------------------------------------------------------------
// 11. Doctor Briefing Formatter & Downloader
// ---------------------------------------------------------------------------
async function generateDoctorBriefingPreview(payload) {
    const pre = document.getElementById('doctorBriefingPre');
    if (!pre) return;

    try {
        const res = await fetch('/api/export-doctor-briefing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload.profile)
        });
        const text = await res.text();
        pre.innerText = text;

        const downloadBtn = document.getElementById('btnDownloadBriefing');
        if (downloadBtn) {
            downloadBtn.onclick = () => {
                const blob = new Blob([text], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `clinical_briefing_${payload.profile.age}y_${payload.profile.sex}.md`;
                a.click();
                URL.revokeObjectURL(url);
            };
        }

        const printBtn = document.getElementById('btnPrintBriefing');
        if (printBtn) {
            printBtn.onclick = () => {
                window.print();
            };
        }
    } catch (err) {
        console.error('Doctor briefing fetch failed:', err);
    }
}

// ---------------------------------------------------------------------------
// 12. Local Qwen AI Handlers & Rich Markdown Formatter
// ---------------------------------------------------------------------------
function initAiHandlers() {
    const btnReport = document.getElementById('btnGenerateReport');
    const reportBox = document.getElementById('aiReportContainer');
    const toolbar = document.getElementById('aiReportToolbar');
    const btnCopy = document.getElementById('btnCopyReport');
    const btnPrint = document.getElementById('btnPrintReport');
    const engineBadge = document.getElementById('aiEngineBadge');

    let currentReportRaw = "";

    if (btnReport && reportBox) {
        btnReport.addEventListener('click', async () => {
            if (!currentPayload) return;
            btnReport.innerHTML = '<span>🧠 Prompting AI Interpreter...</span>';
            reportBox.innerHTML = '<div style="padding:24px; text-align:center; color:var(--primary-cyan);"><em>⚡ Connecting to local health intelligence engine... Synthesizing clinical payload...</em></div>';

            try {
                const res = await fetch('/api/consultation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentPayload)
                });
                const data = await res.json();
                currentReportRaw = data.report || "No report generated.";

                // Format the markdown into rich glassmorphic cards
                renderFormattedAiReport(currentReportRaw, data.mode);

                if (toolbar) toolbar.style.display = 'flex';
                if (engineBadge) {
                    if (data.mode === 'qwen_gpu') {
                        engineBadge.innerText = '🟢 Local Qwen GPU Live';
                        engineBadge.style.color = '#10b981';
                        engineBadge.style.borderColor = '#10b981';
                    } else {
                        engineBadge.innerText = '⚡ Deterministic Clinical Synthesizer';
                        engineBadge.style.color = '#38bdf8';
                        engineBadge.style.borderColor = '#38bdf8';
                    }
                }
            } catch (err) {
                reportBox.innerHTML = `<div style="color:#ef4444; padding:18px;">Error generating consultation: ${err}</div>`;
            } finally {
                btnReport.innerHTML = '<span>✨ Generate AI Consultation Report</span>';
            }
        });
    }

    if (btnCopy) {
        btnCopy.addEventListener('click', () => {
            if (currentReportRaw) {
                navigator.clipboard.writeText(currentReportRaw).then(() => {
                    btnCopy.innerText = '✅ Copied!';
                    setTimeout(() => { btnCopy.innerText = '📋 Copy Report'; }, 2000);
                });
            }
        });
    }

    if (btnPrint) {
        btnPrint.addEventListener('click', () => {
            window.print();
        });
    }

    // Ask Qwen Input
    const btnAsk = document.getElementById('btnAskQwen');
    const inputAsk = document.getElementById('inputAskQwen');
    const answerBox = document.getElementById('aiAskAnswer');

    if (btnAsk && inputAsk && answerBox) {
        btnAsk.addEventListener('click', async () => {
            const question = inputAsk.value.trim();
            if (!question) return;

            btnAsk.innerText = 'Asking...';
            answerBox.style.display = 'block';
            answerBox.innerHTML = '<em>Consulting evidence-based medical knowledge engine...</em>';

            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question, profile: currentPayload ? currentPayload.profile : null })
                });
                const data = await res.json();
                answerBox.innerHTML = formatMarkdownText(data.answer || "No response received.");
            } catch (err) {
                answerBox.innerText = `Error: ${err}`;
            } finally {
                btnAsk.innerText = 'Ask';
            }
        });
    }
}

function formatMarkdownText(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>');
}

function renderFormattedAiReport(reportText, mode) {
    const reportBox = document.getElementById('aiReportContainer');
    if (!reportBox) return;

    // Split report into the 4 standard clinical sections
    const sections = reportText.split(/(?=###\s+\d\.)/);

    if (sections.length < 4) {
        reportBox.innerHTML = `<div style="white-space:pre-wrap; line-height:1.7;">${reportText}</div>`;
        return;
    }

    let html = '';

    sections.forEach(sec => {
        const trimmed = sec.trim();
        if (trimmed.startsWith('### 1.')) {
            const content = trimmed.replace(/^###\s+1\..*?\n/, '');
            html += `
                <div class="ai-consult-card">
                    <h4>🩺 1. Compassionate Health Overview & Demystification</h4>
                    <p>${formatMarkdownText(content)}</p>
                </div>
            `;
        } else if (trimmed.startsWith('### 2.')) {
            const content = trimmed.replace(/^###\s+2\..*?\n/, '');
            html += `
                <div class="ai-consult-card">
                    <h4>🔬 2. Biological Breakdown of Symptoms</h4>
                    <p>${formatMarkdownText(content)}</p>
                </div>
            `;
        } else if (trimmed.startsWith('### 3.')) {
            const content = trimmed.replace(/^###\s+3\..*?\n/, '');
            const levers = content.split(/\n(?=\d\.)/);
            let leversHtml = '';
            levers.forEach((lev, idx) => {
                const cleanLev = lev.replace(/^\d+\.\s*/, '').trim();
                let leverClass = 'lever-sleep';
                if (idx === 1) leverClass = 'lever-nutrition';
                if (idx === 2) leverClass = 'lever-movement';
                leversHtml += `<div class="ai-lever-item ${leverClass}">${formatMarkdownText(cleanLev)}</div>`;
            });
            html += `
                <div class="ai-consult-card">
                    <h4>🎯 3. Your Top 3 High-Impact Action Levers for This Week</h4>
                    <div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">
                        ${leversHtml}
                    </div>
                </div>
            `;
        } else if (trimmed.startsWith('### 4.')) {
            const content = trimmed.replace(/^###\s+4\..*?\n/, '');
            const triageLevel = currentPayload ? currentPayload.triage.level : 'green';
            html += `
                <div class="ai-triage-card triage-${triageLevel}">
                    <h4 style="font-weight:700; margin-bottom:6px;">🛡️ 4. Safety & Medical Next Steps</h4>
                    <p>${formatMarkdownText(content)}</p>
                </div>
            `;
        }
    });

    reportBox.innerHTML = html;
}

// ---------------------------------------------------------------------------
// 13. "Am I Okay?" Anxiety De-escalation Modal
// ---------------------------------------------------------------------------
function initAnxietyModalHandlers() {
    window.alertAnxiety = function(type) {
        const modal = document.getElementById('anxietyModal');
        const title = document.getElementById('modalTitle');
        const body = document.getElementById('modalBody');

        if (type === 'heart') {
            title.innerText = '💓 Why is my heart pounding after coffee or in bed?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> In 95%+ of healthy adults, post-caffeine or bedtime heart thumping is a harmless autonomic arousal response, not cardiac damage.</p>
                <p style="margin-top:10px;">Caffeine blocks your brain's adenosine receptors, temporarily magnifying adrenaline sensitivity. When you lie down in a quiet room, your acoustic and somatic focus shifts onto your chest, making normal resting contractions feel exaggerated.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Drink 1 glass of cold water with electrolytes, take 4 slow breaths with longer exhales, and observe that your heart rate remains regular and calm.</p>
            `;
        } else if (type === 'scale') {
            title.innerText = '⚖️ Why did the scale jump 2 kg (4.5 lbs) overnight?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> Gaining 1 kg of true adipose fat requires consuming ~7,700 kcal <em>above</em> your maintenance burn in a single 24-hour period (virtually impossible from a single normal day).</p>
                <p style="margin-top:10px;">Rapid overnight jumps are <strong>intracellular glycogen and sodium water shifts</strong>. Each gram of stored carbohydrate binds 3 to 4 grams of water in your muscle tissue. High sodium meals temporarily hold extracellular fluid.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Continue normal hydration and balanced meals. The scale will normalize naturally within 48 to 72 hours.</p>
            `;
        } else if (type === 'twitch') {
            title.innerText = '👁️ Why is my eyelid or muscle twitching?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> Benign eyelid fluttering (myokymia) and muscle twitches are classic bodily signals of <strong>Magnesium depletion, elevated sympathetic stress/cortisol, and stimulant overconsumption</strong>—not ALS or motor neuron disease.</p>
                <p style="margin-top:10px;">Magnesium is biologically required for neuromuscular relaxation. When depleted by high caffeine or acute stress, tiny involuntary spasms fire harmlessly.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Drink an electrolyte beverage, eat a handful of pumpkin seeds or dark chocolate, and take a 10-minute digital break.</p>
            `;
        } else if (type === 'crash') {
            title.innerText = '📉 Why do I crash every day at 3:00 PM?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> An afternoon energy slump is a biological combination of your natural circadian core body temperature dip coupled with high-glycemic lunch insulin clearance.</p>
                <p style="margin-top:10px;">It does not mean you have sudden diabetes or hypoglycemia. High-carbohydrate, low-protein lunches trigger a quick insulin spike followed by rapid glucose clearance.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Ensure lunch contains at least 30g of protein and take a brisk 10-minute walk in natural sunlight.</p>
            `;
        } else if (type === 'brainfog') {
            title.innerText = '🧠 Why do I experience severe brain fog while studying or coding?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> Acute brain fog during late afternoon is almost always <strong>adenosine receptor saturation</strong>, mild dehydration (a 2% fluid deficit causes a 10% drop in cognitive speed), and blue-light circadian misalignment.</p>
                <p style="margin-top:10px;">When your brain breaks down ATP for mental energy throughout the day, adenosine accumulates. If sleep latency was prolonged the night before by late-night phone use, adenosine clearance is incomplete.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Drink 500 mL of water with a pinch of sea salt, look at a distant object outside for 3 minutes to relax ciliary eye muscles, and do 15 bodyweight squats to restore cerebral blood flow.</p>
            `;
        } else if (type === 'coldhands') {
            title.innerText = '❄️ Why are my hands and feet icy cold during long computer work?';
            body.innerHTML = `
                <p><strong>The Biological Reality:</strong> Icy extremities during computer work are driven by <strong>sympathetic vasoconstriction and physical immobility</strong>, not poor cardiovascular health or arterial blockage.</p>
                <p style="margin-top:10px;">Intense mental focus activates low-level sympathetic nervous system tone, directing blood toward the brain and major muscle groups while constricting peripheral micro-capillaries in your fingertips. Hours of seated posture also reduce venous pump activation in your calves.</p>
                <p style="margin-top:10px; color:#34d399;"><strong>What to do:</strong> Stand up, rotate your wrists and ankles for 60 seconds, and run warm water over your hands to stimulate instantaneous vasodilation.</p>
            `;
        }

        if (modal) modal.showModal();
    };
}

// ---------------------------------------------------------------------------
// 14. Projector Auto-Resize Engine
// ---------------------------------------------------------------------------
function initWindowResizeHandler() {
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (!currentPayload) return;
            const activeTab = document.querySelector('.tab-pane.active');
            if (activeTab) {
                if (activeTab.id === 'tab-nutrition') {
                    const m = currentPayload.math_metrics;
                    drawMacroDonut(document.getElementById('canvasMacroDonut'), m.target_protein_g, m.target_fat_g, m.target_carbs_g, m.target_calories_kcal);
                } else if (activeTab.id === 'tab-circadian') {
                    const p = currentPayload.profile;
                    drawCaffeineCurve(document.getElementById('canvasCaffeineCurve'), p.daily_caffeine_mg, p.hours_caffeine_before_bed);
                }
            }
        }, 150);
    });
}
