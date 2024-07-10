## Optimization Problems
*July 9, 2024*


1. Maximize expected returns subject to a constraint on the variance:
$$ \text{max}_{w} \ \ \mu^T \mathbf{w} \implies \text{min}_{w} \ \ -\mu^T \mathbf{w} $$
- Constraints:
    - $$ \mathbf{w}^T \Sigma \mathbf{w} = \sigma_t^2 $$
    - $$ \sum_{i=1}^{N} w_i = 1 $$
    - $$w_j \geq 0 \ \forall \ j$$

2. Minimize risk subject to a constraint on the expected return:
$$ \text{min}_{w} \ \ \mathbf{w}^T \Sigma \mathbf{w} $$
- Constraints:
    - $$ \mu^T \mathbf{w} = \mu_t $$
    - $$ \sum_{i=1}^{N} w_i = 1 $$
    - $$w_j \geq 0 \ \forall \ j$$

3. Markowitz Mean Variance Optimization:
$$ \text{min}_{w} \ \ -\mathbf{w}^T \Sigma \mathbf{w} + \lambda \mu^T \mathbf{w} $$
- Where $\lambda$ is called the risk aversion factor, and it balances the trade-off between risk and return.
- Constraints:
    - $$ \sum_{i=1}^{N} w_i = 1 $$
    - $$w_j \geq 0 \ \forall \ j$$


### Implementation
- CVXPY is an open source optimization library, which will be used to solve the above problems.
- We require the objective function and constraints to be defined as a convex optimization problem. 
- $$\text{minimize} \ \frac{1}{2} \mathbf{x}^T \mathbf{P} \mathbf{x} + \mathbf{q}^T \mathbf{x} $$
- $$\text{subject to} \ \mathbf{G} \mathbf{x}  \leq \mathbf{h}, \mathbf{A}\mathbf{x}  = \mathbf{b} $$
- Where $\mathbf{x}$ is the optimization variable, $\mathbf{P}$ is a positive semidefinite matrix, $\mathbf{q}$ is a vector, $\mathbf{G}$ is a matrix, $\mathbf{h}$ is a vector, $\mathbf{A}$ is a matrix, and $\mathbf{b}$ is a vector.

**Bordered Matrices**: 
- Assume we wish to optimize $Q = \mathbf{x}^T \mathbf{P} \mathbf{x}$ subject to $\mathbf{B}\mathbf{x} = \mathbf{0}$
- Let $\mathbf{x} \in \mathbb{R}^n$
- Let $\mathbf{P} \in \mathbb{R}^{n \times n}$
- Let $\mathbf{B} \in \mathbb{R}^{m \times n}$, where $m < n$ and $\text{rank}(\mathbf{B}) = m$, meaning that all $m$ constraints are linearly independent.

- The corresponding bordered matrix is:
$$\mathbf{H} = \begin{bmatrix} \mathbf{0} & \mathbf{B} \\ \mathbf{B^T} & \mathbf{P} \end{bmatrix}$$
- The bordered matrix $\mathbf{H} \in \mathbb{R}^{(n+m) \times (n+m)}$

**Theorem**: 
- If $\text{det}(\mathbf{H})$ and $\text{det}$ of the last $n-m$ leading principal minors have the same sign as $(-1)^m$, then $\mathbf{Q}$ is positive definite on $\mathbf{B}\mathbf{x} = \mathbf{0}$, and there is a unique global minimum on the constraint set