import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import warnings
warnings.filterwarnings('ignore')

def partial_sum_series(t, N_max):
    """حساب سلسلة S(N) = ∑ n^(i t)"""
    S_vals = np.zeros(N_max, dtype=complex)
    S = 0 + 0j
    for n in range(1, N_max + 1):
        S += n ** (1j * t)
        S_vals[n-1] = S
    return S_vals

def running_average(x, window):
    """المتوسط المتحرك"""
    return np.convolve(x, np.ones(window)/window, mode='valid')

def growth_rate_analysis(abs_S):
    """تحليل معدل النمو: هل هو ~ √N أم أبطأ؟"""
    N = len(abs_S)
    expected_sqrt = np.sqrt(np.arange(1, N+1))
    
    # نسبة النمو الفعلي إلى √N
    ratio = abs_S / expected_sqrt
    
    # الانحدار الخطي على مقياس لوغاريتمي
    log_N = np.log(np.arange(1, N+1))
    log_S = np.log(abs_S + 1e-10)
    
    # تجاهل أول 10% لأن التأثيرات الأولية كبيرة
    start_idx = int(N * 0.1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_N[start_idx:], log_S[start_idx:])
    
    return {
        'ratio_mean': np.mean(ratio[start_idx:]),
        'ratio_std': np.std(ratio[start_idx:]),
        'growth_exponent': slope,
        'correlation': r_value**2
    }

def stft_analysis(S_vals, t_label):
    """تحليل فورييه قصير المدى لكشف الترددات المهيمنة"""
    real_part = np.real(S_vals)
    f, t, Zxx = signal.stft(real_part, fs=1.0, nperseg=256, noverlap=128)
    
    # قوة الإشارة عبر الترددات
    power = np.mean(np.abs(Zxx)**2, axis=1)
    
    # أعلى 3 ترددات
    dominant_freqs = f[np.argsort(power)[-5:]]
    
    return f, power, dominant_freqs

# إعداد الاختبارات
N_max = 5000  # نزيد العدد للحصول على نتائج أفضل
t_values = {
    "t_random_1": 10.0,
    "t_random_2": 5.7,
    "t_random_3": 3.14,
    "t_near_zero": 14.13,
    "t_exact_zero": 14.134725141734693790,
    "t_second_zero": 21.022039638771554  # ثاني صفر غير بديهي
}

print("="*80)
print("تحليل متقدم لسلوك ∑ n^(it)")
print("="*80)

results = {}

for label, t in t_values.items():
    print(f"\n--- {label} (t = {t:.10f}) ---")
    
    # حساب S(N)
    S_vals = partial_sum_series(t, N_max)
    abs_S = np.abs(S_vals)
    real_S = np.real(S_vals)
    imag_S = np.imag(S_vals)
    
    # 1. تحليل معدل النمو
    growth = growth_rate_analysis(abs_S)
    print(f"معدل النمو: N^{growth['growth_exponent']:.3f}")
    print(f"نسبة |S|/√N: متوسط = {growth['ratio_mean']:.3f} ± {growth['ratio_std']:.3f}")
    
    # 2. القيم النهائية والسلوك الطويل المدى
    last_100_mean = np.mean(abs_S[-100:])
    last_100_std = np.std(abs_S[-100:])
    print(f"آخر 100 قيمة: |S| = {last_100_mean:.2f} ± {last_100_std:.2f}")
    
    # 3. المتوسطات المتداولة (هل هناك تقارب؟)
    ma_window = 500
    real_ma = running_average(real_S, ma_window)
    imag_ma = running_average(imag_S, ma_window)
    abs_ma = running_average(abs_S, ma_window)
    
    print(f"آخر متوسط متحرك (نافذة {ma_window}):")
    print(f"  الجزء الحقيقي = {real_ma[-1]:.4f}")
    print(f"  الجزء التخيلي = {imag_ma[-1]:.4f}")
    print(f"  المقدار = {abs_ma[-1]:.4f}")
    
    # تخزين النتائج للرسم
    results[label] = {
        'S_vals': S_vals,
        'abs_S': abs_S,
        'real_ma': real_ma,
        'imag_ma': imag_ma,
        'growth': growth
    }
    
    # 4. اختبار إحصائي: هل التوزيع طبيعي؟
    _, p_value = stats.normaltest(real_S)
    print(f"اختبار التوزيع الطبيعي للجزء الحقيقي: p-value = {p_value:.4f}")

