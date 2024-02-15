import streamlit as st

def get_city_name_input():
    """Returns the user input for city name."""
    return st.text_input("E.g., Burela, Spain", key="city_name_input")

def display_intro():
    st.title("How would your road network respond to coastal flooding?")
    st.markdown("""<span style='font-size: 18px;'>Roads are crucial for the mobility of both individuals and goods, 
                acting as the backbone of our communities. Yet, towns along the coast, especially those situated at lower heights, 
                face repeated damage to their infrastructure due to coastal events such as storms and high tides. 
                As climate change intensifies and sea levels rise, it's expected that coastal flooding will increasingly 
                disrupt these networks.""", unsafe_allow_html=True)
    st.markdown("""<span style='font-size: 18px;'>Enter the name of a <span style='font-size: 18px; color: #ffe599;'>coastal town</span>
                to investigate the potential impact of coastal flooding on its road network.</span>""", unsafe_allow_html=True)
    

def display_network_info(city_name, num_nodes):
    st.markdown(f"""<span style='font-size: 18px;'>This is the road network of 
                <span style='font-size: 18px; color: #ffe599;'>{city_name}</span>, which has 
                <span style='font-size: 18px; color: #ffe599;'>{num_nodes} nodes</span>. 
                Nodes represent road intersections and edges are road segments between those intersections.
                Here, nodes have been colored by their elevation (in meters).</span>""", unsafe_allow_html=True)
    st.markdown("""<span style='font-size: 18px;'>Click on the different nodes 
                to explore their elevation, and analyze the network to learn more about 
                its ability to withstand coastal flooding. Note that the <b>processing time of
                the analysis depends on the number of nodes</b> in your selected city.</span>""", unsafe_allow_html=True)

def display_analysis_info(analyzer, city_name):
    st.markdown(f"""<span style='font-size: 18px;'>The vulnerability of a network is typically 
                explored by removing nodes and analyzing the functionality of the remaining network. 
                When enough nodes are removed, travel between different parts of the network becomes impossible
                or requires long travel distances (and time). Considering that nodes at lower elevations are 
                more prone to flooding, we have removed nodes starting from the lowest
                elevation, to identify the critical node whose malfunction might lead to the collapse 
                of the entire network.""", unsafe_allow_html=True)
    st.markdown(f"""<span style='font-size: 18px;'>In <span style='font-size: 18px; color: #ffe599;'>{city_name}</span>, 
                such critical node is located at an elevation of 
                <span style='font-size: 20px; color: #cc0000;'><b>{analyzer.critical_elevation}</b></span> meters above sea level.
                This point, at which the system ceases to operate as a cohesive network,
                is reached after the removal of <span style='font-size: 18px; color: #ffe599;'>{analyzer.perc_nodes_removed:.2f}%</span> 
                nodes. Networks with critical nodes at lower elevations are generally more 
                susceptible to the impacts of coastal flooding. Yet, a comprehensive assessment of the network's 
                vulnerabilities requires considering other factors such as the probability of flooding, overall network's robustness, 
                or the existence of protective measures.</span>""",
                unsafe_allow_html=True)

    st.markdown(f"""<span style='font-size: 18px;'>For further reading on the subject, see our article on 
                <a href='https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021EF002581' target='_blank'
                >Thresholds in Road Network Functioning on US Atlantic and Gulf Barrier Islands</a>.""", unsafe_allow_html=True)

    
def display_city_info(city_name, city_info):
    """Displays information about the city in a formatted way."""
    if city_info:
        # Split the text into paragraphs
        paragraphs = city_info.split('\n')
        # Wrap each paragraph in a <p> tag with the desired style
        styled_paragraphs = ''.join([f"<p style='font-size: 18px;'>{paragraph}</p>" for paragraph in paragraphs if paragraph])
        # Display the styled paragraphs
        st.markdown(f"### Welcome to {city_name}", unsafe_allow_html=True)
        st.markdown(styled_paragraphs, unsafe_allow_html=True)
    else:
        st.error("Failed to fetch city information.")
