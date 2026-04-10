import numpy as np
import matplotlib.pyplot as plt

def C_generalized(sigma, t, N):
    n = np.arange(1, N + 1, dtype=np.float64)
    S = np.sum(n ** (-sigma + 1j * t))
    return np.abs(S) / (N ** (1 - sigma))

# اختبار σ مختلفة مع N أكبر
sigma_test = [0.0, 0.2, 0.4, 0.6, 0.8]
t_fixed = 10.0
N_large = [1000, 5000, 10000, 20000, 50000, 100000, 200000]

plt.figure(figsize=(10, 6))

for sigma in sigma_test:
    theory = 1 / np.sqrt((1 - sigma)**2 + t_fixed**2)
    C_vals = []
    for N in N_large:
        try:
            C_vals.append(C_generalized(sigma, t_fixed, N))
        except:
            C_vals.append(np.nan)
    
    # رسم فقط القيم الصالحة
    valid_N = [N_large[i] for i in range(len(C_vals)) if not np.isnan(C_vals[i])]
    valid_C = [C_vals[i] for i in range(len(C_vals)) if not np.isnan(C_vals[i])]
    
    plt.plot(valid_N, valid_C, 'o-', label=f'σ = {sigma}')
    plt.axhline(y=theory, color=plt.gca().lines[-1].get_color(), 
                linestyle='--', alpha=0.5)

plt.xscale('log')
plt.xlabel('N (مقياس لوغاريتمي)')
plt.ylabel('C(N) = |S_N| / N^{1-σ}')
plt.title(f'تطور C(N) مع N (t = {t_fixed})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()