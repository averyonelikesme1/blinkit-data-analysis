#project for data analysis using streamlit and mysql database with analysis of the data using pandas and numpy and visualization using matplotlib and seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os
import streamlit as st
import mysql.connector

#connecting to the database

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jiraiya123",
    database="rajeev"
)

print("Connected Successfully")

cursor = conn.cursor()

#displaying the tables in the database
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("Blinkit Data Analysis Project")
st.write("This project is for data analysis using streamlit and mysql database with analysis of the data using pandas and numpy and visualization using matplotlib and seaborn.")
st.write("The database used in this project is 'BLINKIT' and the tables in the database are:")
for table in tables:
    st.write(table[0])


#fetching the data from the database
cursor.execute(f"SELECT * FROM {tables[0][0]}")
data = cursor.fetchall()
columns1 = [col[0] for col in cursor.description]
print("Fetching successful !!!")

#converting the data into a pandas dataframe
df = pd.DataFrame(data, columns=columns1)
st.write("Data from the database:")
st.dataframe(df.head(5))

st.write('Number of rows =', df.shape[0])
st.write('Number of Columns =', df.shape[1])

#show the information about the data
st.write("Description of the data:")
st.write(df.describe().T)
st.write("Description of the categorical data:")
st.write(df.describe(include="object").T)

#showing the columns and its info in the data in table format
st.write("Columns and its info in the data:")
st.table(df.dtypes)

#showing the null values in the data with percentage of null values in the data
st.write("Null values in the data:")
st.write(df.isnull().sum())



#showing the unique values in the data
st.write("Unique values in the data:")
st.write(df.nunique())


#finding the distribution of numerical columns in the data with analysis
df_num = df.select_dtypes(include= np.number).columns
st.write("Distribution of numerical columns in the data:")
if st.checkbox("Show Histogram"):
    a = 1
    for i in df_num:
        plt.subplot(2,3,a)
        sns.histplot(df[i],kde=True)
        a += 1
    plt.tight_layout()
    st.pyplot(plt)
    st.write("this histogram shows the distribution of numerical columns in the data, we can see that the 'Sales' column is right skewed, which indicates that there are some extreme values in the data. The 'Weight' column is normally distributed, which indicates that the data is balanced. The 'Item_Visibility' column is left skewed, which indicates that there are some extreme values in the data. The 'Item_MRP' column is normally distributed, which indicates that the data is balanced. The 'Outlet_Establishment_Year' column is normally distributed, which indicates that the data is balanced.")





#showing the distribution of categorical columns in the data with analysis
df['Item Fat Content'].replace({'low fat' : 'Low Fat','LF' : 'Low Fat','Regular' : 'Regular Fat','reg': 'Regular Fat'},inplace=True)
st.write("Distribution of categorical columns in the data:")
avg_content = pd.DataFrame(df.groupby('Item Fat Content')['Sales'].mean()).reset_index()
st.write("Average Sales by Item Fat Content:")
if st.checkbox("Show Pie Chart"):
    plt.figure(figsize=(2,2))
    plt.title('Average Sales of Item Fat Content')
    plt.pie(avg_content['Sales'],autopct= '%1.2f%%', labels= [i for i in avg_content['Item Fat Content']])
    st.pyplot(plt)
    st.write("this pie chart shows the average sales of item fat content, we can see that the low fat items have the highest average sales, followed by regular fat items. This indicates that customers prefer low fat items over regular fat items.")

#showing the number of items by type in the data with analysis
fat_nitems = df['Item Type'].value_counts()
fat_nitems = pd.DataFrame(fat_nitems).reset_index()
fat_nitems.columns = ['Item Type', 'Count']
st.write("Number of Items by Type:")
st.write(fat_nitems)


#showing the number of items by type in the data with analysis in a bar chart
plt.figure(figsize=(10,5))
st.write("Bar chart of Number of Items by Type:")
if st.checkbox("Show Bar Chart"):
    sns.barplot(x = 'Item Type', y = 'Count', data = fat_nitems, width=0.6,)
    plt.xticks(rotation=90)
    st.pyplot(plt)
    st.write("this bar chart shows the number of items by type in the data, we can see that the most common item type is 'Fruits and Vegetables', followed by 'Snack Foods' and 'Household'. This indicates that customers prefer to buy fruits and vegetables over other items.")


#finding the distribution of numerical columns in the data with analysis using boxplot
st.write("Distribution of numerical columns in the data using boxplot:")
if st.checkbox("Show Boxplot"):
    plt.figure(figsize=(10,5))
    a = 1
    for i in df_num:
        plt.subplot(3,2,a)
        sns.boxplot(df[i])
        a += 1
    plt.tight_layout()
    st.pyplot(plt)
    st.write("this boxplot shows the distribution of numerical columns in the data, we can see that there are some outliers in the data, especially in the 'Sales' column. This indicates that there are some extreme values in the data that could affect the analysis. We can also see that the median of the 'Sales' column is lower than the mean, which indicates that the distribution is skewed to the right.")


#side panel to access the data analysis project and dropdown to select the table from the database and column to select the column from the table and display the data in a dropdown and display the data in a table format
st.sidebar.title("Data Analysis Project")
st.sidebar.write("Select Column to Display Data:")
column = st.sidebar.selectbox("Select Column", df.columns)


#function to display the data in a table format which shows the table in side panel and display the data in a table format with the column name and the count of the values in the column
def display_data(column):
    st.sidebar.write("Data in the column:")
    st.sidebar.write(df[column].value_counts())
    st.sidebar.write("Count of values in the column:")
    st.sidebar.write(df[column].value_counts().count())

display_data(column)


#conclusion of the data analysis project
st.write("Conclusion:")
st.write("The data analysis reveals important insights about the distribution and patterns in the dataset. The most common item type is 'Fruits and Vegetables', indicating a preference for healthy options among customers. The distribution of sales data shows some skewness, with extreme values that may impact the overall analysis. Further investigation into these outliers is recommended.")
