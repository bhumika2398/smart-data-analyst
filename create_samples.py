import pandas as pd

# Dataset 1 — Indian Sales
data1 = {
    'product': ['Laptop','Phone','Tablet','Laptop','Phone','Tablet','Laptop','Phone','Tablet','Laptop','Phone','Tablet'],
    'city': ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Pune','Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Pune'],
    'quarter': ['Q1','Q1','Q1','Q2','Q2','Q2','Q3','Q3','Q3','Q4','Q4','Q4'],
    'revenue': [120000,85000,45000,135000,92000,48000,118000,88000,52000,142000,95000,55000],
    'units_sold': [12,34,15,14,37,16,11,35,17,15,38,18]
}
pd.DataFrame(data1).to_csv('data/samples/indian_sales.csv', index=False)
print('indian_sales.csv created')

# Dataset 2 — HR Analytics
data2 = {
    'employee_id': list(range(1,13)),
    'department': ['Engineering','Marketing','Sales','HR','Engineering','Marketing','Sales','HR','Engineering','Marketing','Sales','HR'],
    'city': ['Bangalore','Mumbai','Delhi','Pune','Hyderabad','Chennai','Bangalore','Mumbai','Delhi','Pune','Hyderabad','Chennai'],
    'salary': [95000,65000,72000,55000,105000,68000,78000,52000,112000,71000,82000,58000],
    'performance_rating': [4,3,4,3,5,4,3,4,5,3,4,3],
    'years_experience': [3,2,4,1,5,3,4,2,6,3,5,2]
}
pd.DataFrame(data2).to_csv('data/samples/hr_analytics.csv', index=False)
print('hr_analytics.csv created')

# Dataset 3 — Ecommerce Orders
data3 = {
    'order_id': list(range(1001,1013)),
    'category': ['Electronics','Fashion','Grocery','Electronics','Fashion','Grocery','Electronics','Fashion','Grocery','Electronics','Fashion','Grocery'],
    'city': ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Pune','Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Pune'],
    'payment_method': ['UPI','Card','COD','UPI','Card','COD','UPI','Card','COD','UPI','Card','COD'],
    'order_value': [8500,2300,1200,9200,3100,980,7800,2800,1450,10200,3400,1100],
    'delivery_days': [2,3,1,2,4,1,3,2,1,2,3,1]
}
pd.DataFrame(data3).to_csv('data/samples/ecommerce_orders.csv', index=False)
print('ecommerce_orders.csv created')

print('All 3 sample datasets created successfully!')