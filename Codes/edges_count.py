import sys

def count_edges_in_gml(gml_file):
    edge_count = 0

    with open(gml_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "edge [" in line:
                edge_count += 1

    return edge_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_edges.py <path_to_gml_file>")
        sys.exit(1)

    gml_path = sys.argv[1]
    edges = count_edges_in_gml(gml_path)

    print(f"Total edges in the GML file: {edges}")
