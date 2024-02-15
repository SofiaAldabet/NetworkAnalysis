import requests
import osmnx as ox
import networkx as nx
import numpy as np

class NetworkExtractor:
    def __init__(self, place_name):
        self.place_name = place_name

    def extract_network(self):
        network = ox.graph_from_place(self.place_name, network_type='drive')
        return network


class ElevationUpdater:
    def __init__(self, network):
        self.network = network
        self.open_elevation_url = 'https://api.open-elevation.com/api/v1/lookup'

    def get_elevations_batch(self, locations):
        """Fetch elevations for a batch of locations."""
        # Prepare the locations string for the API request
        locations_param = '|'.join([f"{lat},{lon}" for lat, lon in locations])
        params = {'locations': locations_param}
        response = requests.get(self.open_elevation_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Extract elevations in the order of locations
            return [result['elevation'] for result in data['results']]
        else:
            print(f"Error fetching elevations: HTTP {response.status_code}")
            return [None] * len(locations)  # Return a list of None values if there's an error

    def update_elevation(self):
        nodes, edges = ox.graph_to_gdfs(self.network, nodes=True, edges=True)
        locations = [(row['y'], row['x']) for _, row in nodes.iterrows()]

        # Define the maximum number of locations per batch request
        max_batch_size = 100  # Adjust based on API limitations or testing
        for i in range(0, len(locations), max_batch_size):
            batch_locations = locations[i:i + max_batch_size]
            batch_elevations = self.get_elevations_batch(batch_locations)
            for (lat, lon), elevation in zip(batch_locations, batch_elevations):
                # Find the node corresponding to the lat, lon and update its elevation
                node_id = nodes[(nodes['y'] == lat) & (nodes['x'] == lon)].index[0]
                if elevation is not None:
                    self.network.nodes[node_id]['elevation'] = elevation

        return self.network


class NetworkAnalyzer:
    def __init__(self, network):
        self.G = network
        self.critical_elevation = None
        self.nodes_removed = []
        self.perc_nodes_removed = 0

    def analyze_network(self):
        G = self.G.copy()
        N = len(G.nodes)
        GCCs = []
        
        # Ensure 'elevation' attribute is present
        if not any('elevation' in data for _, data in G.nodes(data=True)):
            print("Elevation data is missing in the network nodes.")
            return

        # Pull out elevation attribute
        Z = nx.get_node_attributes(G, 'elevation')
        # Convert elevation values to float and sort
        Sorted_Z = sorted(Z.items(), key=lambda item: item[1])

        # Separate node IDs and their elevation values
        FT = [i[0] for i in Sorted_Z]  # Node IDs
        ST = [i[1] for i in Sorted_Z]  # Elevations

        CCs = np.zeros([len(Sorted_Z), 2])
        critical_node_id = None  # To store the ID of the critical node

        # Loop through all nodes
        for i in range(len(FT)):
            G_temp = G.copy()
            G_temp.remove_nodes_from(FT[:i])
            # Find the number of connected components and their sizes
            GCC = [len(c) for c in sorted(nx.weakly_connected_components(G_temp), key=len, reverse=True)]
            GCCs.append(GCC)
            # Fill CCs array with the relative sizes of the first and second giant components
            if len(GCC) == 1:
                CCs[i, 0] = GCC[0] / N
                CCs[i, 1] = 0
            else:
                CCs[i, 0] = GCC[0] / N
                CCs[i, 1] = GCC[1] / N

        # Find the critical point
        m = max(CCs[:, 1])
        pos = [i for i, j in enumerate(CCs[:, 1]) if j == m][0]
        self.critical_elevation = ST[pos - 1]  # Elevation of the critical node
        print(f"The critical elevation is {self.critical_elevation} meters.")
        self.nodes_removed = FT[:pos]  # IDs of nodes removed up to the critical node

        self.perc_nodes_removed = (len(self.nodes_removed) / N) * 100 if N > 0 else 0


