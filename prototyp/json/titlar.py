import ijson

# Step 1: Open the JSON file
with open('2022.json', 'r') as file:

    # Step 2: Create an iterator using ijson
    parser = ijson.items(file, 'item')

    # Step 3: Extract values from the 'occupation' column
    unique_values = set()

    for item in parser:
        # Traverse the nested structure to access 'occupation' value
        if 'occupation_group' in item and 'label' in item['occupation_group']:
            unique_values.add(item['occupation_group']['label'])

# Print the number of unique values in the 'occupation' column
print("Number of unique values in 'occupation' column:", len(unique_values))

# Print all the unique values
for value in unique_values:
    print(value)
