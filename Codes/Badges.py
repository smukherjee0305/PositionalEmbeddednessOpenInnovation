import csv
import sys
from xml.dom import pulldom
from datetime import datetime

def parse_creation_date(creation_date_str):
    try:
        dt = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        return dt.year, dt.month  
    except ValueError:
        # If there's an error, print the invalid date and return None
        print(f"Invalid date format: {creation_date_str}")
        return None, None

# Function to parse the cleaned XML file and extract badge data
def parse_badges_xml_streaming(file_path, year, month):
    try:
        doc = pulldom.parse(file_path)
        user_badges = {}

        # Iterate through each node in the document
        for event, node in doc:
            if event == pulldom.START_ELEMENT and node.nodeName == 'row':
                user_id = node.getAttribute('UserId')
                badge_class = node.getAttribute('Class')
                creation_date = node.getAttribute('Date')

                # Filter by year and month
                if creation_date:
                    dt_year, dt_month = parse_creation_date(creation_date)
                    if dt_year == year and dt_month == month:

                        if user_id not in user_badges:
                            user_badges[user_id] = {'gold': 0, 'silver': 0, 'bronze': 0}

                        # Count badges based on the class attribute
                        if badge_class == '1':
                            user_badges[user_id]['gold'] += 1
                        elif badge_class == '2':
                            user_badges[user_id]['silver'] += 1
                        elif badge_class == '3':
                            user_badges[user_id]['bronze'] += 1

        print(f"Total Users Parsed: {len(user_badges)}")
        return user_badges

    except Exception as e:
        print(f"Error while parsing XML: {e}")
        return {}

# Function to save results to a CSV file
def save_results_to_csv(user_badges, year, month, output_csv):
    try:
        # Write the data to a CSV file
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Add a header with Year/Month
            writer.writerow(["UserID", "Year/Month", "#Gold", "#Silver", "#Bronze"])

            # Add year/month for every row
            year_month = f"{year}-{str(month).zfill(2)}"
            for user_id, badges in user_badges.items():
                writer.writerow([user_id, year_month, badges['gold'], badges['silver'], badges['bronze']])

        print(f"CSV file created: {output_csv}")

    except Exception as e:
        print(f"Error while saving CSV: {e}")


if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("Usage: python Badges.py <input_file.xml> <year> <month>")
        sys.exit(1)

    input_file = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])

    
    output_csv = f"badges_{year}_{str(month).zfill(2)}.csv"

    
    user_badges = parse_badges_xml_streaming(input_file, year, month)

    
    if user_badges:
        save_results_to_csv(user_badges, year, month, output_csv)
    else:
        print(f"No badge data found for {year}/{str(month).zfill(2)}.")
