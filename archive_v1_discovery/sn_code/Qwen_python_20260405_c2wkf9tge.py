import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def compute_S_sigma_t(sigma, t, N):
    """حساب S_N(σ, t) بكفاءة عالية"""
    n = np.arange(1, N + 1, dtype=np.float64)
    magnitude = n ** (-sigma)
    angle = t * np.log(n)
    return np.sum(magnitude * np.exp(1j * angle))

def error_function(sigma, t, N):
    """دالة الخطأ E_N(σ, t)"""
    S_val = compute_S_sigma_t(sigma, t, N)
    computed = np.abs(S_val) / (N ** (1 - sigma))
    theory = 1.0 / np.sqrt((1 - sigma)**2 + t**2)
    return abs(computed - theory)

def detect_zeros_advanced(N, t_range, sigma=0.5):
    """
    خوارزمية متقدمة لكشف أصفار زيتا
    مع تحليل طيفي للخطأ
    """
    t_min, t_max = t_range
    num_points = 10000
    t_values = np.linspace(t_min, t_max, num_points)
    
    # حساب دالة الخطأ
    errors = np.array([error_function(sigma, t, N) for t in t_values])
    
    # تطبيع الخطأ
    normalized_errors = errors / np.median(errors)
    
    # كشف القيعان الحادة
    # نبحث عن قيم أقل من 10% من الوسيط
    threshold = 0.1
    candidate_indices = np.where(normalized_errors < threshold)[0]
    
    # تجميع القيعان المتجاورة
    zeros_candidates = []
    if len(candidate_indices) > 0:
        groups = np.split(candidate_indices, 
                         np.where(np.diff(candidate_indices) > 1)[0] + 1)
        for group in groups:
            # أخذ المتوسط المرجح بالخطأ
            idx = group[np.argmin(errors[group])]
            zeros_candidates.append(t_values[idx])
    
    return t_values, errors, zeros_candidates

# ═══════════════════════════════════════════════════════
# التطبيق: البحث عن الأصفار الأولى
# ═══════════════════════════════════════════════════════

N = 50000
t_min, t_max = 10, 35

t_vals, errors, detected_zeros = detect_zeros_advanced(N, (t_min, t_max))

# عرض النتائج
print("🔍 الأصفار المكتشفة:")
print("=" * 50)
known_zeros = [14.1347251417, 21.0220396388, 25.0108575801, 30.4248761259]
for i, t_zero in enumerate(detected_zeros, 1):
    # إيجاد أقرب صفر معروف
    closest = min(known_zeros, key=lambda x: abs(x - t_zero))
    error = abs(t_zero - closest) / closest * 100
    print(f"الصفر {i}: {t_zero:.10f}")
    print(f"        المعروف: {closest:.10f}")
    print(f"        الخطأ: {error:.2e}%")
    print()

# ═══════════════════════════════════════════════════════
# رسم منحنى الخطأ
# ═══════════════════════════════════════════════════════

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# المنحنى الكامل
ax1.plot(t_vals, errors, 'b-', linewidth=1, alpha=0.7)
ax1.set_ylabel('E_N(t)', fontsize=12)
ax1.set_title(f'دالة الخطأ عند σ=0.5, N={N}', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=np.median(errors)*0.1, color='r', linestyle='--', 
            label='العتبة (10% من الوسيط)')
ax1.legend()

# تكبير حول الأصفار
ax2.plot(t_vals, errors, 'b-', linewidth=1.5)
for zero in detected_zeros:
    ax2.axvline(x=zero, color='r', linestyle='--', alpha=0.7)
ax2.set_xlabel('t', fontsize=12)
ax2.set_ylabel('E_N(t)', fontsize=12)
ax2.set_title('تفاصيل القيعان عند الأصفار', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(t_min, t_max)

plt.tight_layout()
plt.show()

# ═══════════════════════════════════════════════════════
# اختبار سرعة التقارب عند الصفر وقربه
# ═══════════════════════════════════════════════════════

print("\n📊 مقارنة سرعة التقارب:")
print("=" * 60)
print(f"{'N':<10} | {'عند الصفر':<15} | {'قرب الصفر':<15} | {'النسبة':<10}")
print("-" * 60)

t_at_zero = 14.1347251417  # صفر حقيقي
t_near_zero = 14.5          # قريب من الصفر

N_values = [10**k for k in range(3, 7)]
for N in N_values:
    err_at = error_function(0.5, t_at_zero, N)
    err_near = error_function(0.5, t_near_zero, N)
    ratio = err_near / err_at if err_at > 0 else float('inf')
    print(f"{N:<10} | {err_at:<15.4e} | {err_near:<15.4e} | {ratio:<10.2f}")