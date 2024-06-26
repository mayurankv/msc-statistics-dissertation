HAR Model
[[Definition - Generalised Autoregressive Conditionally Heteroskedastic Process]] Model

---

Discrete: Returns
Continuous: Price 

> **Vol forecast**
> Realised Measure
> Seasonal S
> Long Memory FI
> Multivariate V
> Rough [1410.3394](https://arxiv.org/pdf/1410.3394) 

**Features**
Seasonal - 
Fractionally Integrated - Long Memory
Asymmetric - 
Exponential - 
Structural Breaks - 


FIGARCH Overview: [stat.tugraz.at/AJS/ausg123/123Tayefi.pdf](https://stat.tugraz.at/AJS/ausg123/123Tayefi.pdf)
SFIGARCH: Bordignon, Caporin, and Lisi (2004)


HAR 
HAR-RV-J and HAR-RV-CJ [Paper](https://pdf.sciencedirectassets.com/271529/1-s2.0-S0378437118X00223/1-s2.0-S0378437118313517/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIHxDyBrWdqboiU7Dt3avw7c6aTMnAXY37PYeDef0iO3HAiEAxyP0sEy3bK7ptpf5o2Lxrm%2BtZeVNkgmikIXIoeI2WzoqsgUIVhAFGgwwNTkwMDM1NDY4NjUiDBMbXqGIdy2Rw4oRACqPBaSFCsDe%2FjPpfBNUtlXwYh98buFznPRKVVLkwbKsYrLsQ56mye1%2BCX6Je0yOAIvrV9QDJ6utCy5vTurPVHL2lysOSO1zdE1EJ1IXXkuY3THRg6hZ7Ga1yvr0YlFIKR%2FjqYf5ArqFaxBiYLD5fh4xW1aZNKXl%2BoZJPGJiApXYwZTjHmbM3XXDU%2FEhXjRCoUrfXVI6sXAcnGjQ6osIKE9UgVvRR2zTyen6amEmTrvZwrdLJHrbpPyZxcpfzHW%2FOzRCxvADMpIarxIMMPSdbM%2FQvxX3G05RAOp884RHfMYV6yO%2BbztEzT5whIBO1cy81taQ0VbePluMiWTh7rXPKhjAXWyXMZtKtSS7waXrVIVMKGspXcaesixa8djUR%2Fq44rpEibP09HZ8kqgYaSjDBV4Q5YL9QC5%2FFU8sJIYi55gb%2BBz%2B%2FX5MbYhUGARntzo03jPMse7t3Phh5vIhYZVniTeLKluA0pYcZ57DbakkjYxQxh040i56cdrS5Zk8BN4Jq5rUhshy3Fc8AQ3TkHIQ0FoFXxrsgQ8CiB7TNJZ3%2Bq6PsdqxTVNP2vetioV5ZPuD1xuXf0n0Z5OAZynwjeoiOZ%2BrEJmqRZEGNt2ZPTfMB4hx%2F8HZEzk2SSKBVY5AJdXfSE7feOjev1hST7MLMSuCNeI8sin9JVjsKAH9P6cP8sKy2hfDqxMQYjU3L0SQkgn6E8IcMn1fStVKqu9W4we0WeVOQWEgiT9bJvXG5M1AVn7OFJpPzZJndfvWgHy6CV2mFckW5EtlnaqHoSydEI9XpeCXlBtqa7Hw1S3%2FfiVXx1uiN%2ByCuyIrDcB72h7MHkcrj9oG7udbEDnCTE4E28%2FLmEx%2FzIHYfaTjnbdxPFYRV8ayE0gww6OfswY6sQF6kdAuehk07%2BXkNPkACmM1HUbbohQD5HyFSC9Kne7%2B6zhdyaTg6zYhdgCVsnl1JHBdqWJB9FRFVzdQuxCQ9HQoQU1mQBVlizzKY5L1%2B0iz1498j4X2TQ1zoxBRn%2FHuhIzyREThDtuN%2FaYZ8fMkweGar1kyHdakhSsH%2F95JJdYBz9Vq0jQmgZn6jnJGip1XXSxd%2B%2BLpN7r1BES3Qb4TPgNR3W2TWT8bN5PU2h7v1OhViTk%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240611T050632Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYYK6KSDFZ%2F20240611%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=96efdd5c7e3f14333e7162d4c75f4d099e9d7534f66ebcce3979d17dcc970d56&hash=a9c805218293556ac2bb528f49b06ae9b7d2ddf4d78445a12c24644e0046e0c0&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S0378437118313517&tid=spdf-c65b7a69-c481-49ab-b779-f63147d5314a&sid=e0000ec9563b4243e87b0b818b963b1584degxrqb&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=1d04595650065e525b0352&rr=891f128b38dc6533&cc=gb)
HARQ model

[[Definition - Generalised Autoregressive Conditionally Heteroskedastic Process]] 

Existing problems:
- Rough volatility - see rough models and levy noise
- h-step forecast will have h-step lag

---

IGARCH Can be [[Definition - Stationarity|Stationary]] even though it is not [[Definition - Wide-Sense Stationarity|Wide-Sense Stationary]]
Though implies [[Definition - Infinite|Infinite]] persistence of a volatility shock

FIGARCH

---

Torben G. Andersen and Tim Bollerslev (1998): "Answering the Skeptics: Yes, Standard Volatility 

---

Maybe:
- Rough stochastic volatility vs discrete realised volatility (Analysis of effectiveness of rough SV models)
	- Best in class comparison (don't think has been done)
	- Potential with VIX smiles
	- Analysis of fit of Rough Quadratic Heston model
		- Longer times to expiry (only short was shown to jointly fit)
		- 
	- HAR with jumps model comparison based on discontinuous paths
- HAR based research
	- 

Maybe too much and may need to drop - likely
${}2$ [[Definition - Heterogenous Autoregressive Process for Realised Variance]] models
${}2$ Rough models 
${}2$ non-rough models

Massive disconnect between what is used in academia and industry
Lots already covered in academia so would like to make it more applicable by focussing on computational efficiency as well
Shying away from Machine learning models due to potential instability in results and training time and amounts of data

---

Basic alternative idea:
- Similar to [[Person - Weinan He|Weinan]] looking at HAR models instead or looking at rough volatility models

Definitely:
- Basis:
	- `Use Realised Measures using high frequency data`
	- `Focus on computational efficiency - want microsecond level timings`
	- 
- Theory
	- MLE and QMLE
		- Consider under OLS but also WLS and other estimation methods 
		- Shrinkage?
	- etc...
	- Look at other papers for more ideas
- Analysis
	- Look at risk measures 
	- Look at for different assets 
	- Compare to existing best models in similar way to [[Person - Weinan He|Weinan]]
	- For each comparison:
		- Look at parameter efficiency 
		- Computational efficiency
		- Data usage requirements

Probably:
- Market microstructure noise negation
	- Take into account microstructure in model?

[Data](https://www.imperial.ac.uk/admin-services/library/subject-support/business/databases-a-z/): Appears that I can get ${}1$ minute level information - `not sure on VIX data`
- Thomson Reuters Tick Group 
- Bloomberg data (see restrictions)
- Oxford–Man Realized Library

Asset:
- Crude oil and Copper futures since they vary the most
- Should also consider lower volatility assets for comparison

Extensions:
- Further comparisons:
	- Realised volatility vs implied volatility
		- Comparison to Model free implied volatility
			- Tie in options trading eventually? [OptionMetrics (Ivy DB US) | Administration and support services | Imperial College London](https://www.imperial.ac.uk/admin-services/library/subject-support/business/optionmetrics-ivy-db-us/)
		- Comparison to SV models like Heston and Black Scholes

---

Is stochastic volatility not really used? Speak to someone at Maven?

Intresting:
1. [Quants of the year – Jim Gatheral and Mathieu Rosenbaum - Risk.net](https://www.risk.net/awards/7736196/quants-of-the-year-jim-gatheral-and-mathieu-rosenbaum)
	1. [arxiv.org/pdf/1609.05177](https://arxiv.org/pdf/1609.05177.pdf)
	2. [arxiv.org/pdf/2001.01789](https://arxiv.org/pdf/2001.01789.pdf)

---

WRDS: Applied 
Alphavantage free

> Need to read papers so know how they used data (open/high/low/close, error-corrected? dividend-corrected?)
