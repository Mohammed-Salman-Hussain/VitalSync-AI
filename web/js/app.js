/**
 * app.js - Master Frontend Controller
 * 
 * Orchestrates:
 * 1. Reactive form input tracking
 * 2. High-speed AJAX communication with FastAPI (/api/analyze, /api/consultation)
 * 3. 60fps Canvas & SVG visualization rendering via charts.js
 * 4. Triage banner state machine & Doctor briefing export
 */

import { updateRadialGauge, drawCaffeineCurve, drawMacroDonut, animateNumber } from './charts.js';

let currentPayload = null;

// ---------------------------------------------------------------------------
// 1. Initial State & DOM Element Caching
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSliders();
    initSymptomPills();
    initFormSubmit();
    initAiHandlers();
    initAnxietyModalHandlers();

    // Trigger initial calculation
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
// 4. Symptom Pill Selection
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
// 5. Form Collection & Diagnostic Execution
// ---------------------------------------------------------------------------
function collectProfileFromDOM() {
    return {
        age: parseInt(document.getElementById('inputAge').value) || 32,
        sex: document.getElementById('inputSex').value,
        height_cm: parseFloat(document.getElementById('inputHeight').value) || 178.0,
        weight_kg: parseFloat(document.getElementById('inputWeight').value) || 78.0,
        waist_cm: null,
        body_fat_pct: null,
        systolic_bp: parseInt(document.getElementById('inputSysBP').value) || 124,
        diastolic_bp: parseInt(document.getElementById('inputDiaBP').value) || 78,
        resting_hr_bpm: parseInt(document.getElementById('inputHR').value) || 68,
        bedtime_hour: 23.5,
        wake_hour: 7.5,
        actual_sleep_hours: parseFloat(document.getElementById('inputSleep').value) || 6.5,
        chronotype: "intermediate",
        snooze_count: 1,
        snoring_frequent: document.getElementById('inputSnoring').checked,
        gasping_choking_nocturnal: false,
        total_screen_time_hours: 6.0,
        social_media_hours: 2.5,
        bedtime_phone_minutes: parseInt(document.getElementById('inputPhone').value) || 45,
        bedtime_app: document.getElementById('inputApp').value,
        screen_brightness_pct: 60,
        blue_light_filter_active: document.getElementById('inputBlueLight').checked,
        daily_water_liters: 2.0,
        fruit_veg_servings: 2,
        fast_food_meals_per_week: 2,
        hours_last_meal_to_bed: 2.0,
        daily_caffeine_mg: parseInt(document.getElementById('inputCaffeine').value) || 200,
        hours_caffeine_before_bed: parseFloat(document.getElementById('inputCaffHours').value) || 5.0,
        alcohol_drinks_per_week: 2,
        alcohol_near_bedtime: false,
        smoker_or_vaper: false,
        daily_steps: parseInt(document.getElementById('inputSteps').value) || 7500,
        resistance_training_days_per_week: 3,
        cardio_sessions_per_week: 1,
        desk_job_sedentary: true,
        symptoms: getSelectedSymptoms(),
        goal_type: document.getElementById('inputGoal').value,
        stress_level_1_to_10: 6
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
// 6. UI Update Engine
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

    // 2. Top Metric Cards
    document.getElementById('valBMI').innerText = `${p.bmi}`;
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

    // 7. Counterfactual Simulation
    const cf = ml.counterfactual_scenarios;
    if (cf) {
        document.getElementById('cfLatencyDrop').innerText = `-${cf.latency_reduction_minutes} min`;
        document.getElementById('cfNewLatency').innerText = `Projected Onset: ~${cf.projected_latency_minutes} min`;
        document.getElementById('cfFatigueDrop').innerText = `-${cf.fatigue_score_reduction} pts`;
        document.getElementById('cfNewFatigue').innerText = `Projected Fatigue: ${cf.projected_fatigue_score}/10`;
        document.getElementById('cfCardioDrop').innerText = `-${cf.cardio_risk_reduction_pct}%`;
        document.getElementById('cfNewCardio').innerText = `Projected Odds: ${cf.projected_cardio_risk_pct}%`;
    }

    // 8. Doctor Briefing Preview
    generateDoctorBriefingPreview(payload);
}

// ---------------------------------------------------------------------------
// 7. Deficiency Card Ingestion
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
// 8. Doctor Briefing Formatter & Downloader
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
    } catch (err) {
        console.error('Doctor briefing fetch failed:', err);
    }
}

// ---------------------------------------------------------------------------
// 9. Local Qwen AI Handlers
// ---------------------------------------------------------------------------
function initAiHandlers() {
    const btnReport = document.getElementById('btnGenerateReport');
    const reportBox = document.getElementById('aiReportContainer');

    if (btnReport && reportBox) {
        btnReport.addEventListener('click', async () => {
            if (!currentPayload) return;
            btnReport.innerHTML = '<span>🧠 Prompting Qwen via Ollama...</span>';
            reportBox.innerHTML = '<em>Connecting to local Ollama on GPU (qwen3.5:0.8b)... Generating clinical consultation...</em>';

            try {
                const res = await fetch('/api/consultation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentPayload)
                });
                const data = await res.json();
                reportBox.innerText = data.report || "No report generated.";
            } catch (err) {
                reportBox.innerText = `Error generating consultation: ${err}`;
            } finally {
                btnReport.innerHTML = '<span>✨ Generate AI Consultation Report</span>';
            }
        });
    }

    const btnAsk = document.getElementById('btnAskQwen');
    const inputAsk = document.getElementById('inputAskQwen');
    const answerBox = document.getElementById('aiAskAnswer');

    if (btnAsk && inputAsk && answerBox) {
        btnAsk.addEventListener('click', async () => {
            const question = inputAsk.value.trim();
            if (!question) return;

            btnAsk.innerText = 'Asking...';
            answerBox.style.display = 'block';
            answerBox.innerText = 'Consulting local Qwen...';

            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question, profile: currentPayload ? currentPayload.profile : null })
                });
                const data = await res.json();
                answerBox.innerText = data.answer || "No response received.";
            } catch (err) {
                answerBox.innerText = `Error: ${err}`;
            } finally {
                btnAsk.innerText = 'Ask';
            }
        });
    }
}

// ---------------------------------------------------------------------------
// 10. "Am I Okay?" Anxiety De-escalation Modal
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
        }

        if (modal) modal.showModal();
    };
}
