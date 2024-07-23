# Heston Model

## Specification

$$
\begin{align*}
dS_t &= \mu_t S_tdt+\sqrt{\nu_t}S_tdW_t^S\\
d\nu_t &= \kappa(\theta-\nu_t)dt + \eta \sqrt{\nu_t}dW_t^\nu\\
dW_t^SdW_t^\nu &= \rho dt\\
\end{align*}
$$

> [!Constraint]
> $\nu_t$ positive if $2\kappa\theta > \xi^2$

- $\nu_0$: Initial variance `{python} initial_variance`
- $\theta$: Long-term volatility  `{python} long_term_volatility`
- $\eta$: Volatility of volatility `{python} volatility_of_volatility`
- $\kappa$: Mean reversion rate `{python} mean_reversion_rate`
- $\rho$: Correlation between Wiener processes `{python} wiener_correlation`

## Integrated Variance

$$
\nu_{t_{2}}=\nu_{t_{1}}
$$

$$
\begin{align*}
IV_{[t_{1},t_{2}]}&=\int_{t_{1}}^{t_{2}} \nu_{t}\:dt  \\
&=
\end{align*}
$$

[^https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1279850]
