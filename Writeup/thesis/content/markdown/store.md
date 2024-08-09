# Store

Cost Function: 2401.03345v1.pdf, 2001.01789v1.pdf, 2301.13235v1.pdf
Cite Heston characteristic function and pricing

---

Use black scholes with dividend yield:

For European options you can utilise put-call parity and reverse out the implied dividend yield.
I.e.
F(T,K) = C(T,K) - P(T,K)
and obviously
F(T) = S(t)*e^[(r-d)*(T-t)]

P-C = Ke^-rt - Se^-qt
P = C + Ke^-rt - Se^-qt
P = C + Ke^-rt - Se^-qt

C = Se^-qt P_1 - Ke^-rt P_2
P = Se^-qt (P_1-1) - Ke^-rt (P_2-1)

---

Future work:

- Heston proper pricing Cui et al

---

## Writeup

Implied Vol:

- [why-do-we-fit-volatility-surfaces-implied-from-a-option-pricing-model-to-the-emp](https://quant.stackexchange.com/questions/47373/why-do-we-fit-volatility-surfaces-implied-from-a-option-pricing-model-to-the-emp)
- [confusion-with-volatility-smiles-implied-by-different-models](https://quant.stackexchange.com/questions/30932/confusion-with-volatility-smiles-implied-by-different-models)

Vol Comparison:

- [realized-volatility-forecast-vs-implied-volatility](https://quant.stackexchange.com/questions/42553/realized-volatility-forecast-vs-implied-volatility)
- [implied-vs-realized-volatility-all-you-need-to-know](https://civolatility.com/implied-vs-realized-volatility-all-you-need-to-know/)

### Self Writeup Notes

- Focus on the mathematics heavy side of things
- Emphasize the realisticness of the data used compared to common simplifications
- Need a BRIEF README
  - Do README after submission deadline and all GitHub pruning
- How quickly could you write a distinction level thesis at absolute max speed: ~ 3 pages a day
- How many pages per section rough guide? ~ #toDo

### Adam Advice

- Do put equations and define all variables
- Include nice visual diagrams
- Make visually appealing
- Include toy example which motivates the project well
  - M: What example for forecasting volatility??
- Give strong message in results and then provide caveats in conclusion
- In future work if have partial results can put in future work section if appendix, else in supplementary materials if applicable
- Use I (or we) instead of passive tense? Ask dad
