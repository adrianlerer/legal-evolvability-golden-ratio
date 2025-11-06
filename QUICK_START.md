# Quick Start Guide

**Repository**: https://github.com/adrianlerer/legal-evolvability-golden-ratio  
**Current Status**: v0.2.0 - Core modules complete (35% done)

---

## Installation

```bash
cd legal-evolvability-golden-ratio
pip install -r requirements.txt
```

---

## Basic Usage

### Calculate Parameters for a Country

```python
from lei_calculator.parameters import calculate_H, calculate_V, calculate_alpha
from lei_calculator.metrics import calculate_LEI, calculate_d_phi, comprehensive_metrics

# Example: USA
H = calculate_H(precedent_strength=0.9, const_rigidity=0.85,
                codification=0.5, judicial_tenure=0.65)
V = calculate_V(federal_autonomy=0.75, amendment_freq=0.4,
                judicial_review=0.85, legislative_turnover=0.5)
alpha = calculate_alpha(compliance_rate=0.75, transparency_score=0.7,
                        enforcement_capacity=0.65, legitimacy_index=0.4)

# Calculate metrics
LEI = calculate_LEI(H, V, alpha)
d_phi = calculate_d_phi(H, V)

print(f"USA: H={H}, V={V}, α={alpha}")
print(f"LEI={LEI}, d_φ={d_phi}")

# Or get full report
comprehensive_metrics(H, V, alpha, "USA")
```

### Simulate Temporal Evolution

```python
from lei_calculator.simulation import simulate_evolution

# Simulate USA trajectory for 200 years
results = simulate_evolution(
    H0=0.72, V0=0.63, alpha0=0.58,
    years=200,
    scenario='baseline'
)

# Plot convergence to golden ratio
import matplotlib.pyplot as plt
plt.plot(results['time'], results['d_phi'])
plt.xlabel('Years')
plt.ylabel('Distance to φ')
plt.title('USA Constitutional Evolution')
plt.show()
```

### Generate Figures

```python
from lei_calculator.visualization import plot_transplant_success
import pandas as pd

# Load transplant data
df = pd.read_csv('data/processed/transplants_with_parameters.csv')

# Generate Figure 8.1
fig = plot_transplant_success(
    df,
    save_path='figures/figure_8.1_transplant_success.pdf',
    show_regression=True
)
```

---

## Run Validation Analysis

Reproduce Table 8.3 and Figure 8.1 from paper:

```bash
python scripts/validate_transplant_regression.py
```

**Output**:
- Table 8.3 printed to console (logistic regression results)
- `figures/figure_8.1_transplant_success.pdf` generated
- `data/processed/transplants_with_parameters.csv` saved

**Expected results**:
- n = 60 cases
- Pearson r ≈ -0.78 (strong negative correlation)
- p < 0.01 (highly significant)
- Success rate when d_φ < 0.5: ~100%
- Success rate when d_φ > 2.0: ~0%

---

## Available Functions

### lei_calculator.parameters
- `calculate_H()` - Heredity from 4 proxies
- `calculate_V()` - Variation from 4 proxies
- `calculate_alpha()` - Differential Fitness from 4 proxies

### lei_calculator.metrics
- `calculate_LEI()` - Legal Evolvability Index
- `calculate_d_phi()` - Distance to golden ratio
- `calculate_CHI()` - Constitutional Health Index
- `classify_zone()` - Goldilocks/High Rigidity/etc.
- `comprehensive_metrics()` - Full diagnostic report

### lei_calculator.simulation
- `simulate_evolution()` - ODE temporal evolution
- `simulate_multiple_trajectories()` - 100 random ICs
- `predict_future_trajectory()` - Scenario forecasting
- `calculate_equilibrium()` - H*/V* = φ calculation

### lei_calculator.visualization
- `plot_darwinian_space_3D()` - 3D scatter (Figure 5.1)
- `plot_transplant_success()` - Logistic regression (Figure 8.1)
- `plot_chi_map()` - Global choropleth (Figure 9.1)

---

## Project Structure

```
legal-evolvability-golden-ratio/
├── lei_calculator/           # Core Python package
│   ├── __init__.py
│   ├── parameters.py         # H, V, α calculations
│   ├── metrics.py            # LEI, d_φ, CHI
│   ├── simulation.py         # ODE evolution
│   └── visualization.py      # Publication figures
├── scripts/                  # Analysis scripts
│   └── validate_transplant_regression.py
├── data/
│   └── processed/
│       └── transplants_with_parameters.csv
├── figures/
│   └── figure_8.1_transplant_success.pdf
├── README.md                 # Full documentation
├── PROJECT_STATUS.md         # Progress tracking
├── SESSION_2_SUMMARY.md      # Detailed handoff
└── requirements.txt          # Dependencies
```

---

## Next Steps

See `PROJECT_STATUS.md` for detailed roadmap.

**High priority remaining (~5 hours)**:
1. Create Jupyter Notebook 03 (Transplants)
2. Generate Figure 5.1 (3D Darwinian Space)
3. Generate Figure 8.2 (ROC curve)
4. Create Notebooks 01-02 (USA, Argentina)
5. Write Appendix B (dataset docs)

---

## Getting Help

- Full documentation: `README.md`
- Progress tracking: `PROJECT_STATUS.md`
- Session details: `SESSION_2_SUMMARY.md`
- Paper: [SSRN link when available]
- Issues: https://github.com/adrianlerer/legal-evolvability-golden-ratio/issues

---

**Last updated**: November 6, 2025 (Session 2)
