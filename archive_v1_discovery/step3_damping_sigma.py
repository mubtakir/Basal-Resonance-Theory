import numpy as np
import matplotlib.pyplot as plt

def investigate_sigma(t, sigma_values, N_max):
    plt.figure(figsize=(12, 6))
    
    print(f"Investigating effect of sigma for t={t} up to N={N_max}")
    
    for sigma in sigma_values:
        n = np.arange(1, N_max + 1)
        # S(N, sigma, t) = sum(n^(-sigma + it))
        terms = n**(-sigma + 1j * t)
        S_N = np.cumsum(terms)
        
        # We expect |S_N| ~ N^(1-sigma) / sqrt((1-sigma)^2 + t^2)
        # So |S_N| / N^(1-sigma) should be constant.
        growth_factor = n**(1 - sigma)
        normalized_mag = np.abs(S_N) / growth_factor
        
        theoretical_constant = 1.0 / np.sqrt((1 - sigma)**2 + t**2)
        
        plt.plot(n, normalized_mag, label=f'sigma={sigma} (Theo={theoretical_constant:.4f})')
        print(f"Sigma={sigma}: Empirical Const={normalized_mag[-1]:.6f}, Theoretical={theoretical_constant:.6f}")

    plt.xlabel('N')
    plt.ylabel('|S_N| / N^(1-sigma)')
    plt.title(f'Effect of Damping Factor sigma on Growth (t={t})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('sigma_damping_effect.png')
    print("Plot saved to sigma_damping_effect.png")

if __name__ == "__main__":
    sigmas = [0.2, 0.5, 0.8]
    investigate_sigma(t=10.0, sigma_values=sigmas, N_max=50000)
