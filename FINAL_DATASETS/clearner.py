import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('NADRA_2.0.csv')

# Remove single quotes from the "Profession" column
df['Profession'] = df['Profession'].str.replace("'", '')

# Save the updated DataFrame back to a CSV file
df.to_csv('NADRA_2.0_updated.csv', index=False)
