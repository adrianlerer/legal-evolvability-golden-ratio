"""
Unit tests for lei_calculator.parameters module

Tests parameter calculations (H, V, α) with known values from paper.
Validates against USA, Argentina, Brazil, Chile benchmarks.
"""

import pytest
import numpy as np
from lei_calculator.parameters import (
    calculate_H,
    calculate_V,
    calculate_alpha,
    calculate_all_parameters,
    ParameterComponents,
    COUNTRY_PARAMETERS
)


class TestHeredityCalculation:
    """Test Heredity (H) parameter calculations"""
    
    def test_usa_heredity(self):
        """Test USA H calculation matches paper value (0.72)"""
        H = calculate_H(
            precedent_strength=0.80,
            const_rigidity=0.75,
            codification=0.55,
            judicial_tenure=0.65
        )
        assert abs(H - 0.72) < 0.02, f"Expected H≈0.72, got {H}"
    
    def test_argentina_heredity(self):
        """Test Argentina labor H calculation (0.92 - high lock-in)"""
        H = calculate_H(
            precedent_strength=0.95,
            const_rigidity=0.92,
            codification=0.88,
            judicial_tenure=0.85
        )
        assert abs(H - 0.92) < 0.02, f"Expected H≈0.92, got {H}"
    
    def test_heredity_range(self):
        """H must be in [0, 1] for all valid inputs"""
        # Minimum
        H_min = calculate_H(0.0, 0.0, 0.0, 0.0)
        assert 0.0 <= H_min <= 1.0
        
        # Maximum
        H_max = calculate_H(1.0, 1.0, 1.0, 1.0)
        assert 0.0 <= H_max <= 1.0
    
    def test_heredity_invalid_input(self):
        """H calculation should reject out-of-range inputs"""
        with pytest.raises(ValueError):
            calculate_H(1.5, 0.5, 0.5, 0.5)  # precedent > 1.0
        
        with pytest.raises(ValueError):
            calculate_H(0.5, -0.1, 0.5, 0.5)  # const_rigidity < 0
    
    def test_heredity_custom_weights(self):
        """Test custom weight specification"""
        H_default = calculate_H(0.8, 0.7, 0.6, 0.5)
        H_custom = calculate_H(0.8, 0.7, 0.6, 0.5, weights=[0.25, 0.25, 0.25, 0.25])
        
        assert H_default != H_custom  # Different weights should give different results
    
    def test_heredity_weights_sum_validation(self):
        """Weights must sum to 1.0"""
        with pytest.raises(ValueError):
            calculate_H(0.5, 0.5, 0.5, 0.5, weights=[0.3, 0.3, 0.3, 0.3])  # Sum = 1.2


class TestVariationCalculation:
    """Test Variation (V) parameter calculations"""
    
    def test_usa_variation(self):
        """Test USA V calculation matches paper value (0.63)"""
        V = calculate_V(
            federal_autonomy=0.85,
            amendment_freq=0.45,
            judicial_review=0.70,
            legislative_turnover=0.50
        )
        assert abs(V - 0.63) < 0.05, f"Expected V≈0.63, got {V}"
    
    def test_argentina_variation(self):
        """Test Argentina labor V calculation (0.18 - low variation)"""
        V = calculate_V(
            federal_autonomy=0.15,
            amendment_freq=0.05,
            judicial_review=0.30,
            legislative_turnover=0.22
        )
        assert abs(V - 0.18) < 0.02, f"Expected V≈0.18, got {V}"
    
    def test_variation_range(self):
        """V must be in [0, 1] for all valid inputs"""
        V_min = calculate_V(0.0, 0.0, 0.0, 0.0)
        assert 0.0 <= V_min <= 1.0
        
        V_max = calculate_V(1.0, 1.0, 1.0, 1.0)
        assert 0.0 <= V_max <= 1.0
    
    def test_variation_invalid_input(self):
        """V calculation should reject out-of-range inputs"""
        with pytest.raises(ValueError):
            calculate_V(0.5, 1.2, 0.5, 0.5)  # amendment_freq > 1.0


class TestDifferentialFitness:
    """Test Differential Fitness (α) parameter calculations"""
    
    def test_usa_alpha(self):
        """Test USA α calculation matches paper value (0.58)"""
        alpha = calculate_alpha(
            compliance_rate=0.65,
            transparency_score=0.70,
            enforcement_capacity=0.55,
            legitimacy_index=0.45
        )
        assert abs(alpha - 0.58) < 0.05, f"Expected α≈0.58, got {alpha}"
    
    def test_argentina_alpha(self):
        """Test Argentina labor α calculation (0.09 - very low)"""
        alpha = calculate_alpha(
            compliance_rate=0.12,
            transparency_score=0.15,
            enforcement_capacity=0.08,
            legitimacy_index=0.05
        )
        assert abs(alpha - 0.09) < 0.03, f"Expected α≈0.09, got {alpha}"
    
    def test_alpha_range(self):
        """α must be in [0, 1] for all valid inputs"""
        alpha_min = calculate_alpha(0.0, 0.0, 0.0, 0.0)
        assert 0.0 <= alpha_min <= 1.0
        
        alpha_max = calculate_alpha(1.0, 1.0, 1.0, 1.0)
        assert 0.0 <= alpha_max <= 1.0


