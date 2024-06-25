---
aliases:
  - Gaussian White Noise Process
  - Gaussian White Noise
  - GWN
tags:
  - Definition
  - TimeSeries
  - Mathematics
  - Statistics
  - SignalProcessing
type: definition
mathLink: $GWN\left(\sigma^{2}\right)$
---
> [!definition]+ Definition: Gaussian White Noise Process
> A [[Definition - White Noise Process|White Noise Process]] with [[Definition - Variance|Variance]] $\sigma^{2}$ is a [[Definition - Gaussian White Noise Process|Gaussian White Noise Process]] [[Definition - Gaussian White Noise Process]] if $\forall\: t: X_{t}\sim \mathcal{N}\left(0,\sigma^{2}\right)$.
^definition

```reference title:Code, fold, ref:[[Definition - Moving Average Process]]
file: [[gaussian_white_noise.py]]
```
^code

# Properties

## [[Definition - Independence|Independence]]

This is an example of a [[Definition - Strict White Noise Process|Strict White Noise Process]]
since [[Definition - Uncorrelated|Uncorrelated]]$\implies$ [[Definition - Independence|Independent]] for [[Definition - Gaussian Distribution | Gaussian Distributed]]  [[Definition - Random Variables|Random Variables]] #toLink.

#toComplete
