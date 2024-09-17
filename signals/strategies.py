import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

def my_cross_over_strategy(ticker, start, end, interval, window_small=5, window_large=20, plot_graphs=True, height=12, width=10):
    """
    Generate buy/sell signals based on the crossover of small and large moving averages.
    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)
    time_series['SMA_small'] = time_series['Close'].rolling(
        window=window_small).mean()
    time_series['SMA_large'] = time_series['Close'].rolling(
        window=window_large).mean()
    time_series['Small > Large'] = time_series['SMA_small'] > time_series['SMA_large']

    signals = {'buy': [], 'sell': []}
    boolean_column = time_series['Small > Large']
    previous = boolean_column.values[0]

    for index in boolean_column.index:
        current = boolean_column[index]
        if previous != current:
            if current:
                signals['buy'].append(index)
            else:
                signals['sell'].append(index)
            previous = current

    time_series['small - large'] = time_series['SMA_small'] - \
        time_series['SMA_large']
    time_series['binary'] = time_series['small - large'].apply(
        lambda x: -1 if x < 0 else 1)

    if plot_graphs:
        fig, ax = plt.subplots(3, 1, figsize=(width, height), sharex=True)
        ax[0].plot(time_series.index,
                   time_series['Close'].values, label='Close')
        ax[0].plot(time_series.index, time_series['SMA_small'].values,
                   color='purple', label='SMA_small')
        ax[0].plot(time_series.index, time_series['SMA_large'].values,
                   color='pink', label='SMA_large')
        ax[0].set_ylabel('Price (USD)')
        ax[0].set_title('Close Prices and SMAs')

        ax[1].plot(time_series.index, time_series['small - large'],
                   label='small - large')
        ax[1].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[1].set_ylabel('Price Differential (USD)')
        ax[1].set_title('Small minus Large SMA Differential')

        ax[2].plot(time_series.index, time_series['binary'],
                   label='small - large (binary)')
        ax[2].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[2].set_ylabel('Buy/Sell')
        ax[2].set_title('Binary Differential')

        for i, series in enumerate(['Close', 'small - large', 'binary']):
            for key in signals.keys():
                for date in signals[key]:
                    ax[i].scatter(date, time_series.loc[date, series], color=(
                        'g' if key == 'buy' else 'r'), zorder=10, marker=('^' if key == 'buy' else 'v'))
            ax[i].grid(zorder=-5)
            ax[i].legend(loc='best')
            ax[i].set_xlabel('Date')
        plt.tight_layout()
        plt.show()

    return signals


def my_roc(ticker, start, end, interval, shift=9, plot_graphs=True, height=12, width=10):
    """
    Generate buy/sell signals based on the Rate of Change (ROC) and its derivative.
    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)
    time_series['ROC'] = (time_series['Close'] /
                          time_series['Close'].shift(shift) - 1) * 100
    time_series['ROC_derivative'] = (time_series['ROC'] - time_series['ROC'].shift(
        1)) / pd.to_timedelta(time_series.index.to_series().diff(1)).dt.total_seconds()

    signals = {'buy': [], 'sell': []}
    signals['buy'] = list(
        time_series[time_series['ROC_derivative'] > 0.0001].index)
    signals['sell'] = list(
        time_series[time_series['ROC_derivative'] < -0.0001].index)

    if plot_graphs:
        fig, ax = plt.subplots(3, 1, figsize=(width, height), sharex=True)
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices')
        ax[0].set_ylabel('Price (USD)')
        ax[0].legend()
        ax[0].grid()
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['ROC'] < 0), color='red', alpha=0.15, interpolate=False, zorder=-5)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['ROC'] >= 0), color='green', alpha=0.15, interpolate=False, zorder=-5)

        ax[1].plot(time_series.index, time_series['ROC'], label='ROC')
        ax[1].set_title('Rate of Change (ROC)')
        ax[1].set_ylabel('ROC (%)')
        ax[1].legend()
        ax[1].grid()
        ax[1].fill_between(time_series.index, 0, time_series['ROC'], where=(
            time_series['ROC'] >= 0), color='g', alpha=0.2, interpolate=True)
        ax[1].fill_between(time_series.index, 0, time_series['ROC'], where=(
            time_series['ROC'] < 0), color='r', alpha=0.2, interpolate=True)
        ax[1].axhline(y=0, color='k', linestyle='--', zorder=-4)

        ax[2].plot(time_series.index, time_series['ROC_derivative'],
                   label='ROC derivative', linewidth=1)
        ax[2].set_title('Derivative of ROC')
        ax[2].set_ylabel('ROC/s')
        ax[2].legend()
        ax[2].grid()
        ax[2].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[2].fill_between(time_series.index, 0, time_series['ROC_derivative'], where=(
            time_series['ROC_derivative'] >= 0), color='g', alpha=0.2, interpolate=True)
        ax[2].fill_between(time_series.index, 0, time_series['ROC_derivative'], where=(
            time_series['ROC_derivative'] < 0), color='r', alpha=0.2, interpolate=True)

        for i, series in enumerate(['Close', 'ROC', 'ROC_derivative']):
            for key in signals.keys():
                for date in signals[key]:
                    ax[i].scatter(date, time_series.loc[date, series], color=(
                        'g' if key == 'buy' else 'r'), zorder=10, marker=('^' if key == 'buy' else 'v'))
            ax[i].set_xlabel('Date')

        plt.tight_layout()
        plt.show()

    return signals


