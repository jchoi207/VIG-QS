# Jonathan Choi
# 06/14/2024
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


class stock:
    def __init__(self, ticker: str, start: str = "2024-01-01", end: str = "2024-05-30", i: str = "1mo") -> None:
        """ 
        Initialization

        Params:
            ticker (str): ticker of the security
            start (str): start date for historical data (default is "2024-01-01")
            end (str): end date for historical data (default is "2024-05-30")
            i (str): interval for historical data (default is "1mo")
        """
        self._initialized = False
        self.ticker = ticker
        self.start = start
        self.end = end
        self.i = i

        self._load_data()

    def _load_data(self) -> None:
        """ 
        Loads historical data and calculates percentage change.
        """
        self.df = yf.Ticker(self.ticker).history(
            start=self.start, end=self.end, interval=self.i)
        self.df["Percent Change %"] = self.df["Close"].pct_change() * 100
        self.df.dropna(subset=["Percent Change %"], inplace=True)
        self.dividend_5 = yf.Ticker(self.ticker).info.get(
            "fiveYearAvgDividendYield")
        self.name = yf.Ticker(self.ticker).info.get("shortName")

    def st_dev(self) -> float:
        """
        Returns the standard deviation of returns.

        Returns:
            float: Standard deviation of returns.
        """
        st_deviation = round(np.std(self.df["Percent Change %"]), 2)
        return st_deviation

    def exp_ret(self) -> float:
        """
        Returns the expected value of historical returns.

        Returns:
            float: Expected value of historical returns.
        """
        exp_returns = round(np.average(self.df["Percent Change %"]), 2)
        return exp_returns

    def coeff_var(self) -> float:
        """
        Returns the coefficient of variation.

        Returns:
            float: Coefficient of variation.
        """
        self._load_data()
        coeff_variation = round(self.st_dev() / self.exp_ret(), 2)
        return coeff_variation

    def beta(self, benchmark: str = "VOO") -> float:
        """
        Returns the beta of self.ticker relative to the benchmark.

        Params:
            benchmark (str): Ticker of the benchmark security (default is "VOO").

        Returns:
            float: Beta of the security relative to the benchmark.
        """
        # create an instance for benchmark
        bmark = stock(benchmark, self.start, self.end)

        # merge dfs to not overwrite
        merged_df = pd.merge(self.df["Percent Change %"], bmark.df["Percent Change %"],
                             left_index=True, right_index=True, suffixes=("_stock", "_benchmark"))
        cov_matrix = np.cov(
            merged_df["Percent Change %_stock"], merged_df["Percent Change %_benchmark"])

        beta = round(cov_matrix[0][1] / cov_matrix[1][1], 2)

        return beta

    def all(self) -> list:
        """
        Returns all calculated metrics in a list.

        Returns:
            list: A list containing the name, ticker, expected returns, standard deviation, 
                  coefficient of variation, and beta of the security.
        """
        return self.name, self.ticker, self.exp_ret(), self.st_dev(), self.coeff_var(), self.beta()


def create_df_INDUSTRY(filename: str, start: str, end: str) -> pd.DataFrame:
    """
    Creates a DataFrame with metrics for each stock in the specified industries.

    Params:
        filename (str): Path to the file containing tickers by industry.
        start (str): Start date for historical data.
        end (str): End date for historical data.

    Returns:
        pd.DataFrame: DataFrame containing sector, name, ticker, expected returns, 
                      standard deviation, coefficient of variation, and beta for each stock.
    """
    with open(filename, "r") as file:
        tickers_dict = {
            "Tech": [],
            "Enrgy": [],
            "Fin": [],
            "Heal": []
        }
        for line in file:
            industry, ticker = line.strip().split(" ")
            tickers_dict[industry].append(ticker)
    industries = list(tickers_dict.keys())

    df = pd.DataFrame(columns=["Sector", "Name", "Ticker", "E[Returns]",
                               "StDev", "Coeff Var", "Beta"])
    k = 0
    for i in range(len(industries)):
        for j in range(len(tickers_dict[industries[i]])):
            df.loc[k] = [industries[i]] + [tickers_dict[industries[i]][j]] + \
                list(stock(tickers_dict[industries[i]][j], start, end).all())
            k += 1
    return df


def create_df(filename: str, start: str, end: str) -> pd.DataFrame:
    """
    Creates a DataFrame with metrics for each stock in the provided file.

    Params:
        filename (str): Path to the file containing tickers.
        start (str): Start date for historical data.
        end (str): End date for historical data.

    Returns:
        pd.DataFrame: DataFrame containing name, ticker, expected returns, 
                      standard deviation, coefficient of variation, and beta for each stock.
    """
    tickers = []
    with open(filename, "r") as file:
        for line in file:
            tickers.append(line.strip())
    print(tickers)
    df = pd.DataFrame(columns=["Name", "Ticker", "E[Returns]",
                               "StDev", "Coeff Var", "Beta",])

    for i in range(len(tickers)):
        df.loc[i] = list(stock(tickers[i], start, end).all())

    return df


def sort(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Sorts the DataFrame based on the specified column.

    Params:
        df (pd.DataFrame): DataFrame to be sorted.
        column (str): Column name to sort by.

    Returns:
        pd.DataFrame: Sorted DataFrame.
    """
    return df.sort_values(column, ascending=True)


# Example Call of YTD data ranking securities by standard deviation
# Replace MY_FILE.txt with your own file containing tickers separated by line breaks
# print(sort(create_df("MY_FILE.txt",
#                      "2024-01-01", "2024-06-14"), "StDev").dropna())
