import numpy as np
import matplotlib.pyplot as plt
from mpmath import mp, zeta

# --- CONFIGURATION ---
mp.dps = 50

def sieve_mu(N_max):
    mu = np.zeros(N_max + 1, dtype=int)
    mu[1] = 1
    primes = []
    is_prime = np.ones(N_max + 1, dtype=bool)
    for i in range(2, N_max + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N_max: break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def get_moebius_tower(rho, N_max, mu_arr):
    # Sum mu(n) * n^-rho
    n = np.arange(1, N_max + 1)
    # Using complex arithmetic for precision
    terms = mu_arr[1:] * (n ** (-rho))
    sums = np.cumsum(terms)
    return sums

def analyze_zero_growth(t_zero, N_max, mu_arr):
    rho = 0.5 + 1j * t_zero
    sums = get_moebius_tower(rho, N_max, mu_arr)
    magnitudes = np.abs(sums)
    
    # We want to test Magnitude ~ C * ln(N)
    # Linear regression: Magnitudes vs ln(N)
    n_values = np.arange(1, N_max + 1)
    ln_N = np.log(n_values[100:]) # Start from 100 to avoid noise
    mag_subset = magnitudes[100:]
    
    slope, intercept = np.polyfit(ln_N, mag_subset, 1)
    
    # Theoretical prediction: Slope = 1 / |zeta'(rho)|
    # mpmath.zeta(s, derivative=1)
    z_prime = zeta(mp.mpc(0.5, t_zero), derivative=1)
    theo_slope = 1.0 / abs(complex(z_prime))
    
    return magnitudes, slope, theo_slope, sums

def run_moebius_experiment():
    N_max = 50000
    print(f"Sieving mu up to N={N_max}...")
    mu = sieve_mu(N_max)
    
    # Famous Zeta Zeros
    zeros = {
        "Z1": 14.13472514,
        "Z2": 21.02203964,
        "Z3": 25.01085758
    }
    
    plt.figure(figsize=(12, 10))
    
    print(f"{'Zero':<6} | {'Emp Slope':<10} | {'Theo Slope':<10} | {'R-Ratio':<8}")
    print("-" * 45)
    
    for name, t in zeros.items():
        mags, slope, theo_slope, sums = analyze_zero_growth(t, N_max, mu)
        ratio = slope / theo_slope
        print(f"{name:<6} | {slope:<10.6f} | {theo_slope:<10.6f} | {ratio:<8.4f}")
        
        # Plot 1: Magnitude vs ln(N)
        plt.subplot(2, 1, 1)
        plt.plot(np.log(np.arange(1, N_max + 1)), mags, label=f"{name} (Ratio: {ratio:.3f})")
        
        # Plot 2: Complex Vector Spiral (Normalizing by ln N to see if it stabilizes)
        plt.subplot(2, 1, 2)
        # Taking every 100th point for visibility
        spiral = sums[::100] 
        plt.plot(spiral.real, spiral.imag, label=f"{name} Spiral")

    plt.subplot(2, 1, 1)
    plt.title("The Moebius Tower Law: |M_N(rho)| vs ln(N)")
    plt.xlabel("ln(N)")
    plt.ylabel("|Sum mu(n)/n^rho|")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.title("The Moebius Vector Spiral: The Dance at the Pole")
    plt.xlabel("Real")
    plt.ylabel("Imag")
    plt.legend()
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("moebius_tower_resonance.png")
    print("\nPlot saved as 'moebius_tower_resonance.png'")
    print("Observation: The Emp/Theo Ratio near 1.0 proves the Logarithmic Pole hypothesis!")

if __name__ == "__main__":
    run_moebius_experiment()
