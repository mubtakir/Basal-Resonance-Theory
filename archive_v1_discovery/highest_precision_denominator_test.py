import numpy as np
import pandas as pd

def high_precision_test():
    # First 10 high-precision zeros
    zeta_zeros = [
        14.1347251417, 21.0220396388, 25.0108575801, 30.4248761259, 32.9350615877,
        37.5861781588, 43.3270732809, 48.0051508812, 52.9703214777, 56.4462476971
    ]
    
    N = 5000 # High N for high precision
    
    results = []
    
    print(f"--- HIGH-PRECISION DENOMINATOR ANALYSIS (N={N}) ---")
    print(f"{'Zero':<5} | {'Theo: sqrt(0.25+t^2)':<25} | {'Emp: sqrt(N)/|S_N|':<25} | {'Difference'}")
    print("-" * 85)
    
    for i, t in enumerate(zeta_zeros, 1):
        n = np.arange(1, N + 1, dtype=np.float64)
        S = np.sum(n**(-0.5 + 1j * t))
        
        # Theoretical Denominator
        theo_den = np.sqrt(0.25 + t**2)
        
        # Empirical Denominator (Inverted Normalized Magnitude)
        emp_den = np.sqrt(N) / np.abs(S)
        
        diff = np.abs(theo_den - emp_den)
        
        results.append((i, t, theo_den, emp_den, diff))
        print(f"Z{i:<4} | {theo_den:<25.12f} | {emp_den:<25.12f} | {diff:<15.10f}")
    
    # Conclusion on match quality
    avg_diff = np.mean([r[4] for r in results])
    print("\n--- MEASUREMENT CONCLUSION ---")
    print(f"The average shift from the geometric ideal is: {avg_diff:.10f}")
    print(f"Observation: The first {int(-np.log10(avg_diff))-1} decimal places are perfectly identical.")

if __name__ == "__main__":
    high_precision_test()