def my_rsi(ticker, start, end, interval, lookback=14, min=30, max=70, plot_graphs=True, height=8, width=10):
    """
    Generate buy/sell signals based on the Relative Strength Index (RSI).

    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)
    difference = time_series['Close'].diff(1)
    price_up = difference.copy()
    price_down = difference.copy()
    price_up[price_up < 0] = 0
    price_down[price_down > 0] = 0
    average_gain = price_up.rolling(window=lookback, min_periods=1).mean()
    average_loss = -price_down.rolling(window=lookback, min_periods=1).mean()
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    time_series['RSI'] = rsi

    signals = {'buy': [], 'sell': []}
    signals['buy'] = list(time_series[time_series['RSI'] < min].index)
    signals['sell'] = list(time_series[time_series['RSI'] > max].index)

    if plot_graphs:
        fig, ax = plt.subplots(2, 1, figsize=(width, height), sharex=True)
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices')
        ax[0].set_ylabel('Price (USD)')
        ax[0].legend()
        ax[0].grid()
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['RSI'] < min), color='green', alpha=0.15, interpolate=False, zorder=-5)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['RSI'] > max), color='red', alpha=0.15, interpolate=False, zorder=-5)

        ax[1].plot(time_series.index, time_series['RSI'],
                   label='RSI', color='purple')
        ax[1].axhline(y=min, color='g', linestyle='--')
        ax[1].axhline(y=max, color='r', linestyle='--')
        ax[1].set_title('Relative Strength Index (RSI)')
        ax[1].set_ylabel('RSI')
        ax[1].set_xlabel('Date')
        ax[1].legend()
        ax[1].grid()

        for i, series in enumerate(['Close', 'RSI']):
            for key in signals.keys():
                for date in signals[key]:
                    ax[i].scatter(date, time_series.loc[date, series], color=(
                        'g' if key == 'buy' else 'r'), zorder=10, marker=('^' if key == 'buy' else 'v'))
            ax[i].set_xlabel('Date')

        plt.tight_layout()
        plt.show()

    return signals


def my_mfi(ticker, start, end, interval, period=14, min=20, max=80, plot_graphs=True, height=8, width=10):
    """
    Calculate the Money Flow Index (MFI) and generate buy/sell signals based on MFI levels.
    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)
    time_series['typical_price'] = (
        time_series['Close'] + time_series['High'] + time_series['Low']) / 3
    time_series['money_flow'] = time_series['typical_price'] * \
        time_series['Volume']

    time_series['flows'] = time_series['typical_price'].diff(1)
    time_series.dropna(inplace=True)

    time_series['flow_positive'] = time_series['money_flow'].where(
        time_series['flows'] > 0, 0)
    time_series['flow_negative'] = time_series['money_flow'].where(
        time_series['flows'] < 0, 0)

    plus_mf = time_series['flow_positive'].rolling(window=period).sum()
    minus_mf = time_series['flow_negative'].rolling(window=period).sum()

    MFI = 100 * (plus_mf / (plus_mf + minus_mf))

    signals = {'buy': [], 'sell': []}
    signals['buy'] = MFI[MFI < min].index
    signals['sell'] = MFI[MFI > max].index

    if plot_graphs:
        fig, ax = plt.subplots(2, 1, figsize=(width, height), sharex=True)

        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices')
        ax[0].fill_between(MFI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(MFI > max), alpha=0.25, color='r', interpolate=False)
        ax[0].fill_between(MFI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(MFI < min), alpha=0.25, color='g', interpolate=False)
        ax[0].set_ylabel('Price (USD)')

        ax[1].plot(MFI.index, MFI, label='MFI', linewidth=1.25)
        ax[1].set_title('Money Flow Index (MFI)')
        ax[1].set_ylabel('MFI')
        ax[1].fill_between(MFI.index, MFI, max, where=(
            MFI > max), alpha=0.25, color='r', interpolate=True)
        ax[1].fill_between(MFI.index, MFI, min, where=(
            MFI < min), alpha=0.25, color='g', interpolate=True)
        ax[1].axhline(y=max, color='r', zorder=-3, alpha=0.35,
                      linestyle='--', label='Sell')
        ax[1].axhline(y=min, color='g', zorder=-3,
                      alpha=0.35, linestyle='--', label='Buy')

        for i in range(2):
            ax[i].set_xlabel('Date')
            ax[i].grid()
            ax[i].legend()
        plt.tight_layout()
        plt.show()

    return signals

