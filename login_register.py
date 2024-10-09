import streamlit as st
from firebase_admin import auth, credentials, initialize_app
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from streamlit_option_menu import option_menu

from pages import General_Information, Crop_Assist, Dimension_Manager



# st.markdown(
#    """
#    <style>
#    .logo-container {
#        position: absolute;
#        top: 0;
#        left: 0;
#    }
#    </style>
#    """,
#   unsafe_allow_html=True,
# )

# Display logo
# st.markdown(
#   f"""
#   <div class="logo-container">
#       <img src="{logo_path}" width="100"/>
#   </div>
#   """,
#   unsafe_allow_html=True,
# )
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


def validate(auth_token):
    """
    Validate method queries the Google OAuth2 API to fetch the user info.
    """
    try:
        # Specify a clock skew allowance in seconds
        clock_skew_in_seconds = 10

        # Create a request object
        request = google_requests.Request()

        # Verify the OAuth2 token
        idinfo = id_token.verify_oauth2_token(auth_token, request, clock_skew_in_seconds=clock_skew_in_seconds)

        # Check if the issuer is Google
        if 'accounts.google.com' in idinfo['iss'] or 'https://accounts.google.com' in idinfo['iss']:
            return idinfo

    except Exception as e:
        # Log the exception if needed
        print(f"An error occurred: {e}")
        return "The token is either invalid or has expired"


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
        user_info = validate(id_token)

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


def login_app():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.image('logo_ata.png', use_column_width=True)

        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "General Information", "Crop Assist", "Dimension Manager"],
                icons=["house", "info", "crop", "table"],
                menu_icon="cast",
                default_index=0,
            )

            if st.sidebar.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()

        if selected == "Home":
            st.markdown("## 👋 Welcome to the Dimension Detection tool!")
            st.markdown("Developed by the Team Quadratech")
            # st.markdown("The app is still under development.")
            st.markdown("""
                    ### Select on the left panel what you want to explore:

                    - With 🔭 General info, you will have a short description of what this tool can do and how to use it.

                    - With 📈 CropAssist, you will be able to Upload the drawings and get the dimensions.

                    - With 🗺️ DimensionManager, you will be able to get all the detected Dimension organized into the corresponding lengths and widths.
                """)
        elif selected == "General Information":
            General_Information.main()
        elif selected == "Crop Assist":
            Crop_Assist.main()
        elif selected == "Dimension Manager":
            Dimension_Manager.main()


    else:
        st.title("Welcome to ATA!")
        st.markdown("Please log in or register to access the app")
        st.sidebar.image('logo_ata.png', use_column_width=True)
        for _ in range(40):
            st.sidebar.write(' ')
        st.sidebar.image('quadratechlogo.png', width=300)
        # st.sidebar.image('Quadratech.png', use_column_width=True)

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if login_user(email, password):
                    st.rerun()  # Rerun the app to go to the home page
                else:
                    st.error("Invalid email or password")

        with tab2:
            new_email = st.text_input("New Email")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                if register_user(new_email, new_password):
                    st.success("Registered and logged in successfully!")
                    st.rerun()  # Rerun the app to go to the home page
                else:
                    st.error("Registration failed")


# Entry point for the app
if __name__ == "__main__":
    login_app()
