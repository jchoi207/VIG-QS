## Assets Pricing Model - Jet Brains
https://www.youtube.com/watch?v=5025sT9GrVs

- Call our universe of stocks to be the S&P500, then $i = 1, 2, ..., 500$ is our universe
- Let's say we have a model with $k$ factors then $k = 1, 2, ..., K$. Factors are variables that we can include in our model that explain the returns of stocks.
- $$r_i = \sum_{k=1}^{K} A_{ik}f_k + \delta_i$$
- We assume that $\text{Corr}(f_k, \delta_j) = 0$ for all $k$ and $j$
- The return on the i-th stock is the sum of the factor loading times the factor return plus the idiosyncratic return. 
- The idiosyncratic return is the return specific to the stock, which is not explained by the factors.
- $A_{ik}$ is a matrix of factor loadings, i.e. how much the i-th stock is exposed to the k-th factor. 
    - e.g. let us call the k-th factor inflation and appoint the $i=116th$ instrument to be Duke Energy (DUK), a utility company. 
    - Then the factor loading $A_{116,k}$ would be the sensitivity of DUK to inflation. 
    - Since a utility company is a necessity, Duke's services will remain relatively unchanged even if price levels change. 
    - As such, the factor loading $A_{116,k}$ would be low, since DUK is not sensitive to inflation. 
_______
- **Portfolio** of stocks from a universe, let our universe be the S&P500 $N = 500$ 

**Returns**
- $$r_p = \sum_{i=1}^{500} w_i r_i = \sum_{i=1}^{500} w_i \sum_{k=1}^{K} A_{ik}f_k + \sum_{i=1}^{500} w_i \delta_i = \mathbf{w}^T \mathbf{A} \mathbf{f} + \mathbf{w}^T \mathbf{\delta}$$
- Dimensions:
    - $r_p$ is a scalar
    - $\mathbf{w}$ is a Nx1 vector of weights, where $\sum_{i=1}^{500} w_i = 1$
    - $A$ is a NxK matrix of factor loadings
        - K factor sensitivities for each of the N stocks
    - $\mathbf{f}$ is a Kx1 vector of factor returns
        - These are measurable quantities, e.g. inflation, interest rates, multiples, dividends, etc.
    - $\mathbf{\delta}$ is a Nx1 vector representing the idosyncratic returns
**Variance**
- Take the variance of $r_p$:
- $$\text{var}( \mathbf{w}^T \mathbf{A} \mathbf{f} + \mathbf{w}^T \mathbf{\delta}) = \text{var}(\mathbf{w}^T \mathbf{A} \mathbf{f}) + \text{var}(\mathbf{w}^T \mathbf{\delta}) + 2\text{cov}(\mathbf{w}^T \mathbf{A} \mathbf{f}, \mathbf{w}^T \mathbf{\delta})$$
- However, we know that $\text{cov}(\mathbf{w}^T \mathbf{A} \mathbf{f}, \mathbf{w}^T \mathbf{\delta}) = 0$ because the factors and idiosyncratic returns are uncorrelated, stated by $\text{Cov}(f_k, \delta_i) = 0$
- $$\text{var}(\mathbf{w}^T \mathbf{A} \mathbf{f}) = \mathbf{w}^T \mathbf{A} \text{Cov}(\mathbf{f}) \mathbf{A}^T \mathbf{w}$$
- $$\text{var}(\mathbf{w}^T \mathbf{\delta}) = \mathbf{w}^T \text{Cov}(\mathbf{\delta}) \mathbf{w}$$
- $$\text{var}(r_p) = \mathbf{w}^T \mathbf{A} \text{Cov}(\mathbf{f}) \mathbf{A}^T \mathbf{w} + \mathbf{w}^T \text{Cov}(\mathbf{\delta}) \mathbf{w}$$
- Note, we simplify the expression by defining $\Sigma = \mathbf{A} \text{Cov}(\mathbf{f}) \mathbf{A}^T + \text{Cov}(\mathbf{\delta})$
- $$\text{var}(r_p) = \mathbf{w}^T \Sigma \mathbf{w}$$

**Optimization**
- 








## Portfolio Management - MIT
https://www.youtube.com/watch?v=8TJQhQ2GZ0Y&list=PLhBQFP9t-O6bLl0cob4nHePdS517MlKcM

**Spending and Earning**
- Consider spending and earning with time across lifespan
    - Will never be equal, how do we compensate for their difference—cashflows from investments

**Mean-Variance Portfolio Theory**

Say we have a portfolio, with N assets
$$ R_p = \sum_{i=1}^{N} w_i R_i $$
$$ \text{Var}(R_p) = \sigma^2_p = \vec{w}^T \Sigma \vec{w} $$
- $\vec{w}$ is the weight vector
- $\Sigma$ is the covariance matrix

**Efficient Frontier**
- Given a set of assets, what is the best portfolio we can construct for a given objective
- The frontier is defined as the boundary for the highest return for a given standard deviation
    - "frontier" because it is the best we can do
