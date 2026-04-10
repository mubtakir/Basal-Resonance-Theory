import numpy as np
import matplotlib.pyplot as plt

def draw_zeta_triangle(t_zeros):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    
    for i, t in enumerate(t_zeros):
        color = colors[i % len(colors)]
        
        # Triangle legs
        real_part = 0.5
        imag_part = t
        hypotenuse = np.sqrt(real_part**2 + imag_part**2)
        
        # Drawing the Triangle
        # Base (Real part)
        ax.plot([0, real_part], [0, 0], color=color, linestyle='-', linewidth=2)
        # Vertical (Imaginary part)
        ax.plot([real_part, real_part], [0, imag_part], color=color, linestyle='-', linewidth=2)
        # Hypotenuse (The Magic Connection)
        ax.plot([0, real_part], [0, imag_part], color=color, linestyle='--', linewidth=3, 
                label=f'Z{i+1}: t={t:.2f}, Hypo={hypotenuse:.2f}')
        
        # Adding labels
        ax.text(real_part/2, -5, '0.5', ha='center', color=color)
        ax.text(real_part+0.5, imag_part/2, f't={t:.2f}', va='center', rotation=90, color=color)

    ax.set_xlim(-1, 5)
    ax.set_ylim(-10, 60)
    ax.set_xlabel('Real Axis Components', fontsize=12)
    ax.set_ylabel('Imaginary Axis (Frequency t)', fontsize=12)
    ax.set_title('The Geometry of Zeta Zeros: The 0.5-t Triangle', fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.savefig('zeta_geometry_triangle.png')
    print("Optimization: Zeta Triangle visualization saved to 'zeta_geometry_triangle.png'")

if __name__ == "__main__":
    # Draw for first few zeros
    first_zeros = [14.13, 30.42, 48.01]
    draw_zeta_triangle(first_zeros)
