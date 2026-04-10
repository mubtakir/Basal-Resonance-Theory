import numpy as np
import matplotlib.pyplot as plt

def draw_vector_dance(t, N_max):
    # n goes from 1 to N_max
    n = np.arange(1, N_max + 1)
    
    # Calculate each terms as a vector: n^it = exp(i * t * ln(n))
    vectors = n**(1j * t)
    
    # The path is the cumulative sum of these vectors
    path = np.cumsum(vectors)
    
    # Prepending zero to start the path from (0,0)
    x = np.insert(np.real(path), 0, 0)
    y = np.insert(np.imag(path), 0, 0)

    plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'b-o', markersize=4, alpha=0.6, label=f'Path for t={t}')
    
    # Highlighting start and end
    plt.plot(0, 0, 'go', markersize=10, label='Start (n=1)')
    plt.plot(x[-1], y[-1], 'ro', markersize=10, label=f'End (n={N_max})')

    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.title(f'The Dance of Vectors: Path of Σ n^it until N={N_max}', fontsize=14)
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')
    plt.legend()
    plt.savefig('vector_dance.png')
    print("Optimization: Visualization saved to 'vector_dance.png'")

if __name__ == "__main__":
    # Let's use a nice frequency like 10
    draw_vector_dance(t=10.0, N_max=100)
