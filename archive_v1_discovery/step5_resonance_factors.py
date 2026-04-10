import numpy as np
import matplotlib.pyplot as plt
from sympy import factorint

def find_best_N(t_zero, N_range):
    depths = []
    
    print(f"Finding best N for zero t={t_zero} in range {N_range}")
    
    for N in N_range:
        # Calculate depth as Mean_Error / Current_Error
        # Here we simplify: Depth = 1 / Error (since higher error is baseline)
        n = np.arange(1, N + 1)
        S = np.sum(n**(-0.5 + 1j * t_zero))
        emp_const = np.abs(S) / np.sqrt(N)
        theo_const = 1.0 / np.sqrt(0.25 + t_zero**2)
        
        error = np.abs(emp_const - theo_const)
        
        # We store (N, depth)
        depths.append((N, 1.0 / (error + 1e-15)))

    depths = np.array(depths)
    best_idx = np.argmax(depths[:, 1])
    best_N = int(depths[best_idx, 0])
    
    print(f"Best N found: {best_N} with Depth score: {depths[best_idx, 1]:.2e}")
    
    # Analyze factors
    factors = factorint(best_N)
    print(f"Prime factors of {best_N}: {factors}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(depths[:, 0], depths[:, 1], 'g-')
    plt.axvline(x=best_N, color='r', linestyle='--', label=f'Best N={best_N}')
    plt.xlabel('N')
    plt.ylabel('Resonance Depth (1/Error)')
    plt.title(f'Resonance Depth vs N for First Zero (t={t_zero:.4f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('resonance_depth_vs_N.png')
    print("Plot saved to resonance_depth_vs_N.png")

if __name__ == "__main__":
    t_zero = 14.13472514173469
    # Testing a wide range of N
    N_test = np.arange(10, 1000)
    find_best_N(t_zero, N_test)
