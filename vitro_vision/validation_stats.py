"""
validation_stats.py — TEMPO V3 validation & analysis modules
ดู research/_architecture_v3_TEMPO.md L7 สำหรับ full spec

Module 1: Inter-rater Reliability (ICC, QWK, Kappa)
Module 2: CV vs Expert Validation (Spearman, Bland-Altman)
Module 3: Treatment Comparison (ART-ANOVA, ART-C)  [Phase C]
Module 4: Growth Curve (Gompertz NLS per bottle)   ← Phase A ทำแล้ว
Module 5: Survival / Contamination (KM, CIF)       [Phase C]
"""
from __future__ import annotations
import json
import numpy as np
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# MODULE 4 — Gompertz Growth Curve  (Phase A — ทำได้เลย)
# ═══════════════════════════════════════════════════════════════

def _gompertz(t, K, k, tm):
    """Gompertz model: y = K * exp(-exp(-k * (t - tm)))"""
    return K * np.exp(-np.exp(-k * (t - tm)))


def gompertz_fit(days: list[float], values: list[float]) -> Optional[dict]:
    """
    Fit Gompertz growth curve ต่อขวด 1 ขวด

    Parameters
    ----------
    days   : list ของ day-point (เช่น [0, 1, 3, 5, 7, 14, 21, 28])
    values : list ของ green_coverage_pct (0–100) ที่ตรงกับ days

    Returns
    -------
    dict ที่มี:
        K          — asymptote (% สูงสุดที่ทำนาย)
        k          — growth rate parameter
        tm         — inflection point (วันที่เติบโตเร็วสุด)
        AGRmax     — maximum absolute growth rate = K*k/e (% / วัน)
        AUC_28     — area under curve วันที่ 0-28 (trapezoid approximation)
        lag_period — วันที่ค่าถึง 5% ของ K (ช่วง lag ก่อนโต)
        r2_adj     — adjusted R² ของ fit
    None ถ้า fit ล้มเหลว (ต้องการ ≥5 data points)
    """
    from scipy.optimize import curve_fit
    from scipy.integrate import trapezoid

    days = np.array(days, dtype=float)
    values = np.array(values, dtype=float)

    if len(days) < 5:
        return None

    # initial guess: K=max, k=0.1, tm=midpoint
    K0 = max(values) * 1.05 if max(values) > 0 else 10.0
    k0 = 0.1
    tm0 = days[len(days) // 2]

    try:
        popt, _ = curve_fit(
            _gompertz, days, values,
            p0=[K0, k0, tm0],
            bounds=([0, 0, -10], [100, 5, 60]),
            maxfev=5000
        )
    except Exception:
        return None

    K, k, tm = popt
    fitted = _gompertz(days, K, k, tm)

    # R² adjusted
    ss_res = np.sum((values - fitted) ** 2)
    ss_tot = np.sum((values - np.mean(values)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    n, p = len(days), 3
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - p - 1) if n > p + 1 else r2

    # AGRmax = K*k/e
    AGRmax = K * k / np.e

    # AUC 0–28 (trapezoid บน fitted curve)
    t_dense = np.linspace(0, 28, 280)
    y_dense = _gompertz(t_dense, K, k, tm)
    AUC_28 = float(trapezoid(y_dense, t_dense))

    # lag period = วันที่ค่าแรกถึง 5% K
    lag_period = None
    threshold = 0.05 * K
    for i, y in enumerate(y_dense):
        if y >= threshold:
            lag_period = float(t_dense[i])
            break

    return {
        'K':          round(float(K), 4),
        'k':          round(float(k), 4),
        'tm':         round(float(tm), 2),
        'AGRmax':     round(float(AGRmax), 4),
        'AUC_28':     round(AUC_28, 2),
        'lag_period': round(lag_period, 1) if lag_period is not None else None,
        'r2_adj':     round(float(r2_adj), 4),
    }


def fit_batch_gompertz(series: list[dict]) -> dict[str, Optional[dict]]:
    """
    Fit Gompertz สำหรับทุกขวดใน batch

    Parameters
    ----------
    series : output ของ database.get_batch_temporal_series() หรือ get_phenotype_series()
             แต่ละ row ต้องมี bottle_id, day_point, feature_vector (dict) หรือ green_coverage_pct

    Returns
    -------
    dict: {bottle_id: gompertz_params_or_None}
    """
    from collections import defaultdict
    grouped: dict[str, list] = defaultdict(list)
    for row in series:
        fv = row.get('feature_vector', {})
        if isinstance(fv, str):
            fv = json.loads(fv)
        # รองรับทั้ง feature_vector dict และ flat row จาก images
        green = fv.get('green_coverage_pct') if isinstance(fv, dict) else row.get('green_coverage_pct')
        if green is not None:
            grouped[row['bottle_id']].append((row['day_point'], green))

    results = {}
    for bottle_id, points in grouped.items():
        points.sort(key=lambda x: x[0])
        days = [p[0] for p in points]
        vals = [p[1] for p in points]
        results[bottle_id] = gompertz_fit(days, vals)
    return results


# ═══════════════════════════════════════════════════════════════
# MODULE 1 — Inter-rater Reliability  (Phase A — skeleton)
# ═══════════════════════════════════════════════════════════════

def icc_21(ratings_matrix: np.ndarray) -> Optional[dict]:
    """
    ICC(2,1) two-way random, absolute agreement
    ratings_matrix shape: (n_subjects, n_raters)
    Returns: {'icc': float, 'ci_lower': float, 'ci_upper': float}
    ต้องการ scipy ≥1.7
    """
    try:
        from scipy.stats import f as f_dist
        n, k = ratings_matrix.shape
        grand_mean = np.mean(ratings_matrix)
        SS_r = k * np.sum((np.mean(ratings_matrix, axis=1) - grand_mean) ** 2)
        SS_c = n * np.sum((np.mean(ratings_matrix, axis=0) - grand_mean) ** 2)
        SS_e = np.sum((ratings_matrix - np.mean(ratings_matrix, axis=1, keepdims=True)
                       - np.mean(ratings_matrix, axis=0, keepdims=True) + grand_mean) ** 2)
        MS_r = SS_r / (n - 1)
        MS_c = SS_c / (k - 1)
        MS_e = SS_e / ((n - 1) * (k - 1))
        icc = (MS_r - MS_e) / (MS_r + (k - 1) * MS_e + k * (MS_c - MS_e) / n)

        # Confidence interval (Shrout & Fleiss 1979 approximation)
        F1 = MS_r / MS_e
        df1, df2 = n - 1, (n - 1) * (k - 1)
        F_lower = F1 / f_dist.ppf(0.975, df1, df2)
        F_upper = F1 * f_dist.ppf(0.975, df2, df1)
        ci_lower = (F_lower - 1) / (F_lower + k - 1)
        ci_upper = (F_upper - 1) / (F_upper + k - 1)
        return {'icc': round(icc, 4), 'ci_lower': round(ci_lower, 4), 'ci_upper': round(ci_upper, 4)}
    except Exception:
        return None


def quadratic_weighted_kappa(r1: list, r2: list, n_categories: int = 5) -> Optional[float]:
    """QWK สำหรับ vigor grade 1–5"""
    try:
        from sklearn.metrics import cohen_kappa_score
        return round(cohen_kappa_score(r1, r2, weights='quadratic'), 4)
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
# MODULE 2 — CV vs Expert Validation  (Phase A — skeleton)
# ═══════════════════════════════════════════════════════════════

def spearman_ci(x: list, y: list, n_boot: int = 1000, seed: int = 42) -> Optional[dict]:
    """Spearman ρ + 95% CI bootstrap"""
    try:
        from scipy.stats import spearmanr
        rho, p = spearmanr(x, y)
        rng = np.random.default_rng(seed)
        boot_rhos = []
        n = len(x)
        xa, ya = np.array(x), np.array(y)
        for _ in range(n_boot):
            idx = rng.integers(0, n, size=n)
            r, _ = spearmanr(xa[idx], ya[idx])
            boot_rhos.append(r)
        ci = np.percentile(boot_rhos, [2.5, 97.5])
        return {
            'rho': round(float(rho), 4),
            'p': round(float(p), 6),
            'ci_lower': round(float(ci[0]), 4),
            'ci_upper': round(float(ci[1]), 4),
        }
    except Exception:
        return None


def bland_altman(method1: list, method2: list) -> Optional[dict]:
    """Bland-Altman: bias + LoA (±1.96 SD of differences)"""
    try:
        a, b = np.array(method1, dtype=float), np.array(method2, dtype=float)
        diff = a - b
        bias = np.mean(diff)
        sd = np.std(diff, ddof=1)
        return {
            'bias':      round(float(bias), 4),
            'loa_lower': round(float(bias - 1.96 * sd), 4),
            'loa_upper': round(float(bias + 1.96 * sd), 4),
            'sd_diff':   round(float(sd), 4),
        }
    except Exception:
        return None
