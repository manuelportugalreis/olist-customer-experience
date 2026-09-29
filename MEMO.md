# Memo: late deliveries are Olist's biggest controllable driver of bad reviews

**To:** Head of Operations, Olist (fictional brief, built on Olist's public dataset)
**From:** Manuel Portugal Reis
**Data:** 96,470 delivered orders, Sept 2016 – Aug 2018

## Bottom line
One in eight orders gets a 1–2 star review. **Delivery delays are the single biggest driver of those reviews, and they are concentrated in a few states.** Fixing them protects marketplace ratings and, to a smaller degree, repeat purchases.

## What the data shows
1. **Late orders are rated much worse.** 9% of orders delivered early get a bad review. That rises to 36% when an order is 1–7 days late, and to 78% when it is more than a week late.
2. **Delays are regional.** 8% of all orders arrive late, but the figure is 14–20% in Maranhão, Ceará, Bahia and Rio de Janeiro, against 5–6% in São Paulo, Minas Gerais and Paraná. RJ alone has over 12,000 orders.
3. **Almost nobody comes back: 3% of customers ever buy a second time.** Among customers whose first order was late and rated 1–2, 2.9% bought again, against 4.1% after an on-time, well-rated first order. The gap is statistically significant (z = 3.2), but this is a correlation. Bad experiences probably play a part, and so do other factors.
4. **Bad reviews are hard to predict at the moment of purchase** (AUC 0.61 using price, freight, promised delivery time, state and category). Once the delivery delay is known, the model improves to AUC 0.71. **The lever is operations, not prediction.**
5. **Some categories disappoint even when they arrive on time.** In bed/bath/table, furniture/décor and computer accessories, 14–15% of on-time orders still get a bad review. That points to product or seller quality rather than logistics.

## Recommendations
| # | Action | Why | How to measure |
|---|---|---|---|
| 1 | Carrier and seller review for RJ, BA, CE, MA routes | Largest share of late orders × high volume | % late per state, monthly |
| 2 | Proactive message plus a small voucher when an order passes its estimated date | Stops a late order from turning into a bad review | Bad-review rate on late orders (baseline 36–78%) |
| 3 | Seller quality audit in the 3 worst categories | Dissatisfaction there is not caused by logistics | Bad-review rate on on-time orders in those categories |
| 4 | Treat retention as a separate problem | Even perfect deliveries only get 4% of customers back | Test a second-purchase campaign as an A/B test |

## Caveats
Public, anonymised sample of Olist data. Repeat customers are identified by `customer_unique_id`. The link between experience and repurchase is observational, not causal.
