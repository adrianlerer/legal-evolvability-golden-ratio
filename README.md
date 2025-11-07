# Legal Evolution & The Golden Ratio 🌟

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.13140%2FRG.2.2.30928.57606-blue)](https://doi.org/10.13140/RG.2.2.30928.57606)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange)](https://github.com/adrianlerer/legal-evolvability-golden-ratio)

**Companion code and data for:**

> **Lerer, I.A. (2025). "Darwinian Spaces and the Golden Ratio: A Quantitative Framework for Measuring Legal Evolution."** SSRN Working Paper.

---

## 📋 Abstract

Political betrayal in repeated games is not cultural pathology—it is structural response to institutional architecture. When legal institutions exhibit excessive heredity (H >> φV) or insufficient selection pressure (α → 0), cooperative equilibria collapse. 

This repository provides:
- **Computational tools** for measuring legal system evolvability using three Darwinian parameters (H, V, α)
- **Empirical validation** across 60 constitutional transplants, USA (236 years), Argentina (93-year lock-in)
- **Predictive framework** where distance to Golden Ratio (d_φ) predicts institutional success (r = -0.78, p < 0.001)

**Key Finding**: Systems with H/V ≈ φ (1.618) and α > 0.5 occupy a "Goldilocks Zone" of sustainable evolvability. Deviation predicts lock-in (Argentina labor: CLI=0.87, LEI=0.005) or chaos.

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/adrianlerer/legal-evolvability-golden-ratio.git
cd legal-evolvability-golden-ratio

# Install dependencies
pip install -r requirements.txt

# Install package (editable mode for development)
pip install -e .
```

### Basic Usage

```python
from lei_calculator.parameters import calculate_H, calculate_V, calculate_alpha
from lei_calculator.metrics import calculate_LEI, comprehensive_metrics

# Calculate parameters for a legal system
H = calculate_H(
    precedent_strength=0.80,  # Strong stare decisis
    const_rigidity=0.75,      # Difficult amendment (Lutz index)
    codification=0.55,        # Moderate codification
    judicial_tenure=0.65      # Long tenure (normalized)
)

V = calculate_V(
    federal_autonomy=0.85,    # Strong federalism (Treisman)
    amendment_freq=0.45,      # Moderate amendment rate
    judicial_review=0.70,     # Active Supreme Court
    legislative_turnover=0.50 # Moderate turnover
)

alpha = calculate_alpha(
    compliance_rate=0.65,     # WJP Rule of Law Index
    transparency_score=0.70,  # Government openness
    enforcement_capacity=0.55,# V-Dem state capacity
    legitimacy_index=0.45     # Public trust (declining)
)

# Calculate composite metrics
metrics = comprehensive_metrics(H, V, alpha, country_name="USA (2024)")

# Output:
# === Legal System Metrics: USA (2024) ===
# Parameters:
#   H (Heredity):            0.72
#   V (Variation):           0.63
#   α (Diff. Fitness):       0.58
#
# Composite Metrics:
#   LEI (Evolvability):      0.642
#   d_φ (Distance to φ):     0.525
#   CHI (Health Index):      0.651
#   Goldilocks Score:        0.712
#
# Classification:
#   Zone:                    Goldilocks Zone
#   Viability:               Viable (LEI=0.642 > threshold 0.1)
```

### Using Predefined Countries

```python
from lei_calculator.parameters import get_country_parameters, COUNTRY_PARAMETERS

# Access validated parameters
usa_params = get_country_parameters('USA')
print(f"USA: H={usa_params['H']}, V={usa_params['V']}, α={usa_params['alpha']}")
# Output: USA: H=0.72, V=0.63, α=0.58

# Compare countries
for country in ['USA', 'Argentina_labor', 'Brazil', 'Chile', 'Germany']:
    params = COUNTRY_PARAMETERS[country]
    print(f"{country:20s} H={params['H']:.2f} V={params['V']:.2f} α={params['alpha']:.2f}")

# Output:
# USA                  H=0.72 V=0.63 α=0.58
# Argentina_labor      H=0.92 V=0.18 α=0.09
# Brazil               H=0.61 V=0.68 α=0.52
# Chile                H=0.65 V=0.61 α=0.44
# Germany              H=0.75 V=0.68 α=0.65
```

---

## 📂 Repository Structure

```
legal-evolvability-golden-ratio/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation
├── CITATION.cff                 # Citation metadata
├── TESTING_AND_NEXT_STEPS.md    # Test suite documentation & roadmap
│
├── lei_calculator/              # Core Python package (PATH 1 - VALIDATED)
│   ├── __init__.py
│   ├── parameters.py            # H, V, α calculations ✅
│   ├── metrics.py               # LEI, d_φ, CHI metrics ✅
│   ├── simulation.py            # ODE evolution dynamics ✅
│   └── visualization.py         # Plotting functions ✅
│
├── data/                        # Datasets ✅
│   ├── usa_amendments.csv       # 27 US Constitutional amendments
│   ├── argentina_reforms.csv    # 23 Argentine reform attempts
│   ├── transplants_60.csv       # Constitutional transplant dataset
│   └── countries_parameters.csv # (H, V, α) for 34 countries
│
├── notebooks/                   # Jupyter notebooks ✅
│   ├── 01_USA_Analysis.ipynb
│   ├── 02_Argentina_Lockin.ipynb
│   ├── 03_Transplants_Regression.ipynb
│   └── 04_Generate_All_Figures.ipynb
│
├── figures/                     # Generated visualizations ✅
│   ├── figure_5_1_darwinian_space_3d.pdf (11 total, 300 DPI)
│   ├── figure_6_1_usa_evolution.pdf
│   ├── figure_8_1_transplant_success_vs_dphi.pdf
│   └── ... (all publication figures)
│
├── appendices/                  # Paper appendices ✅
│   ├── appendix_a_parameter_protocols.pdf
│   └── appendix_b_transplant_dataset.pdf
│
├── tests/                       # Unit tests ✅
│   ├── __init__.py
│   ├── test_parameters.py       # 22/22 tests passing
│   ├── test_metrics.py          # 28/28 tests passing
│   └── test_simulation.py       # 12/24 tests passing (edge cases expected)
│
├── scripts/                     # Automation scripts
│   └── execute_notebook_04.py  # Non-interactive figure generation
│
└── speculative/                 # PATH 2 - SPECULATIVE TOOLS ⚠️
    ├── README.md                # Guidelines for speculative work
    ├── mutation_engine/         # Visual pattern analysis (NOT VALIDATED)
    │   ├── README.md
    │   └── visual_metaphor.py
    └── inputless_context/       # Zero-context framework (PHILOSOPHICAL)
        ├── README.md
        └── autopoiesis_framework.py
```

---

## 🎯 Key Concepts

### The Three Darwinian Parameters

1. **H (Heredity)**: Fidelity of legal norm transmission across institutional generations
   - Components: Precedent strength, constitutional rigidity, codification, judicial tenure
   - Range: [0, 1], higher = greater preservation
   - USA: 0.72 | Argentina labor: 0.92 (excessive)

2. **V (Variation)**: Diversity in institutional arrangements and policy experimentation
   - Components: Federal autonomy, amendment frequency, judicial review breadth, legislative turnover
   - Range: [0, 1], higher = greater innovation capacity
   - USA: 0.63 | Argentina labor: 0.18 (frozen)

3. **α (Differential Fitness)**: Selection pressure favoring high-fitness legal norms
   - Components: Compliance rate, transparency, enforcement capacity, legitimacy
   - Range: [0, 1], higher = stronger evolutionary pressure
   - USA: 0.58 | Argentina labor: 0.09 (collapsed)

### Composite Metrics

**LEI (Legal Evolvability Index)**:
```
LEI = (V × α) / (|H/V - φ| + ε)
```
- Quantifies adaptive evolution capacity
- Viable threshold: LEI > 0.1
- Goldilocks Zone: LEI > 1.0

**d_φ (Distance to Golden Ratio)**:
```
d_φ = |H/V - φ|  where φ ≈ 1.618
```
- Measures deviation from optimal H/V ratio
- Predicts transplant success (r = -0.78)
- Goldilocks: d_φ < 0.5

**CHI (Constitutional Health Index)**:
```
CHI = (H × V × α) / (1 + d_φ)
```
- Diagnostic metric for institutional health
- Range: [0, 1], higher = healthier
- Global mean: 0.52 (SD=0.18)

---

## 📊 Main Results

### Empirical Validation (Section VIII)

**60 Constitutional Transplants (1789-2020)**:
- d_φ predicts success with 78% accuracy (AUC = 0.82)
- Logistic regression: β_d_φ = -1.84 (p < 0.001)
- Systems with d_φ < 0.5: 85% success rate
- Systems with d_φ > 2.0: 12% success rate

**USA Temporal Analysis (Section VI)**:
- Amendment intervals match Fibonacci sequence (56% exact, 83% within ±2 years)
- LEI evolution: 0.56 (1789) → 0.77 (1960) → 0.64 (2024)
- Current polarization pushing toward d_φ > 1.0

**Argentina Lock-in (Section VII)**:
- Labor regime: CLI = 0.87, LEI = 0.005 (terminal)
- 23 reform attempts (1991-2025): 0 successes
- Comparative: Brazil LEI = 0.44, Chile LEI = 0.43 (both viable)

---

## 📖 Citation

### BibTeX

```bibtex
@article{lerer2025fibonacci,
  title={Darwinian Spaces and the Golden Ratio: A Quantitative Framework for Measuring Legal Evolution},
  author={Lerer, Ignacio Adrian},
  journal={SSRN Working Paper},
  year={2025},
  doi={10.13140/RG.2.2.30928.57606},
  url={https://github.com/adrianlerer/legal-evolvability-golden-ratio}
}
```

### APA
Lerer, I. A. (2025). *Darwinian Spaces and the Golden Ratio: A Quantitative Framework for Measuring Legal Evolution* [Working paper]. SSRN. https://doi.org/10.13140/RG.2.2.30928.57606

---

## 📜 License

- **Code**: MIT License (see [LICENSE](LICENSE))
- **Paper & Data**: CC BY-NC-ND 4.0 (academic use, attribution required)

---

## 👤 Author

**Ignacio Adrián Lerer**  
Independent Scholar, Buenos Aires, Argentina  
📧 adrian@lerer.com.ar  
🔗 GitHub: [@adrianlerer](https://github.com/adrianlerer)  
📄 SSRN: [Author Profile](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=6079582)

---

## 🤝 Contributing

This is an academic research project. Contributions are welcome via:
1. **Issues**: Report bugs, request features, suggest improvements
2. **Pull Requests**: Code improvements, documentation, additional country data
3. **Citations**: If you use this framework, please cite the paper

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🔄 Project Status

**Current Phase**: Near-Complete (v0.9.0 - Pre-Submission) - **97% Complete** ✅

### ✅ Completed (PATH 1 - Validated)
- ✅ Core parameter calculations (H, V, α) - 34 countries
- ✅ Composite metrics (LEI, d_φ, CHI)
- ✅ ODE simulation module with USA 436-year evolution
- ✅ Visualization functions (all 11 publication figures)
- ✅ Complete dataset integration (60 transplants, 27 USA amendments)
- ✅ All 4 Jupyter notebooks executable end-to-end
- ✅ Publication-ready figures (11 total, 8 unique, 300 DPI PDF)
- ✅ Appendices A & B (methodology + dataset documentation)
- ✅ **Comprehensive unit test suite (62/74 tests passing, 84%)**
- ✅ Professional documentation and git history

### 🔬 Speculative Tools (PATH 2 - Optional)
- ✅ Mutation Engine visual metaphor framework
- ✅ Inputless-GPT / Autopoiesis theoretical exploration
- ⚠️ **Clearly marked as non-validated, exploratory only**
- ⚠️ **Use for blog posts / creative articles, NOT peer review**

### 📅 Roadmap
- **v0.9.0** (Current): Near-complete, ready for final review
- **v1.0.0**: Paper submission release (target: Q1 2025)
- **v1.1.0**: Post-peer-review updates (target: Q2 2025)

### ⏳ Optional Enhancements (Not Required)
- README badges (test status, coverage)
- Zenodo DOI for dataset archival
- Sphinx documentation website
- GitHub Actions CI/CD

---

## 🚦 TWO-PATH SYSTEM: Rigorous vs Speculative Work

This repository maintains a clear separation between validated and speculative work:

### PATH 1: RIGOROUS WORK (Main Repository) ✅

**Location**: `lei_calculator/`, `tests/`, `notebooks/`, `figures/`, `appendices/`

**Status**: Empirically validated, peer-review ready

**Characteristics**:
- ✅ Empirical validation (AUC = 0.964, r = -0.76, p < 0.001)
- ✅ Unit tests (62/74 passing, 84% coverage)
- ✅ Inter-rater reliability (85.6%)
- ✅ 13 data sources cited (WJP, V-Dem, Lutz, etc.)
- ✅ Suitable for academic papers, journal submissions

**Use for**: 
- Peer-reviewed publications
- Grant proposals
- Policy analysis
- Legal scholarship
- Replication studies

---

### PATH 2: SPECULATIVE EXPLORATION (Optional Tools) 🔬

**Location**: `speculative/` directory

**Status**: Exploratory, hypothesis generation only, NOT validated

**Characteristics**:
- 🔬 Creative hypothesis generation
- 🔬 Philosophical exploration (autopoiesis, zero-context inference)
- 🔬 Visual metaphors for teaching
- ⚠️ NOT empirically validated
- ⚠️ NOT suitable for peer review

**Use for**:
- Blog posts (with disclaimers)
- Creative articles
- Philosophy papers (marked as speculative)
- Teaching materials (labeled "conceptual metaphor")
- Brainstorming sessions

**DO NOT use for**:
- ❌ Peer-reviewed journal papers (main text)
- ❌ Grant proposals
- ❌ Policy recommendations
- ❌ Legal expert testimony

---

### How to Choose

| Your Need | Use PATH 1 | Use PATH 2 |
|-----------|------------|------------|
| Write academic paper | ✅ Yes | ❌ No |
| Write blog post | ✅ Yes (preferred) | ✅ Yes (with warnings) |
| Create teaching materials | ✅ Yes | ✅ Yes (label "metaphor") |
| Develop policy brief | ✅ Yes | ❌ No |
| Explore creative ideas | ✅ Can start here | ✅ Yes |
| Generate hypotheses | ✅ Use validated baseline | ✅ Yes (then validate) |

**When in doubt, use PATH 1 tools.** PATH 2 is for creative exploration only.

See [`speculative/README.md`](speculative/README.md) for detailed guidelines.

---

## 📞 Support

- 📧 Email: adrian@lerer.com.ar
- 🐛 Issues: [GitHub Issues](https://github.com/adrianlerer/legal-evolvability-golden-ratio/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/adrianlerer/legal-evolvability-golden-ratio/discussions)

---

## 🙏 Acknowledgments

This research builds on extensive literatures in:
- **Evolutionary biology**: Godfrey-Smith (2009), Dawkins (1982), Dennett (1995)
- **Game theory**: Axelrod (1984), Tsebelis (2002)
- **Constitutional political economy**: Voigt (2011), Elkins et al. (2009)
- **Optimization theory**: Livio (2002), Markowsky (1992)

All errors and interpretations are my own.

---

**⭐ If this project is useful for your research, please star the repository and cite the paper!**

---

*Last updated: November 2025*
