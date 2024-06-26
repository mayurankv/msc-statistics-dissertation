---
aliases:
  - White Noise Process
  - White Noise
  - WN
tags:
  - Definition
  - TimeSeries
  - Mathematics
  - Statistics
  - SignalProcessing
type: definition
mathLink: $\operatorname*{WN}\left(\sigma^{2}\right)$
---
> [!definition]+ Definition: White Noise Process
> A [[Definition - Time Series|Time Series]] [[Definition - Time Series|$X_{t}$]] is a white noise process [[Definition - White Noise Process]] if it has zero [[Definition - Mean Function|Mean Function]], and [[Definition - Finite|Finite]] constant [[Definition - Variance Function|Variance Function]]:$$\operatorname*{Cov}\left[X_{t},X_{s}\right]=\sigma^{2}\mathbb{1}_{s=t}$$
^definition

```reference title:Code, fold, ref:[[Definition - Moving Average Process]]
file: [[white_noise.py]]
```
^code

# Properties

## [[Definition - Independence|Independence]]

The white noise [[Definition - Random Variables|Random Variables]] are not necessarily [[Definition - Independent|Independent]] (see [[Definition - Strict White Noise Process|Strict White Noise Process]]). However, if the [[Definition - Random Variables|Random Variables]] follow a [[Definition - Gaussian Distribution | Gaussian Distribution]] (see [[Definition - Gaussian White Noise Process|Gaussian White Noise Process]]), then since [[Definition - Uncorrelated|Uncorrelated]]$\implies$ [[Definition - Independence|Independent]] for [[Definition - Gaussian Distribution | Gaussian Distributed]]  [[Definition - Random Variables|Random Variables]] #toLink, we have that the [[Definition - White Noise Process|White Noise Process]] is actually a [[Definition - Strict White Noise Process|Strict White Noise Process]].

#toComplete
