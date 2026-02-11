

import sys
from itertools import combinations
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import chardet  
from xml.dom import pulldom
from datetime import datetime


def create_network_users_common_answer(xml_file, y, m, output_gml_file):

	events = pulldom.parseString(xml_content)

	# Dictionary to store question ID and its asker
	question_asker_dict = {}

	# Dictionary to store question ID and list of answerers
	question_answerers_dict = defaultdict(list)

	# Dictionary to store the weights of edges 
	edge_weights = defaultdict(int)

	# Iterate over the XML events
	for event, node in events:
		if event == pulldom.START_ELEMENT:
			if node.tagName == "row":
				events.expandNode(node)

				PostId = node.getAttribute("Id")
				creationdate = node.getAttribute("CreationDate")
				PostTypeId = node.getAttribute("PostTypeId")
				OwnerUserId = node.getAttribute("OwnerUserId")
				ParentId = node.getAttribute("ParentId")

				# Extract year and month for filtering purposes
				year = int(creationdate.split('T')[0].split('-')[0])
				month = int(creationdate.split('T')[0].split('-')[1])

				if year == int(y) and month == int(m):
					# Case 1: If it's a question (PostTypeId = 1)
					if PostTypeId == '1' and OwnerUserId:
						question_asker_dict[PostId] = OwnerUserId 

					# Case 2: If it's an answer (PostTypeId = 2)
					elif PostTypeId == '2' and ParentId and OwnerUserId:
						if ParentId in question_asker_dict: 
							question_answerers_dict[ParentId].append(OwnerUserId) 
							
	for parent_id, answerers in question_answerers_dict.items():
		if len(answerers) > 1: 
			for pair in combinations(answerers, 2):
				ordered_pair = tuple(sorted(pair))
				edge_weights[ordered_pair] += 1

	 
    for edge, weight in edge_weights.items():
	 	if edge[0].strip() and edge[1].strip() and edge[0]!=edge[1]:
	# 		print(f"Edge {edge}: Weight {weight}")

	# Create a graph and add edges with weights
	G = nx.Graph()
	for edge, weight in edge_weights.items():
		if edge[0].strip() and edge[1].strip() and edge[0]!=edge[1]:
			G.add_edge(edge[0], edge[1], weight=weight)
	G.remove_nodes_from([' '])

	# "F:\\My_folder2\\Sample2.gml"
	nx.write_gml(G, output_gml_file)


def network_centrality_measures(input_gml_file, output_gml_file) :

	# input_gml_file = "F:\\My_folder2\\Sample2.gml" 
	# output_gml_file = "F:\Output_trial_gml_file_with_centralities\Posts_trial_with_centralities.gml'
	# Load the graph from the GML file
	G = nx.read_gml(input_gml_file)

	# 1. Calculate Degree Centrality
	degree_centrality = nx.degree_centrality(G)

	# 2. Calculate K-core number 
	core_number = nx.core_number(G)

	# 3. Calculate Strength (sum of edge weights for each node)
	strength = dict(G.degree(weight='weight'))

	# 4. Calculate Local Clustering Coefficient (takes weights into account)
	clustering_coefficient = nx.clustering(G, weight='weight')

	# Add these attributes to the graph nodes
	for node in G.nodes():
		G.nodes[node]['degree_centrality'] = degree_centrality.get(node, 0)
		G.nodes[node]['core_number'] = core_number.get(node, 0)
		G.nodes[node]['strength'] = strength.get(node, 0)
		G.nodes[node]['clustering_coefficient'] = clustering_coefficient.get(node, 0)

	nx.write_gml(G, output_gml_file)



if __name__ == "__main__" :
	f1 = sys.argv[1]; f2 = sys.argv[2]; #f3 = sys.argv[3]; f4 = sys.argv[4]; #f5 = sys.argv[5];
	# create_network_users_common_answer(f1, f2, f3, f4) 
	network_centrality_measures(f1, f2)



