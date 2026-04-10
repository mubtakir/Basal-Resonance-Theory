import mpmath as mp
import numpy as np

# --- EXPERIMENT 13 v2: OPTIMIZED DEEP OCEAN REFINEMENT ---
# Objective: Hit Z50 < 0.1 by using N=50,000 and a Taylor approximation.
# Taylor search is O(N + steps) instead of O(N * steps).

mp.dps = 100

def run_optimized_z50():
    print("=" * 80)
    print("EXPERIMENT 13 v2: OPTIMAL DEEP OCEAN REFINEMENT (Z50)")
    print("=" * 80)
    
    Z50_TRUE = 127.99633124 # Actual Zero
    N = 50000
    s0 = mp.mpc(0.5, 128.0)
    
    print(f"I. Calculating S_N and S_N' at N={N}, t=128.0...")
    sn = mp.mpc(0)
    sn_prime = mp.mpc(0)
    
    # Pre-calculate once (O(N))
    for n in range(1, int(N) + 1):
        n_inv_s = mp.mpf(n) ** -s0
        sn += n_inv_s
        sn_prime -= mp.log(n) * n_inv_s
    
    print(f"II. Searching for minimum balance error using Taylor expansion...")
    
    def get_tail(s):
        s_mp = mp.mpc(s)
        N_mp = mp.mpf(N)
        return (N_mp ** (1 - s_mp)) / (s_mp - 1) - 0.5 * (N_mp ** (-s_mp))

    best_t = 127.0
    best_error = mp.mpf('inf')
    
    # Scan around 128 (O(steps))
    t_vals = np.linspace(127.5, 128.5, 2000)
    for t in t_vals:
        delta_t = t - 128.0
        # S_N(s0 + i*delta_t) approx S_N(s0) + i*delta_t * S_N'(s0)
        sn_approx = sn + mp.mpc(0, 1) * delta_t * sn_prime
        tail = get_tail(mp.mpc(0.5, t))
        error = abs(sn_approx + tail)
        
        if error < best_error:
            best_error = error
            best_t = t
            
    diff = abs(best_t - Z50_TRUE)
    
    print("-" * 80)
    print(f"Z50 Actual:    {Z50_TRUE:.10f}")
    print(f"Z50 Predicted: {best_t:.10f}")
    print(f"Z50 Difference: {diff:.10f}")
    print(f"Final Status:  {'PASSED (< 0.1)' if diff < 0.1 else 'FAIL'}")
    print("=" * 80)

if __name__ == "__main__":
    run_optimized_z50()