### Two Asset Example
- $$R_P = w_q R_1 + (1- w_1)R_2$$
- $$\sigma^2_p = w_1^2 \sigma_1^2 + (1-w_1)^2 \sigma_2^2 + 2w_1(1-w_1)\sigma_1\sigma_2\rho_{12}$$

**Restrictions example 1**
- $R_1 = R_2$
- $\sigma_1 = 0$
- $\sigma_2 \ne 0$
- $\rho_{12} = undefined$

**Frontier example 1**
- Since the returns on either asset are the same, return on the portfolio is the same as the return on the assets, the weights don't matter. 
- However, at $w_1 = 0$, we have $\sigma^2_p = \sigma_2^2$
- At $w_1 = 1$, we have $\sigma^2_p = \sigma_1^2 = 0 $

**Restrictions example 2**
- $R_1 = R_2$
- $\sigma_1 \ne 0$
- $\sigma_2 \ne 0$
- $\sigma_1 = \sigma_2$
- $\rho_{12} = 0$

**Frontier example 2**
- When $w_1 = 1$ or 0, the portfolio is a single asset, so the variance is $\sigma_1^2 = \sigma_2^2$
- However, we can date the derivative of $\sigma_p^2$ w.r.t $w_1$ and minimize to find the optimal value of $w_1$ that minimizes the variance
- $$ \frac{\partial \sigma^2_p}{\partial w_1} = 2w_1\sigma_1^2 - 2(1-w_1)\sigma_2^2 = 0$$
- $$ w_1 = 1/2 \rightarrow \sigma^2_p = \frac{\sigma_2}{\sqrt{2}}$$
- This is the minimum variance portfolio, which represents the benefit of diversification
- Note that if $\rho_{12} = 1$, there is no diversification, so the variance is the same as the individual assets


## Portfolio Management - Python Demo
https://www.youtube.com/watch?v=BPIMwWCzkYY&list=PLcFcktZ0wnNnqefRpFMS1k9_VlhVw7bzc&index=2

```python
df = df.pivot(
    index='Date',
    columns='Symbol',
    values='Close'
)
```

## Active Portfolio Management - Texbook Notes
https://people.brandeis.edu/~yanzp/Study%20Notes/Active%20Portfolio%20Management.pdf
- Information Ratio = $$\frac{E[R_p - R_b]}{\sigma(R_p - R_b)}$$
    - The amount of additional exceptional return he can generate for each additional unit of risk
- It is important to define a benchmark portfolio, as exceptional returns are relative to the benchmark
- Portfolio management is a process: 
1. Raw info
2. Forecast 
3. Optimaly and efficiently constructs portfolios balacing forecasts of return against risk
- Active management is forecasting
- Active managers should forecast as much as possible


## Hudson and Thames - Portfolio Optimization: Mean-Variance Optimization and the Critical Line Algorithm.
https://www.youtube.com/watch?v=rjKnpkmBZXs
- Many different kinds of optimization problems (efficient returns, efficient frontier, critical line algorithm)


## Hudson and Thames - Portfolio Optimization: library showcase
https://www.youtube.com/watch?v=OeqIGC-WTWo
- Inputs: 
    - Expected returns
    - Covariance matrix
    - Risk aversion parameter
    - Solution type:
        - "Maximum Sharpe Ratio"
        - "Minimum Volatility"
        - "Efficient Returns"
    - Boundaries global: (min, max)
    - Boundaries specific: (min_i, max_i)


## Hudson and Thames - Hierarchical Equal Risk Contribution (HERC)
https://www.youtube.com/watch?v=k1Cjw9z1AKg&list=PLfv9eTYgatm0wXmHA5UZ0icAU-KRqhcsD&index=28


## TO DO
1. Watch more videos 
2. Portfolio optimization for mean variance using historical data for expected returns and covariance matrix
3. Consider other methods for expected returns and covariance  matrix (analyst scores, denoising covariance matrix)
4. Implement other optimization models: HERC, CVaR, etc. 
5. Aggregate all optimization models into a single class for easy use
6. Implement a backtesting framework for the optimization models



## Factor Modeling: The benefits of Disentangling Cross-Sectionally for Explaining Stock Returns
- Fama and French found that cross-sectional approahc based on firm characteristics is better than the time-series approach
- Cross-sectional analysis: comparing companies at a single point in time rather than over time
- Factor can refer to an attribute that proxies a common source of risk 
- Factor loadings are the sensitivities of the stock returns to the factors

### Time series regression
- Factors are estimated from the time series regression, and the factor loadings are constant

### Cross-sectional regression
- Factors are estimated from the cross-sectional approach at a moment in time, thus the factor loadings are time varying depending on the time window of interest.

### Comparison
- If we replace the time-varying factor loadings of the cross-sectional approach with the average time series factor loadings of the time series approach, this still outperforms the time series approach. Thus the cross-sectional factors are more informative than the time series factors.