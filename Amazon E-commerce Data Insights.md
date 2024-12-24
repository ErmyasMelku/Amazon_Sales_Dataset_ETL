# Insights from the Data
1. Rating Distribution
- What It Shows: The script generates a histogram of the ratings
(rating_distribution.png), showing the distribution of product ratings across the dataset.
This insight helps identify whether most products are highly rated, poorly rated, or evenly distributed.
- Possible Observations:
  - A majority of products may have ratings clustered around a specific range (e.g., 3–5 stars).
  - There may be outliers, such as products with extremely low ratings.

2. Top Products by Average Rating
- What It Shows: The bar chart (top_products_by_rating.png) highlights the top 10 products
with the highest average ratings.
- Possible Observations:
  - Products with the highest customer satisfaction can be identified.
  - Helps in prioritizing top-performing products for marketing campaigns or featuring them on e-commerce platforms.

3. Discount Effectiveness
- What It Shows: The is_discounted and price_difference columns provide insights into the pricing strategy:
  - Products with a greater price difference (price_difference) show the effectiveness of discounts.
  - The rating_to_sales_correlation column helps correlate product ratings with discount percentages.
- Possible Observations:
  - Discounts significantly impact customer interest and satisfaction.
  - Products with steep discounts might generate more positive reviews or higher ratings.

# Data Transformation Insights
1. Cleaned and Standardized Data
- The script standardizes prices (discounted_price, actual_price) by removing special characters
and converting them into numeric values. This ensures uniformity in analysis and calculations.

2. Handling Missing Values
- Missing values in rating_count are replaced with 0, and invalid ratings (N/A) are handled. This avoids data quality issues during analysis.

# Insights for Database Analysis
1. Average Ratings by Product
- The aggregate_data function calculates the average rating for each product, which can be further analyzed for:
  - Identifying consistently high- or low-rated products.
  - Comparing product categories for average customer satisfaction.

2. Correlations Between Discounts and Ratings
- The feature_engineering function creates a rating_to_sales_correlation column, which can provide insights into:
  - How discounts affect ratings.
  - Whether discounted products receive higher or lower ratings compared to non-discounted ones.
