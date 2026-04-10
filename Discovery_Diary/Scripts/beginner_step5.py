import numpy as np
import matplotlib.pyplot as plt

def scan_zeta_resonance(t_min, t_max, N):
    t_points = np.linspace(t_min, t_max, 500)
    errors = []
    
    print(f"Scanning for Zeta Resonances in t=[{t_min}, {t_max}] at sigma=0.5...")
    
    sigma = 0.5
    theo_denominator = 1.0 - sigma # which is 0.5
    
    for t in t_points:
        # Complex sum of n^(-0.5 + it)
        n = np.arange(1, N + 1)
        S = np.sum(n**(-sigma + 1j * t))
        
        # Empirical magnitude
        emp_magnitude = np.abs(S) / (n[-1]**(1 - sigma))
        
        # Theoretical law at sigma=0.5: 1 / sqrt(0.25 + t^2)
        theo_magnitude = 1.0 / np.sqrt(theo_denominator**2 + t**2)
        
        # Error between reality and law
        error = np.abs(emp_magnitude - theo_magnitude)
        errors.append(error)
        
    plt.figure(figsize=(10, 6))
    plt.plot(t_points, errors, 'r-', linewidth=1.5, label='Error (Reality - Law)')
    
    # Let's find the deepest point!
    best_idx = np.argmin(errors)
    best_t = t_points[best_idx]
    best_err = errors[best_idx]
    
    plt.axvline(x=best_t, color='blue', linestyle='--', alpha=0.5, label=f'Deepest Valley at t={best_t:.2f}')
    
    plt.yscale('log') # Log scale to see the depth!
    plt.xlabel('t (Imaginary part frequency)', fontsize=12)
    plt.ylabel('The Error (Difference)', fontsize=12)
    plt.title('Finding the Secret Valleys: The Zeta Resonance', fontsize=14)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    plt.savefig('zeta_resonance_discovery.png')
    
    print(f"Discovery: The deepest valley is at t={best_t:.4f} with error {best_err:.10f}")
    print("Optimization: Resonance discovery plot saved to 'zeta_resonance_discovery.png'")

if __name__ == "__main__":
    # Scan around the first known Riemman zero
    scan_zeta_resonance(t_min=10.0, t_max=20.0, N=50000)
