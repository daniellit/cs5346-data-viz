import pandas as pd

# Load the SPX dataset (comma-separated)
spx_df = pd.read_csv("SPX_dataset_cleaned.csv")

# Load the FOMC dataset using pipe delimiter
fomc_df = pd.read_csv("./fomc_statements/fomc_statement_with_sentiment.csv", delimiter='|')

# Convert date columns to datetime format
spx_df['Date'] = pd.to_datetime(spx_df['Date'])
fomc_df['Release Date'] = pd.to_datetime(fomc_df['Release Date'])

# Select necessary columns from FOMC and remove duplicates
fomc_trimmed = fomc_df[['Release Date', 'Type', 'Sentiment', 'HawkishDovish']].drop_duplicates()

# Merge SPX with FOMC data on date
merged_df = pd.merge(spx_df, fomc_trimmed, how='left', left_on='Date', right_on='Release Date')

# Drop 'Release Date' column post-merge
merged_df.drop(columns=['Release Date'], inplace=True)

# Prepare FOMC date list for nearest-day calculations
fomc_dates = fomc_df['Release Date'].dropna().sort_values().unique()

# Function to calculate signed days to the nearest FOMC release
def signed_days_to_nearest_fomc(date):
    closest_date = min(fomc_dates, key=lambda d: abs((date - d).days))
    return (date - closest_date).days

# Apply the function
merged_df['DaysToNearestFOMC'] = merged_df['Date'].apply(signed_days_to_nearest_fomc)

# Save final output to CSV
merged_df.to_csv("SPX_dataset_cleaned.csv", index=False)

# Preview output
print(merged_df.head())
