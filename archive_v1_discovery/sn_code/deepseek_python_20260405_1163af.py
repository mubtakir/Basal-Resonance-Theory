"""
================================================================================
الاختبار التنبؤي: تطبيق نظرية باسل للرنين العددي على صفر جديد
المؤلف: باسل يحيى عبدالله
التاريخ: أبريل 2026

الفرضية: يمكن التنبؤ بأفضل N لأي صفر باستخدام القواعد المكتشفة
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime, factorint
from datetime import datetime

# ============================================================================
# الجزء الأول: القواعد المكتشفة من التحليل السابق
# ============================================================================

print("=" * 80)
print("🔮 الاختبار التنبؤي: نظرية باسل للرنين العددي")
print(f"⏰ وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# القيم الرنانة المعروفة (من التحليل السابق)
known_resonant = {
    14.134725: {'N': 25, 'depth': 18.85, 'factors': [5,5]},
    21.022040: {'N': 70, 'depth': 253.28, 'factors': [2,5,7]},
    25.010858: {'N': 98, 'depth': 201.46, 'factors': [2,7,7]},
    30.424876: {'N': 34, 'depth': 125.50, 'factors': [2,17]},
    32.935062: {'N': 119, 'depth': 146.60, 'factors': [7,17]},
    37.586178: {'N': 20, 'depth': 712.37, 'factors': [2,2,5]}
}

# مجموعة العوامل الأولية المسموحة (من النظرية)
allowed_primes = [2, 5, 7, 17]
candidate_Ns = sorted(set([20, 25, 34, 70, 98, 119]))

print("\n📊 القواعد المستخلصة من النظرية:")
print(f"   - العوامل الأولية المسموحة: {allowed_primes}")
print(f"   - مجموعة N المرشحة: {candidate_Ns}")
print(f"   - العلاقة المقترحة: أفضل N هو الأقرب إلى t₀ / 1.88 (من Z6)")

# ============================================================================
# الجزء الثاني: اختيار صفر جديد للاختبار
# ============================================================================

# الصفر السابع لدالة زيتا (قيمة معروفة)
Z7_t = 43.327073280914999  # الصفر السابع (تقريباً)
Z7_name = "Z7 (الصفر السابع)"

print(f"\n🎯 الصفر المختار للاختبار: {Z7_name} (t = {Z7_t:.6f})")
print("   هذا الصفر لم يستخدم في بناء النظرية")

# ============================================================================
# الجزء الثالث: التنبؤات بناءً على النظريات المختلفة
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 1: التنبؤات المسبقة")
print("=" * 60)

# تنبؤ 1: بناءً على Z6 (N = t/1.88)
prediction_1 = int(np.round(Z7_t / 1.8795))
print(f"\n🔮 التنبؤ 1 (قاعدة Z6: N ≈ t/1.88):")
print(f"   N_pred = round({Z7_t:.4f} / 1.8795) = {prediction_1}")

# تنبؤ 2: أقرب N مرشح من المجموعة المعروفة
distances = [(abs(N - Z7_t/1.88), N) for N in candidate_Ns]
closest_candidate = min(distances)[1]
print(f"\n🔮 التنبؤ 2 (أقرب N مرشح من المجموعة {candidate_Ns}):")
print(f"   N_pred = {closest_candidate}")

# تنبؤ 3: بناءً على العلاقة N/t من Z2, Z3, Z5 (المجموعة المتوسطة)
avg_ratio = np.mean([70/21.022, 98/25.011, 119/32.935])
prediction_3 = int(np.round(Z7_t * avg_ratio))
print(f"\n🔮 التنبؤ 3 (متوسط نسبة N/t من Z2,Z3,Z5 = {avg_ratio:.3f}):")
print(f"   N_pred = round({Z7_t:.4f} × {avg_ratio:.3f}) = {prediction_3}")

# تنبؤ 4: بناءً على مضاعفات 17
prediction_4 = int(np.round(Z7_t / 17) * 17)
print(f"\n🔮 التنبؤ 4 (مضاعفات 17):")
print(f"   N_pred = {prediction_4}")

# جمع التنبؤات
predictions = {
    'قاعدة Z6 (t/1.88)': prediction_1,
    'أقرب N مرشح': closest_candidate,
    f'متوسط النسبة ({avg_ratio:.3f})': prediction_3,
    'مضاعفات 17': prediction_4
}

print(f"\n📋 ملخص التنبؤات:")
for method, pred in predictions.items():
    print(f"   {method}: N = {pred}")

# ============================================================================
# الجزء الرابع: حساب العمق الفعلي لكل N مرشح
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 2: الحساب الفعلي للعمق عند كل N مرشح")
print("=" * 60)

def zeta_sum(t, N, sigma=0.5):
    """حساب المجموع الجزئي لدالة زيتا"""
    n = np.arange(1, N + 1, dtype=np.float64)
    return np.sum(n ** (-sigma + 1j * t))

def compute_depth(t_zero, N, t_span=0.8, n_points=300):
    """حساب عمق القاع"""
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    magnitudes = []
    
    for t in t_values:
        S = zeta_sum(t, N)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    magnitudes = np.array(magnitudes)
    depth = np.mean(magnitudes) / (np.min(magnitudes) + 1e-12)
    return depth, np.min(magnitudes), t_values[np.argmin(magnitudes)]

print(f"\n🔄 جاري حساب العمق للصفر {Z7_name} (t = {Z7_t:.6f})...")

# اختبار جميع N المرشحة
test_results = []
for N in candidate_Ns + [prediction_1, prediction_3, prediction_4]:
    if N not in [r[0] for r in test_results]:
        depth, min_val, t_min = compute_depth(Z7_t, N, t_span=1.0, n_points=350)
        test_results.append((N, depth, min_val, t_min))
        status = "🔥 ممتاز!" if depth > 10 else "✅ جيد" if depth > 5 else "⚠️ ضعيف"
        print(f"   N = {N:3d} → عمق = {depth:8.2f} | min = {min_val:.6f} | {status}")

# ترتيب النتائج حسب العمق
test_results.sort(key=lambda x: x[1], reverse=True)
best_N_actual = test_results[0][0]
best_depth_actual = test_results[0][1]

print(f"\n🏆 النتيجة الفعلية: أفضل N = {best_N_actual} (عمق = {best_depth_actual:.2f})")

# ============================================================================
# الجزء الخامس: تقييم التنبؤات
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 3: تقييم دقة التنبؤات")
print("=" * 60)

print(f"\nالحقيقة المكتشفة: أفضل N = {best_N_actual}")

print("\nترتيب التنبؤات حسب الدقة:")
evaluations = []
for method, pred in predictions.items():
    error = abs(pred - best_N_actual)
    is_correct = (pred == best_N_actual)
    evaluations.append((method, pred, error, is_correct))

evaluations.sort(key=lambda x: x[2])

for method, pred, error, correct in evaluations:
    status = "✅ صحيح!" if correct else f"❌ خطأ بمقدار {error}"
    print(f"   {method}: {pred} → {status}")

# ============================================================================
# الجزء السادس: تحليل العوامل الأولية لأفضل N الفعلي
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 4: تحليل أفضل N الفعلي")
print("=" * 60)

factors = factorint(best_N_actual)
factor_str = ' × '.join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
is_N_prime = isprime(best_N_actual)

print(f"\nأفضل N = {best_N_actual}")
print(f"   هل هو أولي؟ {'نعم' if is_N_prime else 'لا'}")
print(f"   التحليل إلى عوامل: {factor_str}")
print(f"   العوامل الأولية: {list(factors.keys())}")

# هل العوامل ضمن المجموعة المسموحة?
factors_ok = all(p in allowed_primes for p in factors.keys())
print(f"   هل العوامل ضمن {{{allowed_primes}}}؟ {'نعم ✅' if factors_ok else 'لا ❌'}")

# هل N موجود في المجموعة المرشحة؟
in_candidate = best_N_actual in candidate_Ns
print(f"   هل N في مجموعة المرشحين {candidate_Ns}؟ {'نعم ✅' if in_candidate else 'لا ❌'}")

# ============================================================================
# الجزء السابع: تحديث النظرية
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 5: تحديث النظرية بناءً على النتيجة الجديدة")
print("=" * 60)

# إضافة الصفر الجديد إلى المعرفة
updated_resonant = dict(known_resonant)
updated_resonant[Z7_t] = {'N': best_N_actual, 'depth': best_depth_actual, 'factors': list(factors.keys())}

print("\nالقيم الرنانة المحدثة (بما في ذلك Z7):")
for t, info in updated_resonant.items():
    print(f"   t = {t:.3f} → N = {info['N']:3d} (عوامله: {info['factors']})")

# حساب نسبة t/N الجديدة
print("\nنسبة t/N بعد إضافة Z7:")
for t, info in updated_resonant.items():
    ratio = t / info['N']
    print(f"   t={t:.3f}, N={info['N']:3d} → t/N = {ratio:.4f}")

# هل هناك ثابت جديد يظهر؟
ratios = [t/info['N'] for t, info in updated_resonant.items()]
print(f"\nمتوسط النسبة = {np.mean(ratios):.4f}")
print(f"انحراف معياري = {np.std(ratios):.4f}")

# ============================================================================
# الجزء الثامن: الرسوم البيانية
# ============================================================================

print("\n📈 جاري إنشاء الرسوم البيانية...")

fig = plt.figure(figsize=(16, 10))

# الرسم 1: أفضل N مقابل t (مع إضافة Z7)
ax1 = fig.add_subplot(2, 2, 1)
t_vals = list(updated_resonant.keys())
N_vals = [info['N'] for info in updated_resonant.values()]
depths = [info['depth'] for info in updated_resonant.values()]

colors = ['red' if t == Z7_t else 'blue' for t in t_vals]
sizes = [d/5 for d in depths]
ax1.scatter(t_vals, N_vals, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=1.5)
ax1.set_xlabel('t₀ (موقع الصفر)', fontsize=12)
ax1.set_ylabel('أفضل N', fontsize=12)
ax1.set_title('القيم الرنانة (الأحمر = Z7 الجديد)', fontsize=14)
ax1.grid(True, alpha=0.3)

# إضافة خط الاتجاه
z = np.polyfit(t_vals, N_vals, 1)
p = np.poly1d(z)
t_line = np.linspace(min(t_vals)-2, max(t_vals)+2, 100)
ax1.plot(t_line, p(t_line), 'gray', linestyle='--', alpha=0.5, label=f'N = {z[0]:.2f}t + {z[1]:.2f}')
ax1.legend()

# الرسم 2: عمق القاع مقابل N
ax2 = fig.add_subplot(2, 2, 2)
for t, info in updated_resonant.items():
    color = 'red' if t == Z7_t else 'blue'
    ax2.scatter(info['N'], info['depth'], c=color, s=100, alpha=0.7, edgecolors='black')
    ax2.annotate(f't={t:.1f}', (info['N'], info['depth']), xytext=(5, 5), textcoords='offset points', fontsize=8)
ax2.set_xlabel('N', fontsize=12)
ax2.set_ylabel('عمق القاع', fontsize=12)
ax2.set_title('العلاقة بين N وعمق القاع', fontsize=14)
ax2.grid(True, alpha=0.3)

# الرسم 3: نسبة t/N
ax3 = fig.add_subplot(2, 2, 3)
ratios = [t/info['N'] for t, info in updated_resonant.items()]
t_list = list(updated_resonant.keys())
colors_bar = ['red' if t == Z7_t else 'steelblue' for t in t_list]
ax3.bar([f't={t:.1f}' for t in t_list], ratios, color=colors_bar, edgecolor='black')
ax3.axhline(y=np.mean(ratios), color='red', linestyle='--', label=f'المتوسط = {np.mean(ratios):.3f}')
ax3.set_xlabel('الصفر', fontsize=12)
ax3.set_ylabel('t/N', fontsize=12)
ax3.set_title('نسبة t/N لكل صفر', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# الرسم 4: توزيع العوامل الأولية
ax4 = fig.add_subplot(2, 2, 4)
all_factors = []
for info in updated_resonant.values():
    all_factors.extend(info['factors'])
unique, counts = np.unique(all_factors, return_counts=True)
ax4.bar(unique, counts, color='darkgreen', edgecolor='black', alpha=0.7)
ax4.set_xlabel('العوامل الأولية', fontsize=12)
ax4.set_ylabel('التكرار', fontsize=12)
ax4.set_title('توزيع العوامل الأولية في جميع N الرنانة', fontsize=14)
ax4.set_xticks(unique)
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('predictive_test_Z7.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ تم حفظ الرسم البياني باسم 'predictive_test_Z7.png'")

# ============================================================================
# الجزء التاسع: الخلاصة النهائية للاختبار
# ============================================================================

print("\n" + "=" * 80)
print("📋 الخلاصة النهائية للاختبار التنبؤي")
print("=" * 80)

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                          نتيجة الاختبار التنبؤي                           ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   الصفر المختبر: Z7 (t = {Z7_t:.6f})                                        ║
║                                                                           ║
║   أفضل N الفعلي: {best_N_actual}                                                 ║
║   عمق القاع: {best_depth_actual:.2f}                                                    ║
║                                                                           ║
║   هل العوامل ضمن {{{allowed_primes}}}؟ {'نعم ✓' if factors_ok else 'لا ✗'}                          ║
║   هل N في مجموعة المرشحين؟ {'نعم ✓' if in_candidate else 'لا ✗'}                         ║
║                                                                           ║
╠════════════════════════════════════════════════════════════════════════════╣
║                          تقييم النظرية                                      ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   نظرية العوامل الأولية: {'تم تأكيدها ✓' if factors_ok else 'تحتاج مراجعة'}                          ║
║   نظرية المجموعة المرشحة: {'تم تأكيدها ✓' if in_candidate else 'تحتاج توسيع'}                      ║
║                                                                           ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("🏁 انتهى الاختبار التنبؤي")
print("=" * 80)