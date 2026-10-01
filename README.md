# Delivery-SLA-Breach-Analysis
Analysed 50K quick-commerce orders across 12 stores to find why some miss the 10-minute delivery SLA. Used SQL window functions and Python to segment stores and isolate root cause, built a Random Forest model (83% accuracy) to predict breach risk, and visualised findings in Streamlit and Power BI dashboards.

<img width="1092" height="615" alt="image" src="https://github.com/user-attachments/assets/efd57adc-af58-4d78-bc26-b431a0f85b69" />

## 1. The project in simple words

Quick-commerce apps (like Blinkit, Zepto or Instamart) promise to deliver groceries in about 10 minutes. This promise is called the **SLA (Service Level Agreement)**. Each order is packed and dispatched from a nearby **dark store**, a small warehouse that only serves online orders.

When a store delivers later than 10 minutes, that order is a **breach**. Too many breaches mean unhappy customers, refunds and lost repeat orders.

This project analyses 49,944 delivery orders to answer three business questions:

1. **Where** are breaches happening: which stores, which hours, which days?
2. **Why** are they happening: distance, rush hours, too many orders, or problems inside the store?
3. **What** should the company do, and how much would it improve things?

The project covers the full analytics loop: raw data, SQL analysis, Python segmentation, a machine learning model, an interactive dashboard, and a business recommendation.

## 2. Dataset

Real quick-commerce data is not public, so I generated a realistic **simulated dataset** with Python (numpy and pandas).

| Item | Detail |
|---|---|
| Orders | 49,944 |
| Stores | 12 dark stores in 4 cities (Ludhiana, Amritsar, Jalandhar, Chandigarh) |
| Period | 60 days (1 June to 30 July 2026) |
| Promised delivery time | 10 minutes |
| Columns | order_id, store_id, city, order_placed_time, order_delivered_time, delivery_minutes, distance_km, promised_sla_minutes, breached, day_of_week, hour_of_day |

An order is marked as a breach when `delivery_minutes > 10`.

## 3. Tools used

- **Python:** pandas, numpy, scikit-learn, joblib
- **SQL (SQLite):** GROUP BY, CASE WHEN, RANK and rolling-average window functions
- **Visualisation and app:** Plotly, Streamlit
- **Workflow:** Anaconda, Jupyter Notebook, VS Code, Git and GitHub
- **Power BI:** Power Query, DAX measures, conditional formatting (second dashboard)

## 4. How I built it

1. **Data setup:** loaded the CSV into a SQLite database and checked the data for missing values and errors.
2. **SQL analysis:** calculated breach rate per store, per hour and per day of week. Used a window function to calculate a 7-day rolling breach rate for each store.
3. **Segmentation:** grouped stores into three tiers (Chronic Breacher, Average, Strong Performer) and compared distance, delivery time, order volume and hourly patterns across tiers to find the root cause.
4. **Prediction:** trained a Random Forest classifier to predict whether an order will breach the SLA.
5. **Dashboard:** built a Streamlit app with filters, KPI cards, a store leaderboard, an hour-vs-day heatmap and a breach-risk predictor.
6. **Recommendations:** estimated the impact of fixing the worst stores and wrote action points.

## 5. Key findings

**1. The overall breach rate is 41.4%.** Nearly 4 in 10 orders miss the 10-minute promise.

**2. Three stores are far worse than the rest.**

| Store | Breach rate |
|---|---|
| STR-002 | 96.2% |
| STR-003 | 90.6% |
| STR-001 | 73.3% |
| Best stores (STR-009 to STR-012) | 7% to 13% |

These 3 stores are only 25% of the network but cause **53% of all breaches**.

**3. Store tiers compared**

| Tier | Stores | Breach rate | Avg delivery time | Avg distance |
|---|---|---|---|---|
| Chronic Breacher | 3 | 86.8% | 12.3 min | 1.38 km |
| Average | 5 | 39.4% | 9.6 min | 1.41 km |
| Strong Performer | 4 | 9.4% | 7.2 min | 1.39 km |

Distance is almost the same in every tier, and every store handles a similar number of orders (about 4,000 to 4,300 each). So **neither distance nor order volume explains the gap.**

**4. Rush hours make everything worse.** Across the network, the breach rate is **66% during lunch (1 to 3 PM) and dinner (8 to 11 PM)**, against **28% at other times**. The heatmap shows these two dark bands on every day of the week. Weekends and weekdays are almost the same (40.8% vs 41.7%).

