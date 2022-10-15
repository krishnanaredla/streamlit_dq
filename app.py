import streamlit as st
import pandas as pd
from random import randint
from dataqualityreport import dqr_table, DataQualityReport


faq = '''## Understanding Report

    Data statistics for each column in a Pandas DataFrame. Each column is represented in a separate row. No general cross-column statistics (e.g. correlations) are computed, although there is a specific 'partition' column that has some unique treatments.,
    The fields in the  table are defined below. Many fields have tooltips with additional data available on hover.

 ### Type
    DataType (Pandas DType) of the column,

  ### Card(inality)
    Number of unique non-NULL values in the column. Unique fields (where each non-null entry is distinct) will be denoted by a *.,

   ### % Missing Partition,
    The DataFrame is partitioned by the column name provided in the `missing_by` parameter (`active_date` by default if it exists). <br> A missing % is computed for each partition and rendered as a 1-D heatmap / bar chart.
    Datasets collected from production systems through ETL processes often use [horizontal](https://en.wikipedia.org/wiki/Partition_(database)) partitions as a unit of dataset for adding, updates or removal. Upon ETL failures, often times entire individual partitions can be missing, or a subset of fields will be missing for a portion of the partition.
  ### % Missing Heatmap 
    A subset of table is randomly partitioned and a missing % is computed for each partition and rendered as a 1-D heatmap. This is useful to see correlations between missing values across columns.,

   ### % Missing,
    The % of missing (null) values in the column.,

   ### % Zeros
    % of values that are zero (only valid for numeric columns),

   ### % Negative,
    % of values that are negative,

   ### Box Plot,
    A [boxplot](https://en.wikipedia.org/wiki/Box_plot) is a standardized way of displaying the dataset based on the five-number summary: the minimum, the maximum, the sample median, and the first and third quartiles.,

   ### Robust Histogram,
    A robust [histogram](https://en.wikipedia.org/wiki/Histogram) is an approximate representation of the distribution of numerical data, where outliers have been removed using the IQR (Inter-quantile range) method.
'''

st.set_page_config(page_icon="🔍", page_title="Data Quality")

st.title("Data Quality")

if 'upload_key'not in st.session_state:
    st.session_state.upload_key = str(randint(1000, 100000000))

with st.container():
    uploaded_file = st.file_uploader(label="Upload CSV file", type=["csv"],key=st.session_state.upload_key)

with st.container():
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            delimiter = st.text_input(label="Enter Delimiter", value=",")
        with col2:
            header = int(st.text_input(label="Select Header Row", value="0"))
        df = pd.read_csv(uploaded_file, delimiter=delimiter, header=header)
        sample = df.head(5)
        st.title("Sample Data")
        st.dataframe(sample)
        if st.button("Generate Report"):
            with st.spinner('creating report...'):
                report = dqr_table(df).to_html()
            st.title("Report")
            st.markdown(report, unsafe_allow_html=True)
            st.markdown(faq)
            