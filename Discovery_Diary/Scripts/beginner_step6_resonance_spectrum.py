import numpy as np
import matplotlib.pyplot as plt
from sympy import factorint

def get_depth_for_N(t_zero, N):
    """Resonance depth based on Error Collapse."""
    n = np.arange(1, N + 1, dtype=np.float64)
    sigma = 0.5
    
    def get_error(t):
        magnitude = np.abs(np.sum(n**(-sigma + 1j * t))) / np.sqrt(N)
        theory = 1.0 / np.sqrt(0.25 + t**2)
        return np.abs(magnitude - theory)
    
    # Micro-scan to find the minimum error (the perfect match)
    scan_points = np.linspace(t_zero - 0.05, t_zero + 0.05, 300)
    errors = [get_error(t) for t in scan_points]
    min_err = np.min(errors)
    
    # Background error nearby
    background_err = np.mean([get_error(t_zero - 0.5), get_error(t_zero + 0.5)])
    
    depth = background_err / (min_err + 1e-15)
    return depth

def scan_N_spectrum(t_zero, N_range):
    results = []
    
    print(f"Scanning Resonance Spectrum for t={t_zero:.4f} across N range...")
    
    for N in N_range:
        d = get_depth_for_N(t_zero, N)
        results.append((N, d))
        
    # Sort by depth to find top resonant N
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n--- TOP 10 RESONANT N VALUES FOR Z5 ---")
    for i in range(min(10, len(results))):
        N_val, d_val = results[i]
        factors = factorint(N_val)
        print(f"Rank {i+1}: N={N_val:<4} | Depth={d_val:<8.2f} | Factors: {factors}")

    depths = [r[1] for r in sorted(results)]
    N_axis = [r[0] for r in sorted(results)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(N_axis, depths, 'g-', linewidth=2, label='Resonance Depth')
    
    # Highlight the absolute best
    best_N, best_depth = results[0]
    plt.plot(best_N, best_depth, 'ro', label=f'Global Peak N={best_N}')

    plt.xlabel('N (The Filter Choice)', fontsize=12)
    plt.ylabel('The Resonance Depth', fontsize=12)
    plt.title(f'Finding the Master Key N for Z5', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('N_resonance_spectrum.png')
    print("\nOptimization: Spectrum plot and Top 10 data collected.")

if __name__ == "__main__":
    # Scan for Z5: 32.935
    z5 = 32.9350615877
    scan_N_spectrum(z5, np.arange(10, 500))
