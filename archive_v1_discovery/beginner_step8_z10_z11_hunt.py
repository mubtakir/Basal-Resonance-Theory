import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def hunt_z10_z11(t_min, t_max, N):
    t_points = np.linspace(t_min, t_max, 2000)
    errors = []
    
    print(f"Hunting for Z10 & Z11 in t=[{t_min}, {t_max}] using N={N}...")
    
    sigma = 0.5
    theo_denominator = 0.5
    
    for t in t_points:
        n = np.arange(1, N + 1)
        S = np.sum(n**(-sigma + 1j * t))
        emp_magnitude = np.abs(S) / (n[-1]**(1 - sigma))
        theo_magnitude = 1.0 / np.sqrt(theo_denominator**2 + t**2)
        
        # Calculate error signal
        error = np.abs(emp_magnitude - theo_magnitude)
        errors.append(error)
        
    # Find the deepest points (valleys in error)
    # We invert the signal to use 'find_peaks'
    inverted_signal = -np.log10(errors)
    peaks, _ = find_peaks(inverted_signal, height=3) # Look for significant dips
    
    found_zeros = t_points[peaks]
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_points, errors, 'c-', linewidth=1.5, label=f'Resonance Spectrum (N={N})')
    
    for z in found_zeros:
        plt.axvline(x=z, color='red', linestyle='--', alpha=0.6, label=f'Zero Found at t={z:.3f}')
        plt.text(z+0.2, np.min(errors), f'Zero: {z:.2f}', rotation=90, verticalalignment='bottom')

    plt.yscale('log')
    plt.xlabel('t (Scanning Range)', fontsize=12)
    plt.ylabel('The Error (Resonance Valley)', fontsize=12)
    plt.title('Hunting Z10 & Z11: The Next Two Giants', fontsize=14)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    plt.savefig('Z10_Z11_discovery_hunt.png')

    print(f"\n--- HUNTING RESULTS ---")
    for i, z in enumerate(found_zeros, 10):
        print(f"Zero {i} found at t = {z:.4f}")
        
    if len(found_zeros) >= 2:
        gap = found_zeros[1] - found_zeros[0]
        print(f"Gap between Z10 and Z11: {gap:.4f}")
    
    print(f"Optimization: Discovery plot saved to 'Z10_Z11_discovery_hunt.png'")

if __name__ == "__main__":
    # Scan from 55 to 65
    hunt_z10_z11(t_min=55.0, t_max=65.0, N=85)
