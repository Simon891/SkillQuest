import ijson

# Step 1: Open the JSON file
with open('2022.json', 'r') as file:

    # Step 2: Create an iterator using ijson
    parser = ijson.items(file, 'item')

    # Step 3: Extract values from the 'occupation' column
    column_values = []

    for item in parser:
        # Traverse the nested structure to access 'occupation' value
        if 'occupation_group' in item and 'label' in item['occupation_group']:
            column_values.append(item['occupation_group']['label'])

# Print the number of values in the 'occupation' column
print("Number of values in 'occupation' column:", len(column_values))

# Print all the values
for value in column_values:
    print(value)
