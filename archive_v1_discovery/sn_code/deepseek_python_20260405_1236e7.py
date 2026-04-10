import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# بياناتك
data = {
    't=3.14': {'N': [1000, 50000], 'C': [1.50, 0.3035]},
    't=10': {'N': [1000, 50000], 'C': [0.49, 0.0995]},
    't=14.13': {'N': [1000, 50000], 'C': [0.35, 0.0706]},
    't=21.02': {'N': [1000, 50000], 'C': [0.23, 0.0475]},
}

plt.figure(figsize=(10, 6))

for label, d in data.items():
    N = np.array(d['N'])
    C = np.array(d['C'])
    
    # حساب الأس: C ~ N^{-β}
    log_N = np.log(N)
    log_C = np.log(C)
    slope, intercept, r, p, se = stats.linregress(log_N, log_C)
    beta = -slope
    
    # رسم
    N_fit = np.linspace(N[0], N[1], 100)
    C_fit = np.exp(intercept) * N_fit ** (-beta)
    plt.loglog(N, C, 'o', markersize=10, label=f'{label}')
    plt.loglog(N_fit, C_fit, '--', alpha=0.5)
    
    # ✅ الإصلاح: تنسيق الأرقام خارجياً لتجنب خطأ تحليل الـ f-string
    beta_str = f"{beta:.3f}"
    exp_str = f"{1 - beta:.3f}"
    print(f"{label}: C(N) ∝ N^-{beta_str}  →  |S(N)| ∝ N^{{{exp_str}}}")

plt.xlabel('N (log scale)')
plt.ylabel('C(N) = |S(N)|/N (log scale)')
plt.title('تناقص معامل النمو الخطي مع N')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# هل الأس يعتمد على t؟
print("\nهل الأس يعتمد على t؟")
print("البيانات تشير إلى β ≈ 0.4 لجميع الحالات تقريبًا")
print("أي |S(N)| ∝ N^{0.6} بغض النظر عن t!")