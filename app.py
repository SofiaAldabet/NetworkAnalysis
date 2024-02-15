import streamlit as st
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv(".env")

from src import ui_texts as ui
from src import fe_logic as fe
from src.ai_logic import fetch_city_info
from streamlit_folium import st_folium


def main():
    ui.display_intro()  
    
    city_name = ui.get_city_name_input()  # Capture user input for city name

    explore_button_clicked = st.button("Explore Road Network")

    # Store city name in session state only if button is clicked
    if explore_button_clicked and city_name:
        # Update the city name in session state
        st.session_state.city_name = city_name
        # Reset city info to force refetching if a new city is searched
        st.session_state.city_info = None
    
    # # Fetch city information of city using openai (uncomment only if you have an API key stored in .env file)
    # if 'city_name' in st.session_state and st.session_state.city_name:
    #     if 'city_info' not in st.session_state or st.session_state.city_info is None:
    #         st.session_state.city_info = fetch_city_info(st.session_state.city_name)
    #     if st.session_state.city_info:
    #         ui.display_city_info(st.session_state.city_name, st.session_state.city_info)

    # Load and plot the network
    if 'city_name' in st.session_state and st.session_state.city_name:
        if 'network_with_elevation' not in st.session_state:
            network_with_elevation = fe.load_network(st.session_state.city_name)
            if network_with_elevation is not None:
                st.session_state.network_with_elevation = network_with_elevation
                st.session_state.num_nodes = len(network_with_elevation.nodes)  # Initialize num_nodes

        # If network is loaded, plot it
        if 'network_with_elevation' in st.session_state and st.session_state.network_with_elevation:
            fe.plot_network(st.session_state.network_with_elevation, st.session_state.city_name)
            ui.display_network_info(st.session_state.city_name, st.session_state.num_nodes)

            analyze_network_clicked = st.button("Network Analysis")
            
            # Perform network analysis if button is clicked
            if analyze_network_clicked or 'analyzer' in st.session_state:
                if 'analyzer' not in st.session_state:  
                    st.session_state.analyzer = fe.analyze_network(st.session_state.network_with_elevation)
                
                # Plot critical points on the network
                fe.plot_network_critical(st.session_state.analyzer)
                # Display analysis-related text
                ui.display_analysis_info(st.session_state.analyzer, st.session_state.city_name)  

        
        # Clear everything if the user clicks the button
        if st.button('Clear'):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()