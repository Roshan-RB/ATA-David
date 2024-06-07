import streamlit as st
from firebase_admin import auth, credentials, initialize_app
import requests

# Initialize Firebase app if not already initialized
try:
    cred = credentials.Certificate('ata-project-a5bd3-b43dda61efbe.json')
    initialize_app(cred)
except ValueError:
    pass  # Firebase app already initialized

# Firebase API endpoint for client-side authentication
FIREBASE_API_KEY = "AIzaSyBDHSIurYQP9JZcGz5v0vBOkydT9cPChFg"
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"

st.set_option("client.showSidebarNavigation", False)

# Initialize st.session_state.logged_in and st.session_state.user if not already set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

def login_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_AUTH_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        id_token = data["idToken"]
        user_info = auth.verify_id_token(id_token)
        st.session_state.user = user_info
        st.session_state.logged_in = True
        return True
    else:
        return False

def register_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_SIGNUP_URL, json=payload)
    if response.status_code == 200:
        return login_user(email, password)
    else:
        st.error(f"Registration failed: {response.json()}")  # Print detailed error response
        return False

def redirect_to_home():
    # Redirect to Home page by setting query parameters
    st.experimental_set_query_params(page="home")

def login_app():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        st.title("Login or Register")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if login_user(email, password):
                    st.success("Logged in successfully!")
                    redirect_to_home()
                else:
                    st.error("Invalid email or password")

        with tab2:
            new_email = st.text_input("New Email")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                if register_user(new_email, new_password):
                    st.success("Registered and logged in successfully!")
                    redirect_to_home()
                else:
                    st.error("Registration failed")

   # menu()  # Render the dynamic menu!
