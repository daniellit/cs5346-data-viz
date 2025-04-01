import pandas as pd

# Load the events dataset
events = pd.read_csv('Notable_Events_dataset.csv')

# Convert Date to datetime
events['Date'] = pd.to_datetime(events['Date'])

# Create truncated date columns for each granularity
events['Day Truncated'] = events['Date'].dt.to_period('D').dt.to_timestamp()
events['Week Truncated'] = events['Date'].dt.to_period('W').dt.to_timestamp()
events['Month Truncated'] = events['Date'].dt.to_period('M').dt.to_timestamp()

# Group by each granularity and concatenate event names
day_events = events.groupby('Day Truncated')['Event Name'].agg(', '.join).reset_index()
week_events = events.groupby('Week Truncated')['Event Name'].agg(', '.join).reset_index()
month_events = events.groupby('Month Truncated')['Event Name'].agg(', '.join).reset_index()

# Add a Granularity column
day_events['Granularity'] = 'Day'
week_events['Granularity'] = 'Week'
month_events['Granularity'] = 'Month'

# Rename the date columns to a common name
day_events = day_events.rename(columns={'Day Truncated': 'Truncated Date'})
week_events = week_events.rename(columns={'Week Truncated': 'Truncated Date'})
month_events = month_events.rename(columns={'Month Truncated': 'Truncated Date'})

# Concatenate the datasets
combined_events = pd.concat([day_events, week_events, month_events], ignore_index=True)

# Save the combined dataset
combined_events.to_csv('events_aggregated_combined.csv', index=False)