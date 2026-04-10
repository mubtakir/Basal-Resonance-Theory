import numpy as np
import matplotlib.pyplot as plt

def verify_formula(t_min, t_max, N):
    t_points = np.linspace(t_min, t_max, 50)
    empirical_C = []
    theoretical_C = []
    
    print(f"Verifying formula over t in [{t_min}, {t_max}] with N={N}")
    
    for t in t_points:
        n = np.arange(1, N + 1)
        S = np.sum(n**(1j * t))
        c_emp = np.abs(S) / N
        c_theo = 1.0 / np.sqrt(1 + t**2)
        
        empirical_C.append(c_emp)
        theoretical_C.append(c_theo)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_points, empirical_C, 'bo', label='Empirical |S_N|/N', alpha=0.6)
    plt.plot(t_points, theoretical_C, 'r-', label='Theoretical 1/sqrt(1+t^2)', linewidth=2)
    plt.yscale('log')
    plt.xlabel('t (Frequency)')
    plt.ylabel('C (Magnitude Factor)')
    plt.title('Verification of Asymptotic Formula for S_N(0, t)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.savefig('formula_verification.png')
    print("Plot saved to formula_verification.png")
    
    # Calculate Mean Absolute Error
    mae = np.mean(np.abs(np.array(empirical_C) - np.array(theoretical_C)))
    print(f"Mean Absolute Error: {mae:.8f}")

if __name__ == "__main__":
    verify_formula(0.1, 50.0, N=50000)
