import numpy as np
import matplotlib.pyplot as plt

def partial_sum(t, N_max):
    S_vals = np.zeros(N_max, dtype=complex)
    S = 0 + 0j
    for n in range(1, N_max + 1):
        S += n ** (1j * t)
        S_vals[n-1] = S
    return S_vals

# قيم t المطلوب اختبارها
t_values = {
    "t_random": 10.0,
    "t_near_zero": 14.13,
    "t_exact_zero": 14.134725141734693790
}

N_max = 1000

plt.figure(figsize=(10, 6))

for label, t in t_values.items():
    S_vals = partial_sum(t, N_max)
    abs_S = np.abs(S_vals)
    plt.plot(range(1, N_max+1), abs_S, label=label)

plt.xlabel('N')
plt.ylabel('|S(N)|')
plt.title('Comparison of |∑ n^(i t)| for different t')
plt.legend()
plt.grid(True)
plt.yscale('log')  # مقياس لوغاريتمي لرؤية الفروق في النمو
plt.show()

# فحص آخر قيمة لكل t
for label, t in t_values.items():
    S_vals = partial_sum(t, N_max)
    print(f"{label} (t={t:.6f}): |S({N_max})| = {np.abs(S_vals[-1]):.2f}")