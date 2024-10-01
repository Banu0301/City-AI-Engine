import pandas as pd

def profile_city(data):
    population_density = data['population'] / data['area']
    avg_density = population_density.mean()
    return {"Average Density": avg_density}
