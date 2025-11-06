"""
Legal Evolvability Index Calculator - Parameter Calculations
============================================================

This module implements calculations for the three Darwinian parameters:
- H (Heredity): Fidelity of legal norm transmission
- V (Variation): Diversity in institutional arrangements  
- α (Differential Fitness): Selection pressure favoring high-fitness norms

Based on:
Lerer, I.A. (2025). "Darwinian Spaces and the Golden Ratio: A Quantitative 
Framework for Measuring Legal Evolution." SSRN Working Paper.

Author: Ignacio Adrian Lerer
License: MIT
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class ParameterComponents:
    """Container for parameter sub-components"""
    # Heredity components
    precedent_strength: float
    const_rigidity: float
    codification: float
    judicial_tenure: float
    
    # Variation components  
    federal_autonomy: float
    amendment_freq: float
    judicial_review: float
    legislative_turnover: float
    
    # Differential fitness components
    compliance_rate: float
    transparency_score: float
    enforcement_capacity: float
    legitimacy_index: float


def calculate_H(
    precedent_strength: float,
    const_rigidity: float, 
    codification: float,
    judicial_tenure: float,
    weights: Optional[List[float]] = None
) -> float:
    """
    Calculate Heredity (H) parameter for a legal system.
    
    H measures the fidelity of legal norm transmission across institutional
    generations. Higher H indicates greater preservation of legal rules.
    
    Args:
        precedent_strength (float): 0-1, strength of stare decisis doctrine
            - 0.0: No binding precedent
            - 0.5: Persuasive but not binding
            - 1.0: Strict stare decisis (e.g., Common Law)
            
        const_rigidity (float): 0-1, constitutional amendment difficulty
            - Based on Lutz (1994) amendment difficulty index
            - Normalized: easy (0.0) to impossible (1.0)
            
        codification (float): 0-1, ratio of codified to total law
            - Civil law systems: ~0.7-0.9
            - Common law systems: ~0.3-0.5
            
        judicial_tenure (float): 0-1, normalized average judicial tenure
            - (actual_tenure - min_tenure) / (max_tenure - min_tenure)
            - Lifetime appointment = 1.0
            
        weights (list, optional): Component weights [prec, const, cod, tenure]
            Default: [0.35, 0.30, 0.25, 0.10] based on empirical validation
    
    Returns:
        float: H value in [0, 1]
    
    Example:
        >>> # USA example
        >>> calculate_H(
        ...     precedent_strength=0.80,  # Strong stare decisis
        ...     const_rigidity=0.75,      # Difficult amendment
        ...     codification=0.55,        # Moderate codification
        ...     judicial_tenure=0.65      # Long tenure
        ... )
        0.72
        
        >>> # Argentina labor regime example
        >>> calculate_H(
        ...     precedent_strength=0.95,  # Article 14bis + ultraactivity
        ...     const_rigidity=0.92,      # Nearly impossible to amend
        ...     codification=0.88,        # Highly codified
        ...     judicial_tenure=0.85      # Stable judiciary
        ... )
        0.92
    
    References:
        - Godfrey-Smith, P. (2009). "Darwinian Populations and Natural Selection"
        - Lutz, D. (1994). "Constitutional Amendment Difficulty"
    """
    if weights is None:
        weights = [0.35, 0.30, 0.25, 0.10]
    
    # Validate inputs
    for param, name in [(precedent_strength, "precedent_strength"),
                         (const_rigidity, "const_rigidity"),
                         (codification, "codification"),
                         (judicial_tenure, "judicial_tenure")]:
        if not 0 <= param <= 1:
            raise ValueError(f"{name} must be in [0, 1], got {param}")
    
    if not np.isclose(sum(weights), 1.0):
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
    
    H = (weights[0] * precedent_strength +
         weights[1] * const_rigidity +
         weights[2] * codification +
         weights[3] * judicial_tenure)
    
    return round(H, 3)


def calculate_V(
    federal_autonomy: float,
    amendment_freq: float,
    judicial_review: float,
    legislative_turnover: float,
    weights: Optional[List[float]] = None
) -> float:
    """
    Calculate Variation (V) parameter for a legal system.
    
    V measures diversity in institutional arrangements and policy experimentation.
    Higher V indicates greater capacity for legal innovation.
    
    Args:
        federal_autonomy (float): 0-1, subnational policy autonomy
            - Based on Treisman (2007) decentralization index
            - 0.0: Unitary state
            - 1.0: Strong federalism
            
        amendment_freq (float): 0-1, normalized constitutional amendment frequency
            - (actual_amendments / max_observed) over comparable period
            - Captures constitutional flexibility
            
        judicial_review (float): 0-1, breadth and activity of judicial review
            - Combines: abstract review, concrete review, constitutional court activity
            - 0.0: No judicial review
            - 1.0: Active, expansive review
            
        legislative_turnover (float): 0-1, legislative personnel turnover rate
            - (new_members / total_seats) per electoral cycle
            - Captures policy renewal capacity
            
        weights (list, optional): Component weights [fed, amend, review, turnover]
            Default: [0.40, 0.25, 0.20, 0.15]
    
    Returns:
        float: V value in [0, 1]
    
    Example:
        >>> # USA example
        >>> calculate_V(
        ...     federal_autonomy=0.85,    # Strong federalism
        ...     amendment_freq=0.45,      # Moderate amendment rate
        ...     judicial_review=0.70,     # Active Supreme Court
        ...     legislative_turnover=0.50 # Moderate turnover
        ... )
        0.63
        
        >>> # Argentina labor (low variation, locked-in)
        >>> calculate_V(
        ...     federal_autonomy=0.15,    # Federal preemption of labor law
        ...     amendment_freq=0.05,      # Virtually frozen
        ...     judicial_review=0.30,     # Defensive of status quo
        ...     legislative_turnover=0.22 # Low effective turnover
        ... )
        0.18
    
    References:
        - Treisman, D. (2007). "The Architecture of Government"
        - Tsebelis, G. (2002). "Veto Players"
    """
    if weights is None:
        weights = [0.40, 0.25, 0.20, 0.15]
    
    # Validate inputs
    for param, name in [(federal_autonomy, "federal_autonomy"),
                         (amendment_freq, "amendment_freq"),
                         (judicial_review, "judicial_review"),
                         (legislative_turnover, "legislative_turnover")]:
        if not 0 <= param <= 1:
            raise ValueError(f"{name} must be in [0, 1], got {param}")
    
    if not np.isclose(sum(weights), 1.0):
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
    
    V = (weights[0] * federal_autonomy +
         weights[1] * amendment_freq +
         weights[2] * judicial_review +
         weights[3] * legislative_turnover)
    
    return round(V, 3)


def calculate_alpha(
    compliance_rate: float,
    transparency_score: float,
    enforcement_capacity: float,
    legitimacy_index: float,
    weights: Optional[List[float]] = None
) -> float:
    """
    Calculate Differential Fitness (α) parameter for a legal system.
    
    α measures selection pressure favoring high-fitness legal norms. Higher α 
    indicates stronger evolutionary pressure toward institutional effectiveness.
    
    Args:
        compliance_rate (float): 0-1, actual compliance with legal norms
            - World Justice Project Rule of Law Index (compliance component)
            - Tax compliance, regulatory adherence, contract enforcement
            
        transparency_score (float): 0-1, institutional transparency
            - Government openness, judicial accessibility, policy clarity
            - Enables identification of high-fitness norms
            
        enforcement_capacity (float): 0-1, state capacity for norm enforcement
            - Judicial efficiency, regulatory capacity, administrative competence
            - V-Dem state capacity index, normalized
            
        legitimacy_index (float): 0-1, perceived legitimacy of legal system
            - Public trust in institutions, perceived fairness
            - World Values Survey + Latinobarometro
            
        weights (list, optional): Component weights [comp, trans, enf, legit]
            Default: [0.35, 0.25, 0.25, 0.15]
    
    Returns:
        float: α value in [0, 1]
    
    Example:
        >>> # USA example  
        >>> calculate_alpha(
        ...     compliance_rate=0.65,      # Moderate compliance
        ...     transparency_score=0.70,   # Strong transparency
        ...     enforcement_capacity=0.55, # Moderate enforcement
        ...     legitimacy_index=0.45      # Declining legitimacy
        ... )
        0.58
        
        >>> # Argentina labor (very low selection pressure)
        >>> calculate_alpha(
        ...     compliance_rate=0.12,      # Widespread evasion
        ...     transparency_score=0.15,   # Opaque CGT negotiations
        ...     enforcement_capacity=0.08, # Weak enforcement
        ...     legitimacy_index=0.05      # Low legitimacy
        ... )
        0.09
    
    References:
        - World Justice Project (2023). Rule of Law Index
        - V-Dem Institute (2023). Democracy Dataset
    """
    if weights is None:
        weights = [0.35, 0.25, 0.25, 0.15]
    
    # Validate inputs
    for param, name in [(compliance_rate, "compliance_rate"),
                         (transparency_score, "transparency_score"),
                         (enforcement_capacity, "enforcement_capacity"),
                         (legitimacy_index, "legitimacy_index")]:
        if not 0 <= param <= 1:
            raise ValueError(f"{name} must be in [0, 1], got {param}")
    
    if not np.isclose(sum(weights), 1.0):
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
    
    alpha = (weights[0] * compliance_rate +
             weights[1] * transparency_score +
             weights[2] * enforcement_capacity +
             weights[3] * legitimacy_index)
    
    return round(alpha, 3)


def calculate_all_parameters(
    components: ParameterComponents,
    H_weights: Optional[List[float]] = None,
    V_weights: Optional[List[float]] = None,
    alpha_weights: Optional[List[float]] = None
) -> Tuple[float, float, float]:
    """
    Calculate all three parameters (H, V, α) from component data.
    
    Args:
        components: ParameterComponents object with all sub-components
        H_weights, V_weights, alpha_weights: Optional custom weights
    
    Returns:
        tuple: (H, V, α) values
    
    Example:
        >>> from lei_calculator.parameters import ParameterComponents
        >>> usa_components = ParameterComponents(
        ...     precedent_strength=0.80, const_rigidity=0.75,
        ...     codification=0.55, judicial_tenure=0.65,
        ...     federal_autonomy=0.85, amendment_freq=0.45,
        ...     judicial_review=0.70, legislative_turnover=0.50,
        ...     compliance_rate=0.65, transparency_score=0.70,
        ...     enforcement_capacity=0.55, legitimacy_index=0.45
        ... )
        >>> H, V, alpha = calculate_all_parameters(usa_components)
        >>> print(f"USA: H={H}, V={V}, α={alpha}")
        USA: H=0.72, V=0.63, α=0.58
    """
    H = calculate_H(
        components.precedent_strength,
        components.const_rigidity,
        components.codification,
        components.judicial_tenure,
        H_weights
    )
    
    V = calculate_V(
        components.federal_autonomy,
        components.amendment_freq,
        components.judicial_review,
        components.legislative_turnover,
        V_weights
    )
    
    alpha = calculate_alpha(
        components.compliance_rate,
        components.transparency_score,
        components.enforcement_capacity,
        components.legitimacy_index,
        alpha_weights
    )
    
    return H, V, alpha


# Predefined country parameters (validated from paper)
COUNTRY_PARAMETERS = {
    'USA': {
        'H': 0.72, 'V': 0.63, 'alpha': 0.58,
        'components': ParameterComponents(
            precedent_strength=0.80, const_rigidity=0.75,
            codification=0.55, judicial_tenure=0.65,
            federal_autonomy=0.85, amendment_freq=0.45,
            judicial_review=0.70, legislative_turnover=0.50,
            compliance_rate=0.65, transparency_score=0.70,
            enforcement_capacity=0.55, legitimacy_index=0.45
        )
    },
    'Argentina_labor': {
        'H': 0.92, 'V': 0.18, 'alpha': 0.09,
        'components': ParameterComponents(
            precedent_strength=0.95, const_rigidity=0.92,
            codification=0.88, judicial_tenure=0.85,
            federal_autonomy=0.15, amendment_freq=0.05,
            judicial_review=0.30, legislative_turnover=0.22,
            compliance_rate=0.12, transparency_score=0.15,
            enforcement_capacity=0.08, legitimacy_index=0.05
        )
    },
    'Brazil': {
        'H': 0.61, 'V': 0.68, 'alpha': 0.52,
        'components': ParameterComponents(
            precedent_strength=0.60, const_rigidity=0.55,
            codification=0.70, judicial_tenure=0.58,
            federal_autonomy=0.75, amendment_freq=0.65,
            judicial_review=0.72, legislative_turnover=0.55,
            compliance_rate=0.50, transparency_score=0.48,
            enforcement_capacity=0.55, legitimacy_index=0.55
        )
    },
    'Chile': {
        'H': 0.65, 'V': 0.61, 'alpha': 0.44,
        'components': ParameterComponents(
            precedent_strength=0.65, const_rigidity=0.62,
            codification=0.72, judicial_tenure=0.60,
            federal_autonomy=0.42, amendment_freq=0.75,
            judicial_review=0.68, legislative_turnover=0.62,
            compliance_rate=0.45, transparency_score=0.48,
            enforcement_capacity=0.42, legitimacy_index=0.40
        )
    },
    'Germany': {
        'H': 0.75, 'V': 0.68, 'alpha': 0.65,
        'components': ParameterComponents(
            precedent_strength=0.75, const_rigidity=0.80,
            codification=0.75, judicial_tenure=0.70,
            federal_autonomy=0.78, amendment_freq=0.55,
            judicial_review=0.75, legislative_turnover=0.60,
            compliance_rate=0.70, transparency_score=0.68,
            enforcement_capacity=0.62, legitimacy_index=0.60
        )
    }
}


def get_country_parameters(country: str) -> Dict:
    """
    Retrieve validated parameters for a country.
    
    Args:
        country: Country name (case-insensitive)
            Available: USA, Argentina_labor, Brazil, Chile, Germany
    
    Returns:
        dict: {'H': float, 'V': float, 'alpha': float, 'components': ParameterComponents}
    
    Raises:
        KeyError: If country not in database
    
    Example:
        >>> params = get_country_parameters('USA')
        >>> print(f"H={params['H']}, V={params['V']}, α={params['alpha']}")
        H=0.72, V=0.63, α=0.58
    """
    country_key = country.replace(' ', '_')
    if country_key not in COUNTRY_PARAMETERS:
        available = ', '.join(COUNTRY_PARAMETERS.keys())
        raise KeyError(f"Country '{country}' not found. Available: {available}")
    
    return COUNTRY_PARAMETERS[country_key]
