from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QMainWindow)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Assuming your strategies are defined in a separate module called strategies
import strategies


class FigurePlot(QWidget):
    def __init__(self, parent=None, width=15, height=15, dpi=200):
        super(FigurePlot, self).__init__(parent)
        self.width = width
        self.height = height
        self.dpi = dpi
        self.num_subplots = 3
        self.fig = Figure(figsize=(self.width, self.height), dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMaximumSize(1300, 1000)
        self.axes = self.fig.subplots(self.num_subplots, 1, sharex=True)
        self.fig.subplots_adjust(
            left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.3)

        self.setFocusPolicy(Qt.StrongFocus)
        self.user_interface()

    def user_interface(self):
        self.output_layout = QVBoxLayout()
        self.output_layout.addWidget(self.canvas)

        # Inputs
        input_layout = QVBoxLayout()
        self.input_security = QLineEdit(parent=self)
        self.input_security.setText('NVDA')
        self.input_security.editingFinished.connect(self.input_changed)
        self.input_security.setFocusPolicy(Qt.ClickFocus)

        self.input_strategy = QComboBox()
        self.input_strategy.addItems(('Crossover', 'Rate of Change', 'Relative Strength Index',
                                     'Money Flow Index', 'Stochastic Momentum', 'Bollinger Bands', 'todo Ichimoku Cloud', 'todo EMA', 'todo Candlestick', 'todo Earnings', 'todo NLP BERT (sentiment)'))
        self.input_strategy.currentIndexChanged.connect(self.input_changed)
        self.input_strategy.setFocusPolicy(Qt.ClickFocus)

        self.input_start_date = QLineEdit(parent=self)
        self.input_start_date.setText('2024-01-01')
        self.input_start_date.editingFinished.connect(self.input_changed)
        self.input_start_date.setFocusPolicy(Qt.ClickFocus)

        self.input_end_date = QLineEdit(parent=self)
        self.input_end_date.setText('2024-08-01')
        self.input_end_date.editingFinished.connect(self.input_changed)
        self.input_end_date.setFocusPolicy(Qt.ClickFocus)

        self.input_interval = QLineEdit(parent=self)
        self.input_interval.setText('1d')
        self.input_interval.editingFinished.connect(self.input_changed)
        self.input_interval.setFocusPolicy(Qt.ClickFocus)

        input_layout.addWidget(self.input_security)
        input_layout.addWidget(self.input_strategy)
        input_layout.addWidget(self.input_start_date)
        input_layout.addWidget(self.input_end_date)
        input_layout.addWidget(self.input_interval)

        self.total_layout = QHBoxLayout()
        self.total_layout.addLayout(self.output_layout)
        self.total_layout.addLayout(input_layout)

        self.setLayout(self.total_layout)

    def input_changed(self):
        self.plot_time_series()

    def plot_time_series(self):
        # for i in range(self.num_subplots):
        #     self.axes[i].cla()

        def update_subplots(num_subplots):

            self.fig.clf()
            # Update subplots
            self.axes = self.fig.subplots(num_subplots, 1, sharex=True)
            self.fig.subplots_adjust(
                left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.3)

        # Clear the previous plot

        # Retrieve inputs
        ticker = self.input_security.text()
        start_date = self.input_start_date.text()
        end_date = self.input_end_date.text()
        interval = self.input_interval.text()
        strategy_name = self.input_strategy.currentText()

        # Call the appropriate strategy based on user selection
        if strategy_name == 'Crossover':
            update_subplots(3)
            self.plot_crossover_strategy(
                ticker, start_date, end_date, interval)
        elif strategy_name == 'Rate of Change':
            update_subplots(3)
            self.my_roc(ticker, start_date, end_date, interval)
        elif strategy_name == 'Relative Strength Index':
            update_subplots(2)
            self.my_rsi(ticker, start_date, end_date, interval)
        elif strategy_name == 'Money Flow Index':
            update_subplots(2)
            self.my_mfi(ticker, start_date, end_date, interval)
        elif strategy_name == 'Stochastic Momentum':
            update_subplots(2)
            self.my_smi(ticker, start_date, end_date, interval)
        elif strategy_name == 'Bollinger Bands':
            update_subplots(2)
            self.my_bollinger_bands(ticker, start_date, end_date, interval)

        self.canvas.draw_idle()

    def set_main_title(self, strategy, ticker, start, end, interval):
        self.fig.suptitle(f'{ticker}, {strategy} from {start} to {end}', fontsize=10)

    def plot_crossover_strategy(self, ticker, start, end, interval, window_small=5, window_large=20):
        """
        Plot the crossover strategy.
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

        ax = self.axes
        self.set_main_title('Cross-Over', ticker, start, end, interval)
        ax[0].plot(time_series.index,
                   time_series['Close'].values, label='Close')
        ax[0].plot(time_series.index, time_series['SMA_small'].values,
                   color='purple', label='SMA_small')
        ax[0].plot(time_series.index, time_series['SMA_large'].values,
                   color='pink', label='SMA_large')
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].set_title('Close Prices and SMAs', fontsize=8)

        ax[1].plot(time_series.index, time_series['small - large'],
                   label='small - large')
        ax[1].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[1].set_ylabel('Price Differential (USD)', fontsize=6)
        ax[1].set_title('Small minus Large SMA Differential', fontsize=8)

        ax[2].plot(time_series.index, time_series['binary'],
                   label='small - large (binary)')
        ax[2].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[2].set_ylabel('Buy/Sell', fontsize=6)
        ax[2].set_title('Binary Differential', fontsize=8)
        ax[2].set_xlabel('Date', fontsize=6)

        for i, series in enumerate(['Close', 'small - large', 'binary']):
            for key in signals.keys():
                for date in signals[key]:
                    ax[i].scatter(date, time_series.loc[date, series], color=('g' if key == 'buy' else 'r'),
                                  zorder=10, marker=('^' if key == 'buy' else 'v'))
            ax[i].grid(zorder=-5)
            ax[i].legend(loc='best', fontsize=6)
            ax[i].tick_params(axis='both', labelsize=6)

    def my_roc(self, ticker, start, end, interval, shift=9):
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

        ax = self.axes
        self.set_main_title('Rate of Change', ticker, start, end, interval)

        ax[0].clear()
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices', fontsize=8)
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].legend(fontsize=6)
        ax[0].grid()
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(),
                           where=(time_series['ROC'] < 0), color='red', alpha=0.15, interpolate=False, zorder=-5)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(),
                           where=(time_series['ROC'] >= 0), color='green', alpha=0.15, interpolate=False, zorder=-5)

        ax[1].clear()
        ax[1].plot(time_series.index, time_series['ROC'], label='ROC')
        ax[1].set_title('Rate of Change (ROC)', fontsize=8)
        ax[1].set_ylabel('ROC (%)', fontsize=6)
        ax[1].legend(fontsize=6)
        ax[1].grid()
        ax[1].fill_between(time_series.index, 0, time_series['ROC'],
                           where=(time_series['ROC'] >= 0), color='g', alpha=0.2, interpolate=True)
        ax[1].fill_between(time_series.index, 0, time_series['ROC'],
                           where=(time_series['ROC'] < 0), color='r', alpha=0.2, interpolate=True)
        ax[1].axhline(y=0, color='k', linestyle='--', zorder=-4)

        ax[2].clear()
        ax[2].plot(time_series.index, time_series['ROC_derivative'],
                   label='ROC derivative', linewidth=1)
        ax[2].set_title('Derivative of ROC', fontsize=8)
        ax[2].set_ylabel('ROC/s', fontsize=6)
        ax[2].legend(fontsize=6)
        ax[2].grid()
        ax[2].axhline(y=0, color='k', linestyle='--', zorder=-4)
        ax[2].fill_between(time_series.index, 0, time_series['ROC_derivative'],
                           where=(time_series['ROC_derivative'] >= 0), color='g', alpha=0.2, interpolate=True)
        ax[2].fill_between(time_series.index, 0, time_series['ROC_derivative'],
                           where=(time_series['ROC_derivative'] < 0), color='r', alpha=0.2, interpolate=True)
        ax[2].set_xlabel('Date', fontsize=6)

        for i, series in enumerate(['Close', 'ROC', 'ROC_derivative']):
            for key in signals.keys():
                for date in signals[key]:
                    ax[i].scatter(date, time_series.loc[date, series], color=('g' if key == 'buy' else 'r'),
                                  zorder=10, marker=('^' if key == 'buy' else 'v'))
            ax[i].tick_params(axis='both', labelsize=6)

        self.canvas.draw_idle()

    def my_rsi(self, ticker, start, end, interval, lookback=14, min=30, max=70, height=8, width=10):
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
        average_loss = - \
            price_down.rolling(window=lookback, min_periods=1).mean()
        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))
        time_series['RSI'] = rsi
        signals = {'buy': [], 'sell': []}
        signals['buy'] = list(time_series[time_series['RSI'] < min].index)
        signals['sell'] = list(time_series[time_series['RSI'] > max].index)

        # Set up the figure and axes with custom size
        ax = self.axes
        self.set_main_title('RSI', ticker, start, end, interval)

        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices', fontsize=8)
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].legend(fontsize=6)
        ax[0].grid()
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(),
                           where=(time_series['RSI'] < min), color='green', alpha=0.15, interpolate=False, zorder=-5)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(),
                           where=(time_series['RSI'] > max), color='red', alpha=0.15, interpolate=False, zorder=-5)

        ax[1].plot(time_series.index, time_series['RSI'],
                   label='RSI', color='purple')
        ax[1].axhline(y=min, color='g', linestyle='--')
        ax[1].axhline(y=max, color='r', linestyle='--')
        ax[1].set_title('Relative Strength Index (RSI)', fontsize=8)
        ax[1].set_ylabel('RSI', fontsize=6)
        ax[1].set_xlabel('Date', fontsize=6)
        ax[1].fill_between(rsi.index, rsi, max, where=(
            rsi > max), alpha=0.25, color='r', interpolate=True)
        ax[1].fill_between(rsi.index, rsi, min, where=(
            rsi < min), alpha=0.25, color='g', interpolate=True)
        ax[1].axhline(y=max, color='r', zorder=-3, alpha=0.35,
                      linestyle='--', label='Sell')
        ax[1].axhline(y=min, color='g', zorder=-3,
                      alpha=0.35, linestyle='--', label='Buy')
        ax[1].legend(fontsize=6)
        ax[1].grid()

        for i, series in enumerate(['Close', 'RSI']):

            ax[i].tick_params(axis='both', labelsize=6)

        self.canvas.draw_idle()

    def my_mfi(self, ticker, start, end, interval, period=14, min=20, max=80):
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

        ax = self.axes
        self.set_main_title('MFI', ticker, start, end, interval)
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices', fontsize=8)
        ax[0].fill_between(MFI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(MFI > max), alpha=0.25, color='r', interpolate=False)
        ax[0].fill_between(MFI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(MFI < min), alpha=0.25, color='g', interpolate=False)
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].legend(fontsize=6)

        ax[1].plot(MFI.index, MFI, label='MFI', linewidth=1.25)
        ax[1].set_title('Money Flow Index (MFI)', fontsize=8)
        ax[1].set_ylabel('MFI', fontsize=6)
        ax[1].fill_between(MFI.index, MFI, max, where=(
            MFI > max), alpha=0.25, color='r', interpolate=True)
        ax[1].fill_between(MFI.index, MFI, min, where=(
            MFI < min), alpha=0.25, color='g', interpolate=True)
        ax[1].axhline(y=max, color='r', zorder=-3, alpha=0.35,
                      linestyle='--', label='Sell')
        ax[1].axhline(y=min, color='g', zorder=-3,
                      alpha=0.35, linestyle='--', label='Buy')
        ax[1].legend(fontsize=6)
        ax[1].set_xlabel('Date', fontsize=6)

        for i in range(2):
            ax[i].grid()
            ax[i].tick_params(axis='both', labelsize=6)
        self.canvas.draw_idle()

    def my_smi(self, ticker, start, end, interval, lookback=14, smooth_k=3, smooth_d=3, min_level=-40, max_level=40):
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
        ax = self.axes
        self.set_main_title('SMI', ticker, start, end, interval)
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].set_title('Closing Prices', fontsize=8)
        ax[0].fill_between(SMI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(SMI > max_level), alpha=0.25, color='r', interpolate=False)
        ax[0].fill_between(SMI.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(SMI < min_level), alpha=0.25, color='g', interpolate=False)
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].legend(fontsize=6)

        ax[1].plot(SMI.index, SMI, label='SMI', linewidth=1.25)
        ax[1].set_title('Stochastic Momentum Index (SMI)', fontsize=8)
        ax[1].set_ylabel('SMI', fontsize=6)
        ax[1].fill_between(SMI.index, SMI, max_level, where=(
            SMI > max_level), alpha=0.25, color='r', interpolate=True)
        ax[1].fill_between(SMI.index, SMI, min_level, where=(
            SMI < min_level), alpha=0.25, color='g', interpolate=True)
        ax[1].axhline(y=max_level, color='r', zorder=-3,
                      alpha=0.35, linestyle='--', label='Sell')
        ax[1].axhline(y=min_level, color='g', zorder=-3,
                      alpha=0.35, linestyle='--', label='Buy')
        ax[1].legend(fontsize=6)
        ax[1].set_xlabel('Date', fontsize=6)

        for i in range(2):
            ax[i].grid()
            ax[i].tick_params(axis='both', labelsize=6)
        self.canvas.draw_idle()

    def my_bollinger_bands(self, ticker, start, end, interval, lookback=20, num_std_dev=2):
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

        ax = self.axes
        self.set_main_title('Bollinger Bands', ticker, start, end, interval)
        ax[0].plot(time_series.index, time_series['Close'], label='Close')
        ax[0].plot(time_series.index, middle_band,
                   label='Middle Band (SMA)', linestyle='--')
        ax[0].plot(time_series.index, upper_band,
                   label='Upper Band', linestyle='--', color='r')
        ax[0].plot(time_series.index, lower_band,
                   label='Lower Band', linestyle='--', color='g')
        ax[0].fill_between(time_series.index, lower_band,
                           upper_band, color='grey', alpha=0.2)
        ax[0].set_title('Closing Prices with Bollinger Bands', fontsize=8)
        ax[0].set_ylabel('Price (USD)', fontsize=6)
        ax[0].legend(fontsize=6)

        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['Close'] < lower_band), alpha=0.25, color='g', interpolate=False)
        ax[0].fill_between(time_series.index, time_series['Close'].min(), time_series['Close'].max(
        ), where=(time_series['Close'] > upper_band), alpha=0.25, color='r', interpolate=False)

        ax[1].plot(time_series.index, upper_band - lower_band,
                   label='Upper-Lower Band Differential', color='orange')
        ax[1].set_title('Bollinger Band Differential', fontsize=8)
        ax[1].set_xlabel('Date', fontsize=6)

        for i in range(2):
            ax[i].grid()
            ax[i].legend(fontsize=6)
            ax[i].tick_params(axis='both', labelsize=6)

        self.canvas.draw_idle()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Visualizing Trading Strategies"
        self.setWindowTitle(self.title)
        self.plot = FigurePlot(self, width=10, height=15, dpi=200)
        self.setCentralWidget(self.plot)


app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

w = MainWindow()
w.show()
app.exec()
