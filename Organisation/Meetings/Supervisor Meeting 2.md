---
time: 2024-06-04T13:02:52
aliases: 
  - "Supervisor Meeting 2024-06-04"
supervisors: "[[Adam Sykulski]]"
attendees:
  - "[[Francesco Ventura]]"
  - "[[Chiara Ottino]]"
  - "[[Weinan He]]"
degree: MSc Statistics Imperial College London
previous progress report: "[[Progress Report 1]]"
next progress report: "[[Progress Report 2]]"
meeting id: 2
---
# Meeting

## Activity since last meeting

> [!hint] Ideas
>  ![[Progress Report 1#Ideas]]
^ideas

> [!hint] Actions Taken
>  ![[Progress Report 1#Actions Taken]]
^taken-actions

> [!success] Successfully Completed
>  ![[Progress Report 1#Completed]]
^succesful-actions

> [!failure] Problems Encountered
>  ![[Progress Report 1#Problems]]
^problems-encountered

> [!danger] Issues identified
>  ![[Progress Report 1#Issues]]
^issues-identified

---

## Minutes
%%
Use `ChatM`, or similarly `Chat<Letter>` to add a chat entry for someone whose name starts with `<Letter>`
%%

```chat
{mode=minimal}
# Meeting Minutes started at 13:02:52
[Mayuran Visakan=teal, Adam Sykulski=red, Chiara Ottino=indigo, Weinan He=orange, Francesco Ventura=pink]

# Beginning with Finance

> Weinan He | Doing 5 models of GARCH: Normal GARCH, Integrated, fractionally integrated - long memory effect, fractionally integrated exponential, exponential garch - levy noise | 04/06/2024, 13:03:00

> Weinan He | EGARCH uses exponentials for asymmetry | 04/06/2024, 13:05:24

> Weinan He | Use S&P or similar index and model fit - use 10 years | 04/06/2024, 13:05:24

> Weinan He | Use in-sample and out of sample data (90% split) to test model | 04/06/2024, 13:05:24

> Adam Sykulski | Think about seasonality? | 04/06/2024, 13:03:26

> Weinan He | Use MLE for parameter estimation | 04/06/2024, 13:10:17

> Weinan He | Use AIC or BIC to determine best model choice | 04/06/2024, 13:10:36

> Weinan He | Use GARCH(1,1) before introducing the different models for a diagnostic check | 04/06/2024, 13:10:47

> Weinan He | Test different noise distributions | 04/06/2024, 13:12:07

> Adam Sykulski | Multiple testing issue because multiple models. Do you need to do corrections? False discovery rate control | 04/06/2024, 13:12:53

> Francesco Ventura | False rejections over total number of rejections. To esnure that multiple testing so that if its at 95%, the type one errors are controlled | 04/06/2024, 13:13:29

> Adam Sykulski | if you don't think about that, you can end up with over-parameterised models | 04/06/2024, 13:13:57

> Adam Sykulski | Look at multiple indices, check clustering effect and see if common GARCH effects | 04/06/2024, 13:14:13

> Adam Sykulski | Will get more volatility in NASDAQ - tech bubbles and extra vol in tech companies | 04/06/2024, 13:14:29

> Adam Sykulski | For clustering effects, difficult to say whether one stock index has a GARCH effect. Can test whether ALL these stocks have a GARCH effect or don't and can control those type 1 errors. Can also do Bonferroni corrections. | 04/06/2024, 13:14:54

> Francesco Ventura | I can send you some notes on FDR | 04/06/2024, 13:16:44

> Adam Sykulski | You guys can overlap with some methodologies | 04/06/2024, 13:17:00

> Weinan He | For model evaluation, can use metrics like MSE, RMSE on out of sample forecasts to find best model to forecast the index. Or can do further study like adding trading application such as trading performance of models - can add trading applications to paper | 04/06/2024, 13:17:36

> Adam Sykulski | You mentioned RMSE, can think of other metrics more checking robustness. Trivial differences include MAE, but key differences when use relative errors or percentage errors. | 04/06/2024, 13:18:48

# Note to self, should check ASF notes for extreme value theory testing of GARCH models and how can be extended. Do extreme value theory.

> Adam Sykulski | Going to be jumps in volatility that none of these ARIMA GARCH models quite capture | 04/06/2024, 13:21:28

> Chiara Ottino | Maximum of 30 pages | 04/06/2024, 13:22:07

> Adam Sykulski | Will have many figures so he will check whether that is ok to exceed | 04/06/2024, 13:23:26

> Adam Sykulski | Teaches spatial statistics module to third years | 04/06/2024, 13:26:16

> Chiara Ottino | Can you send the notes from the module | 04/06/2024, 13:26:49

> Francesco Ventura | I was going to mainly aim for time series and not spatial techniques | 04/06/2024, 13:27:10

> Chiara Ottino | Haven't done time series or spatial techniques, but gaining access to Time Series Analysis notes currently | 04/06/2024, 13:27:23

< Mayuran Visakan | No longer looking at volatility surface | 04/06/2024, 13:38:08

< Mayuran Visakan | Continuous time volatility models and continuous state space models, or alternative volatility models | 04/06/2024, 13:32:26

> Adam Sykulski | Heston model | 04/06/2024, 13:35:33

> Adam Sykulski | Not necessarily needed to defend everything you need to, have lots to say in future work as well | 04/06/2024, 13:35:11

> Adam Sykulski | Identifiability, parameter estimation, higher order moments. Have opportunity to do some theory. Find some extension. | 04/06/2024, 13:35:38

> Adam Sykulski | One of his ideas was MMS, one was looking at coupled indices and looking at corss-volatilites, one was looking at parameter estimation efficiency, last one was fractional long-memory processes. I have worked a lot on return processes which are short-memory, not long-memory, but behave a little bit like long -memory processes. Id don't think the MATERN model has been used as much as it could in finance.| 04/06/2024, 13:38:16

# Moving onto Sportlite

> Francesco Ventura | Fatigue indicator only has 3 levels and not conitnuous so makes prediction harder. Also not sure what 1 means on scale of 0 to 2 in terms of fatigueness. | 04/06/2024, 13:40:18

> Chiara Ottino | The phd paper is on networks, haven't finished reading the whole thesis but seems hes looked more at the overall structure within the team fatigue-wise rather than the fatigue of a single player. Focussed a lot on the first game of the season and tried to extend that to other games. Some scope for trying to see the relationship between the team and the opposition. | 04/06/2024, 13:47:22

> Chiara Ottino | Do they have any susggestions on whether we should use python or R? | 04/06/2024, 13:49:04

> Chiara Ottino | The hard thing is that we don't have much information on sportlite. Most i could find was that they have a section on their website explaining with articles wwhich the data is useful but not how they are using the data. Is that because the usage is protected within the company? | 04/06/2024, 13:49:20

> Adam Sykulski | Probably using the fatigue information for the trainers and the physios for monitoring injuries and performance etc. | 04/06/2024, 13:50:19

> Adam Sykulski | Doesn't think they will send the code for how they solve the issues. | 04/06/2024, 13:53:03

> Chiara Ottino | The issue is we don't know what they've done and what will be interesting to them | 04/06/2024, 13:53:18

> Adam Sykulski | Would ideally do analysis based off raw time series but could potentially do analysis off the aggregate statistics. | 04/06/2024, 13:53:42

> Chiara Ottino | Online deson't have same millisecond frequency as we have here. Online also has some metrics about what is happening in the game in terms of intensity. | 04/06/2024, 13:56:22

> Chiara Ottino | Keratti used Egenhead - acceleration of ... | 04/06/2024, 13:57:19

> Adam Sykulski | Look at that paper, and also look at papers that cited this paper. things have moved on in 10 years and people have come up with new analysis techniques you can use in your literature review | 04/06/2024, 13:57:35

> Chiara Ottino | It's hard to know where to find this information. Can ask Tim for references | 04/06/2024, 13:58:06

> Adam Sykulski | Look into the basic fatigue and performance as Sportlite would like that. Interest in how the fatigue changes across the match and also across the season. | 04/06/2024, 13:58:51

> Chiara Ottino | Looking at `parquet` files which are weird with different files | 04/06/2024, 14:09:13
```
^minutes

## Results

> [!todo] Actionable Points
> - [ ] Find a specific project question and task
> 	- [ ] Continuous models: 
> 		- [ ] Levy Noise
> 		- [ ] 
> 	- [ ] Volatility models: [Stochastic volatility - Wikipedia](https://en.wikipedia.org/wiki/Stochastic_volatility)
> 		- [ ] Work out where Black-Scholes lies 
> 		- [ ] Look into Heston
> 	- Find a model that is interesting and accessible and look at papers which have cited it
> - [ ] Find data source - tick level data
> - [ ] #toComplete
^actionable-points

## Other Notes

#toComplete

---

## Summary

> [!summary]
> #toComplete
^summary
