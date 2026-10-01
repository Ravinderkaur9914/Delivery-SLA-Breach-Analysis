import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# Load data
df = pd.read_csv('data/delivery_orders.csv')

# Load trained model
model = joblib.load('data/breach_risk_model.pkl')