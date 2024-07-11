import pandas as pd
import numpy as np
import cvxpy as cp
import metrics as met
import matplotlib.pyplot as plt
import yfinance as yf


def optimize(universe: list, start_date: str, end_date: str, min_max_weights: dict = None, short_selling: bool = False, min_return: float = 0.03) -> list:
    """
    Optimize a portfolio using quadratic programming. Note this method is minimum variance. 
    The optimizer assumes any real number of stocks can be purchased (no ints)

    TODO:
        Implement sharpe ratio optimization
        Implement efficient return optimiation (requires casting)
        Come up with a better way to measure expected returns

    Args:
        universe (list): List of possible stock tickers to include in the portfolio. Note, optimizer may not include all tickers.
        start_date (str): The start date for the historical data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the historical data in 'YYYY-MM-DD' format.
        min_max_weights (dict, optional): Dictionary where keys are tickers and values are lists 
                                          specifying the minimum and maximum weights for each ticker.
        short_selling (bool, optional): Whether to allow short-selling. If False, no short-selling is allowed.
        min_return (float, optional): Minimum expected return constraint as a decimal (e.g., 0.1 for 10%).
                                       Defaults to 0.1 (10%).

    Returns:
        opt_dict (dict): Optimal weights for each stock in the portfolio according to input constraints and objectives
        start_date (str): ####idk maybe remove dis
        end_date (str): ####idk maybe remove dis

    """
    n = len(universe)

    returns = []
    returns_matrix = pd.DataFrame()

    for ticker in universe:
        i = met.stock(ticker, start=start_date, end=end_date)
        returns.append(i.exp_ret())
        df = i.df
        returns_matrix[ticker] = df['Percent Change %']

    sigma = np.matrix(returns_matrix.cov())
    w = cp.Variable(n)

    A = np.ones((1, n))
    b = np.array([1])

    G = -np.eye(n)
    h = np.zeros(n)

    expected_returns = np.array(returns)
    min_return = np.array([min_return])

    if short_selling:
        G *= -1
    constraints = [G @ w <= h, A @ w == b, expected_returns @ w >= min_return]

    if min_max_weights:
        for stock, weight in min_max_weights.items():
            idx = universe.index(stock)
            constraints.append(w[idx] >= weight[0])
            constraints.append(w[idx] <= weight[1])

    prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w, sigma)), constraints)
    prob.solve()

    opt_weights = w.value
    expected_portfolio_return = expected_returns @ opt_weights
    expected_portfolio_variance = np.ravel(
        opt_weights.T @ sigma @ opt_weights).item()

    print(f"___________Summary___________")
    for x, y in zip(universe, opt_weights):
        print(f"{x}: {round(y*100, 3)}%")

    print(f"\nExpected monthly portfolio returns: {round(expected_portfolio_return, 2)}%")
    print(f"Portfolio st.dev: {round(expected_portfolio_variance, 2)} \n")

    opt_dict = {}
    for i in range(len(universe)):
        opt_dict[universe[i]] = list(opt_weights)[i]

    return opt_dict, start_date, end_date


def portfolio_performance(opt_dict: dict, start_date: str, end_date: str, principal: float = 1.00):
    """
    Calculate and plot the performance of a portfolio based on optimal weights.
    Also plot the performance of the individual instruments.
    Note this plot assumes that any real number of stocks can be purchased (no ints)

    Args:
        opt_dict (dict): Dictionary where keys are tickers and values are the optimal weights for each ticker.
        start_date (str): Start date for historical data.
        end_date (str): End date for historical data.
        principal (float): Initial investment amount in USD.

    Returns: 
        None
    """

    price_data = {}

    for ticker in list(opt_dict.keys()):
        price_data[ticker] = yf.Ticker(ticker).history(
            start=start_date, end=end_date)['Close']

    df_prices = pd.DataFrame(price_data)
    df_prices = df_prices.div(df_prices.iloc[0])

    weights = pd.Series(opt_dict)
    df_weights = pd.DataFrame(weights, columns=['Weight']).T
    portfolio_value = df_prices.dot(df_weights.T).sum(axis=1) * principal

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value.index, portfolio_value, label="Portfolio Value")

    for ticker in df_prices.columns:
        plt.plot(df_prices.index, df_prices[ticker] *
                 principal, label=f'{ticker} Investment', alpha=0.4)

    print(f"Simple Rate of Return: {round((portfolio_value.iloc[-1]-principal)/principal * 100, 2)}%")
    plt.title(f"Optimal Portfolio Performance w/ Principal {principal}$")
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()
