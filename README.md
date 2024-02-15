How would your road network respond to coastal flooding?
==============================

This repository contains the source code for a Streamlit application that assesses the vulnerability of road networks to coastal flooding. The process includes:

1. Extracting the road network for a chosen city from OpenStreetMap.
2. Determining the elevation for each node (intersection).
3. Sequentially removing nodes based on elevation (from lowest to highest), simulating a simplified “bathtub” flooding model.
4. Evaluating the network's connectivity after each node's removal to identify the critical node, whose elimination leads to the network's total disconnection.

This approach, though streamlined, is supported by peer-reviewed research ([Aldabet et al., 2022](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021EF002581) and serves as a preliminary tool for analysis. It offers a straightforward and effective way to explore the resilience of road systems in the face of extreme flood events, leveraging open-access datasets and methodologies.

--------



