class SavePoint:
    def __init__(self, idx, V, R, delta, theta, E, S_bar, rupture):
        """
        Represents one epistemic state cycle snapshot
        """
        self.idx = idx
        self.V = V              # Projection state
        self.R = R              # Received input (raw or mutated)
        self.delta = delta      # ∆(t): drift
        self.theta = theta      # Θ(t): rupture threshold
        self.E = E              # E(t): misalignment memory
        self.S_bar = S_bar      # S̄(t): projected divergence
        self.rupture = rupture  # rupture occurred?

    def as_dict(self):
        return {
            "idx": self.idx,
            "V": self.V,
            "R": self.R,
            "∆": self.delta,
            "Θ": self.theta,
            "E": self.E,
            "S̄": self.S_bar,
            "rupture": self.rupture
        }


class SaveManager:
    def __init__(self):
        """Tracks sequence of RCC simulation cycles"""
        self.timeline = []

    def add_point(self, V, R, delta, theta, E, S_bar, rupture):
        idx = len(self.timeline)
        point = SavePoint(idx, V, R, delta, theta, E, S_bar, rupture)
        self.timeline.append(point)

    def get_point(self, idx):
        return self.timeline[idx] if 0 <= idx < len(self.timeline) else None

    def all_points(self):
        return [point.as_dict() for point in self.timeline]

    def rupture_points(self):
        return [pt.as_dict() for pt in self.timeline if pt.rupture]

    def reset(self):
        self.timeline = []
