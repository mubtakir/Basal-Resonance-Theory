import numpy as np
import matplotlib.pyplot as plt

def S_generalized(sigma, t, N):
    """حساب S_N(sigma, t) = sum_{n=1}^N n^{-sigma+it}"""
    n = np.arange(1, N + 1, dtype=np.float64)
    exponents = -sigma + 1j * t
    return np.sum(n ** exponents)

def C_generalized(sigma, t, N):
    """حساب |S_N| / N^{1-sigma}"""
    S = S_generalized(sigma, t, N)
    return np.abs(S) / (N ** (1 - sigma))

# المعاملات
t_small = 1.0  # t صغيرة لرؤية الفرق بوضوح
sigma_values = [0.0, 0.2, 0.4, 0.6, 0.8]
N_values = [1000, 5000, 10000, 20000, 50000, 100000, 200000]

print("="*80)
print(f"اختبار حاسم: t = {t_small}")
print("هل الصيغة الصحيحة هي:")
print("  (أ) 1/√((1-σ)² + t²)  أم")
print("  (ب) 1/√(1 + t²) = ثابت؟")
print("="*80)

# تخزين النتائج
results = {sigma: {'values': [], 'theory_a': [], 'theory_b': []} for sigma in sigma_values}

for sigma in sigma_values:
    theory_a = 1 / np.sqrt((1 - sigma)**2 + t_small**2)
    theory_b = 1 / np.sqrt(1 + t_small**2)  # ثابت = 1/√2 ≈ 0.7071
    
    results[sigma]['theory_a'] = theory_a
    results[sigma]['theory_b'] = theory_b
    
    print(f"\nσ = {sigma:.1f}:")
    print(f"  النظرية (أ): {theory_a:.6f}")
    print(f"  النظرية (ب): {theory_b:.6f}")
    print(f"  الفرق بين النظريتين: {abs(theory_a - theory_b):.4f} ({100*abs(theory_a - theory_b)/theory_b:.1f}%)")
    print("-"*50)
    
    for N in N_values:
        C_val = C_generalized(sigma, t_small, N)
        results[sigma]['values'].append(C_val)
        print(f"    N = {N:7d}: C = {C_val:.6f}")

# رسم بياني مقارن
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# الرسم 1: C(N) مقابل N
ax1 = axes[0]
colors = ['blue', 'green', 'red', 'orange', 'purple']

for idx, sigma in enumerate(sigma_values):
    ax1.plot(N_values, results[sigma]['values'], 'o-', 
             color=colors[idx], label=f'σ = {sigma}')
    # خط النظريتين
    ax1.axhline(y=results[sigma]['theory_a'], color=colors[idx], 
                linestyle='--', alpha=0.5, label=f'نظرية (أ) σ={sigma}')
    ax1.axhline(y=results[sigma]['theory_b'], color=colors[idx], 
                linestyle=':', alpha=0.5, label=f'نظرية (ب) σ={sigma}')

ax1.set_xscale('log')
ax1.set_xlabel('N (مقياس لوغاريتمي)')
ax1.set_ylabel('C(N) = |S_N| / N^{1-σ}')
ax1.set_title(f'اختبار الصيغتين (t = {t_small})')
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
ax1.grid(True, alpha=0.3)

# الرسم 2: القيم النهائية مقابل σ
ax2 = axes[1]
sigma_array = np.array(sigma_values)
final_C = [results[s]['values'][-1] for s in sigma_values]
theory_a = [results[s]['theory_a'] for s in sigma_values]
theory_b = [results[s]['theory_b'] for s in sigma_values]

ax2.plot(sigma_array, final_C, 'bo-', linewidth=2, markersize=8, 
         label='محسوب (N=200000)')
ax2.plot(sigma_array, theory_a, 'r--', linewidth=2, 
         label='نظرية (أ): 1/√((1-σ)²+t²)')
ax2.plot(sigma_array, theory_b, 'g--', linewidth=2, 
         label='نظرية (ب): 1/√(1+t²) ثابت')

ax2.set_xlabel('σ')
ax2.set_ylabel('C(σ, t)')
ax2.set_title(f'مقارنة النتائج النهائية (t = {t_small})')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# التحليل النهائي
print("\n" + "="*80)
print("التحليل النهائي")
print("="*80)

for sigma in sigma_values:
    final = results[sigma]['values'][-1]
    err_a = abs(final - results[sigma]['theory_a']) / results[sigma]['theory_a'] * 100
    err_b = abs(final - results[sigma]['theory_b']) / results[sigma]['theory_b'] * 100
    
    print(f"\nσ = {sigma:.1f}:")
    print(f"  القيمة المحسوبة: {final:.6f}")
    print(f"  الخطأ النسبي لنظرية (أ): {err_a:.3f}%")
    print(f"  الخطأ النسبي لنظرية (ب): {err_b:.3f}%")
    
    if err_a < err_b:
        print(f"  → نظرية (أ) أفضل بـ {err_b/err_a:.2f} مرة")
    else:
        print(f"  → نظرية (ب) أفضل بـ {err_a/err_b:.2f} مرة")