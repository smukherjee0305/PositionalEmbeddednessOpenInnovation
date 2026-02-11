import networkx as nx
import csv
import glob
import os

output_csv = r"G:\StackOverflow\Data\Improved\2023\Combined_Network_2023.csv"

files = glob.glob(r"G:\StackOverflow\Data\Improved\2023\**\finalgml_2023_*.gml", recursive=True)

with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    
    writer.writerow([
        "Label", "Year", "Month",
        "Degree Centrality", "Core Number", 
        " Strength", "Clustering Coefficient",
        "Gold Badges", "Silver Badges", "Bronze Badges","No. of Accepted Answers","Active Duration","Reputation Score"
    ])

    for file in files:
        G = nx.read_gml(file)
        filename = os.path.basename(file)
        parts = filename.split("_")
        year = parts[1]
        month = parts[2].split(".")[0]

        for node, attrs in G.nodes(data=True):
            writer.writerow([
                attrs.get("label", node),             
                year,
                month,
                attrs.get("degree_centrality", ""),
                attrs.get("core_number", ""),
                attrs.get("strength", ""),
                attrs.get("clustering_coefficient", ""),                
                attrs.get("gold_badges", ""),
                attrs.get("silver_badges", ""),
                attrs.get("bronze_badges", ""),
                attrs.get("askers_count", ""),
                attrs.get("active_duration", ""),
                attrs.get("reputation_score","")
            ])

print(f"CSV file saved successfully: {output_csv}")
