import numpy as np
import matplotlib.pyplot as plt

def verify_damping(t_range, sigma_list, N):
    plt.figure(figsize=(10, 6))
    
    print(f"Verifying Generalized Hypotenuse Law for sigma in {sigma_list}...")
    
    for sigma in sigma_list:
        empirical_vals = []
        theoretical_vals = []
        
        for t in t_range:
            # Sum of vectors: n^(-sigma + it)
            n = np.arange(1, N + 1)
            S = np.sum(n**(-sigma + 1j * t))
            # Average normalized magnitude relative to N^(1-sigma)
            emp = np.abs(S) / (n[-1]**(1 - sigma))
            
            # Generalized Law: 1/sqrt((1-sigma)^2 + t^2)
            theo = 1.0 / np.sqrt((1 - sigma)**2 + t**2)
            
            empirical_vals.append(emp)
            theoretical_vals.append(theo)
        
        # Plotting comparison for each sigma
        p = plt.plot(t_range, empirical_vals, 'o', alpha=0.4, label=f'Empirical (sigma={sigma})')
        color = p[0].get_color()
        plt.plot(t_range, theoretical_vals, '-', color=color, linewidth=2, label=f'Theoretical (sigma={sigma})')
    
    plt.xlabel('t (Frequency)', fontsize=12)
    plt.ylabel('Magnitude factor', fontsize=12)
    plt.title('Damping Discovery: Does the Hypotenuse Expand?', fontsize=14)
    plt.yscale('log') # Use log scale to see differences clearly
    plt.grid(True, alpha=0.3, which='both')
    plt.legend()
    plt.savefig('damping_verification.png')
    print("Optimization: Damping comparison plot saved to 'damping_verification.png'")

if __name__ == "__main__":
    t_test = np.linspace(0.1, 50.0, 30)
    sigmas = [0.2, 0.5, 0.8]
    verify_damping(t_test, sigmas, N=100000)
