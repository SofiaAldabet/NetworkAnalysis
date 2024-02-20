import streamlit as st
from streamlit_folium import st_folium
from src.network_analysis import NetworkExtractor, ElevationUpdater, NetworkAnalyzer
from src.map_plotting import NetworkPlotter, CriticalPlotter

# Extract network and update elevation data
def load_network(city_name):
    try:
        with st.spinner('Extracting road network...'):
            extractor = NetworkExtractor(city_name)
            network = extractor.extract_network()

        with st.spinner('Updating elevation data...'):
            updater = ElevationUpdater(network)
            network_with_elevation = updater.update_elevation()

        st.success('Your network has been loaded successfully!')
        return network_with_elevation
    except Exception as e:
        st.error(f"Failed to load network: {str(e)}")
        return None

# Plot the network
def plot_network(network_with_elevation, city_name):
    st.markdown(f"### Road network of {city_name}", unsafe_allow_html=True)
    plotter = NetworkPlotter(network_with_elevation)
    folium_map = plotter.plot_network_with_elevation()  
    st_folium(folium_map, width=725, height=500)

# Analyze the network
def analyze_network(network_with_elevation):
    analyzer = NetworkAnalyzer(network_with_elevation)
    analyzer.analyze_network()
    return analyzer

# Plot network analysis
def plot_network_critical(analyzer):
    st.markdown("### Road network analysis", unsafe_allow_html=True)
    critical_plotter = CriticalPlotter(analyzer.G, analyzer.nodes_removed, analyzer.critical_elevation)
    folium_map = critical_plotter.prepare_and_plot()
    
    if folium_map:
        st_folium(folium_map, width=725, height=500)