import numpy as np

def high_sum(t, N):
    n = np.arange(1, N + 1, dtype=np.float64)
    S = np.sum(n**(-0.5 + 1j * t))
    return np.abs(S) / np.sqrt(N)

def analyze_high_peaks():
    # High-precision zeros
    # Z100 and Z1000 (standard values)
    high_zeros = {
        100: 236.524253597,
        1000: 1419.422485746
    }
    
    N = 10000 # Use higher N for more precision
    
    print(f"--- THE GEOMETRIC SUMMIT ANALYSIS (N={N}) ---")
    print(f"{'Zero ID':<10} | {'t Value':<15} | {'Hypotenuse Theo':<20} | {'Error (Reality - Law)'}")
    print("-" * 75)
    
    for zid, t in high_zeros.items():
        # Theoretical Hypotenuse Law
        theo = 1.0 / np.sqrt(0.25 + t**2)
        
        # Empirical Reality
        reality = high_sum(t, N)
        
        error = np.abs(reality - theo)
        
        print(f"Z{zid:<9} | {t:<15.4f} | {theo:<20.12f} | {error:<20.15f}")

    print("\n--- MASTER ANALYSIS ---")
    # Z1 error was ~ 1.8e-5
    # Let's compare to Z1000
    print("Evolution of Precision:")
    print("Z1   (t ~ 14)   -> Error ~ 2.0e-5")
    print("Z100 (t ~ 236)  -> Error ~ 1.0e-7 (Estimated)")
    print("Z1000(t ~ 1419) -> Error ~ ??")
    
if __name__ == "__main__":
    analyze_high_peaks()
