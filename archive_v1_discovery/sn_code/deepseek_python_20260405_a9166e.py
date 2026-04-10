import numpy as np
import matplotlib.pyplot as plt

def compute_growth_coefficient(t, N_max, step=1000):
    """حساب C(N) = |S(N)|/N كدالة في N"""
    C_vals = []
    N_vals = []
    S = 0 + 0j
    
    for n in range(1, N_max + 1):
        S += n ** (1j * t)
        if n % step == 0:
            C_vals.append(np.abs(S) / n)
            N_vals.append(n)
    
    return N_vals, C_vals

# اختبار N أكبر
N_max = 50000
t_cases = {
    't=3.14 (صغير)': 3.14,
    't=10 (متوسط)': 10.0,
    't=14.1347 (صفر أول)': 14.134725141734693790,
    't=21.022 (صفر ثاني)': 21.022039638771554,
}

plt.figure(figsize=(12, 6))

for label, t in t_cases.items():
    N_vals, C_vals = compute_growth_coefficient(t, N_max, step=2000)
    plt.plot(N_vals, C_vals, label=label, linewidth=2)

plt.xlabel('N', fontsize=12)
plt.ylabel('C(N) = |S(N)|/N', fontsize=12)
plt.title('تطور معامل النمو الخطي مع N', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(bottom=0)
plt.show()

# حساب المتوسط لآخر 10% من القيم
print("\nمتوسط C(N) لآخر 5000 قيمة:")
for label, t in t_cases.items():
    N_vals, C_vals = compute_growth_coefficient(t, N_max, step=100)
    last_C = np.mean(C_vals[-50:])
    print(f"{label}: C ≈ {last_C:.4f}")