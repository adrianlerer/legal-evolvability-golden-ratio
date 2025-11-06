#!/usr/bin/env python3
"""
Generate Figure 9.1: Constitutional Health Index (CHI) Global Map

This script creates a global choropleth map showing the Constitutional Health Index
(CHI) for 34 countries from the COUNTRY_PARAMETERS database.

CHI = (H × V × α) / (1 + d_φ)

Color scale: Red (low CHI < 0.2) → Orange → Yellow → Green (high CHI > 0.8)

Outputs:
- figures/figure_9.1_chi_global_map.pdf (300 DPI publication quality)
- figures/figure_9.1_chi_global_map.html (interactive plotly visualization)
"""

import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lei_calculator.parameters import COUNTRY_PARAMETERS
from lei_calculator.metrics import calculate_CHI, calculate_d_phi, calculate_LEI
from lei_calculator.visualization import plot_chi_map


def prepare_chi_data():
    """
    Load country parameters and calculate CHI for all countries.
    
    Returns:
        pd.DataFrame: DataFrame with columns [country, H, V, alpha, CHI, d_phi, LEI]
    """
    countries_data = []
    
    for country, params in COUNTRY_PARAMETERS.items():
        # Extract parameters
        H = params['H']
        V = params['V']
        alpha = params['alpha']
        
        # Calculate metrics
        CHI = calculate_CHI(H, V, alpha)
        d_phi = calculate_d_phi(H, V)
        LEI = calculate_LEI(H, V, alpha)
        HV_ratio = H / V
        
        # Clean country name (replace underscores with spaces)
        country_clean = country.replace('_', ' ').title()
        
        countries_data.append({
            'country': country_clean,
            'H': H,
            'V': V,
            'alpha': alpha,
            'CHI': CHI,
            'd_phi': d_phi,
            'LEI': LEI,
            'HV_ratio': HV_ratio
        })
    
    df = pd.DataFrame(countries_data)
    
    # Sort by CHI descending
    df = df.sort_values('CHI', ascending=False).reset_index(drop=True)
    
    return df


def print_chi_statistics(df):
    """Print summary statistics for CHI distribution."""
    print("\n" + "="*70)
    print("CONSTITUTIONAL HEALTH INDEX (CHI) - GLOBAL STATISTICS")
    print("="*70)
    
    print(f"\nNumber of countries: {len(df)}")
    print(f"\nCHI Statistics:")
    print(f"  Mean:   {df['CHI'].mean():.3f}")
    print(f"  Median: {df['CHI'].median():.3f}")
    print(f"  Std:    {df['CHI'].std():.3f}")
    print(f"  Min:    {df['CHI'].min():.3f} ({df.loc[df['CHI'].idxmin(), 'country']})")
    print(f"  Max:    {df['CHI'].max():.3f} ({df.loc[df['CHI'].idxmax(), 'country']})")
    
    # CHI ranges
    print(f"\nCHI Distribution:")
    print(f"  Excellent (CHI > 0.8):     {len(df[df['CHI'] > 0.8]):2d} countries ({100*len(df[df['CHI'] > 0.8])/len(df):5.1f}%)")
    print(f"  Good (0.6 < CHI ≤ 0.8):    {len(df[(df['CHI'] > 0.6) & (df['CHI'] <= 0.8)]):2d} countries ({100*len(df[(df['CHI'] > 0.6) & (df['CHI'] <= 0.8)])/len(df):5.1f}%)")
    print(f"  Moderate (0.4 < CHI ≤ 0.6): {len(df[(df['CHI'] > 0.4) & (df['CHI'] <= 0.6)]):2d} countries ({100*len(df[(df['CHI'] > 0.4) & (df['CHI'] <= 0.6)])/len(df):5.1f}%)")
    print(f"  Poor (0.2 < CHI ≤ 0.4):    {len(df[(df['CHI'] > 0.2) & (df['CHI'] <= 0.4)]):2d} countries ({100*len(df[(df['CHI'] > 0.2) & (df['CHI'] <= 0.4)])/len(df):5.1f}%)")
    print(f"  Critical (CHI ≤ 0.2):      {len(df[df['CHI'] <= 0.2]):2d} countries ({100*len(df[df['CHI'] <= 0.2])/len(df):5.1f}%)")
    
    # Top 10 and Bottom 10
    print(f"\nTop 10 Countries (Highest CHI):")
    print("-" * 70)
    for i, row in df.head(10).iterrows():
        print(f"  {i+1:2d}. {row['country']:20s} CHI={row['CHI']:5.3f}  (H={row['H']:.2f}, V={row['V']:.2f}, α={row['alpha']:.2f}, d_φ={row['d_phi']:.3f})")
    
    print(f"\nBottom 10 Countries (Lowest CHI):")
    print("-" * 70)
    for i, row in df.tail(10).iterrows():
        print(f"  {len(df)-i:2d}. {row['country']:20s} CHI={row['CHI']:5.3f}  (H={row['H']:.2f}, V={row['V']:.2f}, α={row['alpha']:.2f}, d_φ={row['d_phi']:.3f})")
    
    print("\n" + "="*70)


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("GENERATING FIGURE 9.1: CHI GLOBAL MAP")
    print("="*70)
    
    # Prepare data
    print("\n[1/4] Loading country parameters and calculating CHI...")
    df = prepare_chi_data()
    print(f"      ✓ Loaded {len(df)} countries")
    
    # Print statistics
    print_chi_statistics(df)
    
    # Generate PDF version
    print("\n[2/4] Generating static PDF version...")
    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'figures', 'figure_9.1_chi_global_map.pdf')
    try:
        plot_chi_map(df, save_path=pdf_path, interactive=False)
        print(f"      ✓ Saved: {pdf_path}")
    except Exception as e:
        print(f"      ✗ Error generating PDF: {e}")
    
    # Generate HTML version
    print("\n[3/4] Generating interactive HTML version...")
    html_path = os.path.join(os.path.dirname(__file__), '..', 'figures', 'figure_9.1_chi_global_map.html')
    try:
        plot_chi_map(df, save_path=html_path, interactive=True)
        print(f"      ✓ Saved: {html_path}")
    except Exception as e:
        print(f"      ✗ Error generating HTML: {e}")
    
    print("\n[4/4] Complete!")
    print("\n" + "="*70)
    print("FIGURE 9.1 GENERATION COMPLETE")
    print("="*70)
    print(f"\nOutputs:")
    print(f"  - PDF:  {pdf_path}")
    print(f"  - HTML: {html_path}")
    print("\n")


if __name__ == '__main__':
    main()
