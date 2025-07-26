import numpy as np

def mutate_reception(R_t, S_bar_t, E_t, gamma=0.8, sigma=0.05):
    """
    RCC Post-Rupture Mutation Function

    Simulates cognitive perception distortion after rupture:
    - Injects hallucination into reception field based on:
      - S̄(t): Projected divergence vector (direction of drift)
      - E(t): Accumulated epistemic misalignment
      - gamma: Amplification gain (severity of bias injection)
      - sigma: Noise level (uncertainty in hallucination)

    Returns:
        R_prime_t (float): mutated reception field
    """
    # Bias = direction of drift × magnitude of misalignment × gain
    bias = S_bar_t * E_t * gamma

    # Gaussian noise simulating epistemic uncertainty
    hallucination = np.random.normal(loc=bias, scale=sigma)

    # Final morphed reception field
    R_prime_t = R_t + hallucination

    return R_prime_t
