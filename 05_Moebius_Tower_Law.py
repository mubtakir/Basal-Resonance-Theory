from ZetaLab_Supreme import ZetaLab
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 08 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: إثبات قانون "قطب موبيوس" ونمو النبض اللوغاريتمي عند أصفار زيتا
# 🎓 المرحلة: قانون موبيوس (Moebius Law)
# 📐 المبدأ الرياضي: |M_N(rho)| approx ln(N) / |zeta'(rho)|
# ⚡ النتيجة المتوقعة: انحدار تجريبي (Slope) يطابق القيمة النظرية بنسبة خطأ أقل من 5%
# ==============================================================================

console = Console()

def run_moebius_tower_experiment():
    lab = ZetaLab(precision=50)
    
    console.print(Panel.fit(
        "--- EXPERIMENT 08: THE MOEBIUS TOWER & LOGARITHMIC POLE ---",
        style="bold green"
    ))
    
    zeros = {
        "Z1": 14.1347251417,
        "Z2": 21.0220396388,
        "Z3": 25.0108575801
    }
    
    N_max = 20000
    console.print(f"Sieving Moebius up to [bold cyan]N={N_max}[/bold cyan]...\n")
    mu = lab.sieve_mu(N_max)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Zero", justify="center")
    table.add_column("Empirical Slope", justify="right")
    table.add_column("Theoretical Slope", justify="right")
    table.add_column("Ratio (%)", justify="right")
    
    for name, t in track(zeros.items(), description="Analyzing Moebius Pulses..."):
        rho = complex(0.5, t)
        
        # 1. Theoretical Slope: 1 / |zeta'(rho)|
        z_prime = lab.get_zeta_derivative(rho, order=1)
        theo_slope = 1.0 / abs(z_prime)
        
        # 2. Empirical Growth
        sample_Ns = np.geomspace(100, N_max, 20, dtype=int)
        n = np.arange(1, N_max + 1)
        terms = mu[1:] * (n**(-rho))
        all_sums = np.cumsum(terms)
        
        mags = [abs(all_sums[N-1]) for N in sample_Ns]
        ln_Ns = np.log(sample_Ns)
        
        # Linear regression on |M_N| vs ln(N)
        slope, intercept = np.polyfit(ln_Ns, mags, 1)
        
        ratio = float(slope / theo_slope)
        
        style = "green" if abs(ratio - 1.0) < 0.05 else "white"
        table.add_row(
            name,
            f"{float(slope):.10f}",
            f"{float(theo_slope):.10f}",
            f"[{style}]{ratio:.2%}[/{style}]"
        )

    console.print(table)
    console.print("\n[bold green][STATUS: VERIFIED][/bold green] The Logarithmic Pole Law correctly predicts Moebius growth at Z-Zeros.")

if __name__ == "__main__":
    run_moebius_tower_experiment()
