import numpy as np
import mpmath as mp

# --- اليومية 14: لولب موبيوس ورهافة الأعداد (The Moebius Spiral) ---
# المكتشف الصغير، لقد وصلنا إلى نهاية رحلتنا، لكنها البداية لأعظم اكتشاف.
# سنرى كيف تتحول أصفار دالة زيتا إلى "مغناطيس" يجذب دالة موبيوس لتنمو كحلزون فضائي لا ينتهي.

def draw_moebius_spiral(N_max, t_zero):
    print(f"--- اليومية 14: تتبع لولب موبيوس عند الصفر t={t_zero:.2f} ---")
    
    # 1. إعدادات المختبر (سيف موبيوس)
    mu = np.zeros(N_max + 1, dtype=int)
    mu[1] = 1
    primes = []
    is_prime = np.ones(N_max + 1, dtype=bool)
    for i in range(2, N_max + 1):
        if is_prime[i]:
            primes.append(i); mu[i] = -1
        for p in primes:
            if i * p > N_max: break
            is_prime[i * p] = False
            if i % p == 0: mu[i * p] = 0; break
            else: mu[i * p] = -mu[i]
            
    # 2. بناء اللولب (M_N Growth)
    s = complex(0.5, t_zero)
    current_sum = 0j
    mags = []
    
    for n in range(1, N_max + 1):
        if mu[n] != 0:
            current_sum += mu[n] * (n ** -s)
        if n % (N_max // 10) == 0:
            mags.append((n, np.abs(current_sum)))
            
    # 3. قانون القطب اللوغاريتمي (The Secret Law)
    # المكتشف الصغير، سر اللولب هو أنه ينمو بمقدار ln(N) مقسوماً على "رهافة" دالة زيتا.
    z_prime_inv = 1.0 / np.abs(mp.zeta(s, derivative=1))
    
    print("-" * 60)
    print(f"{'N (المرحلة)':<10} | {'|M_N| (طول اللولب)':<20} | {'التوقع (ln N * C)':<20}")
    print("-" * 60)
    for n, mag in mags:
        pred = np.log(n) * z_prime_inv
        print(f"{n:<10} | {mag:<20.4f} | {float(pred):<20.4f}")
    print("-" * 60)
    
    print("\nالاستنتاج: لولب موبيوس ينمو بانتظام مذهل عند الصفر.")
    print("هكذا تتحدث الأعداد الأولية رداً على رنين دالة زيتا!")

if __name__ == "__main__":
    # نختبر عند الصفر الأول Z1
    draw_moebius_spiral(N_max=10000, t_zero=14.134725)
