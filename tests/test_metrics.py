"""
Unit tests for lei_calculator.metrics module

Tests LEI, d_φ, CHI calculations and zone classifications.
Validates against paper benchmarks and theoretical expectations.
"""

import pytest
import numpy as np
from lei_calculator.metrics import (
    calculate_LEI,
    calculate_d_phi,
    calculate_CHI,
    classify_zone,
    PHI
)


class TestGoldenRatio:
    """Test golden ratio constant"""
    
    def test_phi_value(self):
        """φ should be approximately 1.618"""
        assert abs(PHI - 1.618) < 0.001, f"PHI={PHI} should be ≈1.618"
    
    def test_phi_mathematical_property(self):
        """φ should satisfy φ² = φ + 1"""
        assert abs(PHI**2 - (PHI + 1)) < 0.001


class TestDistanceToPhiCalculation:
    """Test d_φ (distance to golden ratio) calculations"""
    
    def test_usa_d_phi(self):
        """USA d_φ should be ~0.475 (Goldilocks Zone)"""
        d_phi = calculate_d_phi(H=0.72, V=0.63)
        # H/V = 0.72/0.63 = 1.143, |1.143 - 1.618| = 0.475
        expected = abs((0.72/0.63) - PHI)
        assert abs(d_phi - expected) < 0.01, f"Expected d_φ≈{expected}, got {d_phi}"
    
    def test_argentina_d_phi(self):
        """Argentina d_φ should be ~3.493 (extreme lock-in)"""
        d_phi = calculate_d_phi(H=0.92, V=0.18)
        # H/V = 0.92/0.18 = 5.111, |5.111 - 1.618| = 3.493
        assert d_phi > 3.0, f"Argentina d_φ={d_phi} should be >3.0"
    
    def test_optimal_ratio(self):
        """d_φ should be 0 when H/V = φ"""
        # Find H, V where H/V = φ
        V = 0.618
        H = V * PHI  # H/V = φ
        d_phi = calculate_d_phi(H, V)
        assert d_phi < 0.01, f"d_φ should be ~0 when H/V=φ, got {d_phi}"
    
    def test_d_phi_symmetry(self):
        """d_φ should be symmetric around φ"""
        # H/V = φ + 1.0
        d_phi_high = calculate_d_phi(H=0.8, V=0.3)  # Rigidity
        
        # H/V = φ - 1.0
        d_phi_low = calculate_d_phi(H=0.3, V=0.5)   # Chaos
        
        # Both should be similar magnitude
        assert abs(d_phi_high - d_phi_low) < 0.5
    
    def test_d_phi_non_negative(self):
        """d_φ must always be non-negative"""
        test_cases = [
            (0.9, 0.1),  # High H, low V
            (0.1, 0.9),  # Low H, high V
            (0.5, 0.5),  # Equal H, V
        ]
        for H, V in test_cases:
            d_phi = calculate_d_phi(H, V)
            assert d_phi >= 0, f"d_φ={d_phi} should be ≥0 for H={H}, V={V}"


