import streamlit as st

#from menu import menu
import warnings
st.set_page_config(layout="wide")

# Testing 
st.query_params.get_all("http://localhost:8501")



# Check if the 'page' parameter is set to 'home'
if st.query_params.get_all == []:
    # Load the Home page content
    from pages import Home
    Home.main()  # Assuming you have a `main()` function in Home.py
else:
    # Load the default login/register page
    import login_register  # Assuming this script is saved as login_register.py
    login_register.login_app()  # Assuming the login logic is in a function `login_app()`
