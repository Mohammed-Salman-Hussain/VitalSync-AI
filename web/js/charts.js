/**
 * charts.js - High-Performance Vanilla Canvas & SVG Charting Module
 * 
 * Provides 60fps hardware-accelerated animations for:
 * 1. Animated SVG Radial Gauges (Cardio, Diabetes, Apnea, Stress)
 * 2. 24-Hour Pharmacokinetic Caffeine Elimination Canvas Curve
 * 3. Interactive Macronutrient Calorie Donut Chart
 * 4. Animated Number Counters
 */

// Helper to set up high-DPI canvas
function setupHighDpiCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const width = (rect.width > 0) ? rect.width : (canvas.clientWidth || 820);
    const height = (rect.height > 0) ? rect.height : (canvas.clientHeight || 280);
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx, width, height };
}

// ---------------------------------------------------------------------------
// 1. Radial SVG Gauge Animator
// ---------------------------------------------------------------------------
export function updateRadialGauge(circleElement, textElement, targetValue, maxValue = 100, unit = '%', isLowerBetter = true) {
    if (!circleElement || !textElement) return;

    const radius = 64;
    const circumference = 2 * Math.PI * radius;
    circleElement.style.strokeDasharray = `${circumference}`;

    const normalizedValue = Math.min(Math.max(targetValue, 0), maxValue);
    const progressFraction = normalizedValue / maxValue;
    const targetOffset = circumference * (1 - progressFraction);

    // Dynamic Color Mapping based on clinical threshold
    let strokeColor = '#38bdf8'; // Cyan default
    if (isLowerBetter) {
        if (progressFraction >= 0.6) {
            strokeColor = '#ef4444'; // Red
        } else if (progressFraction >= 0.3) {
            strokeColor = '#f59e0b'; // Amber
        } else {
            strokeColor = '#10b981'; // Emerald
        }
    } else {
        if (progressFraction >= 0.7) {
            strokeColor = '#10b981';
        } else if (progressFraction >= 0.4) {
            strokeColor = '#f59e0b';
        } else {
            strokeColor = '#ef4444';
        }
    }

    circleElement.style.stroke = strokeColor;
    circleElement.style.strokeDashoffset = `${targetOffset}`;

    // Animate Number Counting Up
    animateNumber(textElement, targetValue, unit);
}

export function animateNumber(element, target, unit = '', decimals = 1, duration = 800) {
    if (!element) return;
    const start = parseFloat(element.innerText) || 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1.0);
        // Ease-out cubic
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (target - start) * easeOut;

        element.innerText = `${current.toFixed(decimals)}${unit}`;

        if (progress < 1.0) {
            requestAnimationFrame(update);
        }
    }
    requestAnimationFrame(update);
}

