import ijson

# Step 1: Open the JSON file
with open('2022.json', 'r') as file:

    # Step 2: Create an iterator using ijson
    parser = ijson.parse(file)

    # Print the entire JSON data
    for prefix, event, value in parser:
        print(f"Prefix: {prefix}, Event: {event}, Value: {value}")
