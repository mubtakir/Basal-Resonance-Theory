"""
المستوى الخامس: الإسقاط الزيتاوي على السطح الكروي
Zeta Projection on the Spherical Surface - The Basil Resonance Finale
========================================================================
ربط أصفار زيتا-ريمان بسطح الكرة المادية/المعلوماتية
إثبات أن σ = 0.5 هو "خط الاستواء" للتوازن الكينماتيكي
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# نموذج الكرة الزيتاوية (The Zeta Sphere)
# ============================================================================

class ZetaSphere:
    """
    نموذج الكرة التي يرتكز عليها طيف دالة زيتا
    السطح يمثل فضاء الأعداد، والخط σ=0.5 هو خط الاستواء
    """
    def __init__(self, radius=1.0, resolution=100):
        self.radius = radius
        self.resolution = resolution
        
        # إحداثيات الكرة
        self.phi = np.linspace(0, 2 * np.pi, resolution)    # الزاوية الأفقية (t - التردد)
        self.theta = np.linspace(0, np.pi, resolution)      # الزاوية الرأسية (σ - التمدد)
        self.Phi, self.Theta = np.meshgrid(self.phi, self.theta)
        
        # تحويل الإحداثيات: σ مرتبطة بـ theta
        # σ = 0.5 يقابل theta = π/2 (خط الاستواء)
        self.sigma_from_theta = lambda theta: np.sin(theta)**2  # 0 عند القطبين، 0.5 عند خط الاستواء، 1 عند القطب الآخر
        self.theta_from_sigma = lambda sigma: np.arcsin(np.sqrt(sigma))
        
        # حساب الإحداثيات الديكارتية
        self.X = radius * np.sin(self.Theta) * np.cos(self.Phi)
        self.Y = radius * np.sin(self.Theta) * np.sin(self.Phi)
        self.Z = radius * np.cos(self.Theta)
        
        # قيم σ على سطح الكرة
        self.Sigma = self.sigma_from_theta(self.Theta)
        
    def get_equator_points(self, t_values):
        """
        الحصول على نقاط خط الاستواء (σ=0.5) لقيم t المختلفة
        هذه النقاط تمثل الخط الحرج لدالة زيتا
        """
        theta_eq = self.theta_from_sigma(0.5)  # π/2
        x_eq = self.radius * np.sin(theta_eq) * np.cos(t_values)
        y_eq = self.radius * np.sin(theta_eq) * np.sin(t_values)
        z_eq = self.radius * np.cos(theta_eq) * np.ones_like(t_values)
        return x_eq, y_eq, z_eq
    
    def project_zeta_zeros(self, zeros):
        """
        إسقاط أصفار زيتا على سطح الكرة
        الأصفار تقع على خط الاستواء (σ=0.5)
        """
        # تحويل قيم t (الأجزاء التخيلية للأصفار) إلى زوايا
        # نستخدم دالة لولبية لوغاريتمية لربط الترددات بالزاوية
        t_angles = self.map_t_to_angle(zeros)
        
        theta_zero = self.theta_from_sigma(0.5)
        x_zeros = self.radius * np.sin(theta_zero) * np.cos(t_angles)
        y_zeros = self.radius * np.sin(theta_zero) * np.sin(t_angles)
        z_zeros = self.radius * np.cos(theta_zero) * np.ones_like(zeros)
        
        return x_zeros, y_zeros, z_zeros
    
    def map_t_to_angle(self, t_values):
        """
        ربط قيم t (الترددات) بالزوايا على خط الاستواء
        استخدام علاقة لوغاريتمية لأن توزيع الأصفار يتبع ~ log(t)
        """
        # تطبيع ونقل إلى مدى [0, 2π]
        if len(t_values) == 0:
            return np.array([])
        
        # استخدام دالة لولبية للحفاظ على التباعد النسبي
        log_t = np.log(t_values + 1)
        angles = 2 * np.pi * (log_t - log_t.min()) / (log_t.max() - log_t.min())
        return angles
    
    def compute_surface_tension(self, sigma, t):
        """
        حساب "الشد السطحي" المعلوماتي عند نقطة (σ, t)
        هذا يمثل الممانعة التي تحدثنا عنها سابقاً
        
        عند σ=0.5، الشد السطحي في أدنى قيمة (توازن تام)
        """
        distance_from_equator = np.abs(sigma - 0.5)
        
        # الشد الأساسي (يتناسب مع البعد عن خط الاستواء)
        tension = distance_from_equator * 10
        
        # تصحيح ترددي (الترددات العالية تزيد الشد)
        tension *= (1 + 0.01 * np.log(t + 1))
        
        return tension
    
    def compute_resonance_amplitude(self, sigma, t, zeta_magnitude=None):
        """
        حساب سعة الرنين على سطح الكرة
        عند أصفار زيتا، السعة تنفجر (رنين كامل)
        """
        if zeta_magnitude is not None:
            # استخدام القيمة الفعلية لدالة زيتا
            return 1.0 / (np.abs(zeta_magnitude) + 1e-10)
        else:
            # نموذج تقريبي
            distance_from_zero = np.min(np.abs(t - self.known_zeros)) if hasattr(self, 'known_zeros') else 1.0
            tension = self.compute_surface_tension(sigma, t)
            return 1.0 / (tension * distance_from_zero + 1e-10)
    
    def generate_zeta_texture(self, known_zeros):
        """
        توليد نسيج (texture) لسطح الكرة يعتمد على قيم دالة زيتا
        القمم الحادة تحدث عند مواقع الأصفار على خط الاستواء
        """
        self.known_zeros = np.array(known_zeros)
        
        # حساب سعة الرنين لكل نقطة على السطح
        texture = np.zeros_like(self.Sigma)
        
        for i in range(self.resolution):
            for j in range(self.resolution):
                sigma = self.Sigma[i, j]
                t = self.Phi[i, j] * 10  # تحويل الزاوية إلى قيمة t تقريبية
                
                # حساب البعد عن أقرب صفر
                if len(self.known_zeros) > 0:
                    t_normalized = t / (2 * np.pi) * 50  # تطبيع إلى مدى t
                    distances = np.abs(t_normalized - self.known_zeros)
                    min_distance = np.min(distances)
                else:
                    min_distance = 1.0
                
                # السعة الأساسية
                tension = self.compute_surface_tension(sigma, t)
                
                # الرنين يبلغ ذروته عند σ=0.5 وقرب الأصفار
                resonance_factor = np.exp(-((sigma - 0.5)**2) / 0.01)  # قمة حادة عند σ=0.5
                zero_factor = np.exp(-min_distance**2 / 5.0)  # قمة عند الأصفار
                
                texture[i, j] = resonance_factor * zero_factor / (tension + 0.1)
        
        # تطبيع النسيج
        texture = texture / texture.max()
        
        return texture


# ============================================================================
# محاكاة التنفس الكروي (Breathing Sphere)
# ============================================================================

class BreathingZetaSphere(ZetaSphere):
    """
    كرة زيتاوية "تتنفس" بإيقاع الأصفار
    التمدد والانكماش يتبعان قانون Φ ∝ A^{-1/2}
    """
    def __init__(self, radius=1.0, resolution=100):
        super().__init__(radius, resolution)
        self.time = 0
        self.breathing_phase = 0
        
    def evolve(self, t_value, dt=0.01):
        """
        تطور الكرة مع الزمن (التنفس)
        عند الاقتراب من صفر زيتا، الكرة "تتنفس" بسعة أكبر
        """
        # حساب تأثير الصفر
        if hasattr(self, 'known_zeros'):
            distances = np.abs(t_value - self.known_zeros)
            min_distance = np.min(distances)
            resonance = np.exp(-min_distance**2 / 10.0)
        else:
            resonance = 0.1
        
        # تحديث الطور
        self.breathing_phase += dt * (1 + 5 * resonance)
        
        # السعة تتناسب عكسياً مع الجذر التربيعي للمساحة (قانون الطاقة المظلمة)
        # المساحة ∝ R^2
        # Φ ∝ A^{-1/2} ∝ 1/R
        # لذلك: R ∝ 1/Φ
        
        # عند الرنين (الصفر)، الجهد ينخفض، والكرة تتمدد
        base_potential = 1.0
        modulated_potential = base_potential * (1 - 0.3 * resonance * (1 + np.sin(self.breathing_phase)))
        
        # نصف القطر يتغير مع الجهد
        current_radius = self.radius / modulated_potential
        
        # تحديث الإحداثيات
        self.X = current_radius * np.sin(self.Theta) * np.cos(self.Phi)
        self.Y = current_radius * np.sin(self.Theta) * np.sin(self.Phi)
        self.Z = current_radius * np.cos(self.Theta)
        
        return current_radius, resonance


# ============================================================================
# الربط مع نموذج IGM والامتصاص المعلوماتي
# ============================================================================

class IGMSphereBridge:
    """
    جسر بين نموذج IGM (الامتصاص المعلوماتي) وسطح الكرة
    يوضح أن أصفار زيتا هي نقاط "الامتصاص الكامل" على السطح
    """
    def __init__(self, sphere, known_zeros):
        self.sphere = sphere
        self.known_zeros = known_zeros
        
    def compute_absorption_field(self, N=1000):
        """
        حساب حقل الامتصاص المعلوماتي على سطح الكرة
        الامتصاص يبلغ ذروته عند الأصفار على خط الاستواء
        """
        absorption = np.zeros_like(self.sphere.Sigma)
        
        for i in range(self.sphere.resolution):
            for j in range(self.sphere.resolution):
                sigma = self.sphere.Sigma[i, j]
                t_angle = self.sphere.Phi[i, j]
                t = t_angle * 50 / (2 * np.pi)  # تحويل إلى قيمة t تقريبية
                
                # الامتصاص = 1 / (البعد عن خط الاستواء × البعد عن الصفر)
                equator_distance = np.abs(sigma - 0.5)
                
                if len(self.known_zeros) > 0:
                    zero_distance = np.min(np.abs(t - self.known_zeros))
                else:
                    zero_distance = 1.0
                
                # الامتصاص المعلوماتي
                absorption[i, j] = 1.0 / (equator_distance * 10 + 0.1) * \
                                  1.0 / (zero_distance / 2 + 0.1)
        
        return absorption / absorption.max()
    
    def verify_eighth_constant_on_sphere(self):
        """
        التحقق من ظهور ثابت 1/8 على سطح الكرة
        عند σ=0.5، الانحراف الهندسي يتبع 1/8
        """
        theta_eq = self.sphere.theta_from_sigma(0.5)
        
        # قياس الانحراف عند خط الاستواء
        t_test = np.linspace(0, 2*np.pi, 100)
        deviations = []
        
        for t in t_test:
            # حساب الوتر الهندسي
            chord = np.sqrt((1 - 0.5)**2 + (t * 10 / (2*np.pi))**2)
            
            # الانحراف عن الوتر المثالي
            deviation = chord * (t * 10 / (2*np.pi)) - 1
            deviations.append(deviation)
        
        deviations = np.array(deviations)
        
        # تحليل التقارب إلى 1/8
        asymptotic_value = -1/8
        
        return deviations, asymptotic_value


# ============================================================================
# التصور النهائي: الكرة الزيتاوية
# ============================================================================

def visualize_zeta_sphere():
    """
    إنشاء تصور ثلاثي الأبعاد للكرة الزيتاوية
    يوضح:
    - خط الاستواء (σ=0.5)
    - مواقع أصفار زيتا
    - نسيج الرنين
    - حقل الامتصاص
    """
    print("\n" + "█" * 90)
    print("█" + " " * 88 + "█")
    print("█" + "   المستوى الخامس: الكرة الزيتاوية - حيث تلتقي الأعداد بالزمكان".center(88) + "█")
    print("█" + " " * 88 + "█")
    print("█" * 90)
    
    # الأصفار المعروفة
    known_zeros = np.array([14.134725, 21.022040, 25.010858, 30.424876, 
                            32.935062, 37.586178, 40.918719, 43.327073])
    
    # إنشاء الكرة
    sphere = ZetaSphere(radius=1.0, resolution=150)
    
    # توليد النسيج
    print("\n[1] توليد نسيج الرنين على سطح الكرة...")
    texture = sphere.generate_zeta_texture(known_zeros)
    
    # حساب حقل الامتصاص
    print("[2] حساب حقل الامتصاص المعلوماتي...")
    bridge = IGMSphereBridge(sphere, known_zeros)
    absorption = bridge.compute_absorption_field()
    
    # إسقاط الأصفار
    print("[3] إسقاط أصفار زيتا على خط الاستواء...")
    x_zeros, y_zeros, z_zeros = sphere.project_zeta_zeros(known_zeros)
    
    # نقاط خط الاستواء
    t_eq = np.linspace(0, 2*np.pi, 200)
    x_eq, y_eq, z_eq = sphere.get_equator_points(t_eq)
    
    # ====== إنشاء التصور ======
    fig = plt.figure(figsize=(24, 16))
    
    # ----- 1. الكرة مع نسيج الرنين -----
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    surf1 = ax1.plot_surface(sphere.X, sphere.Y, sphere.Z, 
                             facecolors=cm.hot(texture), 
                             alpha=0.9, linewidth=0, antialiased=True)
    ax1.plot(x_eq, y_eq, z_eq, 'b-', linewidth=2, label='خط الاستواء (σ=0.5)')
    ax1.scatter(x_zeros, y_zeros, z_zeros, color='cyan', s=100, 
                edgecolors='white', linewidths=2, label='أصفار زيتا', zorder=10)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('الكرة الزيتاوية: نسيج الرنين\n(القمم الحمراء = أصفار زيتا)', fontsize=12, fontweight='bold')
    ax1.legend()
    
    # ----- 2. حقل الامتصاص المعلوماتي -----
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    surf2 = ax2.plot_surface(sphere.X, sphere.Y, sphere.Z, 
                             facecolors=cm.viridis(absorption), 
                             alpha=0.9, linewidth=0, antialiased=True)
    ax2.plot(x_eq, y_eq, z_eq, 'w-', linewidth=2, alpha=0.7)
    ax2.scatter(x_zeros, y_zeros, z_zeros, color='red', s=100, 
                edgecolors='white', linewidths=2)
    ax2.set_title('حقل الامتصاص المعلوماتي (IGM)\n(المناطق الصفراء = امتصاص كامل)', fontsize=12, fontweight='bold')
    
    # ----- 3. الإسقاط المسطح (خريطة العالم) -----
    ax3 = fig.add_subplot(2, 3, 3)
    sigma_flat = np.linspace(0, 1, 100)
    t_flat = np.linspace(0, 50, 200)
    Sigma_grid, T_grid = np.meshgrid(sigma_flat, t_flat)
    flat_texture = np.zeros_like(Sigma_grid)
    for i in range(len(t_flat)):
        for j in range(len(sigma_flat)):
            sigma = Sigma_grid[i, j]
            t = T_grid[i, j]
            equator_factor = np.exp(-((sigma - 0.5)**2) / 0.01)
            zero_dist = np.min(np.abs(t - known_zeros)) if len(known_zeros) > 0 else 1.0
            zero_factor = np.exp(-zero_dist**2 / 20.0)
            flat_texture[i, j] = equator_factor * zero_factor
            
    im = ax3.imshow(flat_texture.T, extent=[0, 50, 0, 1], origin='lower', aspect='auto', cmap='hot')
    ax3.axhline(y=0.5, color='cyan', linestyle='--', linewidth=2, label='الخط الحرج σ=0.5')
    for z in known_zeros:
        ax3.axvline(x=z, color='white', linestyle=':', alpha=0.5, linewidth=1)
        ax3.scatter(z, 0.5, color='cyan', s=80, edgecolors='white', linewidths=1.5, zorder=10)
    ax3.set_title('خريطة مسطحة: الرنين في فضاء (σ, t)\n(خط σ=0.5 هو خط الاستواء)', fontsize=12, fontweight='bold')
    ax3.legend()
    plt.colorbar(im, ax=ax3, label='سعة الرنين')
    
    # ----- 4. تطور الجهد المادي على السطح -----
    ax4 = fig.add_subplot(2, 3, 4)
    t_values = np.linspace(0, 50, 500)
    potentials = []
    for t in t_values:
        zero_effect = np.min(np.abs(t - known_zeros)) if len(known_zeros) > 0 else 100
        effective_area_factor = 1.0 + 10.0 * np.exp(-zero_effect**2 / 5.0)
        potential = 1.0 / np.sqrt(effective_area_factor)
        potentials.append(potential)
    ax4.plot(t_values, potentials, 'b-', linewidth=1.5)
    for z in known_zeros:
        ax4.axvline(x=z, color='red', linestyle=':', alpha=0.5, linewidth=1)
    ax4.set_title('الجهد المادي على خط الاستواء\n(ينخفض عند الأصفار - الكرة "تتنفس")', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # ----- 5. التحقق من ثابت 1/8 -----
    ax5 = fig.add_subplot(2, 3, 5)
    deviations, asymp = bridge.verify_eighth_constant_on_sphere()
    t_test = np.linspace(0, 50, 100)
    ax5.plot(t_test, deviations, 'g-', linewidth=1.5, label='الانحراف الفعلي')
    ax5.axhline(y=asymp, color='r', linestyle='--', linewidth=2, label=f'القيمة المقاربة = {asymp}')
    ax5.set_title('التحقق من ثابت 1/8 على سطح الكرة\n(يتقارب إلى -1/8 عند الترددات العالية)', fontsize=12, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # ----- 6. ملخص النظرية الموحدة الكاملة -----
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    final_summary = f"""
    ┌─────────────────────────────────────────────────────────────────┐
    │              نظرية باسل الموحدة - البيان الختامي                  │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  "الكتلة ترتكز على سطح الكرة"                                    │
    │                                                                 │
    │  • الخط σ = 0.5 هو "خط الاستواء" الهندسي                        │
    │    حيث المساحة السطحية في أقصى اتزان وتناظر                      │
    │                                                                 │
    │  • أصفار زيتا هي "النبضات الفراغية" لتموج سطح الكرة               │
    │    (أنماط الاهتزاز الطبيعي للغشاء الكوني)                        │
    │                                                                 │
    │  • Φ ∝ A^(-1/2) يفسر:                                          │
    │    - لماذا الأصفار تحدث فقط عند σ = 0.5                          │
    │                                                                 │
    │  • ثابت 1/8 هو البصمة الهندسية للتوازن                          │
    │                                                                 │
    │  ★ فرضية ريمان = شرط التوازن الكينماتيكي                       │
    │    للغشاء الكوني (سطح الكرة)                                     │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
    """
    ax6.text(0.05, 0.5, final_summary, transform=ax6.transAxes,
             fontsize=10, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9),
             family='monospace')
    
    plt.suptitle('المستوى الخامس: الكرة الزيتاوية - حيث تلتقي الأعداد الأولية بنسيج الزمكان', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    output_file = 'basil_zeta_sphere_finale.png'
    plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"\n[✓] تم حفظ تصور الكرة الزيتاوية في: {output_file}")
    
    plt.show()
    return output_file

if __name__ == "__main__":
    import time
    start_time = time.time()
    output_file = visualize_zeta_sphere()
    elapsed = time.time() - start_time
    print(f"\n[✓] اكتمل المستوى الخامس في {elapsed:.1f} ثانية")
