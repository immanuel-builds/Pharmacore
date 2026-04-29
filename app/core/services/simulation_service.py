import math
import numpy as np

class SimulationService:
    @staticmethod
    def run_simulation(substances_data, duration_hours=24, step_hours=1):
        """
        Time-based modeling of substance concentration using first-order decay.
        substances_data: List of dicts with {name, dose, start_time, half_life}
        """
        timeline = np.arange(0, duration_hours + step_hours, step_hours)
        results = []

        for sub in substances_data:
            name = sub.get('name')
            dose = sub.get('dose', 1.0)
            start_time = sub.get('start_time', 0)
            half_life = sub.get('half_life')

            if not half_life:
                continue

            k = math.log(2) / half_life
            concentrations = []

            for t in timeline:
                if t < start_time:
                    conc = 0.0
                else:
                    # C(t) = C0 * e^(-k * (t - t_start))
                    conc = dose * math.exp(-k * (t - start_time))
                concentrations.append(round(conc, 4))

            results.append({
                "name": name,
                "timeline": timeline.tolist(),
                "concentrations": concentrations
            })

        return results
