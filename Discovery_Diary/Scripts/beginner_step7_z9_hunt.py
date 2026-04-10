import numpy as np
import matplotlib.pyplot as plt

def hunt_z9(t_min, t_max, N):
    t_points = np.linspace(t_min, t_max, 1000)
    errors = []
    
    print(f"Hunting for Z9 in t=[{t_min}, {t_max}] using N={N}...")
    
    sigma = 0.5
    theo_denominator = 0.5
    
    for t in t_points:
        n = np.arange(1, N + 1)
        S = np.sum(n**(-sigma + 1j * t))
        emp_magnitude = np.abs(S) / (n[-1]**(1 - sigma))
        theo_magnitude = 1.0 / np.sqrt(theo_denominator**2 + t**2)
        
        # Calculate error (The Resonance Signal)
        error = np.abs(emp_magnitude - theo_magnitude)
        errors.append(error)
        
    plt.figure(figsize=(10, 6))
    plt.plot(t_points, errors, 'm-', linewidth=1.5, label=f'Resonance Signal (N={N})')
    
    # Identify the valley
    best_idx = np.argmin(errors)
    z9_found = t_points[best_idx]
    z9_error = errors[best_idx]
    
    plt.axvline(x=z9_found, color='black', linestyle='--', label=f'Z9 Found at t={z9_found:.3f}')
    
    plt.yscale('log')
    plt.xlabel('t (Scanning Range)', fontsize=12)
    plt.ylabel('The Error (Inverse Resonance)', fontsize=12)
    plt.title('Hunting Z9: The Search for the Next Zero', fontsize=14)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    plt.savefig('Z9_discovery_hunt.png')
    
    print(f"\n--- Z9 HUNTING RESULTS ---")
    print(f"Target Found! Z9 is at t={z9_found:.4f}")
    print(f"Resonance Power (Error): {z9_error:.12f}")
    print(f"Optimization: Z9 Discovery plot saved to 'Z9_discovery_hunt.png'")

if __name__ == "__main__":
    # Scan based on Z8 + 4.86 rhythm
    hunt_z9(t_min=50.0, t_max=55.0, N=119)
