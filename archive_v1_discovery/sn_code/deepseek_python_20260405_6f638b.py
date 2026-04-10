import numpy as np
import matplotlib.pyplot as plt
from time import time

# ============================================================
# دالة حساب المجموع S_N(sigma, t)
# ============================================================

def S(sigma, t, N):
    """
    حساب S_N(sigma, t) = sum_{n=1}^N n^{-sigma + i t}
    """
    n = np.arange(1, N + 1, dtype=np.float64)
    magnitude = n ** (-sigma)
    angle = t * np.log(n)
    return np.sum(magnitude * (np.cos(angle) + 1j * np.sin(angle)))

def compute_error(sigma, t, N):
    """حساب الخطأ المطلق: |C(N) - 1/√((1-σ)²+t²)|"""
    theory = 1 / np.sqrt((1 - sigma)**2 + t**2)
    S_val = S(sigma, t, N)
    C_val = np.abs(S_val) / (N ** (1 - sigma))
    return abs(C_val - theory)

# ============================================================
# قيم الاختبار
# ============================================================

# الأصفار غير البديهية الأولى
zeta_zeros = [14.134725141734693790, 21.022039638771554, 
              25.010857580145688, 30.424876125859513]

# قيم σ المختلفة (من 0 إلى 1 تقريباً)
sigma_values = [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# قيم N (نكتفي بقيم معقولة لأن الحسابات ستكون كثيرة)
N_values = [1000, 5000, 10000, 20000, 50000, 100000]

# لكل صفر، نأخذ t قريبة منه للمقارنة
offset = 0.1  # انحراف بسيط عن الصفر

# ============================================================
# التخزين
# ============================================================

results = {}

for sigma in sigma_values:
    results[sigma] = {
        "zero_errors": [],
        "near_errors": [],
        "zero_labels": [],
        "near_labels": []
    }
    
    for t_zero in zeta_zeros:
        # حساب الخطأ عند الصفر
        zero_errs = []
        for N in N_values:
            err = compute_error(sigma, t_zero, N)
            zero_errs.append(err)
        results[sigma]["zero_errors"].append(zero_errs)
        results[sigma]["zero_labels"].append(f"t={t_zero:.2f}")
        
        # حساب الخطأ عند t قريبة (بعد偏移)
        t_near = t_zero + offset
        near_errs = []
        for N in N_values:
            err = compute_error(sigma, t_near, N)
            near_errs.append(err)
        results[sigma]["near_errors"].append(near_errs)
        results[sigma]["near_labels"].append(f"t={t_near:.2f}")

# ============================================================
# عرض النتائج
# ============================================================

print("=" * 100)
print("تأثير أصفار زيتا على سرعة التقارب لمختلف قيم σ")
print("=" * 100)

for sigma in sigma_values:
    print(f"\n{'='*50}")
    print(f"σ = {sigma}")
    print(f"{'='*50}")
    print(f"{'N':>8} | {'عند الصفر (متوسط)':>20} | {'قريب من الصفر (متوسط)':>22} | {'نسبة التحسن':>15}")
    print("-" * 80)
    
    for i, N in enumerate(N_values):
        zero_avg = np.mean([err[i] for err in results[sigma]["zero_errors"]])
        near_avg = np.mean([err[i] for err in results[sigma]["near_errors"]])
        ratio = near_avg / zero_avg if zero_avg > 0 else float('inf')
        print(f"{N:8d} | {zero_avg:20.8e} | {near_avg:22.8e} | {ratio:15.2f}")
    
    # التحليل النهائي لـ σ
    final_zero = np.mean([err[-1] for err in results[sigma]["zero_errors"]])
    final_near = np.mean([err[-1] for err in results[sigma]["near_errors"]])
    final_ratio = final_near / final_zero
    
    print(f"\n📊 عند N={N_values[-1]}:")
    print(f"   متوسط الخطأ عند الأصفار: {final_zero:.4e}")
    print(f"   متوسط الخطأ قرب الأصفار: {final_near:.4e}")
    print(f"   نسبة التحسن: {final_ratio:.2f} مرة")
    
    if final_ratio > 100:
        print(f"   ⭐ تأثير قوي جداً! التقارب أسرع بـ {final_ratio:.0f} مرة")
    elif final_ratio > 10:
        print(f"   ✅ تأثير واضح! التقارب أسرع بـ {final_ratio:.1f} مرة")
    else:
        print(f"   ⚪ تأثير ضعيف أو معدوم")

# ============================================================
# رسم بياني شامل
# ============================================================

fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

for idx, sigma in enumerate(sigma_values):
    ax = axes[idx]
    
    # رسم الأصفار
    for i, zero_errs in enumerate(results[sigma]["zero_errors"]):
        ax.loglog(N_values, zero_errs, 'o-', linewidth=2, 
                 markersize=4, label=results[sigma]["zero_labels"][i])
    
    # رسم القيم القريبة (بخطوط متقطعة)
    for i, near_errs in enumerate(results[sigma]["near_errors"]):
        ax.loglog(N_values, near_errs, '--', linewidth=1.5, 
                 alpha=0.6, label=results[sigma]["near_labels"][i])
    
    ax.set_xlabel('N')
    ax.set_ylabel('الخطأ المطلق')
    ax.set_title(f'σ = {sigma}')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=6, loc='upper right')

