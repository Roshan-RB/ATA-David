import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/Home.py", label="Home")
    st.sidebar.page_link("pages/1_General_Information.py", label="General Information")
    st.sidebar.page_link("pages/Crop_Assist.py", label="Crop Assist")
    st.sidebar.page_link("pages/Dimension_Manager.py", label="Dimension Manager")
    
   


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Sign_In.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("Sign_In.py")
    menu()
