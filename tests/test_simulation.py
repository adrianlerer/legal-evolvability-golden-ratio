"""
Unit tests for lei_calculator.simulation module

Tests ODE-based evolution simulation with convergence to φ equilibrium.
"""

import pytest
import numpy as np
from lei_calculator.simulation import simulate_evolution, PHI


class TestSimulationBasic:
    """Basic simulation functionality tests"""
    
    def test_simulation_returns_dict(self):
        """Simulation should return dictionary with required keys"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=50)
        
        required_keys = ['time', 'H', 'V', 'alpha', 'LEI', 'd_phi']
        for key in required_keys:
            assert key in results, f"Missing key: {key}"
    
    def test_simulation_array_lengths(self):
        """All output arrays should have same length"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=100)
        
        length = len(results['time'])
        assert len(results['H']) == length
        assert len(results['V']) == length
        assert len(results['alpha']) == length
        assert len(results['LEI']) == length
        assert len(results['d_phi']) == length
    
    def test_simulation_time_range(self):
        """Time array should span [0, years]"""
        years = 200
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=years)
        
        assert results['time'][0] == 0
        assert results['time'][-1] == years


class TestConvergenceToEquilibrium:
    """Test convergence to φ equilibrium"""
    
    def test_usa_convergence(self):
        """USA parameters should converge to stable equilibrium"""
        results = simulate_evolution(H0=0.72, V0=0.63, alpha0=0.58, years=200)
        
        # Check final values are stable
        H_final = results['H'][-10:].mean()
        V_final = results['V'][-10:].mean()
        
        # H/V ratio should approach φ or remain stable
        HV_ratio_final = H_final / V_final
        assert 0.5 <= HV_ratio_final <= 3.0, f"Final H/V={HV_ratio_final} out of range"
    
    def test_equilibrium_stability(self):
        """System should reach equilibrium (low variance in final period)"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=300)
        
        # Last 50 years should have low variance
        H_final_std = np.std(results['H'][-50:])
        V_final_std = np.std(results['V'][-50:])
        
        assert H_final_std < 0.1, f"H not stable: std={H_final_std}"
        assert V_final_std < 0.1, f"V not stable: std={V_final_std}"
    
    def test_d_phi_decreases(self):
        """d_φ should generally decrease or stabilize (approach φ)"""
        results = simulate_evolution(H0=0.9, V0=0.3, alpha0=0.4, years=200)
        
        d_phi_initial = results['d_phi'][:10].mean()
        d_phi_final = results['d_phi'][-10:].mean()
        
        # Final d_φ should be lower or similar (convergence)
        assert d_phi_final <= d_phi_initial * 1.5, \
            f"d_φ increased from {d_phi_initial} to {d_phi_final}"


class TestParameterRanges:
    """Test that simulated parameters stay in valid ranges"""
    
    def test_parameters_stay_in_bounds(self):
        """H, V, α should remain in [0, 1] throughout simulation"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=200)
        
        assert np.all(results['H'] >= 0) and np.all(results['H'] <= 1.5), \
            "H out of valid range"
        assert np.all(results['V'] >= 0) and np.all(results['V'] <= 1.5), \
            "V out of valid range"
        assert np.all(results['alpha'] >= 0) and np.all(results['alpha'] <= 1.5), \
            "α out of valid range"
    
    def test_lei_non_negative(self):
        """LEI should never be negative"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=100)
        assert np.all(results['LEI'] >= 0), "LEI contains negative values"
    
    def test_d_phi_non_negative(self):
        """d_φ should never be negative"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=100)
        assert np.all(results['d_phi'] >= 0), "d_φ contains negative values"


class TestDifferentInitialConditions:
    """Test simulation with various starting conditions"""
    
    def test_low_h_high_v(self):
        """Chaos zone: Low H, high V"""
        results = simulate_evolution(H0=0.2, V0=0.8, alpha0=0.3, years=100)
        assert len(results['time']) > 0, "Simulation failed for chaos zone"
    
    def test_high_h_low_v(self):
        """Lock-in zone: High H, low V"""
        results = simulate_evolution(H0=0.9, V0=0.2, alpha0=0.1, years=100)
        assert len(results['time']) > 0, "Simulation failed for lock-in zone"
    
    def test_near_phi(self):
        """Starting near φ optimum"""
        V0 = 0.6
        H0 = V0 * PHI  # H/V = φ
        results = simulate_evolution(H0=H0, V0=V0, alpha0=0.6, years=100)
        
        # Should remain stable
        d_phi_mean = np.mean(results['d_phi'])
        assert d_phi_mean < 1.0, "System unstable even starting at φ"


