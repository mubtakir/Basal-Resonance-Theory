import numpy as np
import matplotlib.pyplot as plt

def compute_normalized_sum(t, N):
    """
    يحسب |Σ_{n=1}^{N} n^(it)| / N بدقة وكفاءة
    """
    n = np.arange(1, N + 1, dtype=np.float64)
    # n^(it) = exp(it * ln(n))  ← أكثر استقراراً عددياً من n**(1j*t)
    S = np.sum(np.exp(1j * t * np.log(n)))
    return np.abs(S) / N

# ──────────────────────────────────────────────────────
# إعدادات التجربة
t = 10
N_values = [10**k for k in range(2, 7)]  # 100, 1000, ..., 100000

# القيمة النظرية التي يتقارب إليها المقدار
theoretical_limit = 1 / np.sqrt(1 + t**2)

print(f"🔍 التحقق من تقارب |S|/N عند t = {t}\n")
print(f"{'N':<10} | {'|S|/N':<10} | {'الخطأ النسبي':<10}")
print("-" * 35)

for N in N_values:
    val = compute_normalized_sum(t, N)
    rel_error = abs(val - theoretical_limit) / theoretical_limit * 100
    print(f"{N:<10} | {val:<10.6f} | {rel_error:<9.4f}%")

print(f"\n📐 القيمة النظرية (نهاية التكامل): {theoretical_limit:.8f}")
print("💡 ملاحظة: المجموع يتصرف كتقريب للتكامل ∫₁ᴺ x^(it) dx")

# ──────────────────────────────────────────────────────
# رسم بياني لتتبع التقارب (اختياري)
S_vals = [compute_normalized_sum(t, N) for N in N_values]
plt.figure(figsize=(6, 4))
plt.plot(N_values, S_vals, "o-", label="|S|/N")
plt.axhline(theoretical_limit, color="red", linestyle="--", 
            label=f"النهاية النظرية: {theoretical_limit:.5f}")
plt.xscale("log")
plt.xlabel("N (مقياس لوغاريتمي)")
plt.ylabel("|S| / N")
plt.title(f"تقارب |Σ n^(it)| / N عند t = {t}")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()