---
aliases:
  - Moving Average Process
  - Moving Average
  - MA
  - MA(q)
tags:
  - Definition
  - TimeSeries
  - Mathematics
  - Statistics
  - SignalProcessing
type: definition
mathLink: $\operatorname*{MA}\left(q\right)$
---
> [!definition]+ Definition: Moving Average Process
> A [[Definition - Time Series|Time Series]] [[Definition - Time Series|$X_{t}$]] is a [[Definition - Moving Average Process|Moving Average Process]] [[Definition - Moving Average Process]] with coefficients $\vec{\theta}\in \mathbb{R}^{q}$ if for $\varepsilon_{t}\sim$[[Definition - White Noise Process]], $\forall\: t$:
> $$
\begin{align*}
X_{t}&=\mu+\varepsilon_{t} + \sum\limits_{i=1}^{q}\theta_{i}\varepsilon_{t-i}=\mu+\left(1+ \sum\limits_{i=1}^{q}\theta_{i}L^{i}\right)\varepsilon_{t} 
\end{align*}
> $$
^definition

> [!assumption]+ 
> We often assume $\mu=0$ since we can usually just calculate the mean of our time series and subtract it.
^assumptions

```reference title:Code, fold, ref:[[Definition - Moving Average Process]]
file: [[moving_average_process.py]]
```
^code

# Properties

### [[Definition - Mean Function|Mean Function]]

We have that $\forall\: t$:

$$
\begin{align*}
\mathbb{E}\left[X_{t}\right]
&=\mathbb{E}\left[\mu+\varepsilon_{t}+\sum\limits_{i=1}^{q}\theta_{i}\varepsilon_{t-i}\right] \\
&=\mu+\mathbb{E}\left[\varepsilon_{t}\right]+\sum\limits_{i=1}^{q}\theta_{i}\mathbb{E}\left[\varepsilon_{t-i}\right] \\
&=\mu+0+\sum\limits_{i=1}^{q}\theta_{i}\cdot0 \\
&=\mu
\end{align*}
$$

### [[Definition - Variance Function|Variance Function]]

Here we use the [[#^assumptions|assumption]] $\mu=0$:

Taking $\theta_{0}=1$, we have that $\forall\: t$:

$$
\begin{align*}
\operatorname*{Var}\left[X_{t}\right]
&=\mathbb{E}\left[X_{t}^{2}\right] \\
&=\mathbb{E}\left[\left(0+\varepsilon_{t}+\sum\limits_{i=1}^{q}\theta_{i}\varepsilon_{t-i}\right)^{2}\right] \\
&=\mathbb{E}\left[\left(\sum\limits_{i=0}^{q}\theta_{i}\varepsilon_{t-i}\right)^{2}\right] \\
&=\mathbb{E}\left[\sum\limits_{i=0}^{q}\theta_{i}^{2}\varepsilon_{t-i}^{2}+\sum\limits_{i=0}^{q}\sum\limits_{\displaylines{j=0\\i \neq j}}^{q}\theta_{i}\varepsilon_{t-i}\theta_{j}\varepsilon_{t-j}\right] \\
&=\sum\limits_{i=0}^{q}\theta_{i}^{2}\mathbb{E}\left[\varepsilon_{t-i}^{2}\right]+\sum\limits_{i=0}^{q}\sum\limits_{\displaylines{j=0\\i \neq j}}^{q}\theta_{i}\theta_{j}\mathbb{E}\left[\varepsilon_{t-i}\varepsilon_{t-j}\right] \\
&=\sum\limits_{i=0}^{q}\theta_{i}^{2}\operatorname*{Var}\left[\varepsilon_{t-i}\right]+\sum\limits_{i=0}^{q}\sum\limits_{\displaylines{j=0\\i \neq j}}^{q}\theta_{i}\theta_{j}\operatorname*{Cov}\left[\varepsilon_{t-i}\varepsilon_{t-j}\right] \\
&=\sum\limits_{i=0}^{q}\theta_{i}^{2}\sigma^{2}+\sum\limits_{i=0}^{q}\sum\limits_{\displaylines{j=0\\i \neq j}}^{q}\theta_{i}\theta_{j}\cdot 0 \\
&=\sigma^{2}\sum\limits_{i=0}^{q}\theta_{i}^{2}
\end{align*}
$$


### [[Definition - Covariance Function|Covariance Function]]

Here we use the [[#^assumptions|assumption]] $\mu=0$:

Taking $\theta_{0}=1$, we have that $\forall\: t$:

$$
\begin{align*}
\operatorname*{Cov}\left[X_{t},X_{s}\right]
&=\mathbb{E}\left[X_{t}X_{s}\right] \\
&=\mathbb{E}\left[\left(0+\varepsilon_{t}+\sum\limits_{i=1}^{q}\theta_{i}\varepsilon_{t-i}\right)\left(0+\varepsilon_{s}+\sum\limits_{i=1}^{q}\theta_{i}\varepsilon_{s-i}\right)\right] \\
&=\mathbb{E}\left[\left(\sum\limits_{i=0}^{q}\theta_{i}\varepsilon_{t-i}\right)\left(\sum\limits_{i=0}^{q}\theta_{i}\varepsilon_{s-i}\right)\right] \\
&=\mathbb{E}\left[\sum\limits_{i=0}^{q}\sum\limits_{j=0}^{q}\theta_{i}\theta_{j}\varepsilon_{t-i}\varepsilon_{s-j}\right] \\
&=\sum\limits_{i=0}^{q}\sum\limits_{j=0}^{q}\theta_{i}\theta_{j}\mathbb{E}\left[\varepsilon_{t-i}\varepsilon_{s-j}\right] \\
&=\sum\limits_{i=0}^{q}\sum\limits_{j=0}^{q}\theta_{i}\theta_{j}\operatorname*{Cov}\left[\varepsilon_{t-i},\varepsilon_{s-j}\right] \\
&=\sum\limits_{i=0}^{q}\sum\limits_{j=0}^{q}\theta_{i}\theta_{j} \sigma^{2} \mathbb{1}_{t-i=s-j} \\
&=\sigma^{2}\sum\limits_{i=0}^{q}\theta_{i}\theta_{i+s-t}  \mathbb{1}_{0 \leqslant i+s-t\leqslant q} \\
&=\sigma^{2}\sum\limits_{i=0}^{q}\theta_{i}\theta_{i+s-t}  \mathbb{1}_{t-s \leqslant i\leqslant q+t-s} \\
\end{align*}
$$
