import streamlit as st
from utils.auth_utils import validate_login, register_user

st.set_page_config(page_title="AgriPredict", layout="wide")

# Ensure session state is initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# Page Navigation Logic
def set_page(page_name):
    """Updates session state to navigate to the specified page."""
    st.session_state.current_page = page_name

# Authentication UI
if not st.session_state.logged_in:
    # Login and Sign-Up Page
    st.title("🌱 Welcome to AgriPredict")
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])
    
    # Login Tab
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.radio("Login as", ["farmer", "company"], key="login_role")
        if st.button("Login"):
            if validate_login(username, password, role):
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials. Please check your username, password, and role.")
    
    # Sign-Up Tab
    with tab2:
        new_username = st.text_input("Choose a Username", key="signup_user")
        new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        new_role = st.radio("Register as", ["farmer", "company"], key="signup_role")
        if st.button("Sign Up"):
            message = register_user(new_username, new_password, new_role)
            if "🎉" in message:
                st.success(message)
            else:
                st.error(message)

else:
    # Main App Navigation (Post-Login)
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    
    # Sidebar Navigation
    selected_page = st.sidebar.radio(
        "Go to",
        ["Home", "Price Prediction", "Crop Recommendation", "Marketplace"]
    )
    
    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.experimental_rerun()
    
    # Main Content Based on Navigation
    if selected_page == "Home":
        st.title("Welcome to AgriPredict!")
        st.write("Select a feature from the sidebar to get started.")
        
        # Home page dashboard
        col1, col2 = st.columns(2)
        with col1:
            st.info("📈 **Price Prediction**\nPredict crop prices using historical data.")
        with col2:
            st.info("🌱 **Crop Recommendation**\nGet personalized crop recommendations.")
        
        st.info("🛒 **Marketplace**\nConnect with buyers and sellers.")
        
    elif selected_page == "Price Prediction":
        from utils.price_prediction import price_prediction_page
        price_prediction_page()
        
    elif selected_page == "Crop Recommendation":
        from utils.crop_recommendation import crop_recommendation_page
        crop_recommendation_page()
        
    elif selected_page == "Marketplace":
        from utils.marketplace import marketplace_page
        marketplace_page()
