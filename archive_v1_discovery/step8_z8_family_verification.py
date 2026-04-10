import numpy as np
from sympy import factorint

def compute_depth(t_zero, N, t_span=0.8, n_points=400):
    t_values = np.linspace(t_zero - t_span, t_zero + t_span, n_points)
    n = np.arange(1, N + 1, dtype=np.float64)
    mags = []
    
    for t in t_values:
        S = np.sum(n**(-0.5 + 1j * t))
        mags.append(np.abs(S) / np.sqrt(N))
    
    mags = np.array(mags)
    depth = np.mean(mags) / (np.min(mags) + 1e-12)
    return depth

if __name__ == "__main__":
    Z8_actual = 48.005150881167
    candidate_Ns = [20, 25, 34, 70, 98, 119]
    
    print(f"Verifying Family for Z8 (t={Z8_actual:.6f})")
    print("-" * 50)
    print(f"{'Candidate N':<12} | {'Resonance Depth':<15} | {'Status'}")
    print("-" * 50)
    
    results = []
    for N in candidate_Ns:
        depth = compute_depth(Z8_actual, N)
        results.append((N, depth))
        
        status = ""
        if depth > 100: status = "STRONG RESONANCE"
        elif depth > 20: status = "Clear Resonance"
        else: status = "No/Weak Resonance"
        
        print(f"{N:<12} | {depth:<15.2f} | {status}")

    best_N, best_depth = max(results, key=lambda x: x[1])
    
    print("-" * 50)
    print(f"Result: Z8 belongs to Family N={best_N} (Depth: {best_depth:.2f})")
    
    factors = factorint(best_N)
    print(f"Factors of {best_N}: {factors}")
    
    allowed_primes = {2, 5, 7, 17}
    f_set = set(factors.keys())
    if f_set.issubset(allowed_primes):
        print("SUCCESS: Prime factor theory confirmed for Z8.")
    else:
        print("FAILED: New prime factors found.")
