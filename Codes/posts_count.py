import xml.etree.ElementTree as ET

def count_posts(xml_file):
    count = 0
    for event, elem in ET.iterparse(xml_file, events=("end",)):
        if elem.tag == "row":
            count += 1
        elem.clear()  # free memory for large files
    return count

if __name__ == "__main__":
    xml_file = "/media/monica/Expansion/StackOverflow/Data/RawData/PostsFormat.xml"
    print("Total number of posts:", count_posts(xml_file))