# رسم مقارن شامل
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. مقارنة |S(N)| لكل الحالات
ax1 = axes[0, 0]
for label, data in results.items():
    ax1.plot(data['abs_S'][:1000], label=label, alpha=0.7)
ax1.set_xlabel('N')
ax1.set_ylabel('|S(N)|')
ax1.set_title('مقارنة |S(N)| لأول 1000 حد')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# 2. المتوسطات المتحركة (الجزء الحقيقي)
ax2 = axes[0, 1]
for label, data in results.items():
    ax2.plot(data['real_ma'], label=label, alpha=0.7)
ax2.set_xlabel('N (بعد المتوسط المتحرك)')
ax2.set_ylabel('المتوسط المتحرك للجزء الحقيقي')
ax2.set_title('المتوسطات المتحركة (نافذة 500)')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)

# 3. توزيع قيم S(N) للصفر المضبوط
ax3 = axes[1, 0]
exact_data = results['t_exact_zero']['S_vals']
ax3.scatter(np.real(exact_data[::50]), np.imag(exact_data[::50]), 
            c=np.arange(0, len(exact_data[::50])), cmap='viridis', s=5, alpha=0.6)
ax3.set_xlabel('Real part')
ax3.set_ylabel('Imag part')
ax3.set_title('مسار S(N) في المستوى المركب (t = الصفر المضبوط)')
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax3.axvline(x=0, color='k', linestyle='--', alpha=0.3)

# 4. أس النمو لكل الحالات
ax4 = axes[1, 1]
labels = list(results.keys())
growth_exps = [results[l]['growth']['growth_exponent'] for l in labels]
ratios = [results[l]['growth']['ratio_mean'] for l in labels]

x_pos = np.arange(len(labels))
width = 0.35

bars1 = ax4.bar(x_pos - width/2, growth_exps, width, label='أس النمو', color='skyblue')
ax4.set_ylabel('أس النمو (حيث |S| ~ N^α)', color='skyblue')
ax4.tick_params(axis='y', labelcolor='skyblue')

ax4_twin = ax4.twinx()
bars2 = ax4_twin.bar(x_pos + width/2, ratios, width, label='|S|/√N', color='lightcoral')
ax4_twin.set_ylabel('متوسط |S|/√N', color='lightcoral')
ax4_twin.tick_params(axis='y', labelcolor='lightcoral')

ax4.set_xticks(x_pos)
ax4.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
ax4.set_title('مقارنة معاملات النمو')
ax4.legend([bars1, bars2], ['أس النمو', '|S|/√N'], loc='upper left')

plt.tight_layout()
plt.show()

# تحليل فورييه لأهم الحالات
fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
cases_for_fft = ['t_random_1', 't_near_zero', 't_exact_zero', 't_second_zero']

for idx, case in enumerate(cases_for_fft):
    ax = axes2[idx // 2, idx % 2]
    S_vals = results[case]['S_vals']
    
    # تحويل فورييه للجزء الحقيقي
    fft_vals = np.fft.fft(np.real(S_vals))
    freqs = np.fft.fftfreq(len(S_vals))
    
    # نأخذ نصف الترددات الموجبة فقط
    positive_freqs = freqs[:len(freqs)//2]
    power_spectrum = np.abs(fft_vals[:len(fft_vals)//2])**2
    
    ax.plot(positive_freqs[1:100], power_spectrum[1:100])  # نتجاهل التردد الصفري
    ax.set_xlabel('التردد')
    ax.set_ylabel('الطاقة')
    ax.set_title(f'طيف فورييه - {case}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# إحصاءات نهائية
print("\n" + "="*80)
print("الخلاصة والاستنتاجات")
print("="*80)

for label, data in results.items():
    growth = data['growth']
    print(f"\n{label}:")
    print(f"  • |S(N)| يتصرف مثل N^{growth['growth_exponent']:.3f}")
    print(f"  • النسبة إلى √N: {growth['ratio_mean']:.3f}")
    if 'zero' in label:
        print(f"  • ملاحظة: هذا تردد قريب/مساوٍ لصفر زيتا")