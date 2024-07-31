## Balance Sheet Metrics
*July 17, 2024*


[Link](https://www.youtube.com/watch?v=3W_LwpeG8c8)

### Profitability Ratios:
#### Margin Ratios 
- Gross profit margin: sales revenue minus the cost of goods sold.
    - Use: measures efficiency of production process
$$\frac{\text{Gross Profit}}{\text{Revenue}}$$
- Operating profit margin: gross profit minus operating expenses.
    - Use: measures efficiency of operations
$$\frac{\text{GP - variable costs}}{\text{Revenue}}$$
- Net profit margin: revenue minus all expenses.
    - Use: measures overall profitabilit
$$\frac{\text{OP - tax - interest}}{\text{Revenue}}$$

#### Return Ratios
- Return on assets: 
    - Use: measures how well assets are used to generate profit
    - Assets are anything owned by the company that has value: cash, inventory, buildings, equipment, etc.
$$\frac{\text{Net Income}}{\text{Total Assets}}$$
- Return on equity: 
    - Use: measures how well shareholders' equity/stake is used to generate profit
$$\frac{\text{Net Income}}{\text{Total Equity}}$$
- Return on capital employed: 
    - Use: measures how well capital is used to generate profit
    - Capital employed = total assets - current liabilities
    - EBIT = earnings before interest and taxes
$$\frac{\text{EBIT}}{\text{Total Capital Employed}}$$

### Liquidity Ratios:
- Cash ratio: 
    - Use: measures how well a company can cover its short-term liabilities with cash
$$\frac{\text{Cash}}{\text{Current Liabilities}}$$
- Quick ratio: 
    - Use: measures how well a company can cover its short-term liabilities with cash and near-cash assets (just not inventory)
$$\frac{\text{Current Assets - Inventory}}{\text{Current Liabilities}}$$
- Current ratio: 
    - Use: measures how well a company can cover its short-term liabilities with all current assets
$$\frac{\text{Current Assets}}{\text{Current Liabilities}}$$

### Efficiency Ratios:
#### Turnover Ratios:
- Inventory turnover: 
    - Use: measures how many times a company sells its inventory in a year
    - COGS = cost of goods sold in a year
$$\frac{\text{COGS}}{\text{Average Inventory}}$$
- Receivables turnover: 
    - Use: measures how many times a company collects its receivables in a year
    - Receivables = money owed to the company by customers
$$\frac{\text{Revenue}}{\text{Average Receivables}}$$
- Payables turnover: 
    - Use: measures how many times a company pays its suppliers in a year

$$\frac{\text{COGS}}{\text{Average Payables}}$$

#### Cash Conversion Cycle:
- DSO: days sales outstanding
- DIO: days inventory outstanding
- DPO: days payable outstanding
- Use: measures how long it takes a company to convert its resources into cash
- CCC: $$\text{DSO} + \text{DIO} - \text{DPO}$$

### Leverage Ratios:
#### Balance Sheet Ratios:
- Debt to assets:
    - Use: measures how much of a company's assets are financed by debt
 $$\frac{\text{Total Debt}}{\text{Total Assets}}$$

- Debt to equity: 
    - Use: measures how much of a company's equity is financed by debt
$$\frac{\text{Total Debt}}{\text{Total Equity}}$$

#### Income Statement Ratios:
- Interest coverage ratio: 
    - Use: measures how well a company can cover its interest payments with its operating profit
$$\frac{\text{Operating Profit}}{\text{Interest Expense}}$$
- Debt service coverage ratio: 
    - Use: measures how well a company can cover its debt payments with its operating profit
    - EBITDA: earnings before interest, taxes, depreciation, and amortization
$$\frac{\text{EBITDA}}{\text{Total Debt Service}}$$

### Price Ratios:
#### Earnings Ratios
- Earnigns per share: 
    - Use: measures how much profit a company makes per share
$$\frac{\text{Net Profit}}{\text{Shares Outstanding}}$$
- Price to earnings: 
    - Use: measures how much investors are willing to pay for a company's earnings
$$\frac{\text{Price per share}}{\text{Earnings per share}}$$
- Price to earnings to growth ratio: 
    - Use: measures how much investors are willing to pay for a company's earnings growth
$$\frac{\text{Price to earnings}}{\text{EPS Growth rate}}$$

#### Dividend Ratios
- Dividends per share: 
    - Use: measures how much dividend a company pays per share
$$\frac{\text{Dividends}}{\text{Shares Outstanding}}$$
- Dividend yield: 
    - Use: measures how much dividend a company pays relative to its share price
$$\frac{\text{Dividends per share}}{\text{Price per share}}$$
- Dividend payout ratio: 
    - Use: how much of a company's earnings are paid out to shareholders as dividends
$$\frac{\text{Dividends}}{\text{Net Income}}$$


### Ratios Summary:
- **Profit Ratios**
    - Gross profit margin
    - Operating profit margin
    - Net profit margin
- **Return Ratios**
    - Return on assets
    - Return on equity
    - Return on capital employed
- **Liquidity Ratios**
    - Cash ratio
    - Quick ratio
    - Current ratio
- **Efficiency Ratios**
    - Inventory turnover
    - Receivables turnover
    - Payables turnover
    - Cash conversion cycle
- **Leverage Ratios**
    - Debt to assets
    - Debt to equity
    - Interest coverage ratio
    - Debt service coverage ratio
- **Price Ratios**
    - Earnings per share
    - Price to earnings
    - Price to earnings to growth ratio
- **Dividend Ratios**
    - Dividends per share
    - Dividend yield
    - Dividend payout ratio

### Methodology: 
<!-- - Screen companies based on these ratios: set a threshold for each ratio and only consider companies that meet all thresholds
- Ratios are usually calculated quarterly or annually, use EMA, weighting recent data more heavily
- Rank the stocks based on these ratios  -->
- Number of instruments: $N$
- Number of factors: $K$
- Number of time periods: $T$
- We assume that the factor matrix is constant over a reasonable time period
- $$r_{i,0} = \sum_{k=1}^{K} A_{i,k} f_{k,0} + \delta_{i,0} \\ r_{i,1} = \sum_{k=1}^{K} A_{i,k} f_{k,1} + \delta_{i,1} 
\\ ... \\
r_{i,T} = \sum_{k=1}^{K} A_{i,k} f_{k,T} + \delta_{i,T}
$$
- Linear regression in $K+1$ dimensions with $T$ samples

### Alternative Methodology:
- Leaving everything to MSE is not a good idea
- $K$ factors will add up
- Split up the factors into $q$ groups: profitability, liquidity, efficiency, leverage, price, dividend, macroeconomic, technical indicators.
- From there, we can use a weighted sum of the MSE loss for each of the $q$ groups