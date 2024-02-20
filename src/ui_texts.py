import streamlit as st

def get_city_name_input():
    """Returns the user input for city name."""
    return st.text_input("E.g., Burela, Spain", key="city_name_input")

def display_intro():
    st.title("How would your road network respond to coastal flooding?")
    st.markdown("""<span style='font-size: 18px;'>Roads are the backbone of our societies, allowing the movement
                 of people and goods. However, many coastal towns, especially those at lower elevations, 
                consistently experience infrastructure damage due to natural phenomena like storms and high tides. 
                With the progression of climate change and the anticipated rise in sea levels, disruptions 
                to these networks from coastal flooding are expected to become more frequent. Identifying key
                locations in the network that might trigger significant disruptions can inform coastal management 
                and planning efforts, facilitating the development of adaptive strategies to deal with coastal hazards.""", unsafe_allow_html=True)
    st.markdown("""<span style='font-size: 18px;'>Enter the name of a <span style='font-size: 18px; color: #ffe599;'>coastal town</span>
                to investigate the potential impact of coastal flooding on its road network.</span>""", unsafe_allow_html=True)
    

def display_network_info(city_name, num_nodes):
    st.markdown(f"""<span style='font-size: 18px;'>This is the road network of 
                <span style='font-size: 18px; color: #ffe599;'>{city_name}</span>, which has 
                <span style='font-size: 18px; color: #ffe599;'>{num_nodes} nodes</span>. Nodes are the intersections 
                within the network, while edges refer to the stretches of road connecting those intersections.
                Here, nodes have been colored by their elevation (in meters) above sea level.</span>""", unsafe_allow_html=True)
    st.markdown("""<span style='font-size: 18px;'>Click on the different nodes 
                to explore their elevation, and analyze the network to learn more about 
                its ability to withstand coastal flooding. Note that the <b>processing time of
                the analysis depends on the number of nodes</b> in your selected city.</span>""", unsafe_allow_html=True)

def display_analysis_info(analyzer, city_name):
    st.markdown(f"""<span style='font-size: 18px;'>The susceptibility of a network to disruptions is often assessed by 
                removing nodes and analyzing how the remaining network functions. As nodes are progressively eliminated, 
                traveling between different areas of the network can become impractical or require significantly longer travel times. 
                The network reaches a tipping point when the removal of a single node causes a complete disconnection of the network. 
                Here, the critical node is identified by sequentially removing nodes, beginning with those at lower elevations, 
                under the assumption that they are more susceptible to flooding.""", unsafe_allow_html=True)
    
    st.markdown(f"""<span style='font-size: 18px;'>In the case of <span style='font-size: 18px; color: #ffe599;'>{city_name}</span>, 
                the <span style='font-size: 18px; color: #cc0000;'><b>critical node</b></span> is found at an elevation of 
                <span style='font-size: 20px; color: #cc0000;'><b>{analyzer.critical_elevation}</b></span> meters above sea level.
                This point marks the limit beyond which the system ceases to operate as a cohesive network,
                which occurs after the removal of <span style='font-size: 18px; color: #ffe599;'>{analyzer.perc_nodes_removed:.0f}%</span> 
                nodes. Networks that have their critical nodes at lower elevations are generally more susceptible to the effects of coastal flooding. 
                Conversely, a critical node located at a higher elevation suggests a lesser vulnerability to flooding. 
                However, this approach predominantly considers topography as a critical factor influencing flood vulnerability. 
                A more comprehensive analysis would need to account for additional criteria, such as flood likelihood, 
                network's architecture, and existing flood defense systems.</span>""",
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