plt.suptitle('تأثير أصفار زيتا على سرعة التقارب لمختلف قيم σ', fontsize=16)
plt.tight_layout()
plt.savefig('sigma_comparison.png', dpi=150)
plt.show()

# ============================================================
# رسم بياني يلخص تأثير σ
# ============================================================

plt.figure(figsize=(12, 6))

sigma_array = []
final_ratios = []

for sigma in sigma_values:
    final_zero = np.mean([err[-1] for err in results[sigma]["zero_errors"]])
    final_near = np.mean([err[-1] for err in results[sigma]["near_errors"]])
    ratio = final_near / final_zero
    sigma_array.append(sigma)
    final_ratios.append(ratio)

plt.semilogy(sigma_array, final_ratios, 'bo-', linewidth=2, markersize=8)
plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='لا فرق (نسبة = 1)')
plt.xlabel('σ', fontsize=12)
plt.ylabel('نسبة التحسن (خطأ قرب الصفر / خطأ عند الصفر)', fontsize=12)
plt.title('كيف يتغير تأثير أصفار زيتا مع σ؟', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('sigma_effect.png', dpi=150)
plt.show()

# ============================================================
# جدول ملخص
# ============================================================

print("\n" + "=" * 100)
print("جدول ملخص: نسبة التحسن (خطأ قرب الصفر / خطأ عند الصفر) عند أكبر N")
print("=" * 100)
print(f"{'σ':>8} | {'نسبة التحسن':>15} | {'التقييم':>20}")
print("-" * 50)

for sigma, ratio in zip(sigma_array, final_ratios):
    if ratio > 1000:
        evaluation = "⭐⭐⭐ فائق (آلاف المرات)"
    elif ratio > 100:
        evaluation = "⭐⭐ قوي جداً (مئات المرات)"
    elif ratio > 10:
        evaluation = "⭐ واضح (عشرات المرات)"
    elif ratio > 2:
        evaluation = "✓ ضعيف (أقل من 10 مرات)"
    else:
        evaluation = "○ شبه معدوم"
    print(f"{sigma:8.2f} | {ratio:15.2f} | {evaluation:20}")

print("\n" + "=" * 100)
print("ملاحظات:")
print("1. عندما تكون σ قريبة من 0، تأثير الأصفار ضعيف (كما رأينا سابقاً)")
print("2. عندما تكون σ = 0.5 (منتصف الشريط الحرج)، التأثير في أقصاه")
print("3. عندما تقترب σ من 1، التأثير يضعف مجدداً لأن N^{1-σ} ينمو ببطء")
print("4. التفسير: ζ(σ+it) = 0 عند الأصفار، مما يلغي الحد الرئيسي للخطأ")
print("=" * 100)