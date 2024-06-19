How would your road network respond to coastal flooding?
==============================

This repository contains the source code for a Streamlit application that assesses the vulnerability of road networks to coastal flooding. The process includes:

1. Extracting the road network for a chosen city from OpenStreetMap.
2. Determining the elevation for each node (intersection).
3. Sequentially removing nodes based on elevation (from lowest to highest), simulating a simplified “bathtub” flooding scenario.
4. Evaluating the network's connectivity after each node's removal to identify the critical node, whose elimination leads to the network's total disconnection.

This method, grounded in peer-reviewed research ([Aldabet et al., 2022](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021EF002581)), provides a computationally effective way to explore the resilience of road networks to extreme flooding, assuming that topography is a key control on flood susceptibility. Identifying critical nodes that could trigger significant network disruptions can guide coastal management and planning efforts, facilitating the development of adaptive strategies to address the dynamic challenges posed by coastal threats.


--------

## Set up
To run this application locally, you will need venv and python:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py
    ```

If you have an OpenAI API Key, you can activate specific lines in app.py to incorporate AI-generated background details about your selected city.

