import numpy as np
import matplotlib.pyplot as plt

def zeta_sum_magnitude(t, N):
    n = np.arange(1, N + 1)
    S = np.sum(n**(-0.5 + 1j * t))
    return np.abs(S) / np.sqrt(N)

def analyze_conformance():
    # First 10 known zeros from literature
    zeta_zeros = [
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
        37.5862, 43.3271, 48.0052, 52.9703, 56.4462
    ]
    
    N_fixed = 1000
    
    results = []
    
    print(f"{'Zero':<5} | {'t':<10} | {'Magnitude':<12} | {'Theoretical':<12} | {'Error (D)'}")
    print("-" * 65)
    
    for i, t in enumerate(zeta_zeros, 1):
        mag = zeta_sum_magnitude(t, N_fixed)
        theo = 1.0 / np.sqrt(0.25 + t**2)
        error = np.abs(mag - theo)
        
        results.append((i, t, mag, theo, error))
        print(f"Z{i:<4} | {t:<10.4f} | {mag:<12.8f} | {theo:<12.8f} | {error:<12.10f}")
        
    # Analysis & Plotting
    ids = [r[0] for r in results]
    ts = [r[1] for r in results]
    errors = [r[4] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(ts, errors, 'r-o', linewidth=2, markersize=8, label='Non-conformance (Residual Error)')
    
    plt.yscale('log')
    plt.xlabel('t (Zero Location)', fontsize=12)
    plt.ylabel('The Difference (Magnitude Error)', fontsize=12)
    plt.title(f'The Pattern of Error across the first 10 Zeros (N={N_fixed})', fontsize=14)
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.legend()
    plt.savefig('first_10_errors_pattern.png')
    
    print(f"\n--- ANALYSIS SUMMARY ---")
    print(f"Max Error: {max(errors):.8f} (Z{ids[np.argmax(errors)]})")
    print(f"Min Error: {min(errors):.8f} (Z{ids[np.argmin(errors)]})")
    print(f"Optimization: Analysis plotted and saved to 'first_10_errors_pattern.png'")

if __name__ == "__main__":
    analyze_conformance()
