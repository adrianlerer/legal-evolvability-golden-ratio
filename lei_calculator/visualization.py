"""
Legal Evolvability Index Calculator - Visualization Functions
=============================================================

Publication-ready plotting functions for paper figures.

Key functions:
- plot_darwinian_space_3D(): Figure 5.1 - 3D scatter in (H, V, α) space
- plot_transplant_success(): Figure 8.1 - Success vs d_φ with logistic curve
- plot_chi_map(): Figure 9.1 - Global choropleth map

Based on:
Lerer, I.A. (2025). "Darwinian Spaces and the Golden Ratio"

Author: Ignacio Adrian Lerer
License: MIT
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px

from lei_calculator.metrics import calculate_LEI, calculate_d_phi, calculate_CHI

# Golden Ratio
PHI = (1 + np.sqrt(5)) / 2

# Colorblind-friendly palette
COLORS = {
    'goldilocks': '#2ecc71',  # Green
    'blue_zone': '#3498db',   # Blue
    'yellow_zone': '#f39c12', # Yellow/Orange
    'red_zone': '#e74c3c',    # Red
    'phi_surface': '#f1c40f'  # Gold
}


def plot_darwinian_space_3D(
    countries_data: pd.DataFrame,
    save_path: Optional[str] = None,
    show_goldilocks: bool = True,
    show_phi_surface: bool = True,
    interactive: bool = True
) -> go.Figure:
    """
    Generate 3D scatter plot of countries in Darwinian Space (Figure 5.1).
    
    Creates interactive 3D visualization with:
    - Countries as spheres sized by LEI, colored by zone
    - Golden ratio φ surface (H = φV plane)
    - Goldilocks Zone cylinder
    - Optional trajectories (if 'H_prev', 'V_prev' columns present)
    
    Args:
        countries_data: DataFrame with columns:
            - country: Country name
            - H, V, alpha: Darwinian parameters
            - LEI: Legal Evolvability Index (optional, will calculate)
            - zone: Classification (optional, will calculate)
        save_path: If provided, save as HTML (interactive) or PNG (static)
        show_goldilocks: Display Goldilocks Zone cylinder
        show_phi_surface: Display Golden Ratio surface
        interactive: If True, use Plotly (interactive). If False, use matplotlib (static)
    
    Returns:
        plotly.graph_objects.Figure: Interactive 3D plot
    
    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'country': ['USA', 'Argentina', 'Germany'],
        ...     'H': [0.72, 0.92, 0.75],
        ...     'V': [0.63, 0.18, 0.68],
        ...     'alpha': [0.58, 0.09, 0.65]
        ... })
        >>> fig = plot_darwinian_space_3D(data, save_path='figure_5_1.html')
        >>> # Opens in browser automatically
    """
    # Calculate LEI if not present
    if 'LEI' not in countries_data.columns:
        countries_data['LEI'] = countries_data.apply(
            lambda row: calculate_LEI(row['H'], row['V'], row['alpha']),
            axis=1
        )
    
    # Classify zones if not present
    if 'zone' not in countries_data.columns:
        from lei_calculator.metrics import classify_zone
        countries_data['zone'] = countries_data.apply(
            lambda row: classify_zone(row['H'], row['V'], row['alpha']),
            axis=1
        )
    
    # Map zones to colors
    def get_color(zone_name):
        if 'Goldilocks' in zone_name:
            return COLORS['goldilocks']
        elif 'Rigidity' in zone_name or 'Lock-in' in zone_name:
            return COLORS['red_zone']
        elif 'Chaos' in zone_name:
            return COLORS['yellow_zone']
        else:
            return COLORS['blue_zone']
    
    countries_data['color'] = countries_data['zone'].apply(get_color)
    
    if interactive:
        # Plotly 3D scatter
        fig = go.Figure()
        
        # Add country points
        fig.add_trace(go.Scatter3d(
            x=countries_data['H'],
            y=countries_data['V'],
            z=countries_data['alpha'],
            mode='markers+text',
            marker=dict(
                size=countries_data['LEI'] * 15 + 5,  # Size by LEI
                color=countries_data['color'],
                opacity=0.8,
                line=dict(color='white', width=0.5)
            ),
            text=countries_data['country'],
            textposition='top center',
            textfont=dict(size=9),
            hovertemplate='<b>%{text}</b><br>' +
                          'H: %{x:.3f}<br>' +
                          'V: %{y:.3f}<br>' +
                          'α: %{z:.3f}<br>' +
                          '<extra></extra>',
            name='Countries'
        ))
        
        # Add Golden Ratio φ surface (H = φV plane)
        if show_phi_surface:
            v_mesh = np.linspace(0, 1, 20)
            alpha_mesh = np.linspace(0, 1, 20)
            V_grid, Alpha_grid = np.meshgrid(v_mesh, alpha_mesh)
            H_grid = PHI * V_grid
            H_grid = np.clip(H_grid, 0, 1)  # Clip to valid range
            
            fig.add_trace(go.Surface(
                x=H_grid,
                y=V_grid,
                z=Alpha_grid,
                colorscale=[[0, COLORS['phi_surface']], [1, COLORS['phi_surface']]],
                opacity=0.2,
                showscale=False,
                hoverinfo='skip',
                name='φ Surface (H = φV)'
            ))
        
        # Add Goldilocks Zone cylinder (bounded region)
        if show_goldilocks:
            # Cylinder parameters: H/V ≈ φ, α > 0.5, V > 0.4
            theta = np.linspace(0, 2*np.pi, 30)
            v_cyl = 0.55  # Center V
            radius = 0.15  # Tolerance around φV
            
            for alpha_level in [0.5, 0.8]:
                x_cyl = v_cyl * PHI + radius * np.cos(theta)
                y_cyl = v_cyl + (radius/PHI) * np.sin(theta)
                z_cyl = np.full_like(x_cyl, alpha_level)
                
                fig.add_trace(go.Scatter3d(
                    x=x_cyl,
                    y=y_cyl,
                    z=z_cyl,
                    mode='lines',
                    line=dict(color=COLORS['goldilocks'], width=3, dash='dash'),
                    showlegend=(alpha_level == 0.5),
                    name='Goldilocks Zone',
                    hoverinfo='skip'
                ))
        
        # Layout
        fig.update_layout(
            title='<b>Figure 5.1: Darwinian Space 3D</b><br>' +
                  '<sub>Countries in (H, V, α) coordinates with Golden Ratio φ surface</sub>',
            scene=dict(
                xaxis=dict(title='H (Heredity)', range=[0, 1]),
                yaxis=dict(title='V (Variation)', range=[0, 1]),
                zaxis=dict(title='α (Differential Fitness)', range=[0, 1]),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            width=900,
            height=700,
            font=dict(size=11)
        )
        
        # Save if requested
        if save_path:
            if save_path.endswith('.html'):
                fig.write_html(save_path)
            else:
                fig.write_image(save_path, width=1200, height=900)
            print(f"Saved Figure 5.1 to {save_path}")
        
        return fig
    
    else:
        # Matplotlib static version (simpler, for PDF)
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot countries
        scatter = ax.scatter(
            countries_data['H'],
            countries_data['V'],
            countries_data['alpha'],
            s=countries_data['LEI'] * 200 + 50,
            c=countries_data['color'],
            alpha=0.7,
            edgecolors='white',
            linewidth=1.5
        )
        
        # Labels
        for _, row in countries_data.iterrows():
            ax.text(row['H'], row['V'], row['alpha'], 
                   f"  {row['country']}", size=8)
        
        ax.set_xlabel('H (Heredity)', fontsize=11)
        ax.set_ylabel('V (Variation)', fontsize=11)
        ax.set_zlabel('α (Differential Fitness)', fontsize=11)
        ax.set_title('Figure 5.1: Darwinian Space 3D\n' + 
                     'Countries in (H, V, α) coordinates',
                     fontsize=13, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved Figure 5.1 to {save_path}")
        
        return fig


def plot_transplant_success(
    transplants_data: pd.DataFrame,
    save_path: Optional[str] = None,
    show_regression: bool = True,
    confidence_level: float = 0.95
) -> plt.Figure:
    """
    Generate scatter plot of transplant success vs d_φ with logistic curve (Figure 8.1).
    
    Visualizes core finding: d_φ predicts constitutional transplant success
    with r = -0.78 (p < 0.001).
    
    Args:
        transplants_data: DataFrame with columns:
            - case_id or country: Case identifier
            - H_post, V_post: Post-transplant parameters (or will calculate from d_phi)
            - d_phi or (H_post, V_post): Distance to Golden Ratio
            - success: Binary outcome (0/1)
            - Optional: region, year, gdp_pc (for coloring/sizing)
        save_path: Path to save figure (PNG, PDF)
        show_regression: Display logistic regression curve
        confidence_level: Confidence band level (default: 95%)
    
    Returns:
        matplotlib.figure.Figure
    
    Example:
        >>> # Load dataset
        >>> df = pd.read_csv('data/transplants_60.csv')
        >>> fig = plot_transplant_success(
        ...     df, 
        ...     save_path='figures/figure_8_1_transplant_success.png'
        ... )
        >>> # Displays: scatter + logistic curve + 95% CI + correlation stats
    """
    # Calculate d_φ if not present
    if 'd_phi' not in transplants_data.columns:
        if 'H_post' in transplants_data.columns and 'V_post' in transplants_data.columns:
            transplants_data['d_phi'] = transplants_data.apply(
                lambda row: calculate_d_phi(row['H_post'], row['V_post']),
                axis=1
            )
        else:
            raise ValueError("Need either 'd_phi' or ('H_post', 'V_post') columns")
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Color by region if available
    if 'region' in transplants_data.columns:
        regions = transplants_data['region'].unique()
        palette = sns.color_palette('Set2', len(regions))
        region_colors = dict(zip(regions, palette))
        colors = transplants_data['region'].map(region_colors)
    else:
        colors = COLORS['blue_zone']
    
    # Size by GDP if available
    if 'gdp_pc' in transplants_data.columns:
        sizes = (transplants_data['gdp_pc'] / transplants_data['gdp_pc'].max()) * 200 + 50
    else:
        sizes = 100
    
    # Jitter y-values slightly for visibility (since binary 0/1)
    y_jitter = transplants_data['success'] + np.random.normal(0, 0.02, len(transplants_data))
    y_jitter = np.clip(y_jitter, -0.05, 1.05)
    
    # Scatter plot
    scatter = ax.scatter(
        transplants_data['d_phi'],
        y_jitter,
        c=colors,
        s=sizes,
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    
    # Add logistic regression curve if requested
    if show_regression:
        from sklearn.linear_model import LogisticRegression
        from scipy import stats
        
        X = transplants_data[['d_phi']].values
        y = transplants_data['success'].values
        
        # Fit logistic regression
        model = LogisticRegression()
        model.fit(X, y)
        
        # Generate smooth curve
        d_phi_range = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
        y_pred = model.predict_proba(d_phi_range)[:, 1]
        
        # Plot curve
        ax.plot(d_phi_range, y_pred, 
                color=COLORS['red_zone'], linewidth=3, 
                label=f'Logistic Regression (OR={np.exp(model.coef_[0][0]):.3f})')
        
        # Confidence interval (bootstrap)
        n_bootstrap = 1000
        y_preds_bootstrap = []
        
        for _ in range(n_bootstrap):
            idx = np.random.choice(len(X), len(X), replace=True)
            X_boot, y_boot = X[idx], y[idx]
            model_boot = LogisticRegression()
            model_boot.fit(X_boot, y_boot)
            y_pred_boot = model_boot.predict_proba(d_phi_range)[:, 1]
            y_preds_bootstrap.append(y_pred_boot)
        
        y_preds_bootstrap = np.array(y_preds_bootstrap)
        ci_lower = np.percentile(y_preds_bootstrap, (1-confidence_level)/2 * 100, axis=0)
        ci_upper = np.percentile(y_preds_bootstrap, (1+confidence_level)/2 * 100, axis=0)
        
        ax.fill_between(d_phi_range.flatten(), ci_lower, ci_upper,
                        color=COLORS['red_zone'], alpha=0.2,
                        label=f'{int(confidence_level*100)}% CI')
        
        # Calculate and display statistics
        from scipy.stats import pearsonr, spearmanr
        r_pearson, p_pearson = pearsonr(transplants_data['d_phi'], transplants_data['success'])
        r_spearman, p_spearman = spearmanr(transplants_data['d_phi'], transplants_data['success'])
        
        stats_text = (f"n = {len(transplants_data)}\n"
                     f"r (Pearson) = {r_pearson:.3f} (p = {p_pearson:.3f})\n"
                     f"ρ (Spearman) = {r_spearman:.3f} (p = {p_spearman:.3f})\n"
                     f"β (d_φ) = {model.coef_[0][0]:.3f}")
        
        ax.text(0.02, 0.98, stats_text,
               transform=ax.transAxes,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               fontsize=10, family='monospace')
    
    # Styling
    ax.set_xlabel('d_φ (Distance to Golden Ratio)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Transplant Success (0 = Failure, 1 = Success)', fontsize=13, fontweight='bold')
    ax.set_title('Figure 8.1: Constitutional Transplant Success vs Distance to φ\n' +
                 'Lower d_φ predicts higher success rate',
                 fontsize=14, fontweight='bold', pad=15)
    
    ax.set_ylim(-0.1, 1.1)
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.axhline(1, color='gray', linestyle='--', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    
    # Add success rate bands
    for dphi_band, label in [(0.5, 'High Success\n(d_φ < 0.5)'), 
                              (2.0, 'Low Success\n(d_φ > 2.0)')]:
        if dphi_band < transplants_data['d_phi'].max():
            ax.axvline(dphi_band, color='gray', linestyle=':', alpha=0.5)
            ax.text(dphi_band + 0.05, 0.9, label, fontsize=9, 
                   style='italic', color='gray')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved Figure 8.1 to {save_path}")
    
    return fig


def plot_chi_map(
    countries_chi: pd.DataFrame,
    save_path: Optional[str] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generate global choropleth map of Constitutional Health Index (Figure 9.1).
    
    Args:
        countries_chi: DataFrame with columns:
            - country: Country name (ISO3 code or full name)
            - CHI: Constitutional Health Index [0, 1]
            - Optional: H, V, alpha, LEI, d_phi (for hover info)
        save_path: Path to save (HTML for interactive, PNG for static)
        interactive: If True, use Plotly. If False, use matplotlib/geopandas
    
    Returns:
        plotly.graph_objects.Figure or matplotlib.figure.Figure
    
    Example:
        >>> # Prepare data
        >>> df = pd.DataFrame({
        ...     'country': ['USA', 'DEU', 'ARG', 'CHL', 'BRA'],
        ...     'CHI': [0.651, 0.812, 0.032, 0.487, 0.440]
        ... })
        >>> fig = plot_chi_map(df, save_path='figures/figure_9_1_chi_map.html')
    """
    # Validate CHI values
    if 'CHI' not in countries_chi.columns:
        raise ValueError("DataFrame must have 'CHI' column")
    
    if interactive:
        # Plotly choropleth
        fig = px.choropleth(
            countries_chi,
            locations='country',
            locationmode='country names',  # or 'ISO-3' if using codes
            color='CHI',
            color_continuous_scale=[
                (0.0, COLORS['red_zone']),      # CHI < 0.2: Critical
                (0.2, '#e67e22'),                # CHI 0.2-0.4: Poor
                (0.4, COLORS['yellow_zone']),    # CHI 0.4-0.6: Fair
                (0.6, COLORS['blue_zone']),      # CHI 0.6-0.8: Good
                (0.8, COLORS['goldilocks'])      # CHI > 0.8: Excellent
            ],
            range_color=[0, 1],
            hover_data={col: ':.3f' for col in countries_chi.columns 
                       if col in ['H', 'V', 'alpha', 'LEI', 'd_phi']},
            title='<b>Figure 9.1: Constitutional Health Index (CHI) - Global Map</b><br>' +
                  '<sub>Darker green = healthier institutions (CHI closer to 1.0)</sub>'
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            width=1400,
            height=700,
            coloraxis_colorbar=dict(
                title="CHI",
                tickvals=[0.2, 0.4, 0.6, 0.8],
                ticktext=['Poor', 'Fair', 'Good', 'Excellent']
            )
        )
        
        if save_path:
            if save_path.endswith('.html'):
                fig.write_html(save_path)
            else:
                fig.write_image(save_path, width=1400, height=700)
            print(f"Saved Figure 9.1 to {save_path}")
        
        return fig
    
    else:
        # Static matplotlib version (requires geopandas)
        try:
            import geopandas as gpd
        except ImportError:
            raise ImportError("geopandas required for static map. Install with: pip install geopandas")
        
        # Load world map from Natural Earth
        try:
            world = gpd.read_file(
                'https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip'
            )
        except Exception as e:
            raise RuntimeError(f"Could not load world map data: {e}")
        
        # Merge with CHI data
        world = world.merge(countries_chi, left_on='NAME', right_on='country', how='left')
        
        # Plot
        fig, ax = plt.subplots(figsize=(18, 10))
        world.plot(column='CHI', ax=ax, legend=True, cmap='RdYlGn',
                  missing_kwds={'color': 'lightgrey'},
                  vmin=0, vmax=1,
                  legend_kwds={'label': 'Constitutional Health Index (CHI)',
                              'orientation': 'horizontal',
                              'pad': 0.05})
        
        ax.set_title('Figure 9.1: Constitutional Health Index (CHI) - Global Map',
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved Figure 9.1 to {save_path}")
        
        return fig
