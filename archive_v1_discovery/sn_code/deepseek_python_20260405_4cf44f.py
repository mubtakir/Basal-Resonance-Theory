import numpy as np
import matplotlib.pyplot as plt

def chi_4(n):
    rem = n % 4
    if rem == 1: return 1
    if rem == 3: return -1
    return 0

def L_sum(t, N):
    """حساب المجموع الجزئي لدالة L"""
    n = np.arange(1, N + 1, dtype=np.float64)
    chi = np.array([chi_4(x) for x in n])
    terms = chi * (n ** (-0.5 + 1j * t))
    return np.sum(terms)

def compute_depth(t_zero, N, t_span=0.2, n_points=200):
    """حساب عمق القاع عند N معين"""
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    magnitudes = []
    
    for t in t_values:
        S = L_sum(t, N)
        magnitudes.append(np.abs(S) / np.sqrt(N))
    
    min_val = min(magnitudes)
    avg_val = np.mean(magnitudes)
    depth = avg_val / (min_val + 1e-12)
    return depth

# الأصفار المعروفة لدالة L(s, chi_4)
zeros = {
    "first": 6.020948904697828,
    "second": 10.24377030416614,
    "third": 12.988098012718422,
    "fourth": 16.342607104587222,
}

# نطاق البحث عن القيم السحرية لـ N
N_range = range(10, 201, 1)  # من 10 إلى 200 بخطوة 1
t_zero = zeros["first"]

print("🔍 جاري البحث عن القيم السحرية لـ N...")
print("=" * 60)

depths = []
resonant_Ns = []

for N in N_range:
    depth = compute_depth(t_zero, N, t_span=0.15, n_points=150)
    depths.append(depth)
    
    # كشف القمم: إذا كان العمق أكبر من ضعف متوسط الجيران
    if len(depths) > 5:
        if depth > 2.5 * np.mean(depths[-5:-1]):
            resonant_Ns.append((N, depth))
            print(f"🎯 N = {N:3d} | عمق القاع = {depth:.2f} ← رنين محتمل!")

# الرسم البياني
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(list(N_range), depths, 'b-', linewidth=1)
plt.scatter([n for n, _ in resonant_Ns], [d for _, d in resonant_Ns], 
            color='red', s=50, zorder=5, label='قمم الرنين')
plt.xlabel('N (عدد الحدود)')
plt.ylabel('عمق القاع')
plt.title(f'بحث عن القيم السحرية لـ N\nعند الصفر t₀ = {t_zero:.6f}')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
# تحليل العلاقة بين N الرنانة و t₀
if resonant_Ns:
    N_res = np.array([n for n, _ in resonant_Ns])
    depths_res = np.array([d for _, d in resonant_Ns])
    
    plt.bar(N_res, depths_res, width=0.8, color='darkred', alpha=0.7)
    plt.xlabel('N (القيم الرنانة)')
    plt.ylabel('عمق القاع')
    plt.title(f'القمم المكتشفة: {len(resonant_Ns)} رنيناً')
    plt.grid(True, alpha=0.3)
    
    # طباعة القيم الرنانة
    print("\n" + "=" * 60)
    print("📊 القيم الرنانة لـ N (مرتبة):")
    for n, d in sorted(resonant_Ns, key=lambda x: x[1], reverse=True):
        print(f"   N = {n:3d} → عمق = {d:.2f}")

plt.tight_layout()
plt.show()

# اختبار إضافي: هل تتنبأ N الرنانة بأصفار أخرى؟
print("\n" + "=" * 60)
print("🔬 اختبار التنبؤ: هل نفس N الرنانة تعطي قيعاناً عند أصفار أخرى؟")

test_N = [n for n, _ in resonant_Ns[:3]] if len(resonant_Ns) >= 3 else [50, 100, 150]
print(f"سنختبر N = {test_N} على الأصفار الأخرى...\n")

for zero_name, t_val in zeros.items():
    print(f"\n--- {zero_name} صفر عند t = {t_val:.6f} ---")
    for N in test_N:
        depth = compute_depth(t_val, N, t_span=0.2, n_points=150)
        print(f"   N = {N:3d} → عمق القاع = {depth:.2f}")