import numpy as np
import matplotlib.pyplot as plt

def verify_myth(t_range, N):
    empirical_vals = []
    theoretical_vals = []
    
    print(f"Verifying the 'Magic Hypotenuse' for {len(t_range)} frequencies...")
    
    for t in t_range:
        # Summing vectors
        n = np.arange(1, N + 1)
        S = np.sum(n**(1j * t))
        emp = np.abs(S) / N
        
        # Theoretical Law: 1/sqrt(1 + t^2)
        theo = 1.0 / np.sqrt(1 + t**2)
        
        empirical_vals.append(emp)
        theoretical_vals.append(theo)
    
    plt.figure(figsize=(10, 6))
    # Drawing Empirical with thick blue dots
    plt.plot(t_range, empirical_vals, 'bo', label='Empirical Measurements (The Reality)', alpha=0.5, markersize=8)
    # Drawing Theoretical with thin red line
    plt.plot(t_range, theoretical_vals, 'r-', label='Theoretical Prediction (The Law)', linewidth=2.5)
    
    plt.xlabel('t (Frequency)', fontsize=12)
    plt.ylabel('Magnitude factor', fontsize=12)
    plt.title('The Magic Hypotenuse: Reality vs Prediction', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('hypotenuse_verification.png')
    
    # Measuring the Error
    mae = np.mean(np.abs(np.array(empirical_vals) - np.array(theoretical_vals)))
    print(f"Mean Absolute Error: {mae:.10f}")
    print("Optimization: Comparison plot saved to 'hypotenuse_verification.png'")

if __name__ == "__main__":
    t_test = np.linspace(0.1, 50.0, 50)
    verify_myth(t_test, N=50000)
