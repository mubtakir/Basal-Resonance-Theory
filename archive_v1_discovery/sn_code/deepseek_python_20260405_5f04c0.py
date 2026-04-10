import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def S_generalized(sigma, t, N):
    """حساب S_N(sigma, t) = sum_{n=1}^N n^{-sigma+it}"""
    n = np.arange(1, N + 1, dtype=np.float64)
    exponents = -sigma + 1j * t
    return np.sum(n ** exponents)

def C_generalized(sigma, t, N=50000):
    """حساب |S_N| / N^{1-sigma}"""
    S = S_generalized(sigma, t, N)
    return np.abs(S) / (N ** (1 - sigma))

# قيم sigma المختلفة للاختبار
sigma_values = [0.0, 0.2, 0.4, 0.6, 0.8]
t_test = 10.0  # نختار t ثابتة
N_values = [1000, 5000, 10000, 20000, 50000]

print("="*80)
print(f"اختبار التعميم: S_N(sigma, t) مع t = {t_test}")
print("="*80)
print(f"{'sigma':>8} | {'N':>8} | {'C_computed':>12} | {'1/sqrt((1-s)²+t²)':>20} | {'الفرق':>12}")
print("-"*80)

results = {}

for sigma in sigma_values:
    theory = 1 / np.sqrt((1 - sigma)**2 + t_test**2)
    results[sigma] = {'theory': theory, 'values': []}
    
    for N in N_values:
        C_val = C_generalized(sigma, t_test, N)
        results[sigma]['values'].append(C_val)
        diff = abs(C_val - theory)
        print(f"{sigma:8.2f} | {N:8d} | {C_val:12.8f} | {theory:20.8f} | {diff:12.8f}")
    print("-"*80)

# رسم بياني للنتائج
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# الرسم 1: C(N) مقابل N لكل sigma
ax1 = axes[0]
colors = ['blue', 'green', 'red', 'orange', 'purple']
for idx, sigma in enumerate(sigma_values):
    ax1.plot(N_values, results[sigma]['values'], 'o-', 
             color=colors[idx], label=f'σ = {sigma}')
    # إضافة الخط النظري
    ax1.axhline(y=results[sigma]['theory'], color=colors[idx], 
                linestyle='--', alpha=0.5)
ax1.set_xlabel('N')
ax1.set_ylabel('C(N) = |S_N| / N^{1-σ}')
ax1.set_title(f'التقارب مع N (t = {t_test})')
ax1.legend()
ax1.grid(True, alpha=0.3)

# الرسم 2: القيمة النهائية مقابل sigma
ax2 = axes[1]
sigma_array = np.array(sigma_values)
final_C = [results[s]['values'][-1] for s in sigma_values]
theory_C = [results[s]['theory'] for s in sigma_values]

ax2.plot(sigma_array, final_C, 'bo-', linewidth=2, markersize=8, label='محسوب (N=50000)')
ax2.plot(sigma_array, theory_C, 'r--', linewidth=2, label='نظري: 1/√((1-σ)²+t²)')
ax2.set_xlabel('σ')
ax2.set_ylabel('C(σ, t)')
ax2.set_title(f'مقارنة النتائج النظرية والمحسوبة (t = {t_test})')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# تحليل الانحدار للتحقق من الصيغة
print("\n" + "="*80)
print("تحليل دقة الصيغة النظرية")
print("="*80)

for sigma in sigma_values:
    final = results[sigma]['values'][-1]
    theory = results[sigma]['theory']
    error_percent = 100 * abs(final - theory) / theory
    print(f"σ = {sigma:.2f}: خطأ نسبي = {error_percent:.4f}%")