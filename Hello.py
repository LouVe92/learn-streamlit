# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
LOGGER = get_logger(__name__)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Quality", layout="wide")

st.title("Data Quality")
st.markdown("""
            ***Hello!:hand: Welcome to OMNI Classifier Data Quality Dashboard!***
            """)

st.caption('I am currently working with csv file. Link to Azure Blob is still under maintenance.')  
uploaded_file = st.file_uploader('Please upload your csv file below :point_down:', type='csv')
df= pd.read_csv(uploaded_file)

st.header('Prerun Check', divider='gray')
st.markdown(':red[Under maintenance]')

st.header('Data Profiler', divider='gray')
st.markdown("""
            **👈 Select a data level from the sidebar** to filter the data
            """)

level = st.sidebar.selectbox('Select a data level', 
                              options=sorted(df['level'].unique()),
                              index=None)
df_selection = df.query('level == @level')

if level == 'Category':
    sub_level = st.sidebar.selectbox('Select a category name', 
                                  options=sorted(df_selection['category'].unique()),
                                  index=None)
    df_sub_selection = df_selection[df_selection['category'] == sub_level]
elif level == 'Application':
    sub_level = st.sidebar.selectbox('Select an application name', 
                                  options=sorted(df_selection['category'].unique()),
                                  index=None)
    df_sub_selection = df_selection[df_selection['category'] == sub_level]
else:
    df_sub_selection = df_selection

df_sub_selection_size = df_sub_selection[df_sub_selection['name'] =='Size']
df_sub_selection_cnt_msisdn = df_sub_selection[(df_sub_selection['name'] =='CountDistinct') & (df_sub_selection['instance'] =='msisdn')]
df_sub_selection_cnt_session = df_sub_selection[(df_sub_selection['name'] =='CountDistinct') & (df_sub_selection['instance'] =='session')]

metrics = ['Maximum', 'Minimum', 'Mean', 'Sum', 'StandardDeviation', 
           'ApproxQuantiles-0.25', 'ApproxQuantiles-0.5', 'ApproxQuantiles-0.75']
filtered_df = {}
for metric in metrics:
    condition = df_sub_selection[df_sub_selection['name'] == metric]
    if not condition.empty:
      condition = condition.astype(bool)
      filtered_df[metric] = df_sub_selection[condition]
filtered_df_max = filtered_df['Maximum']
filtered_df_min = filtered_df['Minimum']
filtered_df_sum = filtered_df['Sum']
filtered_df_mean = filtered_df['Mean']
filtered_df_sd = filtered_df['StandardDeviation']
filtered_df_q1 = filtered_df['ApproxQuantiles-0.25']
filtered_df_q2 = filtered_df['ApproxQuantiles-0.5']
filtered_df_q3 = filtered_df['ApproxQuantiles-0.75']

if level in ['All', 'Category', 'Application']:
    st.subheader('Size')
    st.markdown(':blue[To analyze the total number of rows in the table]')
    fig, ax = plt.subplots()
    sns.lineplot(data=df_sub_selection_size, x='date', y ='value', ax=ax)
    st.pyplot(fig)

    st.subheader('Count Distinct')
    st.markdown(':blue[To analyze the total distinct number of values in a specific column]')
    st.markdown(':red[msisdn]')
    fig, ax = plt.subplots()
    sns.lineplot(data=df_sub_selection_cnt_msisdn, x='date', y ='value', ax=ax)
    st.pyplot(fig)
    st.markdown(':red[session]')
    fig, ax = plt.subplots()
    sns.lineplot(data=df_sub_selection_cnt_session, x='date', y ='value', ax=ax)
    st.pyplot(fig)

    st.subheader('Metric')
    st.markdown(':blue[To analyze metrics function on the specific column]')

    st.subheader('Completeness')
    st.markdown(':blue[To analyze data completeness in a specific column]')