**5. The worst stores fail even when it is quiet.** In the 3 chronic stores, about 80% of orders breach even in off-peak hours, and 99% to 100% breach at rush hours. Their 7-day rolling breach rate stays flat over the 60 days, so this is a **structural problem, not a temporary bad week**.

**Root cause:** the evidence points to store-level operations (for example staffing, picking and packing speed, or rider availability) at STR-001, STR-002 and STR-003. The data cannot say which operational factor it is, which is why the first recommendation is an audit.

## 6. Machine learning model

A Random Forest classifier (200 trees) predicts whether an order will breach the SLA.

- **Inputs:** store, hour of day, weekend flag, delivery distance (15 features after encoding stores)
- **Split:** 39,955 orders for training, 9,989 for testing

| Class | Precision | Recall | F1-score |
|---|---|---|---|
| On time (False) | 0.86 | 0.85 | 0.86 |
| Breach (True) | 0.79 | 0.81 | 0.80 |

**Overall accuracy: 83%.** The model catches 81% of real breaches, and 79% of the breaches it predicts are real.

Top features from the model: **[PASTE YOUR TOP 3 FROM feature_importances_ HERE]**

## 7. Interactive dashboard

The Streamlit dashboard lets a manager:

- Filter by city and store
- See KPI cards: overall breach rate, worst store, total orders
- Compare stores on a breach-rate bar chart
- Spot the worst time slots on an hour-vs-day heatmap
- Use the **Breach Risk Predictor**: choose a store, hour, weekday or weekend, and distance to see the predicted breach probability


## 7.5 Power BI Dashboard

In addition to the Streamlit dashboard, I built a second dashboard in Power BI to practice the tool most commonly asked for in data analyst job postings.

**Pages:**
- **Overview:** Breach Rate %, Total Orders and Avg Delivery Minutes KPI cards with trend sparklines, a Top Breaching Stores chart, a Worst City / Second Worst City card, a Breach Rate by Month/Week chart, and a Breached vs On-Time pie chart.
- **Root Cause:** Breach rate by store tier, a rolling breach rate trend by store, a Peak vs Off-Peak comparison, and a Breach Rate by Hour vs Day of Week heatmap.

**Built with:** Power Query (data load and cleaning), DAX measures and calculated columns (Breach Rate %, Store Tier, Peak Period, rolling breach rate), and conditional formatting for the heatmap and KPI cards.

![Power BI Overview](powerbi/overview_screenshot.png)
![Power BI Root Cause](powerbi/root_cause_screenshot.png)

The .pbix file is in the `powerbi/` folder of this repository. Open it in Power BI Desktop (free) to explore it interactively.

## 8. Recommendations

1. **Audit STR-001, STR-002 and STR-003** (staffing, packing process, rider availability), since they breach even at quiet hours.
2. **Add extra riders and packers at rush hours** (1 to 3 PM and 8 to 11 PM) across the whole network.
3. **Set an automatic alert** when any store's 7-day rolling breach rate goes above 60%.
4. **Use the risk model at checkout** to flag high-risk orders and show a more realistic delivery time.

**Expected impact:** if the 3 worst stores only reached the average level of the other 9 stores (26%), the network breach rate would fall from **41.4% to about 26.0%**, a drop of about 15 percentage points.

## 9. Limitations

- The data is **simulated**, so real-world factors such as traffic, weather, stock-outs and rider shortages are not captured. Some patterns (such as the rush-hour effect and the weak stores) come from how the data was generated, so this project demonstrates the analysis method rather than proving facts about a real company.
- The patterns show correlation, not proven cause. A real rollout of the recommendations should be tested with an A/B test first.
- The model was tested on a random split of the same time period. A production model should be tested on future dates.

## 10. How to run locally

```bash
git clone https://github.com/[YOUR-USERNAME]/delivery-sla-breach-analysis.git
cd delivery-sla-breach-analysis
pip install -r requirements.txt
streamlit run app.py
```

## 11. Project structure

```
delivery-sla-breach-analysis/
├── data/
│   ├── delivery_orders.csv
│   └── breach_risk_model.pkl
├── sql/
│   └── analysis_queries.sql
├── notebooks/
│   ├── 01_load_and_explore.ipynb
│   └── 02_predictive_model.ipynb
├── docs/
│   └── recommendations.md
├── powerbi/
│   ├── SLA_Breach_Dashboard.pbix
│   ├── overview_screenshot.png
│   └── root_cause_screenshot.png
├── app.py
├── requirements.txt
└── README.md
```

## 12. Author

**Ravinder Kaur**
B.Tech Computer Science Engineering, Desh Bhagat University