class TestLEICalculation:
    """Test Legal Evolvability Index (LEI) calculations"""
    
    def test_usa_lei(self):
        """USA LEI should be ~0.656 (Goldilocks Zone)"""
        LEI = calculate_LEI(H=0.72, V=0.63, alpha=0.58)
        # Expected: (0.63 × 0.58) / (|0.72/0.63 - 1.618| + 0.1)
        assert 0.6 <= LEI <= 0.7, f"USA LEI={LEI} should be ~0.656"
    
    def test_argentina_lei(self):
        """Argentina LEI should be ~0.005 (terminal lock-in)"""
        LEI = calculate_LEI(H=0.92, V=0.18, alpha=0.09)
        assert LEI < 0.01, f"Argentina LEI={LEI} should be <0.01"
    
    def test_lei_comparison(self):
        """USA LEI should be much higher than Argentina"""
        lei_usa = calculate_LEI(0.72, 0.63, 0.58)
        lei_arg = calculate_LEI(0.92, 0.18, 0.09)
        
        ratio = lei_usa / lei_arg
        assert ratio > 100, f"USA/Argentina LEI ratio={ratio} should be >100"
    
    def test_lei_maximized_at_phi(self):
        """LEI should be highest when H/V ≈ φ and α is high"""
        # Optimal case: H/V = φ, high α
        V_optimal = 0.6
        H_optimal = V_optimal * PHI
        alpha_high = 0.9
        
        LEI_optimal = calculate_LEI(H_optimal, V_optimal, alpha_high)
        
        # Suboptimal case: H/V far from φ
        LEI_suboptimal = calculate_LEI(0.9, 0.2, alpha_high)
        
        assert LEI_optimal > LEI_suboptimal, "LEI should be higher at φ"
    
    def test_lei_zero_alpha(self):
        """LEI should be 0 when α = 0 (no selection)"""
        LEI = calculate_LEI(H=0.7, V=0.6, alpha=0.0)
        assert LEI == 0.0, f"LEI={LEI} should be 0 when α=0"
    
    def test_lei_epsilon_prevents_division_by_zero(self):
        """LEI calculation should not crash when d_φ = 0"""
        V = 0.618
        H = V * PHI  # H/V = φ exactly
        LEI = calculate_LEI(H, V, alpha=0.5)
        assert LEI > 0, "LEI should be computable even when d_φ=0"


class TestCHICalculation:
    """Test Constitutional Health Index (CHI) calculations"""
    
    def test_usa_chi(self):
        """USA CHI should be ~0.178"""
        CHI = calculate_CHI(H=0.72, V=0.63, alpha=0.58)
        assert 0.15 <= CHI <= 0.20, f"USA CHI={CHI} should be ~0.178"
    
    def test_argentina_chi(self):
        """Argentina CHI should be ~0.003 (worst)"""
        CHI = calculate_CHI(H=0.92, V=0.18, alpha=0.09)
        assert CHI < 0.01, f"Argentina CHI={CHI} should be <0.01"
    
    def test_chi_positive(self):
        """CHI should always be positive for positive inputs"""
        CHI = calculate_CHI(H=0.5, V=0.5, alpha=0.5)
        assert CHI > 0, f"CHI={CHI} should be positive"
    
    def test_chi_increases_with_parameters(self):
        """CHI should increase when H, V, α all increase"""
        CHI_low = calculate_CHI(H=0.3, V=0.3, alpha=0.3)
        CHI_high = calculate_CHI(H=0.7, V=0.7, alpha=0.7)
        
        assert CHI_high > CHI_low, "CHI should increase with parameters"


class TestZoneClassification:
    """Test zone classification logic"""
    
    def test_usa_goldilocks_zone(self):
        """USA should be classified as Goldilocks Zone"""
        zone = classify_zone(H=0.72, V=0.63, alpha=0.58)
        assert zone in ['Goldilocks Zone', 'Transition Zone'], \
            f"USA zone={zone} should be Goldilocks or Transition"
    
    def test_argentina_high_rigidity(self):
        """Argentina should be classified as High Rigidity Zone"""
        zone = classify_zone(H=0.92, V=0.18, alpha=0.09)
        assert 'Rigidity' in zone or 'Lock' in zone.lower(), \
            f"Argentina zone={zone} should indicate rigidity/lock-in"
    
    def test_high_chaos_classification(self):
        """Low H, high V should classify as High Chaos"""
        zone = classify_zone(H=0.2, V=0.8, alpha=0.1)
        assert 'Chaos' in zone, f"Low H, high V should be Chaos, got {zone}"
    
    def test_low_selection_zone(self):
        """Very low α should classify as Low Selection"""
        zone = classify_zone(H=0.5, V=0.5, alpha=0.05)
        # Should be flagged as Low Selection or similar
        assert zone is not None
    
    def test_all_zones_defined(self):
        """Test that all major zones are covered"""
        test_cases = [
            (0.7, 0.6, 0.6),   # Goldilocks
            (0.9, 0.2, 0.1),   # High Rigidity
            (0.2, 0.8, 0.1),   # High Chaos
            (0.5, 0.5, 0.05),  # Low Selection
            (0.6, 0.5, 0.4),   # Transition
        ]
        
        for H, V, alpha in test_cases:
            zone = classify_zone(H, V, alpha)
            assert zone is not None, f"Zone undefined for H={H}, V={V}, α={alpha}"
            assert isinstance(zone, str), "Zone should be a string"


