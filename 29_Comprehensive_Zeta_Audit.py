import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time
import sys
from datetime import datetime

# ============================================================================
# إعدادات العرض والتهيئة
# ============================================================================

# استخدام خط يدعم العربية والإنجليزية
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.facecolor'] = 'white'

# تخزين مؤقت عالمي لقيم موبيوس
_MU_CACHE = {}

# ============================================================================
# دوال دالة موبيوس
# ============================================================================

def mobius_single(n):
    """
    حساب دالة موبيوس μ(n) لعدد واحد
    ترجع: 0 إذا كان n له عامل مربع
           1 إذا كان عدد العوامل الأولية زوجي
          -1 إذا كان عدد العوامل الأولية فردي
    """
    if n == 1:
        return 1
    
    p = 2
    temp = n
    factors_count = 0
    
    while p * p <= temp:
        if temp % p == 0:
            factors_count += 1
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0
        p += 1
    
    if temp > 1:
        factors_count += 1
    
    return (-1) ** factors_count

def precompute_mobius(N, verbose=True):
    """
    حساب قيم موبيوس مسبقاً لجميع الأعداد حتى N باستخدام غربال فعال
    """
    global _MU_CACHE
    
    if N in _MU_CACHE:
        return _MU_CACHE[N]
    
    if verbose:
        print(f"  [*] جاري حساب قيم موبيوس لـ N={N:,}...", end=" ", flush=True)
        start_time = time.time()
    
    mu = np.ones(N + 1, dtype=int)
    is_square_free = np.ones(N + 1, dtype=bool)
    
    # غربال لإيجاد الأعداد الأولية وحساب موبيوس
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0:2] = False
    
    for i in range(2, int(np.sqrt(N)) + 1):
        if is_prime[i]:
            for j in range(i * i, N + 1, i):
                is_prime[j] = False
    
    primes = np.where(is_prime)[0]
    
    for p in primes:
        p2 = p * p
        if p2 <= N:
            for j in range(p2, N + 1, p2):
                is_square_free[j] = False
        
        for j in range(p, N + 1, p):
            mu[j] *= -1
    
    for i in range(2, N + 1):
        if not is_square_free[i]:
            mu[i] = 0
    
    _MU_CACHE[N] = mu
    
    if verbose:
        elapsed = time.time() - start_time
        print(f"تم ({elapsed:.2f} ثانية)")
    
    return mu

def get_mobius_array(N, use_cache=True):
    """استرجاع مصفوفة قيم موبيوس (بدون العنصر 0)"""
    if use_cache:
        if N not in _MU_CACHE:
            precompute_mobius(N)
        # إرجاع نسخة من العناصر من 1 إلى N فقط
        return _MU_CACHE[N][1:N+1].copy()
    else:
        return np.array([mobius_single(i) for i in range(1, N + 1)])

# ============================================================================
# دوال دالة زيتا ومقلوبها
# ============================================================================

def compute_zeta(a, b, N=1000):
    """
    حساب دالة زيتا-ريمان ζ(s) = Σ n^{-s}
    """
    n = np.arange(1, N + 1)
    s = a + 1j * b
    terms = np.exp(-s * np.log(n))
    return np.sum(terms)

def compute_inverse_zeta(a, b, N=1000, use_cache=True):
    """
    حساب مقلوب دالة زيتا-ريمان 1/ζ(s) = Σ μ(n)·n^{-s}
    """
    n = np.arange(1, N + 1)
    s = a + 1j * b
    
    mu = get_mobius_array(N, use_cache)
    terms = mu * np.exp(-s * np.log(n))
    return np.sum(terms)

def main():
    """الدالة الرئيسية لتشغيل التحليل الكامل"""
    print("\n" + "█" * 80)
    print("█" + "      تحليل شامل لمقلوب دالة زيتا-ريمان وسلوك التقارب".center(78) + "█")
    print("█" + "      Comprehensive Riemann Zeta Function Analysis".center(78) + "█")
    print("█" * 80)
    
    start_total = time.time()
    
    # 1. اختبار القيم الأساسية
    a, b = 2.0, 0.0
    zeta = compute_zeta(a, b, N=10000)
    print(f"\nζ(2) = {zeta.real:.12f} (المتوقع: 1.644934066848)")
    
    # 2. تحليل الخط الحرج
    b_max = 40
    num_points = 500
    b_values = np.linspace(0, b_max, num_points)
    a = 0.5
    N_terms = 2000
    
    precompute_mobius(N_terms)
    
    inv_magnitudes = []
    zeta_magnitudes = []
    
    for b in b_values:
        inv_result = compute_inverse_zeta(a, b, N_terms)
        zeta_result = compute_zeta(a, b, N_terms)
        inv_magnitudes.append(np.abs(inv_result))
        zeta_magnitudes.append(np.abs(zeta_result))
    
    # 3. عرض النتائج
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    ax1.plot(b_values, inv_magnitudes, 'r-', label='|1/zeta(0.5+it)|')
    ax1.set_title('Inverse Zeta Resonance on Critical Line')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(b_values, zeta_magnitudes, 'b-', label='|zeta(0.5+it)|')
    ax2.set_title('Zeta Magnitude (Partial Sum N=2000)')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('29_Comprehensive_Zeta_Audit.png')
    print(f"\n[✓] تم حفظ النتائج في 29_Comprehensive_Zeta_Audit.png")
    
    total_elapsed = time.time() - start_total
    print(f"[✓] اكتمل التحليل في {total_elapsed:.2f} ثانية")

if __name__ == "__main__":
    main()