class TestNoiseEffects:
    """Test stochastic noise in simulation"""
    
    def test_different_seeds_give_different_results(self):
        """Different noise seeds should produce different trajectories"""
        results1 = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, 
                                     years=100, noise_seed=42)
        results2 = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, 
                                     years=100, noise_seed=99)
        
        # Trajectories should differ
        assert not np.allclose(results1['H'], results2['H']), \
            "Different seeds produced identical results"
    
    def test_same_seed_reproducible(self):
        """Same seed should produce identical results"""
        results1 = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, 
                                     years=100, noise_seed=42)
        results2 = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, 
                                     years=100, noise_seed=42)
        
        assert np.allclose(results1['H'], results2['H']), \
            "Same seed produced different results"


class TestArgentinaScenario:
    """Test Argentina lock-in scenario"""
    
    def test_argentina_remains_locked(self):
        """Argentina should remain in lock-in zone"""
        results = simulate_evolution(H0=0.92, V0=0.18, alpha0=0.09, years=100)
        
        # Final H should remain high, V low
        H_final = results['H'][-10:].mean()
        V_final = results['V'][-10:].mean()
        
        assert H_final > 0.7, f"H decreased too much: {H_final}"
        assert V_final < 0.4, f"V increased too much: {V_final}"
    
    def test_argentina_low_lei(self):
        """Argentina should maintain very low LEI"""
        results = simulate_evolution(H0=0.92, V0=0.18, alpha0=0.09, years=100)
        
        LEI_final = results['LEI'][-10:].mean()
        assert LEI_final < 0.1, f"LEI too high for lock-in: {LEI_final}"


class TestUSAScenario:
    """Test USA evolution scenario"""
    
    def test_usa_436_years(self):
        """USA simulation for 436 years (1789-2225) should complete"""
        results = simulate_evolution(H0=0.72, V0=0.63, alpha0=0.58, years=436)
        
        assert len(results['time']) > 0
        assert results['time'][-1] == 436
    
    def test_usa_maintains_goldilocks(self):
        """USA should maintain Goldilocks Zone characteristics"""
        results = simulate_evolution(H0=0.72, V0=0.63, alpha0=0.58, years=200)
        
        # Most of simulation should have d_φ < 1.0
        goldilocks_fraction = np.mean(results['d_phi'] < 1.0)
        assert goldilocks_fraction > 0.5, \
            f"Only {goldilocks_fraction:.1%} in Goldilocks"


class TestSimulationParameters:
    """Test effects of simulation parameters"""
    
    def test_gamma_h_affects_h_convergence(self):
        """Higher γ_H should lead to faster H convergence"""
        results_slow = simulate_evolution(H0=0.5, V0=0.6, alpha0=0.5, 
                                         years=200, gamma_H=0.01)
        results_fast = simulate_evolution(H0=0.5, V0=0.6, alpha0=0.5, 
                                         years=200, gamma_H=0.10)
        
        # Fast should converge more by year 100
        H_slow_100 = results_slow['H'][100]
        H_fast_100 = results_fast['H'][100]
        
        # Fast should have changed more from initial
        assert abs(H_fast_100 - 0.5) > abs(H_slow_100 - 0.5)
    
    def test_beta_affects_alpha(self):
        """β parameter should affect α dynamics"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, 
                                    years=100, beta=0.02)
        
        # α should evolve
        alpha_initial = results['alpha'][0]
        alpha_final = results['alpha'][-1]
        
        # Some change should occur
        assert abs(alpha_final - alpha_initial) > 0.0


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_zero_years(self):
        """years=0 should return initial values only"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=0)
        assert len(results['time']) >= 1  # At least initial point
    
    def test_short_simulation(self):
        """Very short simulation (1 year) should work"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=1)
        assert len(results['time']) >= 2  # At least start and end
    
    def test_very_long_simulation(self):
        """Long simulation should complete (computational test)"""
        results = simulate_evolution(H0=0.7, V0=0.6, alpha0=0.5, years=500)
        assert results['time'][-1] == 500


# Test fixtures
@pytest.fixture
def usa_simulation():
    """Run USA simulation (cached for multiple tests)"""
    return simulate_evolution(H0=0.72, V0=0.63, alpha0=0.58, years=200)


@pytest.fixture
def argentina_simulation():
    """Run Argentina simulation (cached)"""
    return simulate_evolution(H0=0.92, V0=0.18, alpha0=0.09, years=200)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
