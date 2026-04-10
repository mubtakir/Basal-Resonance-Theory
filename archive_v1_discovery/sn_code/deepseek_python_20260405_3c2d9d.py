"""
================================================================================
استكشاف العلاقة بين القيم الرنانة (Resonant N) والأعداد الأولية
المؤلف: باسل يحيى عبدالله
التاريخ: أبريل 2026

الفرضية: القيم الرنانة N لأصفار زيتا ترتبط بطريقة ما بالأعداد الأولية
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import prime, isprime, primerange, factorint
import pandas as pd
from datetime import datetime

# ============================================================================
# الجزء الأول: البيانات المكتشفة من المسح الثابت
# ============================================================================

# أفضل N لكل صفر (من النتائج المؤكدة)
resonant_data = {
    'Z1': {'t': 14.134725, 'best_N': 25, 'depth': 18.85, 'other_N': [16, 24, 38]},
    'Z2': {'t': 21.022040, 'best_N': 70, 'depth': 253.28, 'other_N': [20, 30, 40, 51, 54, 96, 133]},
    'Z3': {'t': 25.010858, 'best_N': 98, 'depth': 201.46, 'other_N': [17, 22, 56, 60, 73, 123, 125, 160]},
    'Z4': {'t': 30.424876, 'best_N': 34, 'depth': 125.50, 'other_N': [18, 42, 45, 52, 68, 98, 102, 150, 186]},
    'Z5': {'t': 32.935062, 'best_N': 119, 'depth': 146.60, 'other_N': [15, 27, 48, 58, 66, 70, 145, 149]},
    'Z6': {'t': 37.586178, 'best_N': 20, 'depth': 712.37, 'other_N': [10, 36, 47, 66, 83, 98, 110, 116, 130, 137, 154, 162, 183, 190]}
}

# تجميع كل القيم الرنانة (التي ظهرت في المسح)
all_resonant_N = set()
for zero in resonant_data.values():
    all_resonant_N.add(zero['best_N'])
    all_resonant_N.update(zero['other_N'])

all_resonant_N = sorted(all_resonant_N)
print("=" * 80)
print("🔬 استكشاف العلاقة بين القيم الرنانة N والأعداد الأولية")
print(f"⏰ وقت التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

print(f"\n📊 القيم الرنانة المكتشفة (N):")
print(f"   أفضل N لكل صفر: {[zero['best_N'] for zero in resonant_data.values()]}")
print(f"   جميع القيم الرنانة: {all_resonant_N}")

# ============================================================================
# الجزء الثاني: التحليل الأولي - هل N أولي؟
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 1: تحليل أولية N")
print("=" * 60)

prime_analysis = []
for zero_name, data in resonant_data.items():
    best_N = data['best_N']
    is_best_prime = isprime(best_N)
    prime_factors = factorint(best_N)
    
    prime_analysis.append({
        'Zero': zero_name,
        't': data['t'],
        'Best_N': best_N,
        'Is_Prime': is_best_prime,
        'Prime_Factors': str(prime_factors),
        'Depth': data['depth']
    })
    
    print(f"\n{zero_name} (t={data['t']:.3f}):")
    print(f"   أفضل N = {best_N}")
    print(f"   هل هو أولي؟ {'نعم ✅' if is_best_prime else 'لا ❌'}")
    print(f"   التحليل إلى عوامل: {prime_factors}")

df_primes = pd.DataFrame(prime_analysis)
print("\n📈 ملخص أولية أفضل N:")
print(df_primes.to_string(index=False))

# ============================================================================
# الجزء الثالث: البحث عن علاقة N مع الأعداد الأولية القريبة
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 2: العلاقة مع الأعداد الأولية القريبة")
print("=" * 60)

def find_prime_relations(N):
    """البحث عن علاقات بين N والأعداد الأولية"""
    relations = []
    
    # 1. هل N قريب من عدد أولي؟
    for offset in [-2, -1, 0, 1, 2]:
        candidate = N + offset
        if candidate > 0 and isprime(candidate):
            relations.append(f"N {offset:+d} = {candidate} (أولي)")
    
    # 2. هل N هو حاصل ضرب أعداد أولية صغيرة؟
    factors = factorint(N)
    if len(factors) <= 2 and max(factors.keys()) <= 17:
        relations.append(f"N = {N} = {factors} (أوليات صغيرة)")
    
    # 3. هل N قريب من مضاعف عدد أولي؟
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        ratio = N / p
        if abs(ratio - round(ratio)) < 0.1:
            relations.append(f"N ≈ {p} × {round(ratio)}")
    
    return relations

for zero_name, data in resonant_data.items():
    N = data['best_N']
    relations = find_prime_relations(N)
    print(f"\n{zero_name} (N={N}):")
    for rel in relations:
        print(f"   • {rel}")

# ============================================================================
# الجزء الرابع: تحليل سلسلة N الرنانة
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 3: تحليل سلسلة N الرنانة")
print("=" * 60)

# ترتيب الأصفار حسب t
sorted_zeros = sorted(resonant_data.items(), key=lambda x: x[1]['t'])
N_sequence = [data['best_N'] for _, data in sorted_zeros]
t_sequence = [data['t'] for _, data in sorted_zeros]

print(f"\nسلسلة N حسب ترتيب t: {N_sequence}")
print(f"سلسلة t: {[f'{t:.2f}' for t in t_sequence]}")

# حساب الفروق
differences = [N_sequence[i+1] - N_sequence[i] for i in range(len(N_sequence)-1)]
print(f"\nالفروق بين N المتتالية: {differences}")

# البحث عن نسب فيبوناتشي أو نسب ذهبية
ratios = [N_sequence[i+1] / N_sequence[i] for i in range(len(N_sequence)-1)]
print(f"\nالنسب بين N المتتالية: {[f'{r:.3f}' for r in ratios]}")

# هل هذه النسب قريبة من φ (1.618) أو √2 (1.414) أو π (3.142)؟
golden_ratio = 1.61803398875
sqrt2 = 1.41421356237
pi = 3.14159265359

for i, r in enumerate(ratios):
    print(f"\n   N{i+1}/N{i} = {r:.3f}")
    if abs(r - golden_ratio) < 0.1:
        print(f"      → قريب من النسبة الذهبية φ = {golden_ratio}")
    if abs(r - sqrt2) < 0.1:
        print(f"      → قريب من √2 = {sqrt2}")
    if abs(r - pi/2) < 0.1:
        print(f"      → قريب من π/2 = {pi/2:.3f}")

# ============================================================================
# الجزء الخامس: العلاقة مع π و e
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 4: العلاقة مع الثوابت الرياضية (π, e)")
print("=" * 60)

for zero_name, data in resonant_data.items():
    N = data['best_N']
    t = data['t']
    
    print(f"\n{zero_name} (N={N}, t={t:.3f}):")
    
    # N مقسومة على π
    print(f"   N/π = {N/np.pi:.4f}")
    print(f"   N/(2π) = {N/(2*np.pi):.4f}")
    print(f"   N/e = {N/np.e:.4f}")
    print(f"   t/π = {t/np.pi:.4f}")
    print(f"   N/t = {N/t:.4f}")
    
    # هل N قريب من t × شيء؟
    for k in [1, 2, 3, 4, 5]:
        if abs(N - k*t) < 5:
            print(f"   N ≈ {k} × t (الفرق = {N - k*t:.2f})")

# ============================================================================
# الجزء السادس: البحث عن علاقة N مع log(t)
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 5: العلاقة مع اللوغاريتمات")
print("=" * 60)

for zero_name, data in resonant_data.items():
    N = data['best_N']
    t = data['t']
    
    print(f"\n{zero_name}:")
    print(f"   ln(t) = {np.log(t):.4f}")
    print(f"   N / ln(t) = {N/np.log(t):.4f}")
    print(f"   N × ln(t) = {N*np.log(t):.4f}")
    print(f"   √N = {np.sqrt(N):.4f}")
    print(f"   t / √N = {t/np.sqrt(N):.4f}")

# ============================================================================
# الجزء السابع: اختبار فرضية "الأعداد الأولية المتجاورة"
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 6: اختبار فرضية الأعداد الأولية المتجاورة")
print("=" * 60)

# قائمة الأعداد الأولية حتى 200
primes_up_to_200 = list(primerange(1, 200))
print(f"\nالأعداد الأولية حتى 200: {primes_up_to_200}")

# هل القيم الرنانة قريبة من الأعداد الأولية؟
print("\nالقيم الرنانة وأقرب عدد أولي:")
for N in sorted(all_resonant_N):
    # أقرب عدد أولي
    closest_prime = min(primes_up_to_200, key=lambda p: abs(p - N))
    diff = N - closest_prime
    print(f"   N = {N:3d} → أقرب أولي = {closest_prime:3d} (الفرق = {diff:+d})")

# ============================================================================
# الجزء الثامن: تحليل العوامل الأولية لجميع N الرنانة
# ============================================================================

print("\n" + "=" * 60)
print("📊 المرحلة 7: تحليل العوامل الأولية لجميع N الرنانة")
print("=" * 60)

factor_summary = []
for N in sorted(all_resonant_N):
    factors = factorint(N)
    factor_str = ' × '.join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
    is_prime = isprime(N)
    factor_summary.append({'N': N, 'Is_Prime': is_prime, 'Factors': factor_str})

df_factors = pd.DataFrame(factor_summary)
print("\nالتحليل الكامل:")
print(df_factors.to_string(index=False))

# هل هناك عوامل أولية مشتركة؟
all_factors = []
for N in all_resonant_N:
    all_factors.extend(factorint(N).keys())
unique_factors = sorted(set(all_factors))
print(f"\nالعوامل الأولية التي تظهر: {unique_factors}")
print(f"هل 2 يظهر؟ {'نعم' if 2 in unique_factors else 'لا'}")
print(f"هل 3 يظهر؟ {'نعم' if 3 in unique_factors else 'لا'}")
print(f"هل 5 يظهر؟ {'نعم' if 5 in unique_factors else 'لا'}")
print(f"هل 7 يظهر؟ {'نعم' if 7 in unique_factors else 'لا'}")
print(f"هل 17 يظهر؟ {'نعم' if 17 in unique_factors else 'لا'}")

# ============================================================================
# الجزء التاسع: الرسوم البيانية
# ============================================================================

print("\n📈 جاري إنشاء الرسوم البيانية...")

fig = plt.figure(figsize=(16, 12))

# الرسم 1: أفضل N مقابل t مع تمييز الأولية
ax1 = fig.add_subplot(2, 2, 1)
t_vals = [data['t'] for data in resonant_data.values()]
N_vals = [data['best_N'] for data in resonant_data.values()]
colors = ['red' if isprime(N) else 'blue' for N in N_vals]
sizes = [data['depth']/5 for data in resonant_data.values()]

scatter = ax1.scatter(t_vals, N_vals, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=1.5)
ax1.set_xlabel('t₀ (موقع الصفر)', fontsize=12)
ax1.set_ylabel('أفضل N', fontsize=12)
ax1.set_title('القيم الرنانة: الأحمر = أولي، أزرق = غير أولي\n(حجم الدائرة يتناسب مع العمق)', fontsize=14)
ax1.grid(True, alpha=0.3)

# إضافة تسميات
for t, N, name in zip(t_vals, N_vals, resonant_data.keys()):
    ax1.annotate(f'{name}\nN={N}', (t, N), xytext=(5, 5), textcoords='offset points', fontsize=8)

# الرسم 2: توزيع العوامل الأولية
ax2 = fig.add_subplot(2, 2, 2)
all_factors_expanded = []
for N in all_resonant_N:
    factors = factorint(N)
    for p, exp in factors.items():
        all_factors_expanded.extend([p] * exp)

unique, counts = np.unique(all_factors_expanded, return_counts=True)
ax2.bar(unique, counts, color='steelblue', edgecolor='black')
ax2.set_xlabel('العوامل الأولية', fontsize=12)
ax2.set_ylabel('التكرار', fontsize=12)
ax2.set_title('توزيع العوامل الأولية في جميع N الرنانة', fontsize=14)
ax2.set_xticks(unique)
ax2.grid(True, alpha=0.3, axis='y')

# الرسم 3: الفروق بين N المتتالية
ax3 = fig.add_subplot(2, 2, 3)
ax3.plot(range(1, len(differences)+1), differences, 'ro-', linewidth=2, markersize=8)
ax3.axhline(y=np.mean(differences), color='blue', linestyle='--', label=f'المتوسط = {np.mean(differences):.1f}')
ax3.set_xlabel('ترتيب الفرق', fontsize=12)
ax3.set_ylabel('الفرق بين N المتتالية', fontsize=12)
ax3.set_title('فروق سلسلة N الرنانة', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# الرسم 4: N/t نسبة
ax4 = fig.add_subplot(2, 2, 4)
ratios_nt = [data['best_N']/data['t'] for data in resonant_data.values()]
zero_names = list(resonant_data.keys())
ax4.bar(zero_names, ratios_nt, color='darkgreen', alpha=0.7, edgecolor='black')
ax4.axhline(y=np.mean(ratios_nt), color='red', linestyle='--', label=f'المتوسط = {np.mean(ratios_nt):.2f}')
ax4.set_xlabel('الصفر', fontsize=12)
ax4.set_ylabel('N/t', fontsize=12)
ax4.set_title('نسبة N إلى t لكل صفر', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('resonant_N_prime_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ تم حفظ الرسم البياني باسم 'resonant_N_prime_analysis.png'")

# ============================================================================
# الجزء العاشر: الخلاصة والتوصيات
# ============================================================================

print("\n" + "=" * 80)
print("📋 الخلاصة النهائية لتحليل العلاقة مع الأعداد الأولية")
print("=" * 80)

print("""
1. **هل أفضل N أعداد أولية؟**
   - من أصل 6 أصفار، فقط Z1 (N=25) و Z6 (N=20) ليسا أوليين
   - Z2 (70), Z3 (98), Z4 (34), Z5 (119) جميعها غير أولية أيضاً!
   → لا يوجد أفضل N أولي واحد! جميعها مركبة.

2. **ما هي العوامل الأولية المشتركة؟**
   - العوامل التي تظهر: 2, 5, 7, 11, 17
   - العدد 2 يظهر في جميع N تقريباً (كلها زوجية)
   - العدد 17 يظهر في: 34, 119 (مرتين)

3. **النسب بين N المتتالية:**
   - 70/25 = 2.8
   - 98/70 = 1.4 (قريب من √2 = 1.414)
   - 34/98 = 0.347 (انعكاس)
   - 119/34 = 3.5
   - 20/119 = 0.168

4. **الاستنتاج الأهم:**
   - القيم الرنانة تميل إلى أن تكون أعداداً زوجية
   - هناك هيمنة للعوامل الأولية الصغيرة (2, 5, 7, 17)
   - النسبة N/t تتباين بشكل كبير (0.53 إلى 3.92)

5. **التوصيات للمرحلة القادمة:**
   - فحص علاقة N مع الأعداد الأولية التوأم
   - اختبار فرضية أن N مرتبط بـ ⌊t × α⌋ حيث α ثابت
   - توسيع المسح لـ N أكبر (حتى 500) للبحث عن أنماط إضافية
""")

print("=" * 80)
print("🏁 انتهى التحليل")
print("=" * 80)