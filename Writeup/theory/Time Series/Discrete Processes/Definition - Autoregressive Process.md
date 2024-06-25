---
aliases:
  - Autoregressive Process
  - Autoregressive
  - AR
  - AR(p)
tags:
  - Definition
  - TimeSeries
  - Mathematics
  - Statistics
  - SignalProcessing
type: definition
mathLink: $AR\left(p\right)$
---
> [!definition]+ Definition: Autoregressive Process
> A [[Definition - Time Series|Time Series]] [[Definition - Time Series|$X_{t}$]] is an [[Definition - Autoregressive Process|Autoregressive Process]] [[Definition - Autoregressive Process]] with coefficients $\vec{\phi}\in \mathbb{R}^{p}$ if for $\varepsilon_{t}\sim$[[Definition - White Noise Process]], $\forall\: t$:
> $$
\begin{align*}
X_{t}&=\sum\limits_{i=1}^{p}\phi_{i}X_{t-i}+\varepsilon_{t}\\
\implies\left(1-\sum\limits_{i=1}^{p}\phi_{i}L^{i}\right)X_{t} & = \varepsilon_{t}  
\end{align*}
> $$
^definition

```reference title:Code, ref:[[Definition - Autoregressive Process]]
file: [[autoregressive_process.py]]
```
^code

# Properties

### [[Definition - Mean Function|Mean Function]]

#toComplete

### [[Definition - Variance Function|Variance Function]]

#toComplete

### [[Definition - Covariance Function|Covariance Function]]

#toComplete
