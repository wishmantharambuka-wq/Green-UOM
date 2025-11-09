import xml.etree.ElementTree as ET
from collections import Counter
import re

# Parse KML file
tree = ET.parse('University of Moratuwa Trees.kml')
root = tree.getroot()

# Extract all tree data
trees = []
species_counter = Counter()
all_dbh = []
all_heights = []

# Find all Placemark elements
for placemark in root.iter('{http://www.opengis.net/kml/2.2}Placemark'):
    description = placemark.find('.//{http://www.opengis.net/kml/2.2}description')
    if description is not None and description.text:
        # Extract NAME
        name_match = re.search(r'NAME:\s*([^\n]+)', description.text)
        if name_match:
            species_name = name_match.group(1).strip()
            if species_name and species_name.lower() not in ['', 'unknown']:
                trees.append({'name': species_name, 'data': description.text})
                species_counter[species_name] += 1
                
                # Extract DBH
                dbh_match = re.search(r'DBS:\s*([\d.]+)', description.text)
                if dbh_match:
                    all_dbh.append(float(dbh_match.group(1)))
                
                # Extract HEIGHT
                height_match = re.search(r'HEIGHT:\s*([\d.]+)', description.text)
                if height_match:
                    all_heights.append(float(height_match.group(1)))

print('=== TREE SURVEY STATISTICS ===')
print(f'Total Trees Surveyed: {len(trees)}')
print(f'Unique Species: {len(species_counter)}')
print(f'\nTop 10 Most Common Species:')
for species, count in species_counter.most_common(10):
    print(f'  {species}: {count}')

if species_counter:
    most_common = species_counter.most_common(1)[0]
    print(f'\nMost Common: {most_common[0]} ({most_common[1]})')

if all_dbh:
    print(f'\nLargest DBH: {max(all_dbh)} inches')
    
if all_heights:
    print(f'Tallest Tree: {max(all_heights)} feet')
