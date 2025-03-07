import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Load the datasets
calendar = pd.read_csv(r'/Users/elvin/Downloads/CDMX AirBNB/calendar.csv')
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
neighbourhoods_price = listings.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)
neighbourhoods_price
# Analyze listings with prices above 100,000
listings[listings['price'] > 100000]
# Aggregate price information (min, max, mean)
price_info = listings['price'].agg(['min', 'max', 'mean'])
price_info
# Plot the mean price by neighbourhood
neighbourhoods_price.plot(kind='bar', figsize=(12, 6))
plt.title('Mean Price by Neighbourhood')
plt.xlabel('Neighbourhoods')
plt.ylabel('Mean Price (USD)')
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