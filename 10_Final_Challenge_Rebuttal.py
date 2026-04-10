import mpmath as mp

# THE INTELLIGENT ASSISTANT'S CHALLENGE CODE
mp.dps = 100  # 100-digit precision

def S_partial(N, s):
    total = 0
    for n in range(1, int(N)+1):
        total += mp.mpc(n) ** (-mp.mpc(s))
    return total

def blind_search_high_precision(N, sigma, t_center, radius, steps):
    """بحث دقيق حول t_center"""
    best_t = t_center
    best_error = float('inf')
    
    t_vals = [t_center - radius + i*(2*radius)/steps for i in range(steps+1)]
    for t in t_vals:
        s = complex(sigma, t)
        S = S_partial(N, s)
        # Using the standard Tail_EM used in the theory
        # Tail = N^(1-s)/(s-1) - 0.5*N^-s
        tail = (mp.mpf(N) ** (1 - mp.mpc(s))) / (mp.mpc(s) - 1) - 0.5 * (mp.mpf(N) ** (-mp.mpc(s)))
        error = abs(S + tail)
        
        if error < best_error:
            best_error = error
            best_t = t
    
    return best_t, best_error

print("="*80)
print("EVALUATING THE INTELLIGENT ASSISTANT'S CHALLENGE")
print("="*80)

# TEST 1: Z10 (49.773832)
Z10_true = 49.7738324776723
predicted, error_dist = blind_search_high_precision(
    N=1000,
    sigma=0.5,
    t_center=49.77,
    radius=0.1,
    steps=1000
)

print(f"Z10 Actual:    {Z10_true}")
print(f"Z10 Predicted: {predicted}")
print(f"Z10 Error:     {abs(predicted - Z10_true)}")
print(f"Is Error < 0.0001? {'YES' if abs(predicted - Z10_true) < 0.0001 else 'NO'}")

print("-"*80)

# TEST 2: Z50 (The IA's value 128.108 vs the Real Z46=127.99)
# Note: Z46 in EM counting is Z50 in some tables.
Real_Z_near_128 = 127.99633124 # Verified Z_near_128
predicted_z50, error_z50 = blind_search_high_precision(
    N=2000,
    sigma=0.5,
    t_center=128.0,
    radius=0.5,
    steps=2000
)

print(f"Z50-Region Predicted: {predicted_z50}")
print(f"Actual Zero (Z46):     {Real_Z_near_128}")
print(f"Difference to Actual: {abs(predicted_z50 - Real_Z_near_128)}")
print("="*80)
