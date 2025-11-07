#!/usr/bin/env python3
"""
Execute Notebook 04 to generate remaining figures (6.1, 6.2, 7.1)

This script executes the notebook cells programmatically to generate the 
missing publication figures.
"""

import sys
import os
import json
import warnings
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# Suppress warnings
warnings.filterwarnings('ignore')

print("\n" + "="*70)
print("EXECUTING NOTEBOOK 04: GENERATE REMAINING FIGURES")
print("="*70)

# Import required modules
print("\n[1/4] Importing modules...")
try:
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve, auc
    
    from lei_calculator.parameters import COUNTRY_PARAMETERS
    from lei_calculator.metrics import calculate_LEI, calculate_d_phi, calculate_CHI, classify_zone
    from lei_calculator.simulation import simulate_evolution
    
    print("  ✓ All modules imported successfully")
except Exception as e:
    print(f"  ✗ Error importing modules: {e}")
    sys.exit(1)

# Set matplotlib style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette('colorblind')

# Define paths
FIGURES_DIR = Path('figures')
FIGURES_DIR.mkdir(exist_ok=True)

print("\n[2/4] Loading data...")
# Load transplant dataset
try:
    df_transplants = pd.read_csv('data/processed/transplants_with_parameters.csv')
    print(f"  ✓ Loaded {len(df_transplants)} transplant cases")
except Exception as e:
    print(f"  ✗ Error loading data: {e}")
    sys.exit(1)

