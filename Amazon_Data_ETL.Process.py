# ETL Script for Amazon E-commerce Data 

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# --- Step 1: Data Extraction ---
# Documentation:
# This step loads the data from an Excel file into a Pandas DataFrame for processing.
data_path = 'amazon_data.xlsx'
amazon_data = pd.read_excel(data_path, sheet_name='amaz')

def extract_data(data):
    """
    Extract data from the source file into a DataFrame.

    Args:
        data (DataFrame): Raw data loaded from the source file.

    Returns:
        DataFrame: A copy of the original data for processing.
    """
    return data.copy()

data = extract_data(amazon_data)

# --- Step 2: Data Transformation ---
# Documentation:
# This step cleans and transforms the data, adding derived columns and handling missing values.
def clean_data(data):
    """
    Clean and preprocess the dataset.

    Steps:
    - Handle missing values.
    - Standardize prices by removing special characters.
    - Convert ratings to numeric values.
    - Add derived columns such as `is_discounted` and `price_difference`.

    Args:
        data (DataFrame): Raw data to be cleaned.

    Returns:
        DataFrame: Cleaned and transformed data.
    """
    # Handle missing values
    data['rating_count'].fillna(0, inplace=True)
    data['rating'].replace('N/A', np.nan, inplace=True)

    # Standardize prices
    data['discounted_price'] = data['discounted_price'].str.replace('â‚¹|,', '', regex=True).astype(float)
    data['actual_price'] = data['actual_price'].str.replace('â‚¹|,', '', regex=True).astype(float)

    # Convert ratings to numeric
    data['rating'] = pd.to_numeric(data['rating'], errors='coerce')

    # Add is_discounted column
    data['is_discounted'] = data['discount_percentage'] > 0

    # Add price_difference column
    data['price_difference'] = data['actual_price'] - data['discounted_price']

    return data

data = clean_data(data)

def aggregate_data(data):
    """
    Perform aggregations on the dataset.

    Steps:
    - Calculate average ratings per product.

    Args:
        data (DataFrame): Transformed data.

    Returns:
        DataFrame: Aggregated data with average ratings.
    """
    avg_ratings = data.groupby('product_id')['rating'].mean().reset_index()
    avg_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)
    return avg_ratings

avg_ratings = aggregate_data(data)

def feature_engineering(data):
    """
    Create new features for the dataset.

    Steps:
    - Add a column for rating-to-sales correlation.

    Args:
        data (DataFrame): Transformed data.

    Returns:
        DataFrame: Data with new features.
    """
    data['rating_to_sales_correlation'] = data['rating'] * data['discount_percentage']
    return data

data = feature_engineering(data)

# --- Step 3: Data Loading ---
# Documentation:
# This step saves the transformed data into a MySQL database for further analysis.
def load_data_to_sql(data, db_name='ecommerce_db'): # Assuming MySQL
    """
    Load the transformed data into a MySQL database.

    Args:
        data (DataFrame): Cleaned and transformed data.
        db_name (str): Name of the MySQL database.

    Returns:
        Engine: SQLAlchemy engine for database connection.
    """
    engine = create_engine(f'mysql+pymysql://<username>:<password>@localhost/{db_name}')
    data.to_sql('amazon_data', engine, if_exists='replace', index=False)
    return engine

# Use your MySQL credentials
engine = load_data_to_sql(data)

# --- Step 4: Reporting and Visualization ---
# Documentation:
# This step generates visualizations to derive insights from the data.
def generate_visualizations(data):
    """
    Generate and save visualizations from the dataset.

    Visualizations:
    - Histogram of rating distribution.
    - Bar chart of top products by average rating.

    Args:
        data (DataFrame): Transformed data.
    """
    import matplotlib.pyplot as plt

    # Rating distribution
    data['rating'].dropna().plot(kind='hist', bins=10, title='Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.savefig('rating_distribution.png')
    plt.close()

    # Top products by average rating
    top_products = data.groupby('product_id').mean(numeric_only=True).nlargest(10, 'rating')
    top_products['rating'].plot(kind='bar', title='Top Products by Rating')
    plt.xlabel('Product ID')
    plt.ylabel('Average Rating')
    plt.savefig('top_products_by_rating.png')
    plt.close()

generate_visualizations(data)
