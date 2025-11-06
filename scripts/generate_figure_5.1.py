#!/usr/bin/env python3
"""
Generate Figure 5.1: 3D Darwinian Space

Visualizes legal systems in (H, V, α) parameter space with:
- Countries as spheres sized by LEI
- Color-coded by zone classification
- Golden ratio φ surface (H = φV plane)
- Goldilocks Zone cylinder
"""

import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lei_calculator.parameters import COUNTRY_PARAMETERS
from lei_calculator.metrics import calculate_LEI, calculate_d_phi, classify_zone
from lei_calculator.visualization import plot_darwinian_space_3D

def main():
    """Generate Figure 5.1"""
    print("\n" + "="*70)
    print("GENERATING FIGURE 5.1: 3D DARWINIAN SPACE")
    print("="*70)
    
    # Prepare country data
    countries_data = []
    
    for country, params in COUNTRY_PARAMETERS.items():
        H = params['H']
        V = params['V']
        alpha = params['alpha']
        
        # Calculate metrics
        LEI = calculate_LEI(H, V, alpha)
        d_phi = calculate_d_phi(H, V)
        zone = classify_zone(H, V, alpha)
        
        countries_data.append({
            'country': country.replace('_', ' '),
            'H': H,
            'V': V,
            'alpha': alpha,
            'LEI': LEI,
            'd_phi': d_phi,
            'zone': zone
        })
    
    df = pd.DataFrame(countries_data)
    
    print(f"\nTotal countries: {len(df)}")
    print(f"\nZone distribution:")
    print(df['zone'].value_counts())
    
    print(f"\nLEI statistics:")
    print(df['LEI'].describe())
    
    print(f"\nd_φ statistics:")
    print(df['d_phi'].describe())
    
    # Generate figure (PDF version)
    print("\nGenerating Figure 5.1 (PDF)...")
    fig_pdf = plot_darwinian_space_3D(
        df,
        save_path='../figures/figure_5.1_darwinian_space.pdf',
        show_goldilocks=True,
        show_phi_surface=True,
        interactive=False  # matplotlib version for PDF
    )
    print("  ✓ PDF saved: figures/figure_5.1_darwinian_space.pdf")
    
    # Generate interactive HTML version
    print("\nGenerating Figure 5.1 (Interactive HTML)...")
    fig_html = plot_darwinian_space_3D(
        df,
        save_path='../figures/figure_5.1_darwinian_space.html',
        show_goldilocks=True,
        show_phi_surface=True,
        interactive=True  # Plotly version for HTML
    )
    print("  ✓ HTML saved: figures/figure_5.1_darwinian_space.html")
    
    print("\n" + "="*70)
    print("FIGURE 5.1 GENERATION COMPLETE")
    print("="*70)
    print(f"\n{len(df)} countries plotted in 3D Darwinian Space")
    print("\nKey features:")
    print("  • Golden ratio φ surface (H = φV plane)")
    print("  • Goldilocks Zone cylinder (LEI > 1.0, d_φ < 0.5)")
    print("  • Color-coded by zone classification")
    print("  • Sphere size proportional to LEI")
    print("\nOutputs:")
    print("  • figures/figure_5.1_darwinian_space.pdf (300 DPI)")
    print("  • figures/figure_5.1_darwinian_space.html (interactive)")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
