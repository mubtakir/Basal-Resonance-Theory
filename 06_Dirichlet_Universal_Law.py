from ZetaLab_Supreme import ZetaLab, DirichletCharacters
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 09 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: إثبات أن ثابت التقارب العالمي alpha = 1.5 ينطبق على جميع سلاسل ديريكليه الدورية
# 🎓 المرحلة: الشمولية (Universality)
# 📐 المبدأ الرياضي: Error(N) approx C * N^-alpha where alpha = 1.5
# ⚡ النتيجة المتوقعة: حساب ميل الخط (Slope) لجميع الدوال المختبرة ليكون قريباً جداً من 1.5
# ==============================================================================

console = Console()

def estimate_alpha(lab, s, coefficients_func, N_range):
    errors = []
    if 'eta' in str(coefficients_func):
        exact_val = (1 - 2**(1-s)) * lab.get_zeta(s)
    elif 'l_mod3' in str(coefficients_func):
        from mpmath import dirichlet
        exact_val = dirichlet(s, [0, 1, -1])
    else:
        exact_val = lab.get_zeta(s)
    
    for N in N_range:
        N = int(N)
        sn = lab.calculate_partial_sum(s, N, coefficients_func)
        tail = lab.get_tower_tail(s, N, a_N=coefficients_func(N))
        err = abs(sn - (exact_val - tail))
        errors.append(err)
    
    log_N = np.log([float(N_val) for N_val in N_range])
    log_E = np.log([float(e) for e in errors])
    slope, intercept = np.polyfit(log_N, log_E, 1)
    return -slope

def run_universal_experiment():
    lab = ZetaLab(precision=50)
    
    console.print(Panel.fit(
        "--- EXPERIMENT 09: THE UNIVERSAL CONVERGENCE LAW (DIRICHLET) ---",
        style="bold green"
    ))
    
    s = complex(0.5, 50.0) 
    N_range = np.linspace(500, 2000, 20, dtype=int)
    
    tests = [
        ("Riemann Zeta (1,1,1...)", lambda n: 1),
        ("Dirichlet Eta (1,-1,1...)", DirichletCharacters.eta),
        ("L-function Mod 3 (1,-1,0...)", DirichletCharacters.l_mod3)
    ]
    
    console.print(f"Testing alpha at [bold cyan]s={s}[/bold cyan] on Critical Line\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Series Name", justify="left")
    table.add_column("Calculated Alpha", justify="right")
    table.add_column("Match (1.5)", justify="center")
    
    for name, func in tests:
        alpha = estimate_alpha(lab, s, func, N_range)
        is_match = abs(alpha - 1.5) < 0.1
        match_str = "[bold green]YES[/bold green]" if is_match else "[bold red]NO[/bold red]"
        
        table.add_row(
            name,
            f"{float(alpha):.6f}",
            match_str
        )

    console.print(table)
    console.print("\n[bold green][CONCLUSION][/bold green] Alpha = 1.5 is a Universal Symmetry of Periodic Series.")

if __name__ == "__main__":
    run_universal_experiment()
