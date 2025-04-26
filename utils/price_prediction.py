import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from utils.model_utils import train_price_model, predict_price

def price_prediction_page():
    """Price prediction page"""
    st.title("📈 Crop Price Prediction")
    
    try:
        # Load data
        df = pd.read_csv("data/price_data.csv")
        
        # User input
        crop = st.selectbox("Select Crop", df["Crop"].unique())
        city = st.selectbox("Select City", df["City"].unique())
        
        # Filter data based on user selection
        filtered = df[(df["Crop"] == crop) & (df["City"] == city)]
        
        # Ensure there is data for the selected crop and city
        if filtered.empty:
            st.error("No data available for the selected crop and city. Please try another combination.")
        else:
            # Train the model
            model = train_price_model(filtered)
            
            # Get the last row for the most recent date
            last_row = filtered.iloc[-1]
            last_date = pd.to_datetime(last_row["Date"])
            
            # Predict prices
            predictions = predict_price(model, 6, last_date.month, last_date.year)
            
            # Unpack predictions
            months, prices = zip(*predictions)
            
            # Plot the data
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Modal Price"], name="Historical"))
            fig.add_trace(go.Scatter(x=months, y=prices, name="Predicted"))
            
            fig.update_layout(
                title=f"Price Prediction for {crop} in {city}",
                xaxis_title="Date",
                yaxis_title="Price (₹/kg)",
                legend_title="Data"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display raw prediction data
            st.subheader("Predicted Prices")
            pred_df = pd.DataFrame({
                "Date": months,
                "Predicted Price (₹/kg)": [round(p, 2) for p in prices]
            })
            st.dataframe(pred_df)
            
    except FileNotFoundError:
        st.error("Price data file not found. Please ensure 'data/price_data.csv' exists.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
