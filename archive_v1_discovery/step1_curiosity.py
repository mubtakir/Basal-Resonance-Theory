import numpy as np
import matplotlib.pyplot as plt

def observe_sum(t_values, N_max):
    plt.figure(figsize=(10, 6))
    
    for t in t_values:
        n = np.arange(1, N_max + 1)
        # S(N) = sum(n^it)
        terms = n**(1j * t)
        S_N = np.cumsum(terms)
        
        # Normalized magnitude |S(N)| / N
        normalized_mag = np.abs(S_N) / n
        
        plt.plot(n, normalized_mag, label=f't = {t}')
        
        # Print final value for quick inspection
        print(f"Final |S_N|/N for t={t}: {normalized_mag[-1]:.6f}")

    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.xlabel('N (Number of terms)')
    plt.ylabel('|S_N| / N')
    plt.title('Observation of |Σ n^it| / N as N increases')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('observation_plot.png')
    print("Plot saved to observation_plot.png")

if __name__ == "__main__":
    t_to_test = [0.5, 2.0, 10.0]
    print("Starting observation of |Sum n^it| / N...")
    observe_sum(t_to_test, N_max=10000)
