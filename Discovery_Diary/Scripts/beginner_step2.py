import numpy as np
import matplotlib.pyplot as plt

def measure_power(t_range, N):
    magnitudes = []
    
    print(f"Measuring average distance for {len(t_range)} frequencies...")
    
    for t in t_range:
        n = np.arange(1, N + 1)
        # S_N = sum(n^it)
        S = np.sum(n**(1j * t))
        # Average distance per vector
        avg_dist = np.abs(S) / N
        magnitudes.append(avg_dist)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_range, magnitudes, 'b-', linewidth=2, label='Measured Data')
    
    plt.xlabel('t (Speed of Rotation)')
    plt.ylabel('Average Magnitude (|S_N| / N)')
    plt.title('How Speed (t) Affects the Total Distance', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('magnitude_curve.png')
    print("Optimization: Comparison curve saved to 'magnitude_curve.png'")

if __name__ == "__main__":
    # Test frequencies from 0.1 to 50
    t_test = np.linspace(0.1, 50.0, 100)
    measure_power(t_test, N=10000)
