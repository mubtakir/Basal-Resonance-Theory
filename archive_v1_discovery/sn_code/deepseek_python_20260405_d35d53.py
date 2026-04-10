import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def compute_C_at_N(t, N_target):
    """حساب C(N) = |S(N)|/N عند N_target"""
    S = 0 + 0j
    for n in range(1, N_target + 1):
        S += n ** (1j * t)
    return np.abs(S) / N_target

# بياناتنا المحسوبة (من النتائج السابقة)
# نستخدم نفس N_target = 50000
t_values_computed = [0.01, 0.1, 0.5, 1.0, 2.0, 3.14, 5.0, 7.0, 10.0, 
                     14.134725, 21.02204, 30.0, 50.0, 100.0, 200.0, 500.0]
C_values_computed = [0.99995007, 0.99504321, 0.89442776, 0.70710901, 0.44722197, 
                     0.30345986, 0.19610460, 0.14144118, 0.09953953, 0.07056554, 
                     0.04750220, 0.03334309, 0.01998018, 0.01012560, 0.00531284, 0.00195149]

# إضافة نقاط إضافية لرسم منحنى نظري سلس
t_smooth = np.logspace(-2, 3, 500)  # من 0.01 إلى 1000
C_theoretical_small = np.ones_like(t_smooth)  # للـ t صغيرة
C_theoretical_large = 1 / t_smooth  # للـ t كبيرة

# التحول عند t=1
t_transition = 1.0

# رسم بياني 1: مقياس خطي-خطي (لرؤية التفاصيل عند t صغيرة)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. مقياس خطي-خطي
ax1 = axes[0, 0]
ax1.plot(t_values_computed, C_values_computed, 'bo-', linewidth=2, markersize=8, label='بيانات محسوبة')
ax1.plot(t_smooth, C_theoretical_small, 'r--', linewidth=1.5, alpha=0.5, label='C(t) ≈ 1 (لـ t→0)')
ax1.plot(t_smooth, C_theoretical_large, 'g--', linewidth=1.5, alpha=0.5, label='C(t) = 1/t (لـ t كبير)')
ax1.axvline(x=t_transition, color='purple', linestyle=':', alpha=0.7, label=f'التحول عند t={t_transition}')
ax1.set_xlabel('t', fontsize=12)
ax1.set_ylabel('C(t) = |S(N)|/N', fontsize=12)
ax1.set_title('السلوك العام لـ C(t) (مقياس خطي)', fontsize=14)
ax1.set_xlim(0, 30)
ax1.set_ylim(0, 1.1)
ax1.grid(True, alpha=0.3)
ax1.legend()

# 2. مقياس لوغاريتمي-لوغاريتمي (لرؤية قانون القوة)
ax2 = axes[0, 1]
ax2.loglog(t_values_computed, C_values_computed, 'bo-', linewidth=2, markersize=8, label='بيانات محسوبة')
ax2.loglog(t_smooth, 1/t_smooth, 'r--', linewidth=2, alpha=0.7, label='C(t) = 1/t (قانون القوة)')
ax2.loglog(t_smooth[t_smooth<1], np.ones_like(t_smooth[t_smooth<1]), 'g--', linewidth=1.5, alpha=0.5, label='C(t) ≈ 1 (لـ t<1)')
ax2.axvline(x=t_transition, color='purple', linestyle=':', alpha=0.7, label=f'التحول عند t={t_transition}')
ax2.set_xlabel('t (مقياس لوغاريتمي)', fontsize=12)
ax2.set_ylabel('C(t) (مقياس لوغاريتمي)', fontsize=12)
ax2.set_title('السلوك اللوغاريتمي لـ C(t)', fontsize=14)
ax2.grid(True, alpha=0.3, which='both')
ax2.legend()

# 3. C(t) × t (يجب أن يكون 1 لـ t > 1)
ax3 = axes[1, 0]
product = np.array(C_values_computed) * np.array(t_values_computed)
ax3.semilogx(t_values_computed, product, 'go-', linewidth=2, markersize=8, label='C(t) × t')
ax3.axhline(y=1, color='r', linestyle='--', linewidth=2, alpha=0.7, label='القيمة النظرية = 1')
ax3.axvline(x=t_transition, color='purple', linestyle=':', alpha=0.7, label=f'التحول عند t={t_transition}')
ax3.set_xlabel('t (مقياس لوغاريتمي)', fontsize=12)
ax3.set_ylabel('C(t) × t', fontsize=12)
ax3.set_title('هل C(t) × t → 1؟', fontsize=14)
ax3.set_ylim(0, 1.2)
ax3.grid(True, alpha=0.3)
ax3.legend()

# 4. الانحراف عن 1/t (لـ t > 1)
ax4 = axes[1, 1]
t_large_mask = np.array(t_values_computed) > 1
t_large = np.array(t_values_computed)[t_large_mask]
C_large = np.array(C_values_computed)[t_large_mask]
deviation = C_large - 1/t_large
ax4.semilogx(t_large, deviation, 'mo-', linewidth=2, markersize=8)
ax4.axhline(y=0, color='k', linestyle='-', linewidth=1, alpha=0.5)
ax4.set_xlabel('t (مقياس لوغاريتمي)', fontsize=12)
ax4.set_ylabel('C(t) - 1/t', fontsize=12)
ax4.set_title('الانحراف عن القانون C(t) = 1/t', fontsize=14)
ax4.grid(True, alpha=0.3)
ax4.axvline(x=t_transition, color='purple', linestyle=':', alpha=0.7)

plt.tight_layout()
plt.show()

# تحليل الانحدار لـ t > 5
t_fit = np.array([5.0, 7.0, 10.0, 14.1347, 21.0220, 30.0, 50.0])
C_fit = np.array([0.19610460, 0.14144118, 0.09953953, 0.07056554, 0.04750220, 0.03334309, 0.01998018])

log_t = np.log(t_fit)
log_C = np.log(C_fit)
slope, intercept, r_value, p_value, std_err = stats.linregress(log_t, log_C)

print("="*70)
print("تحليل الانحدار لـ t > 5")
print("="*70)
print(f"log(C) = {slope:.4f} × log(t) + {intercept:.4f}")
print(f"C(t) = {np.exp(intercept):.4f} × t^{slope:.4f}")
print(f"معامل التحديد R² = {r_value**2:.6f}")
print(f"\nالأس المثالي = -1.0000")
print(f"الأس المحسوب = {slope:.4f}")
print(f"الفرق = {abs(slope + 1):.4f}")

# عرض البيانات النهائية بشكل منظم
print("\n" + "="*70)
print("الجدول النهائي لـ C(t) عند N=50000")
print("="*70)
print(f"{'t':>10} | {'C(t)':>12} | {'1/t':>12} | {'C(t)×t':>12} | {'C(t)-1/t':>12}")
print("-"*70)
for t, C in zip(t_values_computed, C_values_computed):
    one_over_t = 1/t if t > 0 else float('inf')
    product_val = C * t
    diff = C - one_over_t
    print(f"{t:10.4f} | {C:12.8f} | {one_over_t:12.6f} | {product_val:12.6f} | {diff:12.6f}")