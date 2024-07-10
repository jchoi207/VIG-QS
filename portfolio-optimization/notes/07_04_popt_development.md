## Plan of Action 
*July 4, 2024*

1. Understand assumptions of the model:
    - Factors are variables that explain the returns of stocks
    - Idiosyncratic returns are uncorrelated with factors, and have mean 0 (noise)
    - Events follow a normal distribution (poor assumption, fat tails in reality)

2. Choose a universe of 25-50 financial instruments, equities, bonds, futures, real estate, crypto etc. 

3. Choose a set of factors that are quantifiable, and explain returns
    - Balance Sheet Metrics: cash flow, earnings, book value, dividends, multiples
    - Macroeconomic Factors: inflation, interest rates, GDP growth, unemployment (type of employment)
    - Market Factors: market/industry returns, volatility, momentum, liquidity
    - Sentiment Factors: news sentiment, social media sentiment, analyst sentiment (ratings)

4. Streamline Data Collection + Preprocessing
    - Time series data
    - Clean data, remove outliers, missing values, etc.
    - Normalize data (if needed) to ensure that all factors are on the same scale


5. Quantify the idiosyncratic return vector $\delta \in \mathbb{R}^{N}$
    - $r_i = \sum_{k=1}^{K} A_{ik}f_k + \delta_i = \mathbf{A}_i \mathbf{f} + \delta_i \rightarrow \delta_i = r_i - \mathbf{A}_i \mathbf{f}$
    - In other words, if we express the returns of our portfolio as an N x 1 vector, $\vec{\delta} \perp \mathbf{f}$ or $\vec{\delta} \cdot \mathbf{f} = 0$. So the idiosyncratic returns are the residuals of the model. 

6. Construct the factor loading matrix $\mathbf{A} \in \mathbb{R}^{N \times K}$
    - Learn the factor loadings by running a regression of the returns of each stock on the factors
    - Use MSELoss() to minimize the difference between the predicted returns and actual returns

```python

import pytorch as torch
import torch.nn as nn

class FactorModelOne(nn.Module):
    def __init__(self, K):
        super(FactorModelOne, self).__init__()
        self.fc1 = nn.Linear(K, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 256)
        self.fc4 = nn.Linear(256, 128)
        self.fc5 = nn.Linear(128, K)
        
    def forward(self, f):
        x = torch.relu(self.fc1(f))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = self.fc5(x)
        return x


## train_data is comprised of factors as features and returns as labels 
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)


model = FactorModelOne(K)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
.........
```

We coul also use a linear regression model to learn the factor loadings:
$$r_i = A_{i1}f_1 + A_{i2}f_2 + ... + A_{iK}f_K + \delta_i$$
- Tricky part in either case is quantifying $\delta_i$

7. Develop or find optimization algorithms for mean variance