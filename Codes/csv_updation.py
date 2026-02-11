import sys
import networkx as nx
import csv

def update_gml_with_csv_data(gml_file, badges_csv, active_duration_csv, askers_count_csv, reputation_score_csv, output_gml):
    G = nx.read_gml(gml_file)

    badges_data = {}
    askers_data = {}
    active_duration_data = {}
    reputation_score_data = {}

    # Read badges data
    with open(badges_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row.get('UserID')
            if user_id:
                badges_data[user_id] = {
                    "gold_badges": int(row.get('#Gold')),
                    "silver_badges": int(row.get('#Silver')),
                    "bronze_badges": int(row.get('#Bronze')),
                }

    # Read active duration data
    with open(active_duration_csv, 'r', encoding='utf-8') as file2:
        reader = csv.DictReader(file2)
        for row in reader:
            user_id = row.get('User ID')
            if user_id:
                active_duration_data[user_id] = {
                    "active_duration": int(row.get('Active Duration (Days)')),
                }

    # Read askers count data
    with open(askers_count_csv, 'r', encoding='utf-8') as file3:
        reader = csv.DictReader(file3)
        for row in reader:
            user_id = row.get('answerer_user_id')
            if user_id:
                askers_data[user_id] = {
                    "askers_count": int(row.get('askers_count')),
                }

    # Read reputation score data
    with open(reputation_score_csv, 'r', encoding='utf-8') as file4:
        reader = csv.DictReader(file4)
        for row in reader:
            user_id = row.get('answerer_user_id')
            if user_id:
                reputation_score_data[user_id] = {
                    "reputation_score": int(row.get('reputation'))
                }

    # Update graph nodes with data
    for node in G.nodes:
        label = str(node)
        if label in badges_data:
            G.nodes[node].update(badges_data[label])
        else:
            G.nodes[node].update({"gold_badges": 0, "silver_badges": 0, "bronze_badges": 0})

        if label in askers_data:
            G.nodes[node].update(askers_data[label])
        else:
            G.nodes[node].update({"askers_count": 0})

        if label in active_duration_data:
            G.nodes[node].update(active_duration_data[label])
        else:
            G.nodes[node].update({"active_duration": 0})

        if label in reputation_score_data:
            G.nodes[node].update(reputation_score_data[label])
        else:
            G.nodes[node].update({"reputation_score": 0})

    # Save the updated graph to a new GML file
    nx.write_gml(G, output_gml)
    print(f"Updated GML file saved to: {output_gml}")

if __name__ == "__main__":
    gml_file = sys.argv[1]
    badges_csv = sys.argv[2]
    active_duration_csv = sys.argv[3]
    askers_count_csv = sys.argv[4]
    reputation_score_csv = sys.argv[5]
    output_gml = sys.argv[6]

    update_gml_with_csv_data(gml_file, badges_csv, active_duration_csv, askers_count_csv, reputation_score_csv, output_gml)
