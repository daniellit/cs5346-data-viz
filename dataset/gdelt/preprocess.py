import pandas as pd

# Load the dataset
df = pd.read_csv('gdelt_rolling_correl.csv')

# List of columns to keep as-is (non-correlation columns)
id_vars = ['Date', 'SP500%ChgD', 'SrcWgtAvgTone', 'SrcWgtGoldScore']

# List of correlation columns to unpivot
value_vars = [col for col in df.columns if col not in id_vars]

# Unpivot the data
df_melted = df.melt(id_vars=id_vars, value_vars=value_vars, 
                    var_name='Correlation Metric', value_name='Correlation Value')

# Save the reshaped data to a new CSV file
df_melted.to_csv('gdelt_rolling_correl_reshaped.csv', index=False)

print("Data has been reshaped and saved to 'reshaped_data.csv'")