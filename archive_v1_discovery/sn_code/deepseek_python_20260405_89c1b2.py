import numpy as np
import matplotlib.pyplot as plt

def zeta_sum(t, N):
    """المجموع الجزئي لدالة زيتا: Σ n^(-0.5 + it)"""
    n = np.arange(1, N + 1, dtype=np.float64)
    terms = n ** (-0.5 + 1j * t)
    return np.sum(terms)

def compute_depth_zeta(t_zero, N, t_span=0.5, n_points=200):
    """حساب عمق القاع لزيتا عند N معين"""
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    magnitudes = []
    
    for t in t_values:
        S = zeta_sum(t, N)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    min_val = min(magnitudes)
    avg_val = np.mean(magnitudes)
    depth = avg_val / (min_val + 1e-12)
    return depth, min_val, t_values[np.argmin(magnitudes)]

# الأصفار الأولى لدالة زيتا (قيم معروفة بدقة عالية)
zeta_zeros = {
    "first": 14.134725141734693,
    "second": 21.022039638771554,
    "third": 25.010857580145688,
    "fourth": 30.424876125859513,
}

# القيم الرنانة التي اكتشفناها على chi_4
resonant_Ns = [15, 17, 47, 48, 49, 77, 83, 135, 136, 141, 142]

print("=" * 70)
print("🔬 اختبار القيم الرنانة على دالة زيتا لريمان")
print("=" * 70)

results = {}

for zero_name, t0 in zeta_zeros.items():
    print(f"\n📌 {zero_name} صفر عند t = {t0:.6f}")
    print("-" * 50)
    results[zero_name] = []
    
    for N in resonant_Ns[:6]:  # نختبر أول 6 قيم رنانة
        depth, min_val, t_min = compute_depth_zeta(t0, N, t_span=0.8, n_points=250)
        results[zero_name].append((N, depth, min_val, t_min))
        
        # تقييم النتيجة
        if depth > 10:
            status = "🔥 رنين قوي!"
        elif depth > 5:
            status = "✅ رنين واضح"
        elif depth > 3:
            status = "⚠️ رنين ضعيف"
        else:
            status = "❌ لا رنين"
        
        print(f"   N = {N:3d} → عمق = {depth:7.2f} | min |S|/√N = {min_val:.6f} | {status}")

# رسم مقارن
plt.figure(figsize=(14, 8))

# الرسم البياني الأول: عمق القاع كدالة في N لكل صفر
plt.subplot(2, 2, 1)
for zero_name in zeta_zeros.keys():
    depths = [d for _, d, _, _ in results[zero_name]]
    plt.plot(resonant_Ns[:len(depths)], depths, 'o-', label=f'{zero_name} (t={zeta_zeros[zero_name]:.2f})')
plt.xlabel('N (القيم الرنانة من χ₄)')
plt.ylabel('عمق القاع')
plt.title('اختبار القيم الرنانة على أصفار زيتا')
plt.legend()
plt.grid(True, alpha=0.3)

# الرسم البياني الثاني: أعمق قاع لكل صفر
plt.subplot(2, 2, 2)
best_depths = [max(d for _, d, _, _ in results[zero_name]) for zero_name in zeta_zeros.keys()]
best_Ns = [results[zero_name][np.argmax([d for _, d, _, _ in results[zero_name]])][0] for zero_name in zeta_zeros.keys()]
plt.bar(zeta_zeros.keys(), best_depths, color='darkblue', alpha=0.7)
plt.ylabel('أقصى عمق قاع')
plt.title('أفضل رنين لكل صفر')
for i, (name, n) in enumerate(zip(zeta_zeros.keys(), best_Ns)):
    plt.text(i, best_depths[i] + 1, f'N={n}', ha='center')
plt.grid(True, alpha=0.3)

# الرسم البياني الثالث: موقع القاع الدقيق
plt.subplot(2, 2, 3)
for zero_name, t0 in zeta_zeros.items():
    shifts = [abs(t_min - t0) for _, _, _, t_min in results[zero_name][:6]]
    plt.plot(resonant_Ns[:len(shifts)], shifts, 'o-', label=zero_name)
plt.xlabel('N')
plt.ylabel('|t_min - t₀| (الانحراف عن الصفر الحقيقي)')
plt.title('دقة تحديد موقع الصفر')
plt.yscale('log')
plt.legend()
plt.grid(True, alpha=0.3)

# الرسم البياني الرابع: توزيع الأعماق
plt.subplot(2, 2, 4)
all_depths = [d for zero_name in zeta_zeros.keys() for _, d, _, _ in results[zero_name]]
plt.hist(all_depths, bins=15, color='purple', alpha=0.7, edgecolor='black')
plt.xlabel('عمق القاع')
plt.ylabel('التكرار')
plt.title(f'توزيع أعماق القيعان (متوسط = {np.mean(all_depths):.2f})')
plt.axvline(np.mean(all_depths), color='red', linestyle='--', label=f'المتوسط = {np.mean(all_depths):.2f}')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ملخص نهائي
print("\n" + "=" * 70)
print("📊 الملخص النهائي")
print("=" * 70)

for zero_name in zeta_zeros.keys():
    best_N, best_depth, best_min, best_t = max(results[zero_name], key=lambda x: x[1])
    print(f"\n📍 {zero_name} صفر (t = {zeta_zeros[zero_name]:.6f}):")
    print(f"   → أفضل N رنانة من تجربة χ₄: {best_N}")
    print(f"   → العمق المحقق: {best_depth:.2f}")
    print(f"   → الفرق عن الصفر الحقيقي: {abs(best_t - zeta_zeros[zero_name]):.2e}")
    
    if best_depth > 10:
        print(f"   🔥 خلاصة: رنين قوي جداً! النظرية مؤكدة.")
    elif best_depth > 5:
        print(f"   ✅ خلاصة: رنين واضح. النظرية مدعومة.")
    else:
        print(f"   ⚠️ خلاصة: رنين ضعيف. قد تحتاج N أخرى.")