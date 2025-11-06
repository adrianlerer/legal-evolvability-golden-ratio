#!/usr/bin/env python3
"""
Generate Figure 9.2: Fibonacci Reform Sequence Diagram

This script illustrates Section IX.B.4 "Approach φ Gradually" - showing how
gradual Fibonacci-scaled reforms lead to success, while "big bang" approaches fail.

The Fibonacci sequence demonstrates optimal reform pacing, with ratios approaching φ:
- Step 1 (Year 1): +0.05
- Step 2 (Year 2): +0.08 (ratio 0.08/0.05 = 1.60 ≈ φ)
- Step 3 (Year 3): +0.13 (ratio 0.13/0.08 = 1.625 ≈ φ)
- Step 4 (Year 5): +0.21 (ratio 0.21/0.13 = 1.615 ≈ φ)
- Step 5 (Year 8): +0.14 (ratio 0.14/0.21 = 0.667 ≈ 1/φ)

Comparison with failed "cliff jump" approach that attempts 60% reform immediately.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Golden ratio constant
PHI = 1.618


def generate_fibonacci_reform_diagram(save_path=None):
    """
    Generate Figure 9.2: Fibonacci Reform Sequence Diagram.
    
    Args:
        save_path (str, optional): Path to save the figure. If None, displays only.
    
    Returns:
        matplotlib.figure.Figure: The generated figure object.
    """
    # Fibonacci reform sequence data
    fib_years = np.array([0, 1, 2, 3, 5, 8, 15])
    fib_increments = np.array([0, 0.05, 0.08, 0.13, 0.21, 0.14, 0])  # Last is 0 for stable endpoint
    fib_cumulative = np.cumsum(fib_increments)
    
    # Calculate ratios between consecutive increments
    ratios = []
    for i in range(2, len(fib_increments)-1):
        if fib_increments[i-1] > 0:
            ratio = fib_increments[i] / fib_increments[i-1]
            ratios.append((i, ratio))
    
    # Failed "big bang" approach data
    fail_years = np.array([0, 1, 3, 5, 10, 15])
    fail_cumulative = np.array([0, 0.60, 0.45, 0.30, 0.15, 0.08])
    
    # Create figure with single axis
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot Fibonacci gradual sequence (stepped line)
    ax.step(fib_years, fib_cumulative, where='post', linewidth=3, 
            color='#2E7D32', label='Fibonacci Sequence (Gradual)', 
            marker='o', markersize=10, markerfacecolor='#2E7D32', 
            markeredgecolor='white', markeredgewidth=2)
    
    # Plot failed big bang approach (dashed line)
    ax.plot(fail_years, fail_cumulative, linestyle='--', linewidth=2.5, 
            color='#C62828', label='Big Bang Approach (Cliff Jump)', 
            marker='x', markersize=12, markeredgewidth=3)
    
    # Add ratio annotations for Fibonacci steps
    annotation_offset = 0.03
    for i, (step, ratio) in enumerate(ratios):
        year = fib_years[step]
        cumulative = fib_cumulative[step]
        
        # Determine if ratio is close to φ or 1/φ
        if ratio > 1:
            ratio_label = f'{ratio:.2f} ≈ φ'
            color = '#1B5E20'
        else:
            ratio_label = f'{ratio:.2f} ≈ 1/φ'
            color = '#1B5E20'
        
        # Place annotation
        ax.annotate(ratio_label, 
                   xy=(year, cumulative), 
                   xytext=(year + 0.5, cumulative + annotation_offset + (i % 2) * 0.04),
                   fontsize=9, fontweight='bold', color=color,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', 
                            edgecolor=color, linewidth=1.5),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    
    # Add increment labels on Fibonacci steps
    for i in range(1, len(fib_years)-1):
        if fib_increments[i] > 0:
            year = fib_years[i]
            cumulative = fib_cumulative[i]
            increment = fib_increments[i]
            ax.text(year - 0.3, cumulative - 0.04, f'+{increment:.2f}',
                   fontsize=9, color='#1B5E20', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                            edgecolor='#2E7D32', linewidth=1))
    
    # Add success/failure annotations
    # Success annotation
    ax.annotate('SUCCESS:\nGradual adaptation\nallows system to\nstabilize at each step', 
               xy=(8, fib_cumulative[5]), 
               xytext=(10.5, 0.55),
               fontsize=10, fontweight='bold', color='#1B5E20',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', 
                        edgecolor='#2E7D32', linewidth=2),
               arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2,
                             connectionstyle='arc3,rad=0.3'))
    
    # Failure annotation
    ax.annotate('FAILURE:\nShock overwhelms\nsystem capacity,\ntriggers backlash', 
               xy=(1, fail_cumulative[1]), 
               xytext=(3, 0.75),
               fontsize=10, fontweight='bold', color='#B71C1C',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFEBEE', 
                        edgecolor='#C62828', linewidth=2),
               arrowprops=dict(arrowstyle='->', color='#C62828', lw=2,
                             connectionstyle='arc3,rad=-0.3'))
    
    # Add Goldilocks Zone shading
    ax.axhspan(0.3, 0.7, alpha=0.1, color='#FFD700', zorder=0)
    ax.text(14, 0.5, 'Goldilocks\nZone', fontsize=10, fontweight='bold',
           color='#F57F17', ha='right', va='center',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', 
                    edgecolor='#F57F17', linewidth=1.5, alpha=0.8))
    
    # Configure axes
    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Cumulative Reform Magnitude', fontsize=13, fontweight='bold')
    ax.set_title('Figure 9.2: Fibonacci Reform Sequence\n' + 
                'Gradual φ-Scaled Reforms vs. Big Bang Approach',
                fontsize=15, fontweight='bold', pad=20)
    
    ax.set_xlim(-0.5, 16)
    ax.set_ylim(-0.05, 0.85)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    
    # Legend
    ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True,
             fancybox=True, framealpha=0.95)
    
    # Add φ reference box
    phi_text = (f'Golden Ratio φ = {PHI:.3f}\n'
               f'Fibonacci ratios converge to φ\n'
               f'Optimal reform pacing maintains\n'
               f'system near evolutionary optimum')
    ax.text(0.02, 0.98, phi_text,
           transform=ax.transAxes, fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', 
                    edgecolor='#F57F17', linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"Saved Figure 9.2 to {save_path}")
        
        # Also print summary statistics
        print("\nFibonacci Reform Sequence Summary:")
        print("="*60)
        print(f"Total reform magnitude: {fib_cumulative[-2]:.2f}")
        print(f"Time to completion: {fib_years[-2]} years")
        print(f"Number of steps: {len([x for x in fib_increments if x > 0])}")
        print(f"\nStep Details:")
        for i in range(1, len(fib_years)-1):
            if fib_increments[i] > 0:
                print(f"  Year {fib_years[i]:2d}: +{fib_increments[i]:.2f} "
                     f"(cumulative: {fib_cumulative[i]:.2f})")
        print(f"\nRatios to φ:")
        for step, ratio in ratios:
            deviation = abs(ratio - PHI) if ratio > 1 else abs(ratio - 1/PHI)
            print(f"  Step {step}: {ratio:.3f} (deviation from target: {deviation:.3f})")
        print("="*60)
    
    return fig


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("GENERATING FIGURE 9.2: FIBONACCI REFORM SEQUENCE")
    print("="*70)
    
    # Generate figure
    save_path = os.path.join(os.path.dirname(__file__), '..', 'figures', 
                            'figure_9.2_fibonacci_reform_sequence.pdf')
    
    print("\n[1/1] Generating Fibonacci reform sequence diagram...")
    fig = generate_fibonacci_reform_diagram(save_path=save_path)
    
    print("\n" + "="*70)
    print("FIGURE 9.2 GENERATION COMPLETE")
    print("="*70)
    print(f"\nOutput: {save_path}")
    print("\n")


if __name__ == '__main__':
    main()
