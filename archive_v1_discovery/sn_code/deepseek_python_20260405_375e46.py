import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def compute_C_at_N(t, N_target):
    """حساب C(N) = |S(N)|/N عند N_target"""
    S = 0 + 0j
    for n in range(1, N_target + 1):
        S += n ** (1j * t)
    return np.abs(S) / N_target

# قيم t مختلفة (صغيرة جدًا، متوسطة، كبيرة جدًا)
t_values = {
    't=0.01 (صغير جدًا)': 0.01,
    't=0.1 (صغير)': 0.1,
    't=0.5': 0.5,
    't=1': 1.0,
    't=2': 2.0,
    't=3.14': 3.14,
    't=5': 5.0,
    't=7': 7.0,
    't=10': 10.0,
    't=14.1347 (zero1)': 14.134725141734693790,
    't=21.022 (zero2)': 21.022039638771554,
    't=30': 30.0,
    't=50': 50.0,
    't=100': 100.0,
    't=200': 200.0,
    't=500': 500.0,
}

N_target = 50000  # نفس القيمة السابقة
print(f"حساب C(t) عند N = {N_target}...")
print("="*70)
print(f"{'t':>12} | {'C(t) المحسوب':>15} | {'1/t':>12} | {'النسبة C(t)*t':>15}")
print("-"*70)

results = {}
for label, t in t_values.items():
    C = compute_C_at_N(t, N_target)
    results[t] = C
    one_over_t = 1/t if t != 0 else float('inf')
    product = C * t
    print(f"{t:12.6f} | {C:15.8f} | {one_over_t:12.6f} | {product:15.6f}")

# رسم بياني
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# الرسم 1: C(t) و 1/t
ax1 = axes[0]
t_list = list(results.keys())
C_list = list(results.values())

# ترتيب حسب t
sorted_idx = np.argsort(t_list)
t_sorted = np.array(t_list)[sorted_idx]
C_sorted = np.array(C_list)[sorted_idx]

ax1.loglog(t_sorted, C_sorted, 'bo-', linewidth=2, markersize=8, label='C(t) المحسوب')
ax1.loglog(t_sorted, 1/t_sorted, 'r--', linewidth=2, alpha=0.7, label='1/t (نظري)')
ax1.set_xlabel('t (مقياس لوغاريتمي)', fontsize=12)
ax1.set_ylabel('C(t) = |S(N)|/N', fontsize=12)
ax1.set_title('مقارنة C(t) مع 1/t', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.legend()

# الرسم 2: C(t)*t
ax2 = axes[1]
product_vals = C_sorted * t_sorted
ax2.semilogx(t_sorted, product_vals, 'go-', linewidth=2, markersize=8)
ax2.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='القيمة النظرية = 1')
ax2.set_xlabel('t (مقياس لوغاريتمي)', fontsize=12)
ax2.set_ylabel('C(t) × t', fontsize=12)
ax2.set_title('هل C(t) × t → 1؟', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()

# تحليل الانحرافات
print("\n" + "="*70)
print("تحليل الانحرافات عن القانون C(t) = 1/t")
print("="*70)

for t, C in results.items():
    deviation = abs(C * t - 1)
    if t < 1:
        print(f"t = {t:.3f} (صغير): C×t = {C*t:.6f} (انحراف {deviation:.6f})")
    elif t > 100:
        print(f"t = {t:.1f} (كبير): C×t = {C*t:.6f} (انحراف {deviation:.6f})")

# حساب المتوسط لـ C×t للتوسطات الكبيرة
large_t_mask = t_sorted > 10
mean_product = np.mean(product_vals[large_t_mask])
std_product = np.std(product_vals[large_t_mask])
print(f"\nلـ t > 10: متوسط C×t = {mean_product:.4f} ± {std_product:.4f}")

# هل تختلف الأصفار عن المتوسط؟
zero_products = []
for t in [14.134725141734693790, 21.022039638771554]:
    if t in results:
        prod = results[t] * t
        zero_products.append(prod)
        print(f"\nعند الصفر t={t:.4f}: C×t = {prod:.6f}")
        print(f"  الفرق عن المتوسط: {(prod - mean_product)/std_product:.2f}σ")