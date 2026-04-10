# انسخ هذا الكود وشغله في أي بيئة Python بها NumPy
import numpy as np

def find_zeta_zeros(t_start, t_end, N=50000):
    """تكتشف أصفار زيتا تقريباً في المدى [t_start, t_end]"""
    results = []
    for t in np.linspace(t_start, t_end, 2000):
        n = np.arange(1, N+1)
        S = np.sum(n**(-0.5 + 1j*t))
        error = abs(abs(S)/np.sqrt(N) - 1/np.sqrt(0.25 + t**2))
        if error < 1e-4:  # عتبة بسيطة للكشف
            results.append((t, error))
    return results

# مثال: ابحث بين 10 و 35
zeros = find_zeta_zeros(10, 35)
print("القيم المرشحة:", [t for t, _ in zeros])