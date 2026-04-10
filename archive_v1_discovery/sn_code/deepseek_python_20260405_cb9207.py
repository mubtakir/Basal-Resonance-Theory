import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def compute_C_at_N(t, N_target):
    """حساب C(N) = |S(N)|/N عند N_target"""
    S = 0 + 0j
    for n in range(1, N_target + 1):
        S += n ** (1j * t)
    return np.abs(S) / N_target

# قيم t المختلفة (بما فيها أصفار زيتا)
t_values = {
    't=1': 1.0,
    't=2': 2.0,
    't=3.14': 3.14,
    't=5': 5.0,
    't=7': 7.0,
    't=10': 10.0,
    't=12': 12.0,
    't=14.13': 14.13,
    't=14.1347 (zero1)': 14.134725141734693790,
    't=16': 16.0,
    't=18': 18.0,
    't=20': 20.0,
    't=21.022 (zero2)': 21.022039638771554,
    't=23': 23.0,
    't=25': 25.0,
    't=30': 30.0,
}

N_target = 50000  # نفس القيمة التي استخدمناها سابقًا
print(f"حساب C(t) عند N = {N_target}...")
print("="*60)

C_results = {}
for label, t in t_values.items():
    C = compute_C_at_N(t, N_target)
    C_results[label] = C
    zero_marker = " ★ (zero)" if "zero" in label or t in [14.134725141734693790, 21.022039638771554] else ""
    print(f"{label:20s}: C = {C:.6f}{zero_marker}")

# رسم C(t) بدلالة t
plt.figure(figsize=(14, 6))

# فصل الأصفار وغير الأصفار
t_list = []
C_list = []
is_zero = []

for label, C in C_results.items():
    # استخراج قيمة t من الـ label
    if 'zero' in label:
        if '14.1347' in label:
            t_val = 14.1347
        else:
            t_val = 21.022
        is_zero.append(True)
    else:
        t_val = float(label.split('=')[1].split()[0])
        is_zero.append(False)
    t_list.append(t_val)
    C_list.append(C)

# ترتيب حسب t
sorted_indices = np.argsort(t_list)
t_list = np.array(t_list)[sorted_indices]
C_list = np.array(C_list)[sorted_indices]
is_zero = np.array(is_zero)[sorted_indices]

# رسم
plt.subplot(1, 2, 1)
plt.plot(t_list, C_list, 'bo-', linewidth=2, markersize=8, alpha=0.7)
plt.scatter(t_list[is_zero], C_list[is_zero], color='red', s=150, marker='*', 
            label='أصفار زيتا غير البديهية', zorder=5)
plt.xlabel('t', fontsize=12)
plt.ylabel('C(t) = |S(N)|/N عند N=50000', fontsize=12)
plt.title('اعتماد معامل النمو على التردد t', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# مقياس لوغاريتمي لرؤية النمط بشكل أفضل
plt.subplot(1, 2, 2)
plt.semilogy(t_list, C_list, 'bo-', linewidth=2, markersize=8, alpha=0.7)
plt.scatter(t_list[is_zero], C_list[is_zero], color='red', s=150, marker='*', 
            label='أصفار زيتا', zorder=5)
plt.xlabel('t', fontsize=12)
plt.ylabel('C(t) (مقياس لوغاريتمي)', fontsize=12)
plt.title('السلوك اللوغاريتمي لـ C(t)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# تحليل: هل C(t) ~ 1/√t أم 1/t أم شيء آخر؟
log_t = np.log(t_list[~is_zero])
log_C = np.log(C_list[~is_zero])
slope, intercept, r_value, p_value, std_err = stats.linregress(log_t, log_C)

print("\n" + "="*60)
print("تحليل اعتماد C(t) على t")
print("="*60)
print(f"C(t) ∝ t^{slope:.3f} (باستثناء الأصفار)")
print(f"معامل التحديد R² = {r_value**2:.4f}")
print(f"\nإذا كان النموذج صحيحًا، فإن C(t) ≈ {np.exp(intercept):.4f} · t^{slope:.3f}")

# مقارنة الأصفار مع المنحنى الملائم
print("\n" + "="*60)
print("مقارنة الأصفار مع القيم المتوقعة:")
print("="*60)
for i, (t_val, is_z) in enumerate(zip(t_list, is_zero)):
    if is_z:
        expected = np.exp(intercept) * (t_val ** slope)
        ratio = C_list[i] / expected
        print(f"t = {t_val:.4f}: C_actual = {C_list[i]:.6f}, C_expected = {expected:.6f}, النسبة = {ratio:.4f}")
        if ratio < 0.95:
            print(f"  → أقل من المتوقع بنسبة {100*(1-ratio):.1f}%")