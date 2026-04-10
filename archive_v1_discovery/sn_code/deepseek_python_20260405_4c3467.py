"""
================================================================================
التنبؤ بالصفر الثامن (Z8) باستخدام نظرية باسل للرنين العددي
المؤلف: باسل يحيى عبدالله
التاريخ: أبريل 2026

الفرضية: يمكن التنبؤ بموقع الصفر الثامن باستخدام القيم الرنانة N المعروفة
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime, factorint
from datetime import datetime

# ============================================================================
# الجزء الأول: البيانات المعروفة (الأصفار 1-7)
# ============================================================================

# الأصفار المعروفة (من التحليل السابق)
known_zeros = {
    14.134725: {'N': 25, 'depth': 18.85, 'factors': [5,5]},
    21.022040: {'N': 70, 'depth': 253.28, 'factors': [2,5,7]},
    25.010858: {'N': 98, 'depth': 201.46, 'factors': [2,7,7]},
    30.424876: {'N': 34, 'depth': 125.50, 'factors': [2,17]},
    32.935062: {'N': 119, 'depth': 146.60, 'factors': [7,17]},
    37.586178: {'N': 20, 'depth': 712.37, 'factors': [2,2,5]},
    43.327073: {'N': 119, 'depth': 714.29, 'factors': [7,17]}  # Z7 يؤكد أن 119 تخدم Z5 و Z7
}

# مجموعة N الرنانة المعروفة
resonant_Ns = [20, 25, 34, 70, 98, 119]

# العوامل الأولية المسموحة
allowed_primes = [2, 5, 7, 17]

print("=" * 80)
print("🔮 التنبؤ بالصفر الثامن (Z8) باستخدام نظرية باسل")
print(f"⏰ وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

print("\n📊 البيانات المعروفة:")
print(f"   الأصفار المعروفة: {sorted(known_zeros.keys())}")
print(f"   القيم الرنانة N: {resonant_Ns}")
print(f"   العوامل المسموحة: {allowed_primes}")

# ============================================================================
# الجزء الثاني: تحليل الأنماط للتنبؤ
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 1: تحليل الأنماط للتنبؤ بـ Z8")
print("=" * 60)

# ترتيب الأصفار حسب t
sorted_zeros = sorted(known_zeros.items())
t_vals = [t for t, _ in sorted_zeros]
N_vals = [info['N'] for _, info in sorted_zeros]

# حساب الفروق بين الأصفار المتتالية
gaps = [t_vals[i+1] - t_vals[i] for i in range(len(t_vals)-1)]
print(f"\nالفروق بين الأصفار المتتالية: {[f'{g:.3f}' for g in gaps]}")
print(f"متوسط الفرق = {np.mean(gaps):.3f}")
print(f"الانحراف المعياري = {np.std(gaps):.3f}")

# التنبؤ بموقع Z8 بناءً على متوسط الفرق
prediction_by_gap = t_vals[-1] + np.mean(gaps)
print(f"\n🔮 التنبؤ 1 (متوسط الفرق): Z8 ≈ {prediction_by_gap:.3f}")

# التنبؤ باستخدام آخر فرق
prediction_by_last_gap = t_vals[-1] + gaps[-1]
print(f"🔮 التنبؤ 2 (آخر فرق): Z8 ≈ {prediction_by_last_gap:.3f}")

# ============================================================================
# الجزء الثالث: التنبؤ باستخدام القيم الرنانة N
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 2: التنبؤ باستخدام القيم الرنانة N")
print("=" * 60)

# لكل N رنانة، نجد الأصفار التي تخدمها
N_to_zeros = {}
for t, info in known_zeros.items():
    N = info['N']
    if N not in N_to_zeros:
        N_to_zeros[N] = []
    N_to_zeros[N].append(t)

print("\nتوزيع N على الأصفار:")
for N in sorted(N_to_zeros.keys()):
    zeros_list = N_to_zeros[N]
    print(f"   N={N}: يخدم الأصفار عند t = {zeros_list}")

# التنبؤ: N=119 يخدم Z5 (32.94) و Z7 (43.33)
# ما الفرق بينهما؟
diff_119 = 43.327073 - 32.935062
print(f"\n🔮 الفرق بين Z5 و Z7 (كلاهما N=119): {diff_119:.4f}")

# التنبؤ بأن Z9 قد يكون عند Z7 + diff_119
prediction_N119_next = 43.327073 + diff_119
print(f"🔮 التنبؤ 3 (تسلسل N=119): Z8 ≈ {prediction_N119_next:.3f} (إذا تكرر النمط)")

# N=70 يخدم Z2 فقط حالياً
# N=98 يخدم Z3 فقط
# N=34 يخدم Z4 فقط
# N=25 يخدم Z1 فقط
# N=20 يخدم Z6 فقط

# ============================================================================
# الجزء الرابع: التنبؤ باستخدام العلاقة t/N
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 3: التنبؤ باستخدام نسبة t/N")
print("=" * 60)

# حساب نسبة t/N لكل صفر
ratios = [(t, t/info['N']) for t, info in known_zeros.items()]
print("\nنسبة t/N لكل صفر:")
for t, ratio in sorted(ratios):
    print(f"   t={t:.3f}, N={known_zeros[t]['N']} → t/N = {ratio:.4f}")

# هل هناك مجموعة من النسب المتقاربة؟
ratios_values = [r for _, r in ratios]
print(f"\nمتوسط النسبة = {np.mean(ratios_values):.4f}")
print(f"الوسيط = {np.median(ratios_values):.4f}")

# التنبؤ باستخدام النسبة المتوسطة لـ N=119
N119_avg_ratio = np.mean([32.935062/119, 43.327073/119])
prediction_ratio_N119 = 119 * N119_avg_ratio
print(f"\n🔮 التنبؤ 4 (متوسط نسبة N=119 = {N119_avg_ratio:.4f}):")
print(f"   Z8 ≈ 119 × {N119_avg_ratio:.4f} = {prediction_ratio_N119:.3f}")

# ============================================================================
# الجزء الخامس: تجميع التنبؤات
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 4: تجميع التنبؤات")
print("=" * 60)

predictions = {
    'متوسط الفرق بين الأصفار': prediction_by_gap,
    'آخر فرق (Z6→Z7)': prediction_by_last_gap,
    'تسلسل N=119': prediction_N119_next,
    'متوسط نسبة N=119': prediction_ratio_N119
}

print("\nقائمة التنبؤات لموقع Z8:")
for method, pred in predictions.items():
    print(f"   {method}: {pred:.3f}")

# القيمة المرجعية للصفر الثامن (معروفة من الأدبيات)
Z8_actual = 48.005150881167159  # الصفر الثامن المعروف
print(f"\n📖 القيمة المرجعية لـ Z8 (من الأدبيات): {Z8_actual:.6f}")

# حساب دقة التنبؤات
print("\nدقة التنبؤات:")
for method, pred in predictions.items():
    error = abs(pred - Z8_actual)
    accuracy = (1 - error/Z8_actual) * 100
    print(f"   {method}: خطأ = {error:.4f} (دقة = {accuracy:.2f}%)")

# ============================================================================
# الجزء السادس: البحث عن أفضل N لـ Z8 المتوقع
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 5: ما هي أفضل N المتوقعة لـ Z8؟")
print("=" * 60)

# إذا كان Z8 عند 48.005، فما هي N التي تتوقع النظرية أنها ستكون رنانة؟
print(f"\nبناءً على Z8 ≈ {Z8_actual:.3f}، نحسب أي N مرشح سيكون الأفضل:")

def predict_best_N(t):
    """توقع أفضل N لصفر معين بناءً على النظرية"""
    candidates = []
    for N in resonant_Ns:
        # نسبة التقارب
        ratio = t / N
        candidates.append((N, ratio))
    return candidates

candidates = predict_best_N(Z8_actual)
print("\nN المرشحة ونسبة t/N:")
for N, ratio in candidates:
    # مقارنة مع النسب المعروفة
    similar_ratios = [r for t, r in ratios if abs(r - ratio) < 0.1]
    hint = f" (قريب من نسب {similar_ratios[:2]})" if similar_ratios else ""
    print(f"   N={N}: t/N = {ratio:.4f}{hint}")

# أي N من المجموعة يعطي نسبة مشابهة لنسبة معروفة؟
print("\n🔮 توقع أفضل N لـ Z8:")
for N in resonant_Ns:
    ratio = Z8_actual / N
    # البحث عن نسبة مشابهة في البيانات المعروفة
    closest_ratio = min(ratios_values, key=lambda r: abs(r - ratio))
    if abs(ratio - closest_ratio) < 0.05:
        print(f"   N={N}: t/N={ratio:.4f} قريب من نسبة موجودة ({closest_ratio:.4f}) ← مرشح قوي ✓")
    else:
        print(f"   N={N}: t/N={ratio:.4f} بعيد عن النسب المعروفة")

# ============================================================================
# الجزء السابع: تحليل دورية N=119
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 6: تحليل دورية N=119")
print("=" * 60)

# الأصفار التي تخدمها N=119
N119_zeros = sorted(N_to_zeros.get(119, []))
print(f"\nN=119 تخدم الأصفار عند: {N119_zeros}")

if len(N119_zeros) >= 2:
    periods = [N119_zeros[i+1] - N119_zeros[i] for i in range(len(N119_zeros)-1)]
    print(f"الفترات بين هذه الأصفار: {periods}")
    
    # التنبؤ بالصفر التالي في هذه السلسلة
    next_in_series = N119_zeros[-1] + np.mean(periods)
    print(f"\n🔮 إذا استمرت الدورية: الصفر التالي لـ N=119 عند t ≈ {next_in_series:.3f}")
    
    # هل هذا قريب من Z8؟
    print(f"   الفرق عن Z8 الحقيقي: {abs(next_in_series - Z8_actual):.4f}")

# ============================================================================
# الجزء الثامن: التحقق من فرضية أن Z8 قد يكون مرتبطاً بـ N=70 أو N=98
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 7: اختبار فرضيات أخرى لـ Z8")
print("=" * 60)

# هل هناك نمط في تناوب N؟
N_sequence = [info['N'] for _, info in sorted_zeros]
print(f"\nتسلسل N حسب ترتيب الأصفار: {N_sequence}")

# البحث عن نمط دوري في تسلسل N
from collections import Counter
N_counts = Counter(N_sequence)
print(f"\nتكرار كل N: {dict(N_counts)}")

# التنبؤ بـ N التالي في التسلسل
# ما هي N التي لم تظهر مؤخراً؟
last_N = N_sequence[-1]
print(f"\nآخر N ظهر: {last_N} (عند Z7)")

# إذا كان النمط تناوبياً، ما هو N التالي المحتمل?
possible_next_Ns = [n for n in resonant_Ns if n != last_N]
print(f"N المرشحة التالية (مختلفة عن {last_N}): {possible_next_Ns}")

# ============================================================================
# الجزء التاسع: الرسم البياني
# ============================================================================

print("\n📈 جاري إنشاء الرسوم البيانية...")

fig = plt.figure(figsize=(16, 10))

# الرسم 1: الأصفار والقيم الرنانة
ax1 = fig.add_subplot(2, 2, 1)
t_list = list(known_zeros.keys())
N_list = [known_zeros[t]['N'] for t in t_list]
depths = [known_zeros[t]['depth'] for t in t_list]

colors = ['red' if N == 119 else 'blue' for N in N_list]
sizes = [d/5 for d in depths]
ax1.scatter(t_list, N_list, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=1.5)

# إضافة Z8 المتوقع
ax1.scatter([Z8_actual], [119], c='green', s=200, marker='*', label='Z8 (مرجع)', edgecolors='black', linewidth=1.5)
ax1.axvline(x=Z8_actual, color='green', linestyle='--', alpha=0.5)

ax1.set_xlabel('t (موقع الصفر)', fontsize=12)
ax1.set_ylabel('N (القيمة الرنانة)', fontsize=12)
ax1.set_title('القيم الرنانة للأصفار (الأحمر = N=119)', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# الرسم 2: التنبؤات المختلفة
ax2 = fig.add_subplot(2, 2, 2)
methods = list(predictions.keys())
pred_values = list(predictions.values())
errors = [abs(p - Z8_actual) for p in pred_values]

bars = ax2.barh(methods, errors, color='steelblue', edgecolor='black')
ax2.axvline(x=0, color='black', linewidth=1)
ax2.set_xlabel('خطأ التنبؤ', fontsize=12)
ax2.set_title('دقة التنبؤات المختلفة لموقع Z8', fontsize=14)

# إضافة قيمة الخطأ على الأشرطة
for bar, err in zip(bars, errors):
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{err:.3f}', va='center')

# الرسم 3: تطور N مع t
ax3 = fig.add_subplot(2, 2, 3)
ax3.plot(t_list, N_list, 'b-o', linewidth=2, markersize=8, label='البيانات المعروفة')
ax3.scatter([Z8_actual], [119], c='green', s=150, marker='*', label='Z8 (مرجع)')
ax3.set_xlabel('t', fontsize=12)
ax3.set_ylabel('N', fontsize=12)
ax3.set_title('تطور القيم الرنانة مع الأصفار', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# الرسم 4: توزيع العوامل الأولية المحدث
ax4 = fig.add_subplot(2, 2, 4)
all_factors = []
for info in known_zeros.values():
    all_factors.extend(info['factors'])
unique, counts = np.unique(all_factors, return_counts=True)
ax4.bar(unique, counts, color='darkgreen', edgecolor='black', alpha=0.7)
ax4.set_xlabel('العوامل الأولية', fontsize=12)
ax4.set_ylabel('التكرار', fontsize=12)
ax4.set_title('توزيع العوامل الأولية (جميع الأصفار 1-7)', fontsize=14)
ax4.set_xticks(unique)
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('Z8_prediction.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ تم حفظ الرسم البياني باسم 'Z8_prediction.png'")

# ============================================================================
# الجزء العاشر: الخلاصة النهائية
# ============================================================================

print("\n" + "=" * 80)
print("📋 الخلاصة النهائية للتنبؤ بـ Z8")
print("=" * 80)

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                         نظرية باسل للرنين العددي                           ║
║                              - التطبيق على Z8 -                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   الصفر الثامن المرجعي (Z8): {Z8_actual:.6f}                                    ║
║                                                                           ║
║   أفضل التنبؤات:                                                          ║
║   • تسلسل N=119: {prediction_N119_next:.3f} (خطأ = {abs(prediction_N119_next - Z8_actual):.4f})     ║
║   • متوسط نسبة N=119: {prediction_ratio_N119:.3f} (خطأ = {abs(prediction_ratio_N119 - Z8_actual):.4f})   ║
║                                                                           ║
║   التوقع النظري:                                                          ║
║   • N المتوقعة لـ Z8: 119 (إذا استمر النمط) أو 70/98                      ║
║   • العوامل المتوقعة: 7×17 أو 2×5×7 أو 2×7×7                             ║
║                                                                           ║
╠════════════════════════════════════════════════════════════════════════════╣
║                              التوصيات                                      ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   1. التحقق من Z8 عن طريق حساب العمق عند N=119                            ║
║   2. إذا كان العمق > 100، تتأكد نظرية N=119                               ║
║   3. إذا لم يكن، نختبر N=70 و N=98                                        ║
║                                                                           ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("🏁 انتهى التحليل التنبؤي")
print("=" * 80)