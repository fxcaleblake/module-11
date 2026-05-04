 # Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022','Q2 2022','Q3 2022','Q4 2022','Q1 2023','Q2 2023','Q3 2023','Q4 2023']
locations = ['Tampa','Miami','Orlando','Jacksonville']
categories = ['Electronics','Clothing','Home Goods','Sporting Goods','Beauty']

quarterly_data=[]
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(100000, 20000)
            seasonal_factor = 1.3 if quarter.quarter==4 else (0.8 if quarter.quarter==1 else 1.0)
            location_factor = {'Tampa':1.0,'Miami':1.2,'Orlando':0.9,'Jacksonville':0.8}[location]
            category_factor = {'Electronics':1.5,'Clothing':1.0,'Home Goods':0.8,'Sporting Goods':0.7,'Beauty':0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx

            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(1.0, 0.1)

            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(1.0, 0.2)

            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data=[]
total_customers=2000
age_params={'Tampa':(45,15),'Miami':(35,12),'Orlando':(38,14),'Jacksonville':(42,13)}

for location in locations:
    mean_age,std_age=age_params[location]
    customer_count=int(total_customers*{'Tampa':0.3,'Miami':0.35,'Orlando':0.2,'Jacksonville':0.15}[location])
    ages=np.clip(np.random.normal(mean_age,std_age,customer_count),18,80).astype(int)

    for age in ages:
        base_amount=np.random.gamma(5,20)
        price_tier=np.random.choice(['Budget','Mid-range','Premium'],p=[0.3,0.5,0.2])
        tier_factor={'Budget':0.7,'Mid-range':1.0,'Premium':1.8}[price_tier]

        customer_data.append({
            'Location':location,
            'Age':age,
            'PurchaseAmount':round(base_amount*tier_factor,2),
            'PriceTier':price_tier
        })

sales_df=pd.DataFrame(quarterly_data)
customer_df=pd.DataFrame(customer_data)
sales_df['SalesPerDollarSpent']=sales_df['Sales']/sales_df['AdSpend']

# ============================================================
# TODO 1: TIME SERIES VISUALIZATION
# ============================================================

def plot_quarterly_sales_trend():
    fig, ax = plt.subplots()
    data = sales_df.groupby('QuarterLabel')['Sales'].sum()
    ax.plot(data.index, data.values, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    plt.xticks(rotation=45)
    ax.grid()
    return fig

def plot_location_sales_comparison():
    fig, ax = plt.subplots()
    data = sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack()
    for loc in data.columns:
        ax.plot(data.index, data[loc], marker='o', label=loc)
    ax.legend()
    ax.set_title("Sales by Location")
    plt.xticks(rotation=45)
    ax.grid()
    return fig

# ============================================================
# TODO 2: CATEGORICAL COMPARISON
# ============================================================

def plot_category_performance_by_location():
    latest = sales_df['QuarterLabel'].iloc[-1]
    data = sales_df[sales_df['QuarterLabel']==latest]
    pivot = data.pivot_table(index='Category',columns='Location',values='Sales',aggfunc='sum')
    fig, ax = plt.subplots()
    pivot.plot(kind='bar', ax=ax)
    ax.set_title(f"Category Performance ({latest})")
    return fig

def plot_sales_composition_by_location():
    pivot = sales_df.pivot_table(index='Location',columns='Category',values='Sales',aggfunc='sum')
    percent = pivot.div(pivot.sum(axis=1), axis=0)
    fig, ax = plt.subplots()
    percent.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Sales Composition by Location")
    return fig

# ============================================================
# TODO 3: RELATIONSHIP ANALYSIS
# ============================================================

def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'])
    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    ax.plot(sales_df['AdSpend'], m*sales_df['AdSpend']+b)
    ax.set_title("Ad Spend vs Sales")
    return fig

def plot_ad_efficiency_over_time():
    data = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    fig, ax = plt.subplots()
    ax.plot(data.index, data.values, marker='o')
    ax.set_title("Ad Efficiency Over Time")
    plt.xticks(rotation=45)
    return fig

# ============================================================
# TODO 4: DISTRIBUTION ANALYSIS
# ============================================================

def plot_customer_age_distribution():
    fig, axes = plt.subplots(2,2,figsize=(10,8))
    axes = axes.flatten()
    for i, loc in enumerate(locations):
        data = customer_df[customer_df['Location']==loc]['Age']
        axes[i].hist(data, bins=15)
        axes[i].axvline(data.mean(), linestyle='dashed')
        axes[i].axvline(data.median())
        axes[i].set_title(loc)
    return fig

def plot_purchase_by_age_group():
    bins=[18,30,45,60,80]
    labels=['18-30','31-45','46-60','61+']
    customer_df['AgeGroup']=pd.cut(customer_df['Age'], bins=bins, labels=labels)
    data=[customer_df[customer_df['AgeGroup']==l]['PurchaseAmount'] for l in labels]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("Purchase by Age Group")
    return fig

# ============================================================
# TODO 5: SALES DISTRIBUTION
# ============================================================

def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'], bins=20)
    ax.set_title("Purchase Amount Distribution")
    return fig

def plot_sales_by_price_tier():
    totals = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    explode = [0.1 if v==totals.max() else 0 for v in totals]
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%', explode=explode)
    ax.set_title("Sales by Price Tier")
    return fig

# ============================================================
# TODO 6: MARKET SHARE ANALYSIS
# ============================================================

def plot_category_market_share():
    totals = sales_df.groupby('Category')['Sales'].sum()
    explode = [0.1 if v==totals.max() else 0 for v in totals]
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%', explode=explode)
    ax.set_title("Category Market Share")
    return fig

def plot_location_sales_distribution():
    totals = sales_df.groupby('Location')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%')
    ax.set_title("Location Sales Distribution")
    return fig

# ============================================================
# TODO 7: DASHBOARD
# ============================================================

def create_business_dashboard():
    fig, axes = plt.subplots(2,2,figsize=(12,10))
    sales_df.groupby('QuarterLabel')['Sales'].sum().plot(ax=axes[0,0],title="Sales Trend")
    sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack().plot(ax=axes[0,1],title="Location Comparison")
    axes[1,0].scatter(sales_df['AdSpend'],sales_df['Sales'])
    axes[1,0].set_title("Ad vs Sales")
    customer_df.groupby('PriceTier')['PurchaseAmount'].sum().plot(kind='pie',ax=axes[1,1],autopct='%1.1f%%')
    plt.tight_layout()
    return fig

# ============================================================
# MAIN
# ============================================================

def main():
    plot_quarterly_sales_trend()
    plot_location_sales_comparison()
    plot_category_performance_by_location()
    plot_sales_composition_by_location()
    plot_ad_spend_vs_sales()
    plot_ad_efficiency_over_time()
    plot_customer_age_distribution()
    plot_purchase_by_age_group()
    plot_purchase_amount_distribution()
    plot_sales_by_price_tier()
    plot_category_market_share()
    plot_location_sales_distribution()
    create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales increase over time with strong Q4 spikes")
    print("- Miami performs best; Jacksonville lowest")
    print("- Electronics dominate category sales")
    print("- Strong correlation between advertising and sales")
    print("- Mid-range tier generates most revenue")

    plt.show()

if __name__ == "__main__":
    main()