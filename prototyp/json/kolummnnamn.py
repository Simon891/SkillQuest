import ijson

# Step 1: Open the JSON file
with open('2022.json', 'r') as file:

    # Step 2: Create an iterator using ijson
    parser = ijson.items(file, 'item')

    # Step 3: Extract column names from the first object
    column_names = []
    for item in parser:
        column_names = list(item.keys())
        break

# Print the column names
for column_name in column_names:
    print(column_name)
