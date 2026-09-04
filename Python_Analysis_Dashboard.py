import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

 
# 1: Loading Excel File

file_path = r"C:\Users\PCC\Desktop\Python_Analysis_Dashboard_Complete.xlsx"

# Checking Excel Sheets
excel = pd.ExcelFile(file_path)
print("Sheets:")
print(excel.sheet_names)
 
# Loading Python Data sheet
df = pd.read_excel(file_path, sheet_name="Python Data")
 
 
# =========================================================
# STEP 2: Explore the Dataset
# =========================================================
 
# Showing Columns
print("\nColumns:")
print(df.columns.tolist())
 
# Showing First 5 Rows
print("\nFirst 5 Rows:")
print(df.head())
 
# Showing Last 5 Rows
print("\nLast 5 Rows:")
print(df.tail())
 
# Finding Dataset Shape (rows, columns)
print("\nShape:")
print(df.shape)
 
# Finding Data Types
print("\nData Types:")
print(df.dtypes)
 
# Finding Descriptive Statistics (mean, min, max, etc.)
print("\nDescriptive Statistics:")
print(df.describe())
 
 
# =========================================================
# STEP 3: Data Quality Checks (and fixing issues, not just finding them)
# =========================================================
 
# Finding Missing Values per column
print("\nMissing Values per Column:")
print(df.isnull().sum())
 
# Finding Total Missing Values in the whole dataset
print("\nTotal Missing Values:")
print(df.isnull().sum().sum())
 
# Fixing missing values instead of just reporting them
                                
print("\nMissing values after cleaning:")
print(df.isnull().sum().sum())
 
# Finding Duplicate Rows
print("\nDuplicate Rows Found:")
print(df.duplicated().sum())
 
# Removing duplicate rows (keep the first occurrence)
df = df.drop_duplicates()
print("Shape after removing duplicates:", df.shape)
 
 
# =========================================================
# STEP 4: Reusable function for saving/plotting charts
# =========================================================
# Instead of repeating the same 6 lines of plotting code for every chart,
# this function does it once and can be reused for every chart below.
 
def plot_and_save(data, kind, title, xlabel, ylabel, filename, rotation=45, marker=None):
    
    plt.figure(figsize=(10, 6))
    if kind == "line":
        data.plot(kind=kind, marker=marker)
        plt.grid(True)
    else:
        data.plot(kind=kind)
 
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.savefig(filename)   # saves chart as an image file for reports/presentations
    plt.show()
 
 
# =========================================================
# STEP 5: Category, Quarter, and Status Analysis
# =========================================================
 
# Finding Category-wise Achievement
category_performance = df.groupby("Category")["Achievement"].sum()
print("\nCategory-wise Achievement:")
print(category_performance)
 
# Finding Quarter-wise Achievement
quarter_performance = df.groupby("Quarter")["Achievement"].sum()
print("\nQuarter-wise Achievement:")
print(quarter_performance)
 
# Finding Status Count (how many activities are Completed / Pending / etc.)
status_count = df["Status"].value_counts()
print("\nStatus Count:")
print(status_count)
 
 
# =========================================================
# STEP 6: District-wise Target vs Achievement Analysis
# =========================================================
 
district_analysis = df.groupby("District").agg({
    "Target": "sum",
    "Achievement": "sum"
})
 
# Calculating Achievement Percentage = (Achievement / Target) * 100
district_analysis["Achievement_Percentage"] = (
    district_analysis["Achievement"] / district_analysis["Target"]
) * 100
 
print("\nDistrict-wise Analysis (sorted by Achievement %):")
print(district_analysis.sort_values("Achievement_Percentage", ascending=False))
 
# Finding Best Performing District
best_district = district_analysis["Achievement_Percentage"].idxmax()
best_value = district_analysis["Achievement_Percentage"].max()
print(f"\nBest District: {best_district} ({round(best_value, 2)}%)")
 
# Finding Lowest Performing District
lowest_district = district_analysis["Achievement_Percentage"].idxmin()
lowest_value = district_analysis["Achievement_Percentage"].min()
print(f"Lowest District: {lowest_district} ({round(lowest_value, 2)}%)")
 
 
# =========================================================
# STEP 7: Budget Analysis
# =========================================================
 
# Finding Total Budget Allocated and Utilized
total_allocated = df["Budget_Allocated_PKR"].sum()
total_utilized = df["Budget_Utilized_PKR"].sum()
 
print("\nTotal Budget Allocated:", total_allocated)
print("Total Budget Utilized:", total_utilized)
 
# Finding District-wise Budget
district_budget = df.groupby("District").agg({
    "Budget_Allocated_PKR": "sum",
    "Budget_Utilized_PKR": "sum"
})
 
# Calculating Budget Utilization Percentage
district_budget["Budget_Utilization_Percentage"] = (
    district_budget["Budget_Utilized_PKR"] / district_budget["Budget_Allocated_PKR"]
) * 100
 
print("\nDistrict-wise Budget Analysis:")
print(district_budget)
 
 
# =========================================================
# STEP 8: Extra insight — does more budget mean better achievement?
# =========================================================
# This checks correlation between Budget Utilized and Achievement.
# A value close to +1 means "more budget used -> more achievement".
# A value close to 0 means there isn't a strong relationship.
 
correlation = df["Budget_Utilized_PKR"].corr(df["Achievement"])
print(f"\nCorrelation between Budget Utilized and Achievement: {round(correlation, 2)}")
 
 
# =========================================================
# STEP 9: Visualizations (all charts are displayed AND saved as PNG files)
# =========================================================
 
# Chart 1: District-wise Achievement
district_performance = df.groupby("District")["Achievement"].sum()
plot_and_save(
    district_performance, "bar",
    "District-wise Achievement", "District", "Total Achievement",
    "chart1_district_achievement.png"
)
 
# Chart 2: Category-wise Achievement
plot_and_save(
    category_performance, "bar",
    "Category-wise Achievement", "Category", "Total Achievement",
    "chart2_category_achievement.png", rotation=30
)
 
# Chart 3: Quarterly Achievement Trend
plot_and_save(
    quarter_performance, "line",
    "Quarterly Achievement Trend", "Quarter", "Total Achievement",
    "chart3_quarterly_trend.png", marker="o"
)
 
# Chart 4: Budget Allocated vs Utilized
budget_series = pd.Series(
    [total_allocated, total_utilized],
    index=["Allocated", "Utilized"]
)
plot_and_save(
    budget_series, "bar",
    "Budget Allocated vs Utilized", "", "Amount (PKR)",
    "chart4_budget_comparison.png", rotation=0
)
 
# Chart 5: Activity Status Distribution
plot_and_save(
    status_count, "bar",
    "Activity Status Distribution", "Status", "Number of Activities",
    "chart5_status_distribution.png", rotation=30
)
 
# Chart 6: District-wise Budget Utilization
district_utilization = district_budget["Budget_Utilization_Percentage"].sort_values(ascending=False)
plot_and_save(
    district_utilization, "bar",
    "District-wise Budget Utilization", "District", "Budget Utilization %",
    "chart6_budget_utilization.png"
)
 
print("\nAll charts saved successfully in the project folder.")
 