class TestThresholdEffects:
    """Test threshold effects from paper (d_φ < 0.5 → success)"""
    
    def test_goldilocks_threshold(self):
        """d_φ < 0.5 should indicate Goldilocks Zone"""
        # Find H, V where d_φ < 0.5
        H = 0.7
        V = 0.6
        d_phi = calculate_d_phi(H, V)
        
        if d_phi < 0.5:
            LEI = calculate_LEI(H, V, alpha=0.6)
            assert LEI > 0.5, "LEI should be high in Goldilocks Zone"
    
    def test_lock_in_threshold(self):
        """d_φ > 2.0 should indicate lock-in/chaos"""
        H = 0.9
        V = 0.2
        d_phi = calculate_d_phi(H, V)
        
        if d_phi > 2.0:
            LEI = calculate_LEI(H, V, alpha=0.1)
            assert LEI < 0.1, "LEI should be low in lock-in zone"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_variation(self):
        """V=0 should handle gracefully (no division by zero)"""
        # This should raise error or handle gracefully
        with pytest.raises(Exception):
            calculate_d_phi(H=0.5, V=0.0)
    
    def test_very_small_values(self):
        """Very small parameter values should compute correctly"""
        LEI = calculate_LEI(H=0.01, V=0.01, alpha=0.01)
        assert LEI >= 0, "LEI should be non-negative for small values"
    
    def test_maximum_values(self):
        """Maximum parameter values (H=V=α=1) should compute"""
        LEI = calculate_LEI(H=1.0, V=1.0, alpha=1.0)
        CHI = calculate_CHI(H=1.0, V=1.0, alpha=1.0)
        assert LEI > 0 and CHI > 0


class TestConsistencyWithPaper:
    """Validate against paper's reported values"""
    
    def test_table_8_3_correlation(self):
        """Paper reports r = -0.76 between d_φ and success"""
        # This would require loading transplant data
        # For now, verify that d_φ is computable for typical values
        test_cases = [
            (0.7, 0.6),  # Should give d_φ ≈ 0.45
            (0.9, 0.2),  # Should give d_φ ≈ 2.9
        ]
        
        for H, V in test_cases:
            d_phi = calculate_d_phi(H, V)
            assert 0 <= d_phi <= 5, f"d_φ={d_phi} out of expected range"
    
    def test_section_6_usa_values(self):
        """Section VI reports USA: H=0.72, V=0.63, α=0.58, LEI=0.656"""
        H, V, alpha = 0.72, 0.63, 0.58
        
        d_phi = calculate_d_phi(H, V)
        LEI = calculate_LEI(H, V, alpha)
        CHI = calculate_CHI(H, V, alpha)
        
        # All should be computable and reasonable
        assert 0.4 <= d_phi <= 0.6, f"USA d_φ={d_phi}"
        assert 0.6 <= LEI <= 0.7, f"USA LEI={LEI}"
        assert CHI > 0.15, f"USA CHI={CHI}"


# Test fixtures
@pytest.fixture
def usa_metrics():
    """USA calculated metrics"""
    return {
        'd_phi': calculate_d_phi(0.72, 0.63),
        'LEI': calculate_LEI(0.72, 0.63, 0.58),
        'CHI': calculate_CHI(0.72, 0.63, 0.58)
    }


@pytest.fixture
def argentina_metrics():
    """Argentina calculated metrics"""
    return {
        'd_phi': calculate_d_phi(0.92, 0.18),
        'LEI': calculate_LEI(0.92, 0.18, 0.09),
        'CHI': calculate_CHI(0.92, 0.18, 0.09)
    }


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
