"""
Mutation Engine Visual Metaphor Tool

⚠️ SPECULATIVE CODE - PATH 2 - NOT VALIDATED

Purpose: Generate mutation-style visualizations for legal evolution
         as creative/pedagogical tool.

Suitable for: Blog posts, teaching materials, creative articles
NOT suitable for: Peer-reviewed papers, empirical claims

Author: Ignacio Adrian Lerer
Email: adrian@lerer.com.ar
Last updated: November 7, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Optional
import warnings

# Add speculative warning
warnings.warn(
    "\n"
    "╔═══════════════════════════════════════════════════════════╗\n"
    "║  ⚠️  SPECULATIVE MODULE - NOT VALIDATED                  ║\n"
    "║                                                           ║\n"
    "║  This module generates METAPHORICAL visualizations only. ║\n"
    "║  Do NOT use for empirical claims or peer review.         ║\n"
    "║  For validated analysis, use PATH 1 tools.               ║\n"
    "╚═══════════════════════════════════════════════════════════╝\n",
    UserWarning
)


def classify_evolution_zone(d_phi: float) -> Dict[str, str]:
    """
    Classify legal evolution zone based on d_phi (METAPHORICAL).
    
    ⚠️ WARNING: This classification is CONCEPTUAL ONLY.
    
    Args:
        d_phi: Distance to golden ratio φ
        
    Returns:
        Dictionary with color, label, and stability assessment
    """
    if d_phi < 0.5:
        return {
            'color': 'green',
            'label': 'Stable Evolution (Goldilocks)',
            'stability': 'high',
            'metaphor': 'Low mutation rate (stable genome)'
        }
    elif d_phi < 1.0:
        return {
            'color': 'yellow',
            'label': 'Moderate Drift (Transition)',
            'stability': 'medium',
            'metaphor': 'Moderate mutation rate (adapting)'
        }
    elif d_phi < 2.0:
        return {
            'color': 'orange',
            'label': 'High Instability (Risk Zone)',
            'stability': 'low',
            'metaphor': 'High mutation rate (stressed)'
        }
    else:
        return {
            'color': 'red',
            'label': 'Terminal Lock-in (Collapse)',
            'stability': 'critical',
            'metaphor': 'Lethal mutation rate (extinction)'
        }


def generate_circular_pattern(d_phi: float, n_circles: int = 50, 
                              n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate circular propagation pattern (METAPHORICAL representation).
    
    ⚠️ This function generates VISUAL METAPHORS, not empirical data.
    
    Args:
        d_phi: Distance to golden ratio
        n_circles: Number of concentric circles
        n_points: Points per circle
        
    Returns:
        theta, r: Polar coordinates for plotting
    """
    theta = np.linspace(0, 2*np.pi, n_points)
    r_values = np.linspace(0, d_phi, n_circles)
    
    return theta, r_values


