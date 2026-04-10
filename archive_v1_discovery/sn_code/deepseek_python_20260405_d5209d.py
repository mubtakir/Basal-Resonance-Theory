import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def compute_C_at_N(t, N_target):
    """حساب C(N) = |S(N)|/N"""
    S = 0 + 0j
    for n in range(1, N_target + 1):
        S += n ** (1j * t)
    return np.abs(S) / N_target

t_fixed = 10.0
N_values = [1000, 5000, 10000, 20000, 50000, 80000, 100000]

C_vals = []
for N in N_values:
    C = compute_C_at_N(t_fixed, N)
    C_vals.append(C)
    print(f"N = {N:6d}: C = {C:.6f}")

# حساب الأس من العلاقة |S| = A * N^α
log_N = np.log(N_values)
log_S = np.log(np.array(C_vals) * np.array(N_values))  # S = C*N

slope, intercept, r_value, p_value, std_err = stats.linregress(log_N, log_S)
alpha = slope

print(f"\nالأس α = {alpha:.4f}")
print(f"|S(N)| ∝ N^{alpha:.4f}")
print(f"معامل التحديد R² = {r_value**2:.6f}")

# الرسم
plt.figure(figsize=(10, 6))
plt.loglog(N_values, np.array(C_vals)*np.array(N_values), 'bo-', linewidth=2, markersize=8)
plt.xlabel('N (log scale)')
plt.ylabel('|S(N)| (log scale)')
plt.title(f'نمو |S(N)| مع N عند t = {t_fixed}')
plt.grid(True, alpha=0.3)

# منحنى الملاءمة
N_fit = np.linspace(N_values[0], N_values[-1], 100)
S_fit = np.exp(intercept) * N_fit ** alpha
plt.loglog(N_fit, S_fit, 'r--', alpha=0.7, label=f'ملاءمة: N^{alpha:.4f}')
plt.legend()
plt.show()