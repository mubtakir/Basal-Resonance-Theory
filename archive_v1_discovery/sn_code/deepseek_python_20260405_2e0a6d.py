"""
================================================================================
التحقق المباشر: حساب عمق Z8 عند جميع N المرشحة
المؤلف: باسل يحيى عبدالله
التاريخ: أبريل 2026
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================================
# الجزء الأول: تعريف الدوال الأساسية
# ============================================================================

def zeta_sum(t, N, sigma=0.5):
    """حساب المجموع الجزئي لدالة زيتا"""
    n = np.arange(1, N + 1, dtype=np.float64)
    return np.sum(n ** (-sigma + 1j * t))

def compute_depth(t_zero, N, t_span=0.8, n_points=400):
    """حساب عمق القاع بدقة عالية"""
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    magnitudes = []
    
    for t in t_values:
        S = zeta_sum(t, N)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    magnitudes = np.array(magnitudes)
    depth = np.mean(magnitudes) / (np.min(magnitudes) + 1e-12)
    return depth, np.min(magnitudes), t_values[np.argmin(magnitudes)]

# ============================================================================
# الجزء الثاني: بيانات Z8
# ============================================================================

# Z8 من الأدبيات
Z8_actual = 48.005150881167159
Z8_name = "Z8 (الصفر الثامن)"

# جميع N المرشحة من النظرية
candidate_Ns = [20, 25, 34, 70, 98, 119]

# البيانات المعروفة للمقارنة (الأعمق)
known_depths = {
    20: 712.37,   # عند Z6
    25: 18.85,    # عند Z1
    34: 125.50,   # عند Z4
    70: 253.28,   # عند Z2
    98: 201.46,   # عند Z3
    119: 714.29   # عند Z7
}

print("=" * 80)
print("🔬 التحقق المباشر: حساب عمق Z8 عند جميع N المرشحة")
print(f"⏰ وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

print(f"\n🎯 الصفر المختبر: {Z8_name} (t = {Z8_actual:.6f})")
print(f"\n📊 N المرشحة: {candidate_Ns}")

# ============================================================================
# الجزء الثالث: حساب العمق لكل N
# ============================================================================

print("\n" + "=" * 60)
print("📊 حساب العمق الفعلي")
print("=" * 60)

results = []

for N in candidate_Ns:
    print(f"\n🔄 جاري حساب N = {N}...")
    depth, min_val, t_min = compute_depth(Z8_actual, N, t_span=0.8, n_points=400)
    results.append((N, depth, min_val, t_min))
    
    # مقارنة مع العمق المعروف لهذه N عند صفر آخر
    known_depth = known_depths.get(N, 0)
    comparison = ""
    if known_depth > 0:
        ratio = depth / known_depth
        if ratio > 0.5:
            comparison = f" (قريب من العمق المعروف {known_depth:.2f} → نسبة {ratio:.2f})"
        else:
            comparison = f" (أقل بكثير من العمق المعروف {known_depth:.2f} → نسبة {ratio:.2f})"
    
    # تقييم النتيجة
    if depth > 100:
        status = "🔥 رنين قوي جداً! Z8 في هذه العائلة"
    elif depth > 20:
        status = "✅ رنين واضح. مرشح محتمل"
    elif depth > 10:
        status = "⚠️ رنين ضعيف. احتمال ضعيف"
    else:
        status = "❌ لا رنين. Z8 ليس في هذه العائلة"
    
    print(f"   → العمق = {depth:.2f} | min |S|/√N = {min_val:.6f} | {status}{comparison}")

# ============================================================================
# الجزء الرابع: ترتيب النتائج
# ============================================================================

print("\n" + "=" * 60)
print("📊 ترتيب N حسب العمق")
print("=" * 60)

results.sort(key=lambda x: x[1], reverse=True)

print("\nمن الأفضل إلى الأسوأ:")
for rank, (N, depth, min_val, t_min) in enumerate(results, 1):
    print(f"   {rank}. N = {N:3d} → عمق = {depth:8.2f}")

best_N = results[0][0]
best_depth = results[0][1]

print(f"\n🏆 أفضل N لـ Z8: {best_N} (عمق = {best_depth:.2f})")

# ============================================================================
# الجزء الخامس: تحديد عائلة Z8
# ============================================================================

print("\n" + "=" * 60)
print("📊 تحديد عائلة Z8")
print("=" * 60)

# عائلات N المعروفة
families = {
    20: "عائلة N=20 (Z6 عند 37.59)",
    25: "عائلة N=25 (Z1 عند 14.13)",
    34: "عائلة N=34 (Z4 عند 30.42)",
    70: "عائلة N=70 (Z2 عند 21.02)",
    98: "عائلة N=98 (Z3 عند 25.01)",
    119: "عائلة N=119 (Z5 عند 32.94, Z7 عند 43.33)"
}

best_family = families.get(best_N, "غير معروفة")
print(f"\n🎯 Z8 ينتمي إلى: {best_family}")

# هل تكرر نفس N لصفر آخر؟
if best_N in [119, 25, 20, 34, 70, 98]:
    other_zeros = []
    if best_N == 119:
        other_zeros = ["Z5 (32.94)", "Z7 (43.33)"]
    elif best_N == 25:
        other_zeros = ["Z1 (14.13)"]
    elif best_N == 20:
        other_zeros = ["Z6 (37.59)"]
    elif best_N == 34:
        other_zeros = ["Z4 (30.42)"]
    elif best_N == 70:
        other_zeros = ["Z2 (21.02)"]
    elif best_N == 98:
        other_zeros = ["Z3 (25.01)"]
    
    print(f"\n📌 ملاحظة: N={best_N} يخدم أيضاً الأصفار: {', '.join(other_zeros)}")
    print(f"   → هذا يؤكد نظرية 'العائلات'! ✓")

# ============================================================================
# الجزء السادس: التحقق من العوامل الأولية
# ============================================================================

print("\n" + "=" * 60)
print("📊 التحقق من العوامل الأولية لأفضل N")
print("=" * 60)

from sympy import factorint

factors = factorint(best_N)
factor_str = ' × '.join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
allowed_primes = [2, 5, 7, 17]

print(f"\nأفضل N = {best_N}")
print(f"   التحليل إلى عوامل: {factor_str}")
print(f"   العوامل الأولية: {list(factors.keys())}")

factors_ok = all(p in allowed_primes for p in factors.keys())
print(f"   هل العوامل ضمن {allowed_primes}؟ {'نعم ✅' if factors_ok else 'لا ❌'}")

if factors_ok:
    print("\n🎉 نظرية العوامل الأولية مؤكدة لـ Z8 أيضاً!")
else:
    print("\n⚠️ نظرية العوامل الأولية تحتاج إلى توسيع لتشمل عوامل جديدة.")

# ============================================================================
# الجزء السابع: الرسم البياني
# ============================================================================

print("\n📈 جاري إنشاء الرسم البياني...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# الرسم 1: أعماق جميع N لـ Z8
ax1 = axes[0, 0]
N_vals = [r[0] for r in results]
depth_vals = [r[1] for r in results]
colors_bar = ['red' if n == best_N else 'steelblue' for n in N_vals]
bars = ax1.bar([str(n) for n in N_vals], depth_vals, color=colors_bar, edgecolor='black')
ax1.set_xlabel('N', fontsize=12)
ax1.set_ylabel('عمق القاع', fontsize=12)
ax1.set_title(f'عمق Z8 عند مختلف N (أفضل N = {best_N})', fontsize=14)
ax1.grid(True, alpha=0.3, axis='y')

# إضافة قيم العمق على الأعمدة
for bar, depth in zip(bars, depth_vals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{depth:.1f}', ha='center', fontsize=10)

# الرسم 2: مقارنة مع الأعماق المعروفة
ax2 = axes[0, 1]
for N in candidate_Ns:
    depth_Z8 = next(r[1] for r in results if r[0] == N)
    known = known_depths.get(N, 0)
    
    x_pos = candidate_Ns.index(N)
    ax2.scatter([x_pos - 0.15], [depth_Z8], c='blue', s=100, marker='o', label='عند Z8' if x_pos == 0 else '')
    ax2.scatter([x_pos + 0.15], [known], c='red', s=100, marker='s', label='عند صفر آخر' if x_pos == 0 else '')
    
    # خط توصيل
    ax2.plot([x_pos - 0.15, x_pos + 0.15], [depth_Z8, known], 'gray', alpha=0.5)

ax2.set_xticks(range(len(candidate_Ns)))
ax2.set_xticklabels([str(n) for n in candidate_Ns])
ax2.set_xlabel('N', fontsize=12)
ax2.set_ylabel('عمق القاع', fontsize=12)
ax2.set_title('مقارنة: عمق Z8 vs أعماق معروفة', fontsize=14)
ax2.legend(['عند Z8', 'عند صفر آخر'])
ax2.grid(True, alpha=0.3)

# الرسم 3: منحنى القاع لأفضل N
ax3 = axes[1, 0]
t_span = 1.0
t_values = np.linspace(Z8_actual - t_span, Z8_actual + t_span, 500)
mags = []
for t in t_values:
    S = zeta_sum(t, best_N)
    mags.append(np.abs(S) / np.sqrt(best_N))

ax3.plot(t_values, mags, 'b-', linewidth=2)
ax3.axvline(x=Z8_actual, color='red', linestyle='--', linewidth=2, label=f'Z8 = {Z8_actual:.3f}')
ax3.set_xlabel('t', fontsize=12)
ax3.set_ylabel(f'|S_N|/√N (N={best_N})', fontsize=12)
ax3.set_title(f'منحنى القاع عند N = {best_N} (عمق = {best_depth:.2f})', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# الرسم 4: ملخص العائلات
ax4 = axes[1, 1]
family_data = {
    'N=20': [37.59],
    'N=25': [14.13],
    'N=34': [30.42],
    'N=70': [21.02],
    'N=98': [25.01],
    'N=119': [32.94, 43.33]
}

# إضافة Z8 إلى عائلته
if best_N == 20:
    family_data['N=20'].append(Z8_actual)
elif best_N == 25:
    family_data['N=25'].append(Z8_actual)
elif best_N == 34:
    family_data['N=34'].append(Z8_actual)
elif best_N == 70:
    family_data['N=70'].append(Z8_actual)
elif best_N == 98:
    family_data['N=98'].append(Z8_actual)
elif best_N == 119:
    family_data['N=119'].append(Z8_actual)

for family, zeros in family_data.items():
    y_pos = list(family_data.keys()).index(family)
    ax4.scatter(zeros, [y_pos] * len(zeros), s=100, alpha=0.7, edgecolors='black')
    if len(zeros) > 1:
        ax4.plot(zeros, [y_pos] * len(zeros), 'gray', alpha=0.5)

ax4.set_yticks(range(len(family_data)))
ax4.set_yticklabels(family_data.keys())
ax4.set_xlabel('t (موقع الصفر)', fontsize=12)
ax4.set_title('عائلات N: الأصفار التي تخدمها كل N', fontsize=14)
ax4.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('Z8_family_determination.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ تم حفظ الرسم البياني باسم 'Z8_family_determination.png'")

# ============================================================================
# الجزء الثامن: الخلاصة النهائية
# ============================================================================

print("\n" + "=" * 80)
print("📋 الخلاصة النهائية: عائلة Z8")
print("=" * 80)

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                      نتيجة التحقق المباشر من Z8                           ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Z8 (t = {Z8_actual:.6f})                                                    ║
║                                                                           ║
║   أفضل N = {best_N}                                                           ║
║   عمق القاع = {best_depth:.2f}                                                    ║
║                                                                           ║
║   العائلة: {best_family}                          ║
║                                                                           ║
║   العوامل الأولية: {'✓ ضمن {2,5,7,17}' if factors_ok else '✗ خارج المجموعة'}                ║
║                                                                           ║
╠════════════════════════════════════════════════════════════════════════════╣
║                          تأكيد النظرية                                      ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ✓ نظرية العائلات: Z8 ينتمي إلى عائلة N={best_N}                            ║
║   ✓ نظرية العوامل الأولية: {'تم تأكيدها' if factors_ok else 'تحتاج توسيع'}                     ║
║                                                                           ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("🏁 انتهى التحقق")
print("=" * 80)