import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Load data from Excel
def load_data(uploaded_file):
    data = io.BytesIO(uploaded_file.read())
    df = pd.read_excel(data)
    return df

# Create line chart with annotations
def create_line_chart(df):
    st.subheader("Line Chart: Relation between Bulan and Pend_Total")

    # Convert the "bulan" column to string type
    df['bulan'] = df['bulan'].astype(str)
    
    fig, ax = plt.subplots()
    ax.plot(df['bulan'], df['pend_total'], marker='o', linestyle='-', color='b', label='Pend_Total')
    
    max_index = df['pend_total'].idxmax()
    min_index = df['pend_total'].idxmin()
    
    max_value = df.loc[max_index, 'pend_total']
    min_value = df.loc[min_index, 'pend_total']
    
    ax.annotate(f'Highest: {max_value}', xy=(max_index, max_value), xytext=(max_index, max_value + 500),
                arrowprops=dict(facecolor='black', shrink=0.05),)
    
    ax.annotate(f'Lowest: {min_value}', xy=(min_index, min_value), xytext=(min_index, min_value - 500),
                arrowprops=dict(facecolor='black', shrink=0.05),)
    
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Pend_Total')
    ax.set_title('Relation between Bulan and Pend_Total')
    ax.legend()
    
    st.pyplot(fig)

# Create pie chart for diskon
def create_pie_chart(df):
    st.subheader("Pie Chart: Count of Diskon (excluding 0% and 100%)")

    filtered_df = df[(df['diskon'] > 0) & (df['diskon'] < 100)]
    diskon_counts = filtered_df['diskon'].value_counts()

    labels = diskon_counts.index
    sizes = diskon_counts.values

    most_common_diskon = labels[0]
    explode = [0.1 if label == most_common_diskon else 0 for label in labels]

    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot()  # Display the pie chart

def main():
    st.title("Excel Data Visualization Dashboard")
    
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        st.dataframe(df.head())  # Display the first few rows of the dataframe
        
        create_line_chart(df)  # Create the line chart
        create_pie_chart(df)   # Create the pie chart

if __name__ == "__main__":
    main()
