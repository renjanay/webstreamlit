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
def create_pie_chart_diskon(df):
    st.subheader("Pie Chart: Relation between Sum of Qty and Diskon")

    filtered_df = df[(df['diskon'] > 0) & (df['diskon'] < 100)]  # Exclude 0% and 100% diskon
    qty_sum = filtered_df['qty'].sum()
    diskon_sum = filtered_df['diskon'].sum()

    labels = ['Qty', 'Diskon']
    sizes = [qty_sum, diskon_sum]
    explode = (0.1, 0)  # Explode the first slice (Qty)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    most_amount_label = labels[sizes.index(max(sizes))]
    ax.annotate(f'Most: {most_amount_label}', xy=(0.5, 0.5), xytext=(0.5, 0.2), fontsize=12,
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.set_title('Relation between Sum of Qty and Diskon')
    st.pyplot(fig)

# Create pie chart for jenis_penjualan
def create_pie_chart_jenis_penjualan(df):
    st.subheader("Pie Chart: Relation between Sum of Quantity and Jenis Penjualan")

    filtered_df = df[df['jenis_penjualan'] != 'giveaway']  # Exclude 'giveaway' jenis_penjualan
    qty_sum_by_jenis = filtered_df.groupby('jenis_penjualan')['qty'].sum()

    labels = qty_sum_by_jenis.index
    sizes = qty_sum_by_jenis.values

    most_amount_index = sizes.argmax()
    explode = [0.1 if i == most_amount_index else 0 for i in range(len(labels))]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, explode=explode)

    most_amount_label = labels[most_amount_index]
    ax.annotate(f'Most: {most_amount_label}', xy=(0.5, 0.5), xytext=(0.5, 0.2), fontsize=12,
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.set_title('Relation between Sum of Quantity and Jenis Penjualan')
    st.pyplot(fig)

def create_dual_bar_chart_qty(df):
    st.subheader("Dual Bar Chart: Sum of Qty1 vs. Qty2 by Month")

    df['tgl_jual'] = pd.to_datetime(df['tgl_jual'])
    df['tgl_prod'] = pd.to_datetime(df['tgl_prod'])

    df['month_jual'] = df['tgl_jual'].dt.month
    df['month_prod'] = df['tgl_prod'].dt.month

    grouped_df = df.groupby(['month_jual'])['qty1'].sum().reset_index().merge(
        df.groupby(['month_prod'])['qty2'].sum().reset_index(),
        how='outer', left_on='month_jual', right_on='month_prod', suffixes=('_jual', '_prod')
    ).fillna(0)

    ax = grouped_df.plot(x='month_jual', kind='bar', stacked=True, figsize=(10, 6))
    ax.set_xlabel('Month')
    ax.set_ylabel('Sum of Quantity')
    ax.set_title('Sum of Qty1 vs. Qty2 by Month')
    ax.legend(title='Quantity Type')

    st.pyplot(plt)

# Create table to show relation between prov, kategori, jenis_barang
def create_relation_table(df):
    st.subheader("Table: Relation between Prov, Kategori, and Jenis Barang")

    relation_df = df.groupby(['prov', 'kategori', 'jenis_barang']).size().reset_index(name='count')
    st.dataframe(relation_df)

def create_dual_bar_chart_qty(df):
    st.subheader("Dual Bar Chart: Sum of Qty1 vs. Qty2 by Month")

    df['tgl_jual'] = pd.to_datetime(df['tgl_jual'])
    df['tgl_prod'] = pd.to_datetime(df['tgl_prod'])

    df['month_jual'] = df['tgl_jual'].dt.month
    df['month_prod'] = df['tgl_prod'].dt.month

    grouped_df = df.groupby(['month_jual'])['qty1'].sum().reset_index().merge(
        df.groupby(['month_prod'])['qty2'].sum().reset_index(),
        how='outer', left_on='month_jual', right_on='month_prod', suffixes=('_jual', '_prod')
    ).fillna(0)

    ax = grouped_df.plot(x='month_jual', kind='bar', stacked=True, figsize=(10, 6))
    ax.set_xlabel('Month')
    ax.set_ylabel('Sum of Quantity')
    ax.set_title('Sum of Qty1 vs. Qty2 by Month')
    ax.legend(title='Quantity Type')

    st.pyplot(plt)

def main():
    st.title("Twinkle Well Data Visualization Dashboard")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        st.dataframe(df.head())  # Display the first few rows of the dataframe

        create_line_chart(df)  # Create the line chart
        create_pie_chart_diskon(df)  # Create the pie chart for diskon
        create_pie_chart_jenis_penjualan(df)  # Create the pie chart for jenis_penjualan
        create_relation_table(df) #C Create table
        create_dual_bar_chart_qty(df)  # Create the dual bar chart for qty1 and qty2


if __name__ == "__main__":
    main()
