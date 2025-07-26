import numpy as np

class RCC:
    def __init__(self, V0=0.5, E0=0.0, 
                 Θ0=0.35, a=0.05, c=0.1, σ_Θ=0.025, Δt=0.1):
        """
        RCC Core Engine implementing Axioms 1-4 and foundational state variables
        """
        self.V = V0          # Current projection state
        self.E = E0          # Epistemic misalignment accumulator
        self.V0 = V0         # Reset base projection
        self.Θ0 = Θ0         # Base rupture threshold
        self.a = a           # E(t) influence on rupture threshold
        self.c = c           # Drift scaling in E(t)
        self.σ_Θ = σ_Θ       # Noise in rupture threshold
        self.Δt = Δt         # Timestep size for S̄(t)

        self.history = []    # State trace across cycles

    def rupture_threshold(self):
        """Computes Θ(t) using adaptive + stochastic terms"""
        noise = np.random.normal(0, self.σ_Θ)
        return self.Θ0 + self.a * self.E + noise

    def project_divergence(self, R_t, V_prev):
        """Computes S̄(t): Projected epistemic divergence"""
        return (R_t - V_prev) / self.Δt

    def update(self, R_t):
        """
        Core RCC update function for timestep t:
        - Computes ∆(t), Θ(t), S̄(t)
        - Determines rupture or realignment
        - Updates V(t), E(t) accordingly
        - Stores full trace
        """
        V_prev = self.V
        Δ = abs(R_t - V_prev)                              # Axiom 1
        Θ = self.rupture_threshold()                       # Axiom 6

        if Δ > Θ:  # Rupture triggered                     # Axiom 3
            self.V = self.V0
            self.E = 0
            rupture = True
        else:       # Continuity Monad ⊙                   # Axiom 4
            k = np.random.uniform(0.3, 0.7)
            self.V = V_prev + k * Δ * (1 + self.E)
            self.E += self.c * Δ                           # Axiom 2
            rupture = False

        S̄ = self.project_divergence(R_t, V_prev)

        self.history.append({
            'V': self.V,
            'R': R_t,
            'Δ': Δ,
            'Θ': Θ,
            'E': self.E,
            'S̄': S̄,
            'rupture': rupture
        })

        return self.V, self.E, Δ, Θ, S̄, rupture

    def get_history(self):
        return self.history
