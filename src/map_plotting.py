import osmnx as ox
import folium
from folium import FeatureGroup
import branca.colormap as cm

class NetworkPlotter:
    def __init__(self, network):
        self.network = network

    def plot_network_with_elevation(self):
        # Convert the network into GeoDataFrames for nodes and edges
        nodes, edges = ox.graph_to_gdfs(self.network, nodes=True, edges=True)

        # Ensure the elevation data is sorted and clean
        if 'elevation' in nodes:
            # Filter out any nodes with None elevation
            nodes = nodes[nodes['elevation'].notnull()]
            # Sort nodes by elevation
            nodes = nodes.sort_values(by='elevation')

        # Find the center of the map
        x, y = nodes.unary_union.centroid.xy
        center = (y[0], x[0])

        # Create a folium map centered at the calculated center
        m = folium.Map(location=center, zoom_start=13, tiles='CartoDB positron')

        # Feature groups for nodes and edges
        fg_nodes = folium.FeatureGroup(name='Nodes 🟢')
        fg_edges = folium.FeatureGroup(name='Edges ➖')

        # Plot edges
        for _, row in edges.iterrows():
            start_point = [row['geometry'].coords[0][1], row['geometry'].coords[0][0]]
            end_point = [row['geometry'].coords[-1][1], row['geometry'].coords[-1][0]]
            line = folium.PolyLine(locations=[start_point, end_point], weight=2, color='gray')
            fg_edges.add_child(line)

        # Plot nodes with elevation data
        if 'elevation' in nodes:
            min_elevation = nodes['elevation'].min()
            max_elevation = nodes['elevation'].max()
            color_scale = cm.linear.viridis.scale(min_elevation, max_elevation)

            for _, row in nodes.iterrows():
                if 'elevation' in row:
                    color = color_scale(row['elevation'])
                    popup_text = f"Elevation: {row['elevation']} meters"
                else:
                    color = 'grey'
                    popup_text = "Elevation data not available"
                
                marker = folium.CircleMarker(location=(row['y'], row['x']),
                                             radius=3,
                                             fill=True,
                                             fill_color=color,
                                             color=None,
                                             fill_opacity=1.0,
                                             popup=popup_text)
                fg_nodes.add_child(marker)

        # Add feature groups to map
        m.add_child(fg_edges)
        m.add_child(fg_nodes)

        # Add the color scale to the map for reference
        m.add_child(color_scale)

        # Add layer control to toggle visibility
        folium.map.LayerControl('bottomleft', collapsed=False).add_to(m)

        return m
    
class CriticalPlotter:

    def __init__(self, network, nodes_removed, critical_elevation):
        self.G = network
        self.nodes_removed = nodes_removed
        self.critical_elevation = critical_elevation

    def prepare_and_plot(self):
        if self.critical_elevation is None or not self.nodes_removed:
            print("Network not analyzed yet or no nodes were identified for removal.")
            return None

        # Convert the network into GeoDataFrames for nodes and edges
        nodes, edges = ox.graph_to_gdfs(self.G, nodes=True, edges=True)

        # Find the center of the map
        x, y = nodes.unary_union.centroid.xy
        center = (y[0], x[0])

        # Create a folium map centered at the calculated center
        m = folium.Map(location=center, zoom_start=13, tiles='CartoDB positron')

        # Assuming the last node removed before the largest drop is the critical one
        critical_node_id = self.nodes_removed[-1] if self.nodes_removed else None

        # Add feature groups for edges, connected nodes, disconnected nodes, and critical node
        edges_fg = FeatureGroup(name='Edges ➖')
        connected_nodes_fg = FeatureGroup(name='Connected Nodes 🟢')
        disconnected_nodes_fg = FeatureGroup(name='Disconnected Nodes ⚫')
        critical_node_fg = FeatureGroup(name='Critical Node 🔴')

        # Add edges
        for _, row in edges.iterrows():
            if 'geometry' in row:
                # For edges with complex geometries
                xy = [(lat, lon) for lon, lat in row['geometry'].coords]
            else:
                # For straight edges not having a 'geometry' attribute
                start_node = row['u']
                end_node = row['v']
                start_pos = (nodes.loc[start_node, 'y'], nodes.loc[start_node, 'x'])
                end_pos = (nodes.loc[end_node, 'y'], nodes.loc[end_node, 'x'])
                xy = [start_pos, end_pos]

            folium.PolyLine(
                locations=xy,
                color='grey',  # Default color for all edges
                weight=2,
                opacity=1.0
            ).add_to(edges_fg)

        # Plot nodes with color based on their status (critical, disconnected, connected)
        for node_id, row in nodes.iterrows():
            color = 'green'  # Default for connected nodes
            if node_id in self.nodes_removed[:-1]:
                color = 'black'  # Disconnected nodes
            if node_id == critical_node_id:
                color = 'red'  # Critical node

            folium.CircleMarker(
                location=(row['y'], row['x']),
                radius=5 if node_id == critical_node_id else 3,  # Larger radius for critical node
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1.0,
                popup=f"Elevation: {row['elevation']}m"
            ).add_to(connected_nodes_fg if color == 'green' else disconnected_nodes_fg if color == 'black' else critical_node_fg)

        # Add feature groups to the map
        edges_fg.add_to(m)
        connected_nodes_fg.add_to(m)
        disconnected_nodes_fg.add_to(m)
        critical_node_fg.add_to(m)

        # Add layer control to toggle visibility
        folium.map.LayerControl('bottomleft', collapsed= False).add_to(m)

        return m