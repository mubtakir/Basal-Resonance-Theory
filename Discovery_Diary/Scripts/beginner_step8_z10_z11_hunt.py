import numpy as np
import mpmath as mp

# --- المسبار الثامن: صيد Z10 الجبار بدقة فائقة ---
# في هذه النسخة المحدثة، سنستخدم كل ما تعلمناه للوصول لأدق تنبؤ ممكن للصفر العاشر Z10.

def hunt_z10_high_precision(t_guess, radius, N):
    print(f"الصيد جارٍ لـ Z10 حول {t_guess} باستخدام رنين عميق N={N}...")
    
    t_points = np.linspace(t_guess - radius, t_guess + radius, 1000)
    errors = []
    
    # 1. إعدادات المختبر (الخط الحرج)
    sigma = 0.5
    
    for t in t_points:
        s = mp.mpc(sigma, t)
        
        # مجموع الأسهم (Partial Sum)
        n = np.arange(1, N + 1)
        # Using mpmath for higher precision in the sum
        S = mp.mpc(0)
        for val in range(1, N + 1):
            S += mp.mpf(val) ** -s
            
        # التكامل الهندسي (The Tail)
        tail = (mp.mpf(N) ** (1 - s)) / (s - 1) - 0.5 * (mp.mpf(N) ** (-s))
        
        # ميزان القوى (The Balance)
        error = abs(S + tail)
        errors.append(float(error))
        
    # البحث عن أدنى نقطة (The Valley)
    best_idx = np.argmin(errors)
    found_t = t_points[best_idx]
    min_err = errors[best_idx]
    
    print("-" * 50)
    print(f"Z10 الحقيقي: 49.773832...")
    print(f"قنص المكتشف: {found_t:.6f}")
    print(f"الفارق (الدقة): {min_err:.10f}")
    
    if min_err < 0.0001:
        print("\nتهانينا! لقد حققنا 'الرنين الكامل'. الصفر الآن في قبضة العلم!")

if __name__ == "__main__":
    # نبحث عن Z10 حول 49.77
    hunt_z10_high_precision(t_guess=49.77, radius=0.1, N=5000)
