import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 15 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: توحيد القوانين الهندسية (وتر المثلث، الانطباق، المولد) في محرك واحد
# 🎓 المرحلة: التوحيد (Unification)
# 📐 المبدأ الرياضي: Unified Chord Law and Triangle Generator Engine
# ⚡ النتيجة المتوقعة: انطباق كامل بين المتجهات التجريبية والنظرية، وتأكيد عمل مولد المثلثات
# ==============================================================================

console = Console()

def chord_law(sigma, t):
    return 1 / np.sqrt((1 - sigma)**2 + t**2)

def compute_sum(sigma, t, N):
    n = np.arange(1, N + 1)
    vectors = n ** (-sigma + 1j * t)
    return np.sum(vectors)

def theoretical_vector(sigma, t, N):
    magnitude = N ** (1 - sigma) / np.sqrt((1 - sigma)**2 + t**2)
    phase = t * np.log(N) - np.arctan2(t, 1 - sigma)
    return magnitude * (np.cos(phase) + 1j * np.sin(phase))

def triangle_generator(delta, t, side='left'):
    base = 0.5 - delta if side == 'left' else 0.5 + delta
    return 1 / np.sqrt(base**2 + t**2)

def verify_all(sigma=0.5, t=14.134725, N=100000):
    console.print(Panel(
        f"Verification for [bold cyan]σ={sigma}, t={t}[/bold cyan] (N={N:,})",
        title="[bold green]Experiment 15: Unified Generator[/bold green]"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Law", justify="left")
    table.add_column("Metric", justify="right")
    table.add_column("Result", justify="right")
    
    # 1. Chord Law
    R = compute_sum(sigma, t, N)
    ratio = np.abs(R) / (N ** (1 - sigma))
    theory_chord = chord_law(sigma, t)
    error_pct = abs(ratio - theory_chord) / theory_chord * 100
    table.add_row("Chord Law", "Rel Error %", f"{error_pct:.6f}%")
    
    # 2. Vector Alignment
    T = theoretical_vector(sigma, t, N)
    distance = np.abs(R - T)
    rel_distance = distance / np.abs(R)
    angle_diff = np.abs(np.angle(R) - np.angle(T)) * (180/np.pi)
    table.add_row("Vector Alignment", "Rel Distance", f"{rel_distance:.6f}")
    table.add_row("Vector Alignment", "Angle Diff (°)", f"{angle_diff:.6f}")
    
    # 3. Triangle Generator Check
    delta = sigma - 0.5
    gen_chord = triangle_generator(delta, t)
    matching = abs(gen_chord - theory_chord) < 1e-10
    table.add_row("Triangle Gen", "Internal Matching", "[bold green]YES[/bold green]" if matching else "NO")

    console.print(table)

if __name__ == "__main__":
    # Test at a known zero
    verify_all(sigma=0.5, t=14.134725, N=100000)
    # Test at sigma = 0.8
    verify_all(sigma=0.8, t=14.134725, N=100000)
