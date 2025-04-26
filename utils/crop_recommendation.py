
import streamlit as st
import pandas as pd
import numpy as np

def crop_recommendation_page():
    """Crop recommendation page"""
    st.title("🌱 Crop Recommendation System")
    
    st.write("Enter your soil and climate conditions to get personalized crop recommendations.")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        nitrogen = st.slider("Nitrogen (N) level", 0, 140, 50)
        phosphorus = st.slider("Phosphorus (P) level", 0, 140, 50)
        potassium = st.slider("Potassium (K) level", 0, 200, 50)
        temperature = st.slider("Temperature (°C)", 0.0, 40.0, 25.0)
    
    with col2:
        rainfall = st.slider("Annual Rainfall (mm)", 0.0, 300.0, 100.0)
        humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
        ph = st.slider("pH value", 0.0, 14.0, 7.0)
    
    # Mock recommendation model (replace with your actual model)
    if st.button("Get Recommendation"):
        st.subheader("Recommended Crops")
        
        # Simple mock model - just for demonstration
        possible_crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Pulses"]
        compatibility = {}
        
        # Mock scoring logic - replace with your actual prediction logic
        for crop in possible_crops:
            score = 0
            # Simple rules - replace with your model's logic
            if nitrogen > 80 and crop in ["Rice", "Maize"]:
                score += 20
            if phosphorus > 70 and crop in ["Pulses", "Cotton"]:
                score += 15
            if potassium > 100 and crop in ["Sugarcane", "Cotton"]:
                score += 15
            if temperature > 30 and crop in ["Cotton", "Sugarcane"]:
                score += 10
            if temperature < 20 and crop in ["Wheat"]:
                score += 20
            if rainfall > 200 and crop in ["Rice"]:
                score += 15
            if rainfall < 100 and crop in ["Pulses", "Wheat"]:
                score += 10
            if ph > 6 and ph < 8 and crop in ["Wheat", "Maize", "Pulses"]:
                score += 10
            
            # Add some randomness for demonstration
            score += np.random.randint(0, 10)
            compatibility[crop] = score
        
        # Sort by score
        sorted_crops = sorted(compatibility.items(), key=lambda x: x[1], reverse=True)
        
        # Create and display recommendation dataframe
        rec_df = pd.DataFrame(sorted_crops, columns=["Crop", "Compatibility Score"])
        rec_df["Compatibility"] = rec_df["Compatibility Score"].apply(
            lambda x: "High" if x > 40 else "Medium" if x > 20 else "Low"
        )
        
        # Color code for compatibility
        def highlight_compatibility(val):
            if val == "High":
                return 'background-color: #90EE90'
            elif val == "Medium":
                return 'background-color: #FFFFE0'
            else:
                return 'background-color: #FFCCCB'
        
        st.dataframe(rec_df.style.applymap(highlight_compatibility, subset=["Compatibility"]))
        
        # Additional information for the top crop
        if sorted_crops:
            top_crop = sorted_crops[0][0]
            st.subheader(f"Top Recommendation: {top_crop}")
            
            crop_info = {
                "Rice": "Rice thrives in warm and humid conditions with plenty of water. It's a staple food crop.",
                "Wheat": "Wheat grows best in cool, dry conditions and requires moderate rainfall.",
                "Maize": "Maize prefers warm soil and is sensitive to frost. It needs adequate moisture and sunlight.",
                "Cotton": "Cotton requires a long frost-free period, warm temperatures, and abundant sunshine.",
                "Sugarcane": "Sugarcane is a tropical crop that needs high temperatures and high rainfall.",
                "Pulses": "Pulses are leguminous crops that can fix nitrogen in the soil and are relatively drought-resistant."
            }
            
            st.info(crop_info.get(top_crop, "No additional information available."))