def visualize_mutation_metaphor(H: float, V: float, alpha: float,
                                country_name: str = "Legal System",
                                save_path: Optional[str] = None) -> plt.Figure:
    """
    Generate mutation-engine style visualization for legal evolution.
    
    ⚠️ CRITICAL WARNING: This is a METAPHORICAL visualization ONLY.
    Do NOT interpret as empirical analysis. Use for creative/pedagogical
    purposes only (blog posts, teaching materials).
    
    Args:
        H: Heredity parameter [0, 1]
        V: Variation parameter [0, 1]
        alpha: Differential fitness parameter [0, 1]
        country_name: Name for plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
        
    Example:
        >>> fig = visualize_mutation_metaphor(0.72, 0.63, 0.58, "USA")
        >>> # ⚠️ For blog posts only, NOT for peer review
    """
    # Calculate d_phi
    phi = 1.618
    d_phi = abs(H/V - phi)
    
    # Get zone classification
    zone = classify_evolution_zone(d_phi)
    
    # Generate pattern data
    theta, r_values = generate_circular_pattern(d_phi)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot concentric circles with decreasing opacity
    for i, r_val in enumerate(r_values):
        alpha_val = 1.0 - (i / len(r_values)) * 0.7  # Fade outward
        ax.plot(theta, [r_val]*len(theta), 
                color=zone['color'], 
                alpha=alpha_val,
                linewidth=1.5)
    
    # Add radial "mutation" lines (metaphor for variation)
    n_radial = int(V * 50)  # More lines = higher variation
    for angle in np.linspace(0, 2*np.pi, n_radial):
        ax.plot([angle, angle], [0, d_phi], 
                color=zone['color'], 
                alpha=0.2,
                linewidth=0.5)
    
    # Title with parameters
    ax.set_title(
        f"Legal Evolution Pattern: {country_name}\n"
        f"(METAPHORICAL VISUALIZATION)\n\n"
        f"H={H:.2f} | V={V:.2f} | α={alpha:.2f} | d_φ={d_phi:.2f}\n"
        f"{zone['label']}",
        fontsize=14,
        pad=20
    )
    
    # Add zone label
    ax.text(0, d_phi * 1.1, 
            f"Metaphor: {zone['metaphor']}",
            ha='center',
            fontsize=10,
            style='italic',
            color=zone['color'])
    
    # Add parameter annotations
    param_text = (
        f"Parameters (validated):\n"
        f"• Heredity (H): {H:.2f}\n"
        f"• Variation (V): {V:.2f}\n"
        f"• Selection (α): {alpha:.2f}\n\n"
        f"Derived metrics:\n"
        f"• d_φ: {d_phi:.3f}\n"
        f"• H/V ratio: {H/V:.3f}\n"
        f"• Target (φ): 1.618"
    )
    
    fig.text(0.02, 0.98, param_text,
             transform=fig.transFigure,
             fontsize=9,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Add prominent warning watermark
    fig.text(0.5, 0.02, 
             '⚠️ SPECULATIVE VISUALIZATION - NOT VALIDATED - FOR CREATIVE USE ONLY ⚠️', 
             ha='center', 
             fontsize=12, 
             color='red', 
             weight='bold',
             transform=fig.transFigure)
    
    # Add PATH 2 badge
    fig.text(0.98, 0.02,
             'PATH 2\n(Speculative)',
             ha='right',
             fontsize=9,
             color='red',
             weight='bold',
             transform=fig.transFigure,
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved to: {save_path}")
        print("⚠️ WARNING: This is a speculative visualization. Include disclaimer if sharing.")
    
    return fig


def compare_mutation_patterns(countries: Dict[str, Tuple[float, float, float]],
                              save_path: Optional[str] = None) -> plt.Figure:
    """
    Compare mutation-style patterns across multiple legal systems.
    
    ⚠️ WARNING: METAPHORICAL COMPARISON ONLY.
    
    Args:
        countries: Dict mapping country names to (H, V, alpha) tuples
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure with subplots
        
    Example:
        >>> countries = {
        ...     'USA': (0.72, 0.63, 0.58),
        ...     'Argentina': (0.92, 0.18, 0.09)
        ... }
        >>> fig = compare_mutation_patterns(countries)
        >>> # ⚠️ For creative visualization only
    """
    n_countries = len(countries)
    fig = plt.figure(figsize=(15, 5 * ((n_countries + 1) // 2)))
    
    phi = 1.618
    
    for idx, (country_name, (H, V, alpha)) in enumerate(countries.items(), 1):
        ax = fig.add_subplot((n_countries + 1) // 2, 2, idx, projection='polar')
        
        d_phi = abs(H/V - phi)
        zone = classify_evolution_zone(d_phi)
        theta, r_values = generate_circular_pattern(d_phi, n_circles=30)
        
        # Plot pattern
        for i, r_val in enumerate(r_values):
            alpha_val = 1.0 - (i / len(r_values)) * 0.7
            ax.plot(theta, [r_val]*len(theta), 
                    color=zone['color'], 
                    alpha=alpha_val,
                    linewidth=1.5)
        
        # Add radial lines
        n_radial = max(5, int(V * 30))
        for angle in np.linspace(0, 2*np.pi, n_radial):
            ax.plot([angle, angle], [0, d_phi], 
                    color=zone['color'], 
                    alpha=0.2,
                    linewidth=0.5)
        
        ax.set_title(
            f"{country_name}\n"
            f"H={H:.2f}, V={V:.2f}, α={alpha:.2f}\n"
            f"d_φ={d_phi:.2f} ({zone['label']})",
            fontsize=11
        )
    
    fig.suptitle(
        "Legal Evolution Pattern Comparison (METAPHORICAL)\n"
        "⚠️ For Creative Visualization Only - Not Empirical Analysis",
        fontsize=16,
        weight='bold',
        color='red'
    )
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved to: {save_path}")
        print("⚠️ WARNING: Speculative comparison. Include disclaimer.")
    
    return fig


def print_usage_guidelines():
    """Print guidelines for using this speculative tool."""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                   MUTATION METAPHOR USAGE GUIDE                   ║
╚═══════════════════════════════════════════════════════════════════╝

✅ APPROPRIATE USES:
  • Blog posts (with disclaimer)
  • Teaching materials (labeled "conceptual metaphor")
  • Public lectures (with verbal disclaimer)
  • Creative articles (with warnings)
  • Brainstorming sessions

❌ INAPPROPRIATE USES:
  • Peer-reviewed journal papers
  • Grant proposals
  • Policy recommendations
  • Expert testimony
  • Academic dissertations (main text)

🚨 REQUIRED DISCLAIMER:
  "This visualization is a METAPHORICAL representation inspired by
   mutation dynamics. It has NOT been empirically validated and should
   NOT be interpreted as evidence of a relationship between biological
   mutation rates and legal evolution. For validated analysis, see
   PATH 1 tools in the main repository."

📚 VALIDATION PATHWAY:
  If you want to test this hypothesis empirically:
  1. Formalize testable hypothesis
  2. Gather data (mutation rates + legal parameters)
  3. Run statistical tests (correlation, regression)
  4. If significant (p < 0.05): Promote to PATH 1
  5. Otherwise: Remains creative metaphor

📧 Questions? adrian@lerer.com.ar
    """)


# Example usage (if run as script)
if __name__ == "__main__":
    print_usage_guidelines()
    
    print("\n" + "="*70)
    print("GENERATING EXAMPLE VISUALIZATIONS (SPECULATIVE)")
    print("="*70 + "\n")
    
    # Example 1: USA (Goldilocks Zone)
    print("1. USA (Goldilocks Zone) - METAPHORICAL")
    fig_usa = visualize_mutation_metaphor(
        H=0.72, V=0.63, alpha=0.58,
        country_name="USA",
        save_path="mutation_metaphor_usa_SPECULATIVE.png"
    )
    plt.show()
    
    # Example 2: Argentina (Lock-in)
    print("\n2. Argentina Labor (Terminal Lock-in) - METAPHORICAL")
    fig_arg = visualize_mutation_metaphor(
        H=0.92, V=0.18, alpha=0.09,
        country_name="Argentina Labor",
        save_path="mutation_metaphor_argentina_SPECULATIVE.png"
    )
    plt.show()
    
    # Example 3: Comparison
    print("\n3. Comparative Analysis - METAPHORICAL")
    countries = {
        'USA': (0.72, 0.63, 0.58),
        'Argentina Labor': (0.92, 0.18, 0.09),
        'Brazil': (0.61, 0.68, 0.52),
        'Chile': (0.65, 0.61, 0.44)
    }
    
    fig_compare = compare_mutation_patterns(
        countries,
        save_path="mutation_comparison_SPECULATIVE.png"
    )
    plt.show()
    
    print("\n" + "="*70)
    print("✓ Examples generated (saved with SPECULATIVE suffix)")
    print("⚠️ REMEMBER: These are METAPHORS, not empirical evidence")
    print("="*70)
