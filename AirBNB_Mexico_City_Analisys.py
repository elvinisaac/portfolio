import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
import numpy as np

# Load the datasets
calendar_df = pd.read_csv(r'/Users/elvin/Downloads/CDMX AirBNB/calendar.csv')
listings = pd.read_csv(r'/Users/elvin/Downloads/CDMX AirBNB/listings-2.csv')
neighbourhoods = pd.read_csv(r'/Users/elvin/Downloads/CDMX AirBNB/neighbourhoods.csv')
reviews = pd.read_csv(r'/Users/elvin/Downloads/CDMX AirBNB/reviews-2.csv')


# Display the dataframes to analyze the data
calendar
listings
neighbourhoods
reviews

# Data Cleaning
# Drop rows with missing prices in the listings dataframe
listings.dropna(subset=['price'], inplace=True)
listings.info()
# Drop the 'neighbourhood_group' column
listings = listings.drop(columns=['neighbourhood_group'])

# Clean the 'price' column in the calendar dataframe by removing dollar signs and converting to float
calendar['price'] = calendar['price'].replace('[\$,]', '', regex=True).astype(float)
# Drop rows with missing prices in the calendar dataframe
calendar.dropna(subset=['price'], inplace=True)

# CORRELATION ANALYSIS
# Select only numeric columns
numeric_columns = listings.select_dtypes(include=['int64', 'float64'])
# Calculate the correlation matrix
correlation_matrix = numeric_columns.corr()
# Display the correlation matrix
print(correlation_matrix)
# Set the size of the heatmap
plt.figure(figsize=(12, 8))
# Create the heatmap
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values in each cell
    cmap='coolwarm',  # Color palette
    fmt=".2f",  # Number format (2 decimal places)
    linewidths=0.5,  # Line thickness between cells
)
# Add title
plt.title('Correlation Matrix - Dataset Listings')

# Display the heatmap
plt.show()


# NEIGHBOURHOODS ANALYSIS
# Calculate the mean price by neighbourhood
neighbourhoods_price = listings('neighbourhood')['price'].mean().sort_values(ascending=False)
neighbourhoods_price
# Aggregate price information (min, max, mean)
price_info = listings['price'].agg(['min', 'max', 'mean'])
price_info
# Plot the mean price by neighbourhood
neighbourhoods_price.plot(kind='bar', figsize=(12, 6), color='#DA847C')
plt.title('Mean Price by Neighbourhood', pad=15, fontsize=20, fontweight='semibold', color='#222222')
plt.xlabel('Neighbourhoods',labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.ylabel('Mean Price (USD)', labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.xticks(fontsize=14, color='#555555')
plt.yticks(fontsize=14, color='#555555')
plt.grid(color='#E0E0E0')
plt.tight_layout()
plt.show()

# Create a figure for neighborhood distribution
neighborhood_counts = listings['neighbourhood'].value_counts().head(10)
plt.figure(figsize=(9, 6))
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)
plt.show()

# Analyze room type vs price
plt.figure(figsize=(9, 6))
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

# Create boxplot for price by room type (excluding outliers)

sns.boxplot(x='room_type', 
            y='price', 
            data=listings[listings['price'] < listings['price'].quantile(0.95)],
            palette=['#1B47A7', '#1BA75F', '#7FA71B', '#A7271B'])
plt.title('Price Distribution by Room Type (excluding top 5% outliers)', pad=15)
plt.xlabel('Room Type', labelpad=10)
plt.ylabel('Price (in local currency)', labelpad=10)
plt.grid(linestyle='--', alpha=0.6, axis='y')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_color('#EDEDED')
plt.gca().spines['bottom'].set_color('#EDEDED')
plt.gca().set_axisbelow(True)
plt.show()

# Create a map of Airbnb listings in Mexico City
# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(
    listings,
    geometry=gpd.points_from_xy(listings['longitude'], listings['latitude']),
    crs="EPSG:4326"  # WGS84 coordinate system (lat/lon)
)

# Convert to a projected coordinate system (to use contextily)
gdf = gdf.to_crs(epsg=3857)

# Create the static map
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the points with colors based on price
scatter = gdf.plot(
    ax=ax,
    marker='o',
    c=gdf['price'],  # Colors based on price
    cmap='coolwarm',  # Color palette
    markersize=5,  # Size of the points
    alpha=0.5,  # Transparency
    legend=True  # Show color bar
)

# Add a base map (OpenStreetMap)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Add title and labels
ax.set_title('Airbnb Listings in Mexico City', fontsize=16)
ax.set_axis_off()  # Hide the axes

# Add color bar
cbar = plt.colorbar(scatter.collections[0], ax=ax, orientation='vertical', fraction=0.02, pad=0.1)
cbar.set_label('Price (MXN)')

# Show the map
plt.show()

#Data Analysis about calendar.csv
# Clean the price column: remove dollar sign and comma, then convert to float
calendar_df['price_clean'] = calendar_df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Convert date column to datetime
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

# Add month column for aggregation
calendar_df['month'] = calendar_df['date'].dt.to_period('M').astype(str)

# Create a booking indicator: if available is 'f', then it's booked
calendar_df['booked'] = calendar_df['available'].apply(lambda x: 1 if x.lower() == 'f' else 0)

# Aggregate pricing trends by month 
avg_price_by_month = calendar_df.groupby('month')['price_clean'].mean().reset_index()
print('Average price by month:')
print(avg_price_by_month)

# Aggregate booking trends by month
bookings_by_month = calendar_df.groupby('month')['booked'].sum().reset_index()
print('Number of booked dates by month:')
print(bookings_by_month)

# Plot average price over months
plt.figure(figsize=(9, 6))
plt.plot(avg_price_by_month['month'], avg_price_by_month['price_clean'], marker='o', color='#766CDB', label='Avg Price')
plt.title('Average Price by Month', pad=15, fontsize=20, fontweight='semibold', color='#222222')
plt.xlabel('Month', labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.ylabel('Average Price ($)', labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.xticks(rotation=45, fontsize=14, color='#555555')
plt.yticks(fontsize=14, color='#555555')
plt.grid(color='#E0E0E0')
plt.legend(fontsize=12, loc='lower center')
plt.tight_layout()
plt.show()

# Plot booked dates over months
plt.figure(figsize=(9, 6))
plt.bar(bookings_by_month['month'], bookings_by_month['booked'], color='#DA847C', label='Booked Dates')
plt.title('Booked Dates by Month', pad=15, fontsize=20, fontweight='semibold', color='#222222')
plt.xlabel('Month', labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.ylabel('Number of Booked Dates', labelpad=10, fontsize=16, fontweight='medium', color='#333333')
plt.xticks(rotation=45, fontsize=14, color='#555555')
plt.yticks(fontsize=14, color='#555555')
plt.grid(color='#E0E0E0')
plt.legend(fontsize=12, loc='lower center')
plt.tight_layout()
plt.show()