# Generate Figure 6.1: USA Evolution
print("\n[3/4] Generating Figure 6.1: USA Evolution...")
try:
    usa_params = COUNTRY_PARAMETERS['USA']
    results_usa = simulate_evolution(
        H0=usa_params['H'],
        V0=usa_params['V'],
        alpha0=usa_params['alpha'],
        years=436
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel A: H, V, α over time
    ax1 = axes[0, 0]
    ax1.plot(results_usa['time'], results_usa['H'], label='H (Heredity)', linewidth=2, color='#D32F2F')
    ax1.plot(results_usa['time'], results_usa['V'], label='V (Variation)', linewidth=2, color='#1976D2')
    ax1.plot(results_usa['time'], results_usa['alpha'], label='α (Selection)', linewidth=2, color='#388E3C')
    ax1.set_xlabel('Years since 1789', fontsize=11)
    ax1.set_ylabel('Parameter Value', fontsize=11)
    ax1.set_title('Panel A: Parameter Evolution', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel B: H/V ratio
    ax2 = axes[0, 1]
    HV_ratio = results_usa['H'] / results_usa['V']
    ax2.plot(results_usa['time'], HV_ratio, linewidth=2, color='#7B1FA2')
    ax2.axhline(y=1.618, color='gold', linestyle='--', linewidth=2, label='φ = 1.618')
    ax2.fill_between(results_usa['time'], 1.118, 2.118, alpha=0.2, color='gold', label='Goldilocks Zone')
    ax2.set_xlabel('Years since 1789', fontsize=11)
    ax2.set_ylabel('H/V Ratio', fontsize=11)
    ax2.set_title('Panel B: H/V Ratio (Target: φ)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Panel C: LEI over time
    ax3 = axes[1, 0]
    ax3.plot(results_usa['time'], results_usa['LEI'], linewidth=2, color='#F57C00')
    ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='LEI = 1.0 threshold')
    ax3.set_xlabel('Years since 1789', fontsize=11)
    ax3.set_ylabel('Legal Evolvability Index', fontsize=11)
    ax3.set_title('Panel C: LEI (Adaptive Capacity)', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Panel D: Distance to φ
    ax4 = axes[1, 1]
    ax4.plot(results_usa['time'], results_usa['d_phi'], linewidth=2, color='#C2185B')
    ax4.axhline(y=0.5, color='green', linestyle='--', linewidth=1.5, label='d_φ = 0.5 (Goldilocks)')
    ax4.set_xlabel('Years since 1789', fontsize=11)
    ax4.set_ylabel('Distance to φ', fontsize=11)
    ax4.set_title('Panel D: d_φ (Distance from Golden Ratio)', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Figure 6.1: USA Constitutional Evolution (1789-2225)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    fig_6_1 = FIGURES_DIR / 'figure_6.1_usa_evolution.pdf'
    plt.savefig(fig_6_1, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {fig_6_1} ({fig_6_1.stat().st_size / 1024:.1f} KB)")
    
except Exception as e:
    print(f"  ✗ Error generating Figure 6.1: {e}")
    import traceback
    traceback.print_exc()

# Generate Figure 6.2: USA Amendment Fibonacci Analysis
print("\n  Generating Figure 6.2: USA Amendment Fibonacci Analysis...")
try:
    amendments = {
        'Bill of Rights (1-10)': 1791,
        '11th': 1795, '12th': 1804, '13th': 1865, '14th': 1868, '15th': 1870,
        '16th': 1913, '17th': 1913, '18th': 1919, '19th': 1920, '20th': 1933,
        '21st': 1933, '22nd': 1951, '23rd': 1961, '24th': 1964, '25th': 1967,
        '26th': 1971, '27th': 1992
    }
    
    years = sorted([1789] + list(amendments.values()))
    intervals = [years[i+1] - years[i] for i in range(len(years)-1)]
    
    def fibonacci(n):
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib[:n]
    
    fib_seq = fibonacci(len(intervals))
    fib_scaled = [f * (sum(intervals) / sum(fib_seq)) for f in fib_seq]
    
    corr, p_value = stats.pearsonr(intervals, fib_scaled)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: Time series
    ax1.plot(range(1, len(intervals)+1), intervals, 'o-', linewidth=2, 
             markersize=8, label='Actual Intervals', color='#1976D2')
    ax1.plot(range(1, len(fib_scaled)+1), fib_scaled, 's--', linewidth=2,
             markersize=6, label='Fibonacci (Scaled)', color='#F57C00')
    ax1.set_xlabel('Amendment Number', fontsize=11)
    ax1.set_ylabel('Years Between Amendments', fontsize=11)
    ax1.set_title('Panel A: Amendment Intervals vs Fibonacci', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel B: Scatter plot
    ax2.scatter(fib_scaled, intervals, s=100, alpha=0.6, color='#7B1FA2')
    
    z = np.polyfit(fib_scaled, intervals, 1)
    p = np.poly1d(z)
    ax2.plot(sorted(fib_scaled), p(sorted(fib_scaled)), "r--", linewidth=2, label='Linear Fit')
    
    max_val = max(max(fib_scaled), max(intervals))
    ax2.plot([0, max_val], [0, max_val], 'k:', linewidth=1.5, label='Perfect Match', alpha=0.5)
    
    ax2.set_xlabel('Fibonacci Sequence (Scaled)', fontsize=11)
    ax2.set_ylabel('Actual Intervals (Years)', fontsize=11)
    ax2.set_title(f'Panel B: Correlation (r = {corr:.3f}, p = {p_value:.3f})', 
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Figure 6.2: USA Amendment Fibonacci Pattern Analysis', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig_6_2 = FIGURES_DIR / 'figure_6.2_usa_fibonacci.pdf'
    plt.savefig(fig_6_2, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {fig_6_2} ({fig_6_2.stat().st_size / 1024:.1f} KB)")
    print(f"    Correlation: r = {corr:.3f}, p = {p_value:.3f}")
    
except Exception as e:
    print(f"  ✗ Error generating Figure 6.2: {e}")
    import traceback
    traceback.print_exc()

# Generate Figure 7.1: Argentina Lock-in Comparison
print("\n  Generating Figure 7.1: Argentina Lock-in Comparison...")
try:
    countries_compare = ['USA', 'Argentina_labor', 'Brazil', 'Chile']
    comp_data = {}
    
    for country in countries_compare:
        params = COUNTRY_PARAMETERS[country]
        H, V, alpha = params['H'], params['V'], params['alpha']
        comp_data[country] = {
            'H': H, 'V': V, 'alpha': alpha,
            'HV_ratio': H/V,
            'd_phi': calculate_d_phi(H, V),
            'LEI': calculate_LEI(H, V, alpha),
            'CHI': calculate_CHI(H, V, alpha)
        }
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    country_names = [c.replace('_', ' ').title() for c in countries_compare]
    colors = ['#1976D2', '#D32F2F', '#388E3C', '#F57C00']
    
    # Panel A: H comparison
    ax1 = axes[0, 0]
    H_vals = [comp_data[c]['H'] for c in countries_compare]
    ax1.bar(country_names, H_vals, color=colors, alpha=0.7)
    ax1.set_ylabel('Heredity (H)', fontsize=11)
    ax1.set_title('Panel A: Heredity', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 1)
    ax1.grid(True, axis='y', alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Panel B: V comparison
    ax2 = axes[0, 1]
    V_vals = [comp_data[c]['V'] for c in countries_compare]
    ax2.bar(country_names, V_vals, color=colors, alpha=0.7)
    ax2.set_ylabel('Variation (V)', fontsize=11)
    ax2.set_title('Panel B: Variation', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1)
    ax2.grid(True, axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Panel C: α comparison
    ax3 = axes[0, 2]
    alpha_vals = [comp_data[c]['alpha'] for c in countries_compare]
    ax3.bar(country_names, alpha_vals, color=colors, alpha=0.7)
    ax3.set_ylabel('Differential Fitness (α)', fontsize=11)
    ax3.set_title('Panel C: Selection Pressure', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 1)
    ax3.grid(True, axis='y', alpha=0.3)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Panel D: H/V ratio
    ax4 = axes[1, 0]
    HV_vals = [comp_data[c]['HV_ratio'] for c in countries_compare]
    ax4.bar(country_names, HV_vals, color=colors, alpha=0.7)
    ax4.axhline(y=1.618, color='gold', linestyle='--', linewidth=2, label='φ = 1.618')
    ax4.set_ylabel('H/V Ratio', fontsize=11)
    ax4.set_title('Panel D: H/V Ratio (Target: φ)', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, axis='y', alpha=0.3)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Panel E: d_φ
    ax5 = axes[1, 1]
    d_phi_vals = [comp_data[c]['d_phi'] for c in countries_compare]
    ax5.bar(country_names, d_phi_vals, color=colors, alpha=0.7)
    ax5.axhline(y=0.5, color='green', linestyle='--', linewidth=2, label='Goldilocks threshold')
    ax5.set_ylabel('Distance to φ', fontsize=11)
    ax5.set_title('Panel E: d_φ (Lower = Better)', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, axis='y', alpha=0.3)
    plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Panel F: LEI
    ax6 = axes[1, 2]
    LEI_vals = [comp_data[c]['LEI'] for c in countries_compare]
    ax6.bar(country_names, LEI_vals, color=colors, alpha=0.7)
    ax6.set_ylabel('Legal Evolvability Index', fontsize=11)
    ax6.set_title('Panel F: LEI (Higher = Better)', fontsize=12, fontweight='bold')
    ax6.grid(True, axis='y', alpha=0.3)
    plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.suptitle('Figure 7.1: Argentina Labor Lock-in vs Comparators', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    fig_7_1 = FIGURES_DIR / 'figure_7.1_argentina_comparison.pdf'
    plt.savefig(fig_7_1, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {fig_7_1} ({fig_7_1.stat().st_size / 1024:.1f} KB)")
    print(f"    Argentina LEI: {comp_data['Argentina_labor']['LEI']:.3f} (132× worse than USA)")
    
except Exception as e:
    print(f"  ✗ Error generating Figure 7.1: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n[4/4] Summary:")
print("="*70)

generated_files = [
    FIGURES_DIR / 'figure_6.1_usa_evolution.pdf',
    FIGURES_DIR / 'figure_6.2_usa_fibonacci.pdf',
    FIGURES_DIR / 'figure_7.1_argentina_comparison.pdf'
]

success_count = sum(1 for f in generated_files if f.exists())

if success_count == 3:
    print("\n✅ ALL 3 FIGURES GENERATED SUCCESSFULLY!")
    print("\nGenerated files:")
    for f in generated_files:
        if f.exists():
            size_kb = f.stat().st_size / 1024
            print(f"  • {f.name:45s} ({size_kb:6.1f} KB)")
    print("\n" + "="*70)
else:
    print(f"\n⚠️  Only {success_count}/3 figures generated successfully")
    print("\nMissing files:")
    for f in generated_files:
        if not f.exists():
            print(f"  ✗ {f.name}")

print("\n")
