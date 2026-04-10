import numpy as np
import matplotlib.pyplot as plt

def test_zeta_resonance(t_random, t_zero, N_max):
    plt.figure(figsize=(10, 6))
    
    t_list = [t_random, t_zero]
    labels = ["Random (t=10.0)", "Zeta Zero (t~14.1347)"]
    
    print(f"Testing resonance at sigma=0.5 up to N={N_max}")
    
    for t, label in zip(t_list, labels):
        n = np.arange(1, N_max + 1)
        # S_N for sigma=0.5
        S_N = np.cumsum(n**(-0.5 + 1j * t))
        
        # normalized magnitude |S_N| / sqrt(N)
        emp_const = np.abs(S_N) / np.sqrt(n)
        theo_const = 1.0 / np.sqrt(0.25 + t**2)
        
        error = np.abs(emp_const - theo_const)
        
        plt.plot(n, error, label=label)
        print(f"{label}: Final Error at N={N_max}: {error[-1]:.12f}")

    plt.yscale('log')
    plt.xlabel('N')
    plt.ylabel('Absolute Error |Empirical - Theoretical|')
    plt.title('The Zeta Resonance: Sharp Drop in Error at a Zero (sigma=0.5)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.savefig('zeta_resonance_test.png')
    print("Plot saved to zeta_resonance_test.png")

if __name__ == "__main__":
    # First Riemann zero approx
    t_zero = 14.13472514173469
    test_zeta_resonance(t_random=10.0, t_zero=t_zero, N_max=100000)