def my_smi(ticker, start, end, interval, lookback=14, smooth_k=3, smooth_d=3, min_level=-40, max_level=40, plot_graphs=True, height=8, width=10):
    """
    Calculate the Stochastic Momentum Index (SMI) and generate buy/sell signals based on SMI levels.
    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)
    high_max = time_series['High'].rolling(window=lookback).max()
    low_min = time_series['Low'].rolling(window=lookback).min()

    mid_point = (high_max + low_min) / 2
    price_diff = time_series['Close'] - mid_point

    smi_numerator = price_diff.rolling(window=smooth_k).mean()
    smi_denominator = (high_max - low_min).rolling(window=smooth_k).mean()

    SMI = (smi_numerator / (smi_denominator / 2)) * 100
    SMI = SMI.rolling(window=smooth_d).mean().dropna()

    signals = {'buy': [], 'sell': []}
    signals['buy'] = SMI[SMI < min_level].index
    signals['sell'] = SMI[SMI > max_level].index

    if plot_graphs:
        fig, ax = plt.subplots(2, 1, figsize=(width, height), sharex=True)

        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices')
        ax[0].fill_between(SMI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(SMI > max_level), alpha=0.25, color='r', interpolate=False)
        ax[0].fill_between(SMI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(SMI < min_level), alpha=0.25, color='g', interpolate=False)
        ax[0].set_ylabel('Price (USD)')

        ax[1].plot(SMI.index, SMI, label='SMI', linewidth=1.25)
        ax[1].set_title('Stochastic Momentum Index (SMI)')
        ax[1].set_ylabel('SMI')
        ax[1].fill_between(SMI.index, SMI, max_level, where=(
            SMI > max_level), alpha=0.25, color='r', interpolate=True)
        ax[1].fill_between(SMI.index, SMI, min_level, where=(
            SMI < min_level), alpha=0.25, color='g', interpolate=True)
        ax[1].axhline(y=max_level, color='r', zorder=-3,
                      alpha=0.35, linestyle='--', label='Sell')
        ax[1].axhline(y=min_level, color='g', zorder=-3,
                      alpha=0.35, linestyle='--', label='Buy')

        for i in range(2):
            ax[i].set_xlabel('Date')
            ax[i].grid()
            ax[i].legend()
        plt.tight_layout()
        plt.show()

    return signals


def my_bollinger_bands(ticker, start, end, interval, lookback=20, num_std_dev=2, plot_graphs=True, height=8, width=10):
    """
    Calculate Bollinger Bands and generate buy/sell signals based on the closing price relative to the bands.

    """
    time_series = yf.Ticker(ticker).history(
        start=start, end=end, interval=interval)

    middle_band = time_series['Close'].rolling(window=lookback).mean()
    std_dev = time_series['Close'].rolling(window=lookback).std()

    upper_band = middle_band + (std_dev * num_std_dev)
    lower_band = middle_band - (std_dev * num_std_dev)

    signals = {'buy': [], 'sell': []}
    signals['buy'] = time_series[time_series['Close'] < lower_band].index
    signals['sell'] = time_series[time_series['Close'] > upper_band].index

    if plot_graphs:
        fig, ax = plt.subplots(2, 1, figsize=(width, height), sharex=True)

        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].plot(time_series.index, middle_band,
                   label='Middle Band (SMA)', linestyle='--')
        ax[0].plot(time_series.index, upper_band,
                   label='Upper Band', linestyle='--', color='r')
        ax[0].plot(time_series.index, lower_band,
                   label='Lower Band', linestyle='--', color='g')
        ax[0].fill_between(time_series.index, lower_band,
                           upper_band, color='grey', alpha=0.2)
        ax[0].set_title('Closing Prices with Bollinger Bands')
        ax[0].set_ylabel('Price (USD)')

        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['Close'] < lower_band), alpha=0.25, color='g', interpolate=False)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['Close'] > upper_band), alpha=0.25, color='r', interpolate=False)

        ax[1].plot(time_series.index, upper_band - lower_band,
                   label='Upper-Lower Band Differential', color='orange')
        ax[1].set_title('Bollinger Band Differential')

        for i in range(2):
            ax[i].set_xlabel('Date')
            ax[i].grid()
            ax[i].legend()
        plt.tight_layout()
        plt.show()

    return signals
