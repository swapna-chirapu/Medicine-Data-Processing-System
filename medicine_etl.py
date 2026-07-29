import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ---------------------------
# EXTRACT
# ---------------------------
df = pd.read_csv("medicine_data.csv")
print("Original Data:\n", df)

# ---------------------------
# TRANSFORM
# ---------------------------
# Remove extra spaces in column names
df.columns = df.columns.str.strip()

# Convert date column
df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'])

# Remove expired medicines
df = df[df['Expiry_Date'] > pd.Timestamp.today()]

# Create new column
df['Total_Value'] = df['Price'] * df['Stock']

print("\nCleaned Data:\n", df)

# ---------------------------
# LOAD
# ---------------------------
conn = sqlite3.connect("medicine.db")
df.to_sql("medicines", conn, if_exists="replace", index=False)

print("\nData loaded into database!")

# ---------------------------
# ANALYSIS
# ---------------------------
query = "SELECT Category, SUM(Total_Value) as Total FROM medicines GROUP BY Category"
result = pd.read_sql(query, conn)

print("\nAnalysis:\n", result)

# ---------------------------
# VISUALIZATION
# ---------------------------
plt.bar(result['Category'], result['Total'])
plt.xlabel("Category")
plt.ylabel("Total Value")
plt.title("Medicine Analysis")
plt.show()

conn.close()