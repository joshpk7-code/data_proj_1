import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to Northwind database

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="Northwind",
    user="postgres",
    password="7701"
)

# Pulling sales data from the database

query = """
    SELECT 
        o.order_id,
        o.order_date,
        od.unit_price,
        od.quantity,
        od.discount,
        p.product_name,
        c.category_name
    FROM orders o
    JOIN order_details od 
         ON o.order_id = od.order_id
    JOIN products p 
         ON od.product_id = p.product_id
    JOIN categories c 
         ON p.category_id = c.category_id
"""

df = pd.read_sql(query, conn)

print(f"Total rows: {len(df)}")
print(df.head())

### Analyses
## Total Revenue
df["revenue"] = df["unit_price"] * df["quantity"] *(1 - df["discount"])

# Analysis 1 - Revenue by Category
cat_rev = df.groupby("category_name")["revenue"].sum().sort_values(ascending=False)

print("\n--- Revenue by Category ---")
print(cat_rev)

# Plot
plt.figure(figsize=(10,6))
cat_rev.plot(kind="bar", color="steelblue")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("revenue_by_category.png")
plt.show()

## Analysis 2 - Top 10 best-selling products
prod_rev = df.groupby("product_name")["revenue"].sum().sort_values(ascending=False).head(10)

print("\n--- Top 10 Best Selling Products ---")
print(prod_rev)

plt.figure(figsize=(10,6))
prod_rev.plot(kind="bar", color="green")
plt.title("Top 10 Best Selling Products")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("rev_by_prod")
plt.show()

## Analysis 3 - Monthly Sales Trend
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M")

monthly_revenue = df.groupby("month")["revenue"].sum()

print("\n--- Monthly Sales Trend ---")
print(monthly_revenue)

# Plot it
plt.figure(figsize=(14, 6))
monthly_revenue.plot(kind="line", color="green", linewidth=2, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("monthly_sales_trend.png")
plt.show()
