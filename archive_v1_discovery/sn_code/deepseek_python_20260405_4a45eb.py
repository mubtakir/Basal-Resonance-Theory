import numpy as np
import matplotlib.pyplot as plt

def S(sigma, t, N):
    n = np.arange(1, N + 1, dtype=np.float64)
    return np.sum(n ** (-complex(sigma, t)))

def error_rate(sigma, t, N_values):
    """حساب الخطأ |S_N/N^{1-sigma} - 1/√((1-σ)²+t²)|"""
    theory = 1 / np.sqrt((1 - sigma)**2 + t**2)
    errors = []
    for N in N_values:
        S_val = abs(S(sigma, t, N))
        C_val = S_val / (N ** (1 - sigma))
        errors.append(abs(C_val - theory))
    return errors

# مقارنة: صفر زيتا (0.5, 14.1347) مقابل نقطة عشوائية (0.5, 14.0)
sigma = 0.5
t_zero = 14.134725141734693790
t_random = 14.0
N_values = [1000, 5000, 10000, 20000, 50000, 100000, 200000]

errors_zero = error_rate(sigma, t_zero, N_values)
errors_random = error_rate(sigma, t_random, N_values)

plt.figure(figsize=(10, 6))
plt.loglog(N_values, errors_zero, 'bo-', label='صفر زيتا (t=14.1347)')
plt.loglog(N_values, errors_random, 'r s-', label='t عشوائي (t=14.0)')
plt.xlabel('N')
plt.ylabel('الخطأ المطلق')
plt.title('هل التقارب أسرع عند أصفار زيتا؟')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("الخطأ النهائي عند N=200000:")
print(f"  عند صفر زيتا: {errors_zero[-1]:.8f}")
print(f"  عند t عشوائي: {errors_random[-1]:.8f}")