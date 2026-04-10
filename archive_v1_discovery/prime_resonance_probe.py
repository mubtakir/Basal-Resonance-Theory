import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpmath import mp, zeta

# --- CONFIGURATION ---
mp.dps = 50 

def sieve_functions(N_max):
    mu = np.zeros(N_max + 1, dtype=int)
    lambda_val = np.zeros(N_max + 1, dtype=float)
    
    mu[1] = 1
    primes = []
    is_prime = np.ones(N_max + 1, dtype=bool)
    
    for i in range(2, N_max + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
            lambda_val[i] = np.log(i)
            
            # Von Mangoldt lambda(p^k) = ln p
            pk = i * i
            while pk <= N_max:
                lambda_val[pk] = np.log(i)
                pk *= i
                
        for p in primes:
            if i * p > N_max:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
                
    return mu, lambda_val

def get_prime_resonance(t, N_max, mu_arr, lambda_arr):
    s = complex(0.5, t)
    n = np.arange(1, N_max + 1)
    
    # Partial sums for mu and lambda (weighted by n^-0.5)
    # Using np.cumsum for efficiency
    terms_mu = mu_arr[1:] * (n**(-0.5 + 1j * t))
    sum_mu = np.cumsum(terms_mu)
    
    terms_lambda = lambda_arr[1:] * (n**(-0.5 + 1j * t))
    sum_lambda = np.cumsum(terms_lambda)
    
    return sum_mu, sum_lambda

def run_prime_research():
    N_max = 50000
    print(f"Generating sieve up to N={N_max}...")
    mu, lamb = sieve_functions(N_max)
    
    # Test on a zero and a non-zero
    t_zero = 14.134725
    t_non_zero = 10.0
    
    print("Analyzing resonance for t=14.13 (Z1)...")
    s_mu_z1, s_lam_z1 = get_prime_resonance(t_zero, N_max, mu, lamb)
    
    print("Analyzing resonance for t=10.0 (Background)...")
    s_mu_bg, s_lam_bg = get_prime_resonance(t_non_zero, N_max, mu, lamb)
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    n = np.arange(1, N_max + 1)
    ax1.plot(n, np.abs(s_mu_z1), label=f"t=14.13 (Z1)")
    ax1.plot(n, np.abs(s_mu_bg), label=f"t=10.0 (BG)")
    ax1.set_title("Moebius Sum Resonance $| \sum_{n=1}^N \mu(n) n^{-0.5-it} |$")
    ax1.set_xlabel("N")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(n, np.abs(s_lam_z1), label=f"t=14.13 (Z1)")
    ax2.plot(n, np.abs(s_lam_bg), label=f"t=10.0 (BG)")
    ax2.set_title("Von Mangoldt Sum Resonance $| \sum_{n=1}^N \Lambda(n) n^{-0.5-it} |$")
    ax2.set_xlabel("N")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("prime_resonance_discovery.png")
    print("Plot saved as 'prime_resonance_discovery.png'.")
    
    # Print stats
    print(f"\n--- RESONANCE METRICS (at N={N_max}) ---")
    print(f"|Sum Mu| at Z1: {np.abs(s_mu_z1[-1]):.4f}")
    print(f"|Sum Mu| at BG: {np.abs(s_mu_bg[-1]):.4f}")
    print(f"Resonance Ratio (Mu): {np.abs(s_mu_z1[-1]) / np.abs(s_mu_bg[-1]):.4f}")
    
    print(f"\n|Sum Lam| at Z1: {np.abs(s_lam_z1[-1]):.4f}")
    print(f"|Sum Lam| at BG: {np.abs(s_lam_bg[-1]):.4f}")
    print(f"Resonance Ratio (Lambda): {np.abs(s_lam_z1[-1]) / np.abs(s_lam_bg[-1]):.4f}")

if __name__ == "__main__":
    run_prime_research()