// ---------------------------------------------------------------------------
// 2. 24-Hour Pharmacokinetic Caffeine Elimination Canvas Curve
// ---------------------------------------------------------------------------
export function drawCaffeineCurve(canvas, dailyCaffeineMg, hoursBeforeBed) {
    if (!canvas) return;
    const { ctx, width, height } = setupHighDpiCanvas(canvas);

    ctx.clearRect(0, 0, width, height);

    const padLeft = 45;
    const padRight = 25;
    const padTop = 25;
    const padBottom = 35;
    const plotW = width - padLeft - padRight;
    const plotH = height - padTop - padBottom;

    const maxHours = 20;
    const halfLife = 5.5;
    const maxMg = Math.max(dailyCaffeineMg * 1.15, 120);

    // 1. Grid lines and axis labels
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#64748b';
    ctx.font = '11px Plus Jakarta Sans, sans-serif';

    // Horizontal Y grid
    const ySteps = 4;
    for (let i = 0; i <= ySteps; i++) {
        const mgVal = Math.round((maxMg / ySteps) * i);
        const y = padTop + plotH - (i / ySteps) * plotH;
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(padLeft + plotW, y);
        ctx.stroke();
        ctx.fillText(`${mgVal}mg`, 8, y + 4);
    }

    // Horizontal 25 mg Sleep Disruption Threshold Line
    const y25 = padTop + plotH - (25 / maxMg) * plotH;
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.45)';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padLeft, y25);
    ctx.lineTo(padLeft + plotW, y25);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#f87171';
    ctx.fillText('25mg Disruption Floor', padLeft + plotW - 120, y25 - 6);

    // Vertical Bedtime Marker Line
    const clampedBedHours = Math.min(Math.max(hoursBeforeBed, 0), maxHours);
    const xBed = padLeft + (clampedBedHours / maxHours) * plotW;
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.5)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(xBed, padTop);
    ctx.lineTo(xBed, padTop + plotH);
    ctx.stroke();

    ctx.fillStyle = '#38bdf8';
    ctx.fillText('Bedtime', xBed - 18, padTop - 8);

    // 2. Plot First-Order Decay Curve: C(t) = C0 * 0.5^(t/5.5)
    ctx.beginPath();
    ctx.lineWidth = 3;
    const gradient = ctx.createLinearGradient(padLeft, 0, padLeft + plotW, 0);
    gradient.addColorStop(0, '#38bdf8');
    gradient.addColorStop(1, '#a855f7');
    ctx.strokeStyle = gradient;

    const points = [];
    for (let h = 0; h <= maxHours; h += 0.25) {
        const cVal = dailyCaffeineMg * Math.pow(0.5, h / halfLife);
        const x = padLeft + (h / maxHours) * plotW;
        const y = padTop + plotH - (cVal / maxMg) * plotH;
        points.push({ x, y, cVal });
        if (h === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Fill under curve
    ctx.lineTo(padLeft + plotW, padTop + plotH);
    ctx.lineTo(padLeft, padTop + plotH);
    ctx.closePath();
    const fillGrad = ctx.createLinearGradient(0, padTop, 0, padTop + plotH);
    fillGrad.addColorStop(0, 'rgba(56, 189, 248, 0.25)');
    fillGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
    ctx.fillStyle = fillGrad;
    ctx.fill();

    // 3. Highlight exact bedtime caffeine point
    const activeAtBed = dailyCaffeineMg * Math.pow(0.5, clampedBedHours / halfLife);
    const yBedPoint = padTop + plotH - (activeAtBed / maxMg) * plotH;

    ctx.beginPath();
    ctx.arc(xBed, yBedPoint, 6, 0, Math.PI * 2);
    ctx.fillStyle = activeAtBed > 25 ? '#ef4444' : '#10b981';
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();

    // Point badge
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px Outfit, sans-serif';
    ctx.fillText(`${activeAtBed.toFixed(1)} mg`, xBed + 10, yBedPoint + 4);
}

// ---------------------------------------------------------------------------
// 3. Macronutrient Donut Chart (Protein, Fat, Carbs)
// ---------------------------------------------------------------------------
export function drawMacroDonut(canvas, proteinG, fatG, carbsG, targetKcal) {
    if (!canvas) return;
    const { ctx, width, height } = setupHighDpiCanvas(canvas);

    ctx.clearRect(0, 0, width, height);

    const pKcal = proteinG * 4;
    const fKcal = fatG * 9;
    const cKcal = carbsG * 4;
    const totalKcal = Math.max(pKcal + fKcal + cKcal, 1);

    const segments = [
        { label: 'Protein', kcal: pKcal, grams: proteinG, color: '#38bdf8' },
        { label: 'Fats', kcal: fKcal, grams: fatG, color: '#f59e0b' },
        { label: 'Carbs', kcal: cKcal, grams: carbsG, color: '#a855f7' }
    ];

    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 20;
    const innerRadius = radius * 0.65;

    let startAngle = -Math.PI / 2;

    segments.forEach(seg => {
        const sliceAngle = (seg.kcal / totalKcal) * (Math.PI * 2);
        const endAngle = startAngle + sliceAngle;

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.arc(centerX, centerY, innerRadius, endAngle, startAngle, true);
        ctx.closePath();
        ctx.fillStyle = seg.color;
        ctx.fill();

        startAngle = endAngle;
    });

    // Center Display Text
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 22px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${Math.round(targetKcal)}`, centerX, centerY - 8);

    ctx.font = '11px Plus Jakarta Sans, sans-serif';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('TARGET KCAL', centerX, centerY + 14);
}
