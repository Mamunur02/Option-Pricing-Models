import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from option_pricing.base import OptionPricingModel

# Class calculating price of European options with the Monte Carlo Simulation
class MonteCarloPricing(OptionPricingModel):

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations):
        self.S_0 = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma

        # Parameters for simulation
        self.N = number_of_simulations
        self.num_of_steps = days_to_maturity
        self.dt = self.T / self.num_of_steps

    # Simulating price movements using a Brownian random process
    def simulate_prices(self):
        np.random.seed(20)
        self.simulation_results = None
        S = np.zeros((self.num_of_steps, self.N))
        S[0] = self.S_0

        for t in range(1, self.num_of_steps):
            # Random values to simulate Brownian motion
            Z = np.random.standard_normal(self.N)
            # Updating prices for next point in time
            S[t] = S[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dt + (self.sigma * np.sqrt(self.dt) * Z))

        self.simulation_results_S = S

    # Calculates payoffs at expiry, finds the average then discounts
    def _calculate_call_option_price(self):
        if self.simulation_results_S is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.simulation_results_S[-1] - self.K, 0))

    def _calculate_put_option_price(self):
        if self.simulation_results_S is None:
            return -1
        return np.exp(-self.r * self.T) * 1 / self.N * np.sum(np.maximum(self.K - self.simulation_results_S[-1], 0))

    # Plots simulated price movements
    def plot_simulation_results(self, num_of_movements):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(self.simulation_results_S[:, 0:num_of_movements])
        ax.axhline(self.K, c='k', label='Strike Price')
        ax.set_xlim([0, self.num_of_steps])
        ax.set_ylabel('Simulated price movements')
        ax.set_xlabel('Days in future')
        ax.set_title(f'First {num_of_movements}/{self.N} Random Price Movements')
        ax.legend(loc='best')  
        return fig