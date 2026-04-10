import numpy as np
import matplotlib.pyplot as plt

def chi_4(n):
    rem = n % 4
    if rem == 1: return 1
    if rem == 3: return -1
    return 0

def L_partial(t, sigma, N):
    n = np.arange(1, N + 1)
    chi_values = np.array([chi_4(x) for x in n])
    term = chi_values * (n ** (-sigma + 1j * t))
    return np.sum(term)

# أول صفر معروف لـ L(s, chi_4)
t_zero = 6.0209489

# نطاق حول الصفر
t_range = np.linspace(5.9, 6.15, 500)

# اختبار عتبتين مختلفتين
N_small = 50      # √N ≈ 7.07
N_large = 100000  # √N ≈ 316.23

sigma = 0.5

results_small = []
results_large = []

for t in t_range:
    S_small = L_partial(t, sigma, N_small)
    S_large = L_partial(t, sigma, N_large)
    
    # نرصد |S_N| / √N
    results_small.append(np.abs(S_small) / np.sqrt(N_small))
    results_large.append(np.abs(S_large) / np.sqrt(N_large))

# الرسم
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(t_range, results_small, 'b-', linewidth=1.5)
plt.axvline(x=t_zero, color='r', linestyle='--', label=f'Zero at {t_zero}')
plt.title(f'N = {N_small} (√N = {np.sqrt(N_small):.2f})\nعتبة منتهكة → القاع غير واضح')
plt.xlabel('t')
plt.ylabel('|S_N| / √N')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_range, results_large, 'g-', linewidth=1.5)
plt.axvline(x=t_zero, color='r', linestyle='--', label=f'Zero at {t_zero}')
plt.title(f'N = {N_large} (√N = {np.sqrt(N_large):.2f})\nعتبة محققة → القاع الحاد يظهر')
plt.xlabel('t')
plt.ylabel('|S_N| / √N')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()