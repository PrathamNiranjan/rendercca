import streamlit as st
import pandas as pd
import os

def marketplace_page():
    """Marketplace page"""
    st.title("🛒 Agricultural Marketplace")
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Create or load marketplace data
    if not os.path.exists("data/marketplace_data.csv"):
        df = pd.DataFrame(columns=["Company", "Crop", "Quantity (kg)", "Price (₹/kg)", "Deadline", "Contact"])
        df.to_csv("data/marketplace_data.csv", index=False)
    else:
        df = pd.read_csv("data/marketplace_data.csv")
    
    st.subheader("Available Market Requirements")
    if df.empty:
        st.info("No requirements posted yet.")
    else:
        st.dataframe(df)
    
    # Allow companies to post requirements
    if st.session_state.role == "company":
        st.subheader("Post a Requirement")
        with st.form("market_form"):
            company = st.text_input("Company Name")
            crop = st.text_input("Crop")
            quantity = st.number_input("Quantity (kg)", min_value=1)
            price = st.number_input("Price (₹/kg)", min_value=1.0)
            deadline = st.date_input("Deadline")
            contact = st.text_input("Contact Info")
            
            submit = st.form_submit_button("Submit")
            if submit:
                if company and crop and contact:
                    new_entry = pd.DataFrame([[company, crop, quantity, price, deadline, contact]],
                                         columns=df.columns)
                    df = pd.concat([df, new_entry], ignore_index=True)
                    df.to_csv("data/marketplace_data.csv", index=False)
                    st.success("Requirement posted successfully!")
                else:
                    st.error("Please fill all required fields.")
    else:
        st.info("Only companies can post requirements. Farmers can contact the companies directly using the contact information provided.")
        
    # Allow farmers to filter requirements
    if st.session_state.role == "farmer":
        st.subheader("Find Requirements")
        if not df.empty:
            crops = ["All"] + list(df["Crop"].unique())
            selected_crop = st.selectbox("Filter by Crop", crops)
            
            if selected_crop != "All":
                filtered_df = df[df["Crop"] == selected_crop]
                st.dataframe(filtered_df)
            
            st.info("Contact the companies directly if you can fulfill any of these requirements.")
