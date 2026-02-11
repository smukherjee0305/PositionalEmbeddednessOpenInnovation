
import csv
from datetime import datetime
from xml.dom import pulldom
from collections import defaultdict
import sys

def parse_and_calculate_duration(xml_file, output_csv, year, month):
    answerer_activity = defaultdict(list)

    events = pulldom.parse(xml_file)

    for event, node in events:
        if event == pulldom.START_ELEMENT and node.tagName == "row":
            events.expandNode(node)

            # Extract relevant attributes
            post_type_id = node.getAttribute("PostTypeId")
            owner_user_id = node.getAttribute("OwnerUserId")
            creation_date_str = node.getAttribute("CreationDate")

            # Process only answers (PostTypeId == "2")
            if post_type_id == "2" and owner_user_id and creation_date_str:
                # Parse the creation date
                creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")

                # Filter by the given year and month
                if creation_date.year == int(year) and creation_date.month == int(month):
                    answerer_activity[owner_user_id].append(creation_date)

    answerer_duration = []
    for user_id, dates in answerer_activity.items():
        if len(dates) > 1:
            min_date = min(dates)
            max_date = max(dates)
            active_duration = (max_date - min_date).days
        else:
            active_duration = 0  

        # Format year/month for the output
        year_month = f"{year}-{str(month).zfill(2)}"
        answerer_duration.append((user_id, year_month, active_duration))


    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User ID", "Year/Month", "Active Duration (Days)"])
        writer.writerows(answerer_duration)

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <xml_file> <output_file> <year> <month>")
        sys.exit(1)

    xml_file = sys.argv[1]  
    output_file = sys.argv[2]  
    year = sys.argv[3]  
    month = sys.argv[4]  


    parse_and_calculate_duration(xml_file, output_file, year, month)
