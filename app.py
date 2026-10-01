import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --------------------------------------------------
# LOAD DATA AND MODEL
# --------------------------------------------------

df = pd.read_csv(
    r"C:\Users\jai ganesh\Documents\sla_analysis\data\delivery_order.csv"
)

model = joblib.load(
    r"C:\Users\jai ganesh\Documents\sla_analysis\data\breach_risk_model.pkl"
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header('Filters')

city_filter = st.sidebar.multiselect(
    'City',
    df['city'].unique(),
    default=df['city'].unique()
)

store_filter = st.sidebar.multiselect(
    'Store',
    df['store_id'].unique(),
    default=df['store_id'].unique()
)

filtered = df[
    df['city'].isin(city_filter) &
    df['store_id'].isin(store_filter)
]

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title('Delivery SLA Breach Analysis')

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    'Overall Breach Rate',
    f"{filtered['breached'].mean() * 100:.1f}%"
)

col2.metric(
    'Worst Store',
    filtered.groupby('store_id')['breached'].mean().idxmax()
)

col3.metric(
    'Total Orders',
    f"{len(filtered):,}"
)

# --------------------------------------------------
# BREACH RATE BY STORE
# --------------------------------------------------

store_rates = (
    filtered.groupby('store_id')['breached']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig1 = px.bar(
    store_rates,
    x='store_id',
    y='breached',
    title='Breach Rate by Store'
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# HEATMAP: HOUR VS DAY
# --------------------------------------------------

heatmap_data = filtered.pivot_table(
    values='breached',
    index='hour_of_day',
    columns='day_of_week',
    aggfunc='mean'
)

fig2 = px.imshow(
    heatmap_data,
    title='Breach Rate: Hour vs Day of Week',
    color_continuous_scale='Reds'
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# PREDICT BREACH RISK
# --------------------------------------------------

st.subheader('Predict Breach Risk')

selected_store = st.selectbox(
    'Select Store',
    df['store_id'].unique()
)

selected_hour = st.slider(
    'Hour of Day',
    min_value=0,
    max_value=23,
    value=12
)

selected_weekend = st.selectbox(
    'Is Weekend?',
    ['No', 'Yes']
)

selected_distance = st.slider(
    'Distance (km)',
    min_value=float(df['distance_km'].min()),
    max_value=float(df['distance_km'].max()),
    value=float(df['distance_km'].median())
)

# Convert weekend selection to 0/1
is_weekend = 1 if selected_weekend == 'Yes' else 0

# Create input row
prediction_data = pd.DataFrame({
    'store_id': [selected_store],
    'hour_of_day': [selected_hour],
    'is_weekend': [is_weekend],
    'distance_km': [selected_distance]
})

# Convert store_id into the same one-hot encoded format
prediction_data = pd.get_dummies(
    prediction_data,
    columns=['store_id'],
    prefix='store_id'
)

# Match exactly the columns used when training the model
prediction_data = prediction_data.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)

# Predict probability
breach_probability = model.predict_proba(prediction_data)[0][1]

st.metric(
    'Predicted Breach Probability',
    f'{breach_probability * 100:.1f}%'
)