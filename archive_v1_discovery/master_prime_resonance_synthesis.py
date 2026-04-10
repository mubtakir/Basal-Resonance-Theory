import numpy as np
import matplotlib.pyplot as plt

def prime_resonance_wave(x, t_zeros):
    """
    Simplified Riemann explicit formula approximation.
    Each zero t contributes a wave of frequency t and weight 1/H.
    """
    waves = []
    # Base trend (Li(x) approximation)
    trend = x / np.log(x + 1e-12)
    
    total_correction = np.zeros_like(x)
    
    for t in t_zeros:
        # The weight is our Hypotenuse Law!
        H = np.sqrt(0.25 + t**2)
        weight = 1.0 / H
        
        # Correction wave: Cosine oscillation weighted by 1/H
        # (This is a simplification of x^0.5 / t * cos(t ln x))
        wave = (np.sqrt(x) * weight) * np.cos(t * np.log(x))
        total_correction += wave
        waves.append(wave)
        
    return trend, total_correction, waves

def run_final_synthesis():
    x = np.linspace(2, 500, 1000)
    
    # We use our best zeros (Z1 to Z12)
    t_zeros = [14.13, 21.02, 25.01, 30.42, 32.94, 37.59, 43.33, 48.01, 52.97, 56.45, 59.34, 60.83]
    
    trend, correction, waves = prime_resonance_wave(x, t_zeros)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: The Prime Approximation
    ax1.plot(x, trend, 'k--', alpha=0.5, label='Basic Prime Trend (Li(x))')
    ax1.plot(x, trend + correction, 'r-', linewidth=1.5, label='Unified Resonance (Zeta-Corrected)')
    ax1.set_title('Zeta Zeros as Correction Waves for Primes', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.2)
    
    # Plot 2: The Individual Resonance Weights (1/H)
    for i, t in enumerate(t_zeros):
        H = np.sqrt(0.25 + t**2)
        ax2.bar(t, 100/H, width=1, label=f'Z{i+1}: t={t:.1f}' if i < 3 else "")
        
    ax2.set_xlabel('Frequency t (Zero Location)', fontsize=12)
    ax2.set_ylabel('Wave Weight (1/Hypotenuse) %', fontsize=12)
    ax2.set_title('The Geometric Law: Weights diminish as Triangle thins', fontsize=14)
    ax2.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('prime_zeta_unified_resonance.png')
    print("Optimization: Final Synthesis plot saved to 'prime_zeta_unified_resonance.png'")

if __name__ == "__main__":
    run_final_synthesis()
