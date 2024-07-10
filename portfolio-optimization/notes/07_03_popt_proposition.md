## Assets Pricing Model QS 
*July 3, 2024*

Source: https://www.youtube.com/watch?v=5025sT9GrVs

- Call our universe of stocks to be the S&P500, then $i = 1, 2, ..., 500$ is our universe
- Let's say we have a model with $k$ factors then $k = 1, 2, ..., K$. Factors are variables that we can include in our model that explain the returns of stocks.
- $$r_i = \sum_{k=1}^{K} A_{ik}f_k + \delta_i$$
- We assume that $\text{corr}(f_k, \delta_j) = 0 \implies \text{cov} = 0 \ \forall \ k, j$

- The return on the i-th stock is the sum of the factor loading times the factor return plus the idiosyncratic return ($\delta_i$).
    - The idiosyncratic return is the return specific to the stock, which is not explained by the factors.
- $A_{ik}$ is a matrix of factor loadings, i.e. how much the i-th stock is exposed to the k-th factor. 
    - e.g. let us call the k-th factor inflation and appoint the $i=116th$ instrument to be Duke Energy (DUK), a utility company. 
    - Then the factor loading $A_{116,k}$ would be the sensitivity of DUK to inflation. 
    - Since a utility company is a necessity, Duke's services will remain relatively unchanged even if price levels change. 
    - As such, the factor loading $A_{116,k}$ would be low, since DUK is  insensitive to inflation. 
_______
**Portfolio** of stocks from a universe, let our universe be the S&P500 $N = 500$ 

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
- Now, we can consider how to use the above to optimize a portfolio:
- The video proposes 3 problems:


1. Maximize the expected return of the portfolio, subject to a constraint on the variance:
$$U(\mathbf{w}) = \mathbf{w}^T \mathbf{A} \mathbf{f} \rightarrow \text{max}, \text{ subject to } \mathbf{w}^T \Sigma \mathbf{w} \leq \sigma^2$$
2. Minimize the variance of the portfolio, subject to a constraint on the expected return:
$$U(\mathbf{w}) = \mathbf{w}^T \Sigma \mathbf{w} \rightarrow \text{min}, \text{ subject to } \mathbf{w}^T \mathbf{A} \mathbf{f} \geq \mu$$
3. Combine the two: Markowitz's mean-variance optimization problem
$$U(\mathbf{w}) = \mathbf{w}^T \mathbf{A} \mathbf{f} - \lambda \mathbf{w}^T \Sigma \mathbf{w} \rightarrow \text{max}$$
- $\lambda$ is a scalar that balances the trade-off between risk and returns

