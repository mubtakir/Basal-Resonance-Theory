import numpy as np
from sympy import factorint

def get_depth_for_N(t_zero, N):
    theo_const = 1.0 / np.sqrt(0.25 + t_zero**2)
    
    # Calculate error at the exact zero
    n = np.arange(1, N + 1)
    S_zero = np.sum(n**(-0.5 + 1j * t_zero))
    err_zero = np.abs(np.abs(S_zero)/np.sqrt(N) - theo_const)
    
    # Calculate error at a small neighborhood (background)
    # We take 2 points slightly away
    background_errors = []
    offsets = [-0.1, 0.1]
    for off in offsets:
        t_off = t_zero + off
        S_off = np.sum(n**(-0.5 + 1j * t_off))
        err_off = np.abs(np.abs(S_off)/np.sqrt(N) - (1.0 / np.sqrt(0.25 + t_off**2)))
        background_errors.append(err_off)
        
    mean_background = np.mean(background_errors)
    depth = mean_background / (err_zero + 1e-15)
    return depth, err_zero

if __name__ == "__main__":
    zeta_zeros = [14.1347251417, 21.0220396388, 25.0108575801, 30.4248761259]
    allowed_primes = {2, 5, 7, 17}
    
    print(f"{'Zero':<10} | {'Best N':<6} | {'Depth':<8} | {'Factors':<15} | {'Match'}")
    print("-" * 65)
    
    for t in zeta_zeros:
        best_depth = -1
        best_N = -1
        
        # Testing N in a range where resonance is expected to show
        for N in range(10, 500):
            d, _ = get_depth_for_N(t, N)
            if d > best_depth:
                best_depth = d
                best_N = N
        
        factors = factorint(best_N)
        f_set = set(factors.keys())
        match = "YES" if f_set.issubset(allowed_primes) else "NO"
        
        print(f"{t:<10.2f} | {best_N:<6} | {best_depth:<8.2f} | {str(factors):<15} | {match}")