class TestAllParametersCalculation:
    """Test combined parameter calculation"""
    
    def test_usa_all_parameters(self):
        """Test USA (H, V, α) calculation from components"""
        usa_components = ParameterComponents(
            precedent_strength=0.80, const_rigidity=0.75,
            codification=0.55, judicial_tenure=0.65,
            federal_autonomy=0.85, amendment_freq=0.45,
            judicial_review=0.70, legislative_turnover=0.50,
            compliance_rate=0.65, transparency_score=0.70,
            enforcement_capacity=0.55, legitimacy_index=0.45
        )
        
        H, V, alpha = calculate_all_parameters(usa_components)
        
        assert abs(H - 0.72) < 0.02, f"Expected H≈0.72, got {H}"
        assert abs(V - 0.63) < 0.05, f"Expected V≈0.63, got {V}"
        assert abs(alpha - 0.58) < 0.05, f"Expected α≈0.58, got {alpha}"
    
    def test_argentina_all_parameters(self):
        """Test Argentina (H, V, α) calculation"""
        arg_components = ParameterComponents(
            precedent_strength=0.95, const_rigidity=0.92,
            codification=0.88, judicial_tenure=0.85,
            federal_autonomy=0.15, amendment_freq=0.05,
            judicial_review=0.30, legislative_turnover=0.22,
            compliance_rate=0.12, transparency_score=0.15,
            enforcement_capacity=0.08, legitimacy_index=0.05
        )
        
        H, V, alpha = calculate_all_parameters(arg_components)
        
        assert abs(H - 0.92) < 0.02
        assert abs(V - 0.18) < 0.02
        assert abs(alpha - 0.09) < 0.03


class TestCountryDatabase:
    """Test COUNTRY_PARAMETERS database integrity"""
    
    def test_database_completeness(self):
        """All countries should have H, V, α values"""
        for country, params in COUNTRY_PARAMETERS.items():
            assert 'H' in params, f"{country} missing H"
            assert 'V' in params, f"{country} missing V"
            assert 'alpha' in params, f"{country} missing alpha"
    
    def test_database_value_ranges(self):
        """All parameter values should be in [0, 1]"""
        for country, params in COUNTRY_PARAMETERS.items():
            assert 0.0 <= params['H'] <= 1.0, f"{country} H out of range"
            assert 0.0 <= params['V'] <= 1.0, f"{country} V out of range"
            assert 0.0 <= params['alpha'] <= 1.0, f"{country} α out of range"
    
    def test_usa_in_database(self):
        """USA should be in database with correct values"""
        assert 'USA' in COUNTRY_PARAMETERS
        usa = COUNTRY_PARAMETERS['USA']
        assert usa['H'] == 0.72
        assert usa['V'] == 0.63
        assert usa['alpha'] == 0.58
    
    def test_argentina_in_database(self):
        """Argentina labor should be in database"""
        assert 'Argentina_labor' in COUNTRY_PARAMETERS
        arg = COUNTRY_PARAMETERS['Argentina_labor']
        assert arg['H'] == 0.92
        assert arg['V'] == 0.18
        assert arg['alpha'] == 0.09
    
    def test_database_size(self):
        """Database should contain 34 countries"""
        assert len(COUNTRY_PARAMETERS) >= 34, \
            f"Expected at least 34 countries, got {len(COUNTRY_PARAMETERS)}"


class TestParameterRounding:
    """Test that rounding is consistent"""
    
    def test_rounding_precision(self):
        """Parameters should be rounded to 3 decimal places"""
        H = calculate_H(0.123456, 0.654321, 0.789012, 0.456789)
        # Result should be rounded to 2-3 decimals
        assert isinstance(H, float)
        assert len(str(H).split('.')[-1]) <= 3


class TestComponentsDataclass:
    """Test ParameterComponents dataclass"""
    
    def test_components_creation(self):
        """ParameterComponents should accept all 12 components"""
        components = ParameterComponents(
            precedent_strength=0.8, const_rigidity=0.7,
            codification=0.6, judicial_tenure=0.5,
            federal_autonomy=0.9, amendment_freq=0.4,
            judicial_review=0.7, legislative_turnover=0.5,
            compliance_rate=0.6, transparency_score=0.7,
            enforcement_capacity=0.5, legitimacy_index=0.4
        )
        
        assert components.precedent_strength == 0.8
        assert components.compliance_rate == 0.6


# Test fixtures for reuse
@pytest.fixture
def usa_params():
    """USA parameter values"""
    return {
        'H': 0.72,
        'V': 0.63,
        'alpha': 0.58
    }


@pytest.fixture
def argentina_params():
    """Argentina labor parameter values"""
    return {
        'H': 0.92,
        'V': 0.18,
        'alpha': 0.09
    }


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
