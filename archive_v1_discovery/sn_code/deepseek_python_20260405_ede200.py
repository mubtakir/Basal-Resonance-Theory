import numpy as np
import matplotlib.pyplot as plt
from time import time

# ============================================================
# دالة حساب المجموع S_N(sigma, t)
# ============================================================

def S(sigma, t, N):
    """
    حساب S_N(sigma, t) = sum_{n=1}^N n^{-sigma + i t}
    باستخدام numpy للسرعة
    """
    n = np.arange(1, N + 1, dtype=np.float64)
    # n^(-sigma + i t) = n^(-sigma) * exp(i t ln n)
    magnitude = n ** (-sigma)
    angle = t * np.log(n)
    # جمع الأعداد المركبة
    return np.sum(magnitude * (np.cos(angle) + 1j * np.sin(angle)))

# ============================================================
# دالة حساب الخطأ: |S_N|/N^{1-sigma} - 1/√((1-σ)²+t²)
# ============================================================

def compute_error(sigma, t, N):
    """حساب الخطأ المطلق"""
    theory = 1 / np.sqrt((1 - sigma)**2 + t**2)
    S_val = S(sigma, t, N)
    C_val = np.abs(S_val) / (N ** (1 - sigma))
    return abs(C_val - theory)

# ============================================================
# إعداد قيم الاختبار
# ============================================================

# نقطة الاختبار: نأخذ σ = 0.5 (منتصف الشريط الحرج)
sigma_test = 0.5

# الأصفار غير البديهية الأولى لزيتا
# (الأجزاء التخيلية التقريبية)
zeta_zeros = {
    "Zero 1": 14.134725141734693790,
    "Zero 2": 21.022039638771554,
    "Zero 3": 25.010857580145688,
    "Zero 4": 30.424876125859513,
}

# قيم t عشوائية قريبة من هذه الأصفار للمقارنة
random_offsets = [-0.1, -0.05, 0.05, 0.1]
random_ts = {}
for name, t0 in zeta_zeros.items():
    for offset in random_offsets:
        random_ts[f"{name} ± {abs(offset)}"] = t0 + offset

# ============================================================
# قيم N التي سنختبرها
# ============================================================

N_values = [1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]

# ============================================================
# الاختبار الرئيسي
# ============================================================

print("=" * 80)
print("اختبار سرعة التقارب عند أصفار زيتا مقابل قيم t العشوائية")
print(f"σ = {sigma_test}")
print("=" * 80)

results = {}

# تخزين النتائج لكل t
for label, t_val in zeta_zeros.items():
    print(f"\n📊 حساب {label} (t = {t_val:.10f})...")
    errors = []
    for N in N_values:
        err = compute_error(sigma_test, t_val, N)
        errors.append(err)
        print(f"  N = {N:7d}: error = {err:.8e}")
    results[label] = errors

for label, t_val in random_ts.items():
    print(f"\n📊 حساب {label} (t = {t_val:.10f})...")
    errors = []
    for N in N_values:
        err = compute_error(sigma_test, t_val, N)
        errors.append(err)
        print(f"  N = {N:7d}: error = {err:.8e}")
    results[label] = errors

# ============================================================
# الرسم البياني
# ============================================================

plt.figure(figsize=(12, 7))

# رسم الأصفار
for label in zeta_zeros.keys():
    plt.loglog(N_values, results[label], 'o-', linewidth=2, 
               markersize=6, label=f"{label} (صفر زيتا)")

# رسم القيم العشوائية (بخطوط أفتح)
for label in random_ts.keys():
    plt.loglog(N_values, results[label], '--', linewidth=1.5, 
               alpha=0.6, label=f"{label} (عشوائي)")

plt.xlabel('N (مقياس لوغاريتمي)', fontsize=12)
plt.ylabel('الخطأ المطلق |C(N) - 1/√((1-σ)²+t²)|', fontsize=12)
plt.title(f'مقارنة سرعة التقارب: أصفار زيتا vs قيم عشوائية (σ = {sigma_test})', 
          fontsize=14)
plt.grid(True, alpha=0.3, which='both')
plt.legend(loc='upper right', fontsize=8, ncol=2)
plt.tight_layout()
plt.savefig('zeta_zeros_convergence.png', dpi=150)
plt.show()

# ============================================================
# التحليل الإحصائي: هل الفرق معنوي؟
# ============================================================

print("\n" + "=" * 80)
print("التحليل الإحصائي: هل التقارب أسرع عند الأصفار؟")
print("=" * 80)

# آخر خطأ (عند أكبر N)
for label in zeta_zeros.keys():
    final_error = results[label][-1]
    print(f"\n{label}:")
    print(f"  الخطأ النهائي عند N={N_values[-1]}: {final_error:.8e}")
    
    # مقارنة مع أقرب قيمة عشوائية
    t0 = zeta_zeros[label]
    for offset in random_offsets:
        random_label = f"{label} ± {abs(offset)}"
        if random_label in results:
            random_error = results[random_label][-1]
            ratio = random_error / final_error if final_error > 0 else float('inf')
            print(f"  مقارنة مع {random_label}: خطأ عشوائي = {random_error:.8e}, النسبة = {ratio:.4f}")

# ============================================================
# اختبار إضافي: نفس σ ولكن t مختلفة تماماً (بعيدة عن الأصفار)
# ============================================================

print("\n" + "=" * 80)
print("اختبار إضافي: t بعيدة جداً عن الأصفار")
print("=" * 80)

far_ts = [5.0, 10.0, 30.0, 50.0, 100.0]
far_results = {}

for t_val in far_ts:
    print(f"\n📊 حساب t = {t_val}...")
    errors = []
    for N in N_values:
        err = compute_error(sigma_test, t_val, N)
        errors.append(err)
        print(f"  N = {N:7d}: error = {err:.8e}")
    far_results[t_val] = errors

plt.figure(figsize=(12, 6))
for t_val, errors in far_results.items():
    plt.loglog(N_values, errors, 'o-', linewidth=2, label=f"t = {t_val}")
plt.xlabel('N', fontsize=12)
plt.ylabel('الخطأ المطلق', fontsize=12)
plt.title(f'سرعة التقارب لـ t بعيدة عن الأصفار (σ = {sigma_test})', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('far_ts_convergence.png', dpi=150)
plt.show()

print("\n" + "=" * 80)
print("✅ انتهى الاختبار. أرسل لي:")
print("  1. مخرجات الطباعة (الأخطاء لكل N)")
print("  2. الصور الناتجة (zeta_zeros_convergence.png و far_ts_convergence.png)")
print("  3. ملاحظاتك حول ما إذا كان التقارب أسرع عند الأصفار")
print("=" * 80)