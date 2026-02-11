import sys
from xml.dom import pulldom
import csv
from collections import defaultdict

def collect_reputation_score_for_answerers(xml_file, year, month):
    events = pulldom.parse(xml_file)

    answerers = defaultdict(lambda: {'reputation': 0})

    for event, node in events:
        if event == pulldom.START_ELEMENT and node.tagName == "row":  
            events.expandNode(node)  

            post_type_id = node.getAttribute("PostTypeId")            
            creation_date_str = node.getAttribute("CreationDate")    
            owner_user_id = node.getAttribute("OwnerUserId")         
            reputation_score = node.getAttribute("Score")            

            # Extract year and month from the creation date
            year_extracted = int(creation_date_str.split('T')[0].split('-')[0])
            month_extracted = int(creation_date_str.split('T')[0].split('-')[1])

            if post_type_id == "2" and year_extracted == int(year) and month_extracted == int(month):
                if owner_user_id:  
                    if reputation_score:  
                        answerers[owner_user_id]['reputation'] += int(reputation_score)


    return answerers

def save_results_to_csv(answerers, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['answerer_user_id', 'reputation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for answerer_user_id, data in answerers.items():
            row = {
                'answerer_user_id': answerer_user_id,
                'reputation': data['reputation']
            }
            writer.writerow(row)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <xml_file> <output_file> <year> <month>")
        sys.exit(1)

    xml_file = sys.argv[1]
    output_file = sys.argv[2]
    year = sys.argv[3]
    month = sys.argv[4]

    answerers = collect_reputation_score_for_answerers(xml_file, year, month)
    save_results_to_csv(answerers, output_file)
