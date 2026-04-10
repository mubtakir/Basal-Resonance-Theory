"""
================================================================================
إعادة المسح بمنهجية ثابتة - البحث عن عائلات الرنين الحقيقية
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

def zeta_sum(t, N, sigma=0.5):
    n = np.arange(1, N + 1, dtype=np.float64)
    return np.sum(n ** (-sigma + 1j * t))

def compute_depth_stable(t_zero, N, t_span=0.5, n_points=500):
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    mags = []
    for t in t_values:
        S = zeta_sum(t, N)
        mags.append(np.abs(S) / np.sqrt(N))
    mags = np.array(mags)
    depth = np.mean(mags) / (np.min(mags) + 1e-12)
    return depth, np.min(mags), t_values[np.argmin(mags)]

# الأصفار
zeros = {
    14.134725: "Z1",
    21.022040: "Z2", 
    25.010858: "Z3",
    30.424876: "Z4",
    32.935062: "Z5",
    37.586178: "Z6"
}

N_range = range(10, 201)

print("=" * 80)
print("🔬 إعادة المسح بمنهجية ثابتة (t_span=0.5, n_points=500)")
print("=" * 80)

all_resonances = {}

for t0, name in zeros.items():
    print(f"\n📌 {name} (t = {t0:.3f})")
    results = []
    for N in N_range:
        depth, min_val, t_min = compute_depth_stable(t0, N)
        results.append((N, depth, min_val, t_min))
        if depth > 5:
            print(f"   N={N:3d} → عمق={depth:.2f} ⚡")
    
    # ترتيب حسب العمق
    results.sort(key=lambda x: x[1], reverse=True)
    all_resonances[name] = results[:10]
    print(f"   🏆 أفضل N: {results[0][0]} (عمق={results[0][1]:.2f})")

# رسم بياني مقارن
plt.figure(figsize=(14, 8))
for name, results in all_resonances.items():
    N_vals = [r[0] for r in results[:20]]
    depth_vals = [r[1] for r in results[:20]]
    plt.plot(N_vals, depth_vals, 'o-', label=name)

plt.xlabel('N')
plt.ylabel('عمق القاع')
plt.title('عائلات الرنين لكل صفر (منهجية ثابتة)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()