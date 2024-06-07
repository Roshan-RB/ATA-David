import streamlit as st
from streamlit_option_menu import option_menu

# Import other page scripts
from pages import General_Information, Crop_Assist, Dimension_Manager

def main():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]

    st.sidebar.image('logo_ata.png', use_column_width=True)

    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "General Information", "Crop Assist", "Dimension Manager"],
            icons=["house", "info", "crop", "dashboard"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Home":
        st.markdown("## 👋 Welcome to the Dimension Detection tool!")
        st.markdown("Developed by the Team Quadratech")
        st.markdown("The app is still under development.")
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

if __name__ == "__main__":
    main()
