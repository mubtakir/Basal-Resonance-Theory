"""
================================================================================
البحث: اكتشاف القيم الرنانة (Resonant N) لأصفار دالة زيتا لريمان
المؤلف: باسل يحيى عبدالله
التاريخ: أبريل 2026

الهدف: إيجاد العلاقة بين عدد الحدود N وعمق القاع عند كل صفر من أصفار زيتا
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# الجزء الأول: تعريف الدوال الأساسية
# ============================================================================

def zeta_partial_sum(t, N, sigma=0.5):
    """
    حساب المجموع الجزئي لدالة زيتا: Σ n^(-σ + it)
    
    المعاملات:
    t : الجزء التخيلي (التردد)
    N : عدد الحدود
    sigma : الجزء الحقيقي (ثابت عند 0.5 للخط الحرج)
    
    المخرج:
    S : المجموع المركب
    """
    n = np.arange(1, N + 1, dtype=np.float64)
    terms = n ** (-sigma + 1j * t)
    return np.sum(terms)


def compute_depth(t_zero, N, t_span=0.8, n_points=250, sigma=0.5):
    """
    حساب عمق القاع عند صفر معين لعدد حدود N محدد
    
    العمق = متوسط |S_N| / أقل |S_N|
    كلما كان العمق أكبر، كان القاع أوضح والرنين أقوى
    
    المعاملات:
    t_zero : موقع الصفر المفترض
    N : عدد الحدود
    t_span : نصف عرض النافذة حول الصفر
    n_points : عدد النقاط في النافذة
    sigma : الجزء الحقيقي (0.5 للخط الحرج)
    
    المخرجات:
    depth : عمق القاع
    min_val : أقل قيمة لـ |S_N|/√N
    t_min : موقع القاع الفعلي (قد ينحرف قليلاً عن t_zero)
    """
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    magnitudes = []
    
    for t in t_values:
        S = zeta_partial_sum(t, N, sigma)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    magnitudes = np.array(magnitudes)
    min_val = np.min(magnitudes)
    avg_val = np.mean(magnitudes)
    depth = avg_val / (min_val + 1e-12)
    
    min_idx = np.argmin(magnitudes)
    t_min = t_values[min_idx]
    
    return depth, min_val, t_min


def scan_resonant_N(t_zero, N_range, t_span=0.8, n_points=200, verbose=True):
    """
    مسح شامل لمجموعة من قيم N لإيجاد القيم الرنانة (ذات العمق الأكبر)
    
    المعاملات:
    t_zero : موقع الصفر
    N_range : قائمة أو نطاق قيم N لفحصها
    t_span : نصف عرض النافذة حول الصفر
    n_points : عدد النقاط لكل حساب
    verbose : هل نطبع التقدم؟
    
    المخرجات:
    results : قائمة تحتوي (N, depth, min_val, t_min)
    """
    results = []
    total = len(N_range) if hasattr(N_range, '__len__') else N_range.stop - N_range.start
    
    for i, N in enumerate(N_range):
        depth, min_val, t_min = compute_depth(t_zero, N, t_span, n_points)
        results.append((N, depth, min_val, t_min))
        
        if verbose and (i + 1) % 20 == 0:
            print(f"   تقدم: {i+1}/{total} N تم فحصها")
    
    return results


# ============================================================================
# الجزء الثاني: الأصفار المرجعية لدالة زيتا
# ============================================================================

# أصفار دالة زيتا على الخط الحرج (قيم معروفة بدقة عالية)
ZETA_ZEROS = {
    'first': {
        't': 14.134725141734693,
        'name': 'الصفر الأول',
        'order': 1
    },
    'second': {
        't': 21.022039638771554,
        'name': 'الصفر الثاني',
        'order': 2
    },
    'third': {
        't': 25.010857580145688,
        'name': 'الصفر الثالث',
        'order': 3
    },
    'fourth': {
        't': 30.424876125859513,
        'name': 'الصفر الرابع',
        'order': 4
    },
    'fifth': {
        't': 32.93506158773919,
        'name': 'الصفر الخامس',
        'order': 5
    },
    'sixth': {
        't': 37.58617815882567,
        'name': 'الصفر السادس',
        'order': 6
    }
}


# ============================================================================
# الجزء الثالث: تنفيذ المسح الشامل
# ============================================================================

print("=" * 80)
print("🔬 مسح القيم الرنانة (Resonant N) لأصفار دالة زيتا لريمان")
print(f"⏰ وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# نطاق البحث لـ N
N_min = 5
N_max = 200
N_step = 1
N_range = range(N_min, N_max + 1, N_step)

print(f"\n📊 إعدادات المسح:")
print(f"   - نطاق N: {N_min} إلى {N_max} (خطوة {N_step})")
print(f"   - عدد قيم N: {len(N_range)}")
print(f"   - عدد الأصفار: {len(ZETA_ZEROS)}")
print(f"   - إجمالي العمليات: {len(N_range) * len(ZETA_ZEROS)}")
print()

# تخزين جميع النتائج
all_results = {}

for zero_key, zero_info in ZETA_ZEROS.items():
    t0 = zero_info['t']
    zero_name = zero_info['name']
    order = zero_info['order']
    
    print(f"\n{'='*60}")
    print(f"📌 {zero_name} (t = {t0:.6f}, الرتبة {order})")
    print(f"{'='*60}")
    print("🔄 جاري المسح...")
    
    results = scan_resonant_N(t0, N_range, t_span=1.0, n_points=200, verbose=True)
    all_results[zero_key] = results
    
    # إيجاد أفضل 5 قيم N (أعلى عمق)
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    top5 = sorted_results[:5]
    
    print(f"\n🏆 أفضل 5 قيم رنانة لـ N (أعلى عمق):")
    print("-" * 50)
    print(f"{'الرتبة':^6} | {'N':^6} | {'العمق':^10} | {'min |S|/√N':^14} | {'t_min':^12}")
    print("-" * 50)
    for rank, (N, depth, min_val, t_min) in enumerate(top5, 1):
        print(f"{rank:^6} | {N:^6} | {depth:^10.2f} | {min_val:^14.6f} | {t_min:^12.6f}")
    
    # تخزين أفضل N
    all_results[zero_key + '_best'] = top5[0][0]

print("\n" + "=" * 80)
print("📊 الملخص النهائي: أفضل N لكل صفر")
print("=" * 80)
print(f"{'الصفر':^15} | {'t₀':^15} | {'أفضل N':^10} | {'العمق':^10} | {'الانحراف عن t₀':^15}")
print("-" * 80)

best_N_summary = {}

for zero_key, zero_info in ZETA_ZEROS.items():
    t0 = zero_info['t']
    results = all_results[zero_key]
    best_N, best_depth, _, best_t = max(results, key=lambda x: x[1])
    deviation = abs(best_t - t0)
    best_N_summary[zero_key] = {
        'N': best_N,
        'depth': best_depth,
        'deviation': deviation,
        't_min': best_t
    }
    print(f"{zero_info['name']:^15} | {t0:^15.6f} | {best_N:^10} | {best_depth:^10.2f} | {deviation:^15.6f}")

print("=" * 80)


# ============================================================================
# الجزء الرابع: التحليل والرسوم البيانية
# ============================================================================

print("\n📈 جاري إنشاء الرسوم البيانية...")

# إعداد الشكل
fig = plt.figure(figsize=(16, 12))

# الرسم البياني 1: عمق القاع كدالة في N لجميع الأصفار
ax1 = fig.add_subplot(2, 2, 1)
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']
markers = ['o', 's', '^', 'D', 'v', '<']

for idx, (zero_key, zero_info) in enumerate(ZETA_ZEROS.items()):
    results = all_results[zero_key]
    N_vals = [r[0] for r in results]
    depth_vals = [r[1] for r in results]
    ax1.plot(N_vals, depth_vals, color=colors[idx % len(colors)], 
             marker=markers[idx % len(markers)], markersize=2, linewidth=0.8,
             label=f"{zero_info['name']} (t={zero_info['t']:.2f})", alpha=0.7)

ax1.set_xlabel('N (عدد الحدود)', fontsize=12)
ax1.set_ylabel('عمق القاع', fontsize=12)
ax1.set_title('عمق القاع كدالة في N لجميع الأصفار', fontsize=14)
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# الرسم البياني 2: أفضل N مقابل t₀
ax2 = fig.add_subplot(2, 2, 2)
t_vals = [ZETA_ZEROS[k]['t'] for k in ZETA_ZEROS.keys()]
best_N_vals = [best_N_summary[k]['N'] for k in ZETA_ZEROS.keys()]
depths_vals = [best_N_summary[k]['depth'] for k in ZETA_ZEROS.keys()]

scatter = ax2.scatter(t_vals, best_N_vals, c=depths_vals, s=100, 
                      cmap='viridis', edgecolors='black', linewidth=1.5)
ax2.set_xlabel('t₀ (موقع الصفر)', fontsize=12)
ax2.set_ylabel('أفضل N', fontsize=12)
ax2.set_title('العلاقة بين أفضل N وموقع الصفر', fontsize=14)
ax2.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('عمق القاع', fontsize=10)

# إضافة خط الاتجاه (تقريبي)
z = np.polyfit(t_vals, best_N_vals, 1)
p = np.poly1d(z)
ax2.plot(t_vals, p(t_vals), "r--", alpha=0.5, label=f'خط الاتجاه: N ≈ {z[0]:.2f}t + {z[1]:.2f}')
ax2.legend()

# إضافة تسميات النقاط
for i, (t, n, d) in enumerate(zip(t_vals, best_N_vals, depths_vals)):
    ax2.annotate(f'N={n}', (t, n), xytext=(5, 5), textcoords='offset points', fontsize=9)

# الرسم البياني 3: توزيع أعماق القيعان
ax3 = fig.add_subplot(2, 2, 3)
all_depths = []
for zero_key in ZETA_ZEROS.keys():
    results = all_results[zero_key]
    all_depths.extend([r[1] for r in results])

ax3.hist(all_depths, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
ax3.set_xlabel('عمق القاع', fontsize=12)
ax3.set_ylabel('التكرار', fontsize=12)
ax3.set_title(f'توزيع أعماق القيعان (المتوسط = {np.mean(all_depths):.2f})', fontsize=14)
ax3.axvline(np.mean(all_depths), color='red', linestyle='--', linewidth=2, 
            label=f'المتوسط = {np.mean(all_depths):.2f}')
ax3.axvline(np.median(all_depths), color='green', linestyle='--', linewidth=2,
            label=f'الوسيط = {np.median(all_depths):.2f}')
ax3.legend()
ax3.grid(True, alpha=0.3)

# الرسم البياني 4: أفضل N لكل صفر (شريطي)
ax4 = fig.add_subplot(2, 2, 4)
zero_names = [ZETA_ZEROS[k]['name'] for k in ZETA_ZEROS.keys()]
best_N_list = [best_N_summary[k]['N'] for k in ZETA_ZEROS.keys()]
depth_list = [best_N_summary[k]['depth'] for k in ZETA_ZEROS.keys()]

bars = ax4.bar(zero_names, best_N_list, color=plt.cm.plasma(np.array(depth_list)/max(depth_list)))
ax4.set_xlabel('الصفر', fontsize=12)
ax4.set_ylabel('أفضل N', fontsize=12)
ax4.set_title('أفضل قيمة رنانة N لكل صفر', fontsize=14)
ax4.grid(True, alpha=0.3, axis='y')

# إضافة قيم العمق على الأعمدة
for bar, depth in zip(bars, depth_list):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'd={depth:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('zeta_resonant_N_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ تم حفظ الرسم البياني باسم 'zeta_resonant_N_analysis.png'")


# ============================================================================
# الجزء الخامس: التحليل الإحصائي والعلاقات
# ============================================================================

print("\n" + "=" * 80)
print("📐 التحليل الرياضي للعلاقات")
print("=" * 80)

# استخراج البيانات
t_array = np.array([ZETA_ZEROS[k]['t'] for k in ZETA_ZEROS.keys()])
N_array = np.array([best_N_summary[k]['N'] for k in ZETA_ZEROS.keys()])
depth_array = np.array([best_N_summary[k]['depth'] for k in ZETA_ZEROS.keys()])

# 1. علاقة خطية: N = a*t + b
coef_linear = np.polyfit(t_array, N_array, 1)
linear_fit = np.poly1d(coef_linear)
r_squared_linear = 1 - np.sum((N_array - linear_fit(t_array))**2) / np.sum((N_array - np.mean(N_array))**2)

print(f"\n📈 العلاقة الخطية (N = a·t + b):")
print(f"   a = {coef_linear[0]:.4f}")
print(f"   b = {coef_linear[1]:.2f}")
print(f"   R² = {r_squared_linear:.4f}")

# 2. علاقة جذرية: N = a*sqrt(t) + b
coef_sqrt = np.polyfit(np.sqrt(t_array), N_array, 1)
sqrt_fit = np.poly1d(coef_sqrt)
r_squared_sqrt = 1 - np.sum((N_array - sqrt_fit(np.sqrt(t_array)))**2) / np.sum((N_array - np.mean(N_array))**2)

print(f"\n📈 العلاقة الجذرية (N = a·√t + b):")
print(f"   a = {coef_sqrt[0]:.4f}")
print(f"   b = {coef_sqrt[1]:.2f}")
print(f"   R² = {r_squared_sqrt:.4f}")

# 3. علاقة لوغاريتمية: N = a*ln(t) + b
coef_log = np.polyfit(np.log(t_array), N_array, 1)
log_fit = np.poly1d(coef_log)
r_squared_log = 1 - np.sum((N_array - log_fit(np.log(t_array)))**2) / np.sum((N_array - np.mean(N_array))**2)

print(f"\n📈 العلاقة اللوغاريتمية (N = a·ln(t) + b):")
print(f"   a = {coef_log[0]:.4f}")
print(f"   b = {coef_log[1]:.2f}")
print(f"   R² = {r_squared_log:.4f}")

# 4. نسبة N/t
ratio = N_array / t_array
print(f"\n📊 إحصاءات نسبة N/t:")
print(f"   المتوسط = {np.mean(ratio):.4f}")
print(f"   الانحراف المعياري = {np.std(ratio):.4f}")
print(f"   المدى = [{np.min(ratio):.4f}, {np.max(ratio):.4f}]")

# 5. العلاقة مع العمق
print(f"\n💎 العلاقة بين أفضل N وعمق القاع:")
correlation = np.corrcoef(N_array, depth_array)[0, 1]
print(f"   معامل الارتباط = {correlation:.4f}")


# ============================================================================
# الجزء السادس: تنبؤات للمستقبل
# ============================================================================

print("\n" + "=" * 80)
print("🔮 تنبؤات للمستقبل (بناءً على النماذج الحالية)")
print("=" * 80)

# أصفار مستقبلية معروفة (قيم تقريبية)
future_zeros = {
    'العاشر': 49.773832,
    'العشرون': 77.144841,
    'الخمسون': 110.9387,
    'المائة': 236.524
}

print("\nتنبؤ بأفضل N لأصفار مستقبلية:")
print("-" * 60)
print(f"{'الصفر':^10} | {'t₀':^10} | {'خطي (N=a·t+b)':^15} | {'جذري (N=a·√t+b)':^15}")
print("-" * 60)

for name, t_pred in future_zeros.items():
    N_linear = linear_fit(t_pred)
    N_sqrt = sqrt_fit(np.sqrt(t_pred))
    print(f"{name:^10} | {t_pred:^10.1f} | {N_linear:^15.1f} | {N_sqrt:^15.1f}")


# ============================================================================
# الجزء السابع: حفظ النتائج إلى ملف
# ============================================================================

print("\n💾 جاري حفظ النتائج إلى ملف...")

with open('zeta_resonant_N_results.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("نتائج مسح القيم الرنانة (Resonant N) لأصفار دالة زيتا لريمان\n")
    f.write(f"تاريخ التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("المؤلف: باسل يحيى عبدالله\n")
    f.write("=" * 80 + "\n\n")
    
    for zero_key, zero_info in ZETA_ZEROS.items():
        f.write(f"\n{zero_info['name']} (t = {zero_info['t']:.6f})\n")
        f.write("-" * 50 + "\n")
        results = all_results[zero_key]
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        f.write("N\tالعمق\tmin |S|/√N\tt_min\n")
        for N, depth, min_val, t_min in sorted_results[:20]:
            f.write(f"{N}\t{depth:.4f}\t{min_val:.6f}\t{t_min:.6f}\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("ملخص أفضل N لكل صفر\n")
    f.write("=" * 80 + "\n")
    for zero_key in ZETA_ZEROS.keys():
        best = best_N_summary[zero_key]
        f.write(f"{ZETA_ZEROS[zero_key]['name']}: N = {best['N']}, عمق = {best['depth']:.2f}, انحراف = {best['deviation']:.6f}\n")

print("✅ تم حفظ النتائج في 'zeta_resonant_N_results.txt'")

print("\n" + "=" * 80)
print("🏁 انتهى المسح بنجاح")
print("=" * 80)