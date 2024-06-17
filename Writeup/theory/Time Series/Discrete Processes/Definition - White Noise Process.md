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
mathLink: $WN\left(\sigma^{2}\right)$
---
> [!definition]+ Definition: White Noise Process
> A sequence of [[Definition - Random Variables|Random Variables]] $\left(X_{t}\right)$ is a white noise process $WN\left(\sigma\right)$ if the [[Definition - Random Variables|Random Variables]] are [[Definition - Uncorrelated|Uncorrelated]], have zero [[Definition - Mean|Mean]], and [[Definition - Finite|Finite]] [[Definition - Variance|Variance]]:
> 
> $$
\begin{align*}
\forall\: t: &&\mathbb{E}\left[X_{t}\right]&=0\\
\forall\: s,t: &&\operatorname*{Cov}\left[X_{t},X_{s}\right]&=\sigma^{2}\mathbb{1}_{s=t}\\
\end{align*}
> $$
^definition

## Properties

### Independence

The white noise [[Definition - Random Variables|Random Variables]] are not necessarily [[Definition - Independent|Independent]] (see [[Definition - Strict White Noise Process|Strict White Noise Process]]). However, if the [[Definition - Random Variables|Random Variables]] follow a [[Definition - Gaussian Distribution | Gaussian Distribution]] (see [[Definition - Gaussian White Noise Process|Gaussian White Noise Process]]), then since [[Definition - Uncorrelated|Uncorrelated]]$\implies$ [[Definition - Independence|Independent]] for [[Definition - Gaussian Distribution | Gaussian Distributed]]  [[Definition - Random Variables|Random Variables]] #toLink, we have that the [[Definition - White Noise Process|White Noise Process]] is actually a [[Definition - Strict White Noise Process|Strong White Noise Process]].

#toComplete
