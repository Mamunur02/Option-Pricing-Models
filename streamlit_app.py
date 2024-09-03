# Importing libraries
from enum import Enum
from datetime import datetime, timedelta
import streamlit as st
from option_pricing import BinomialTreeModel, BlackScholesModel, MonteCarloPricing, Ticker

class OPTION_PRICING_MODEL(Enum):
    BINOMIAL = 'Binomial Model'
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'

# Getting historical data
@st.cache_data
def get_historical_data(ticker):
    return Ticker.get_historical_data(ticker)

# Main title
st.title('Option pricing')

# User selected model from sidebar
pricing_method = st.sidebar.radio('Please select option pricing method',
                                  options=[model.value for model in OPTION_PRICING_MODEL])

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # Parameters for Binomial-Tree model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0.0, step=0.01)
    risk_free_rate = st.number_input('Risk-free rate%', 0.0, step=0.01)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_time_steps = st.slider('Number of time steps', 5000, 100000, 15000)

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for selected ticker
        data = get_historical_data(ticker)
        st.write(data.tail())
        fig = Ticker.plot_data(data, ticker, 'Adj Close')
        st.pyplot(fig)

        # Formatting simulation parameters
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate / 100
        sigma = Ticker.get_volatility(data, 'Adj Close')
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculating option price
        BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
        call_option_price = round(BOPM.calculate_option_price('Call Option'), 2)
        put_option_price = round(BOPM.calculate_option_price('Put Option'), 2)

        # Displaying call/put option price
        st.subheader(f'Call option price: {call_option_price}')
        st.subheader(f'Put option price: {put_option_price}')

elif pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    # Parameters for Black-Scholes model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0.0, step=0.01)
    risk_free_rate = st.number_input('Risk-free rate%', 0.0, step=0.01)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1),
                                      value=datetime.today() + timedelta(days=365))

    if st.button(f'Calculate option price for {ticker}'):

        data = get_historical_data(ticker)
        st.write(data.tail())
        fig = Ticker.plot_data(data, ticker, 'Adj Close')
        st.pyplot(fig)

        spot_price = Ticker.get_last_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate / 100
        sigma = Ticker.get_volatility(data, 'Adj Close')
        days_to_maturity = (exercise_date - datetime.now().date()).days

        BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
        call_option_price = round(BSM.calculate_option_price('Call Option'), 2)
        put_option_price = round(BSM.calculate_option_price('Put Option'), 2)

        st.subheader(f'Call option price: {call_option_price}')
        st.subheader(f'Put option price: {put_option_price}')

elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    # Parameters for Monte Carlo simulation
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0.0, step=0.01)
    risk_free_rate = st.number_input('Risk-free rate%', 0.0, step=0.01)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_simulations = st.slider('Number of simulations', 100, 100000, 10000)
    num_of_movements = st.slider('Number of price movement simulations to be visualized ', 0, int(number_of_simulations/10), 100)

    if st.button(f'Calculate option price for {ticker}'):
        data = get_historical_data(ticker)
        st.write(data.tail())
        fig = Ticker.plot_data(data, ticker, 'Adj Close')
        st.pyplot(fig)

        spot_price = Ticker.get_last_price(data, 'Adj Close')
        risk_free_rate = risk_free_rate / 100
        sigma = Ticker.get_volatility(data, 'Adj Close')
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Simulating stock movements
        MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
        MC.simulate_prices()

        # Visualizing Monte Carlo Simulation
        fig_2 = MC.plot_simulation_results(num_of_movements)
        st.pyplot(fig_2)

        call_option_price = round(MC.calculate_option_price('Call Option'), 2)
        put_option_price = round(MC.calculate_option_price('Put Option'), 2)

        st.subheader(f'Call option price: {call_option_price}')
        st.subheader(f'Put option price: {put_option_price}')