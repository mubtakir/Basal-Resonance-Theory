import numpy as np

def chi_4(n):
    rem = n % 4
    if rem == 1: return 1
    if rem == 3: return -1
    return 0

def L_sum(t, N):
    n = np.arange(1, N + 1)
    chi = np.array([chi_4(x) for x in n])
    # حساب n^(-0.5 + i t)
    terms = chi * (n ** (-0.5 + 1j * t))
    return np.sum(terms)

# الصفر المعروف
t_zero = 6.020948904697828

# اختبار قيم N المختلفة
N_values = [10, 20, 50, 100, 1000]
t_values = np.linspace(t_zero - 0.1, t_zero + 0.1, 200)

for N in N_values:
    magnitudes = []
    for t in t_values:
        S = L_sum(t, N)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    # حساب عمق القاع: النسبة بين أقل قيمة ومتوسط القيم
    min_val = min(magnitudes)
    avg_val = np.mean(magnitudes)
    depth = avg_val / (min_val + 1e-12)  # كلما كان أكبر، القاع أوضح
    
    print(f"N = {N:4d}, sqrt(N) = {np.sqrt(N):6.2f}, عمق القاع = {depth:.2f}")