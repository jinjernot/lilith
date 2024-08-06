import pandas as pd

# Load the Excel file
file_path = 'PLCRegionalAll.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows to understand the structure
print("Original DataFrame:")
print(df.head())

# Use a set to track the unique values from the "Material No." column
unique_values_set = set()

# Create a list to store the filtered results
filtered_rows = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    material_no = row['Material No.']
    region = row['Country']
    
    # Check if this material number is already in our set
    if material_no not in unique_values_set:
        # Add the unique material number to the set
        unique_values_set.add(material_no)
        
        # Append the row to the filtered rows list
        filtered_rows.append({'Material No.': material_no, 'Region': region})

# Create a DataFrame from the filtered rows list
filtered_data = pd.DataFrame(filtered_rows, columns=['Material No.', 'Region'])

# Display the filtered results
print("\nFiltered DataFrame with unique values from 'Material No.':")
print(filtered_data)

# Save the filtered data to a new Excel file
filtered_file_path = 'filtered_report.xlsx'
filtered_data.to_excel(filtered_file_path, index=False)

print(f"\nFiltered results saved to '{filtered_file_path}'")
