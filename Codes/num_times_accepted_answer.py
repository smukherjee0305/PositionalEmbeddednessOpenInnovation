import sys
from xml.dom import pulldom
import csv
from collections import defaultdict

# Function to parse XML and collect users for accepted answers
def collect_answerers(xml_file, year, month):
    events = pulldom.parse(xml_file)
    
    # Dictionary to store answerers and the count of askers
    answerers = defaultdict(lambda: {'askers': 0, 'year_month': set()})
    answer_post_id = {}

    for event, node in events:
        if event == pulldom.START_ELEMENT and node.tagName == "row":
            events.expandNode(node)
            
            post_id = node.getAttribute("Id")
            owner_user_id = node.getAttribute("OwnerUserId")  
            accepted_answer_id = node.getAttribute("AcceptedAnswerId")  
            post_type_id = node.getAttribute("PostTypeId")  
            creation_date_str = node.getAttribute("CreationDate")
            
            # Extract year and month 
            year_extracted = int(creation_date_str.split('T')[0].split('-')[0])
            month_extracted = int(creation_date_str.split('T')[0].split('-')[1])
            year_month = f"{year_extracted}-{str(month_extracted).zfill(2)}"

            # Track answers (PostTypeId = "2")
            if post_type_id == "2" and owner_user_id:  
                answer_post_id[post_id] = (owner_user_id, year_month)

            # Process questions (PostTypeId = "1")
            if post_type_id == "1" and accepted_answer_id and owner_user_id:
                if year_extracted == int(year) and month_extracted == int(month):
                    answerer_info = answer_post_id.get(accepted_answer_id)
                    if answerer_info:
                        answerer_user_id, answer_year_month = answerer_info
                        if answer_year_month == year_month:
                            answerers[answerer_user_id]['askers'] += 1
                            answerers[answerer_user_id]['year_month'].add(year_month)

    return answerers

# Function to save results to a CSV file
def save_results_to_csv(answerers, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['answerer_user_id', 'year_month', 'askers_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for answerer_user_id, data in answerers.items():
            for year_month in data['year_month']:
                row = {
                    'answerer_user_id': answerer_user_id,
                    'year_month': year_month,
                    'askers_count': data['askers']  
                }
                writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <xml_file> <output_file> <year> <month>")
        sys.exit(1)

    xml_file = sys.argv[1]
    output_file = sys.argv[2]
    year = sys.argv[3]
    month = sys.argv[4]
    
    try:
        answerers = collect_answerers(xml_file, year, month)
        save_results_to_csv(answerers, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

