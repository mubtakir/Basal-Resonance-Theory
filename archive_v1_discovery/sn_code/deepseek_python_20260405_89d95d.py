import numpy as np
import matplotlib.pyplot as plt

# التردد المطلوب
t = 14.134725141734693790

# عدد الحدود
N_max = 5000

# مصفوفة لتخزين S(N) لكل N
S_vals = np.zeros(N_max, dtype=complex)

# حساب S(N) تراكمياً
S = 0 + 0j
for n in range(1, N_max + 1):
    S += n ** (1j * t)   # n^(i t)
    S_vals[n-1] = S

# الجزء الحقيقي والتخيلي لـ S(N)
real_parts = np.real(S_vals)
imag_parts = np.imag(S_vals)

# طباعة أول 10 قيم للاطلاع
print("n\tReal(S(n))\t\tImag(S(n))")
for i in range(min(N_max-1, N_max)):
    print(f"{i+1}\t{real_parts[i]:.6f}\t\t{imag_parts[i]:.6f}")

# رسم الجزء الحقيقي والتخيلي
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(range(1, N_max+1), real_parts, 'b-')
plt.xlabel('n')
plt.ylabel('Real part of S(n)')
plt.title(f'Real part of Σ n^(i t), t = {t}')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(range(1, N_max+1), imag_parts, 'r-')
plt.xlabel('n')
plt.ylabel('Imag part of S(n)')
plt.title(f'Imag part of Σ n^(i t), t = {t}')
plt.grid(True)

plt.tight_layout()
plt.show()

# تقييم التقارب: هل تبقى S(N) محدودة؟
abs_S = np.abs(S_vals)
plt.figure()
plt.plot(range(1, N_max+1), abs_S, 'g-')
plt.xlabel('n')
plt.ylabel('|S(n)|')
plt.title('Magnitude of partial sum')
plt.grid(True)
plt.show()

print(f"\nآخر قيمة |S({N_max})| = {abs_S[-1]:.6f}")