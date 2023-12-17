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
data = pd.read_csv(uploaded_file)

if uploaded_file is not None:
    st.markdown("""
                **👈 Filter your data from the sidebar**
                """)
    
    dates=data['date'].unique().tolist()
    date_selection = st.sidebar.slider('Select date',
                                        min_value=min(dates), max_value=max(dates),
                                        value=(min(dates), max(dates)))
    type_selection = st.sidebar.selectbox('Select a data quality type',
                                           options=sorted(data['tag'].unique()),
                                           index=None)
    filtered_all = data[(data['date'].between(*date_selection)) & (data['tag'] == type_selection)]
    table_selection = st.sidebar.selectbox('Select a table',
                                         options=sorted(filtered_all['table_name'].unique()),
                                         index=None)
    filtered_all = filtered_all[filtered_all['table_name'] == table_selection]

    level = st.sidebar.selectbox('Select a data level', 
                                  options=sorted(filtered_all['level'].unique()),
                                  index=None)
    df_selection = filtered_all.query('level == @level')

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

    if type_selection == 'pre-run check':
        st.header('Prerun Check', divider='gray')
        st.markdown(':red[Sorry, this tab is still under maintenance]')
    elif type_selection == 'data profiler':
        st.header('Data Profiler', divider='gray')

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

        filtered_df_max = filtered_df.get('Maximum', pd.DataFrame())
        filtered_df_min = filtered_df.get('Minimum', pd.DataFrame())
        filtered_df_sum = filtered_df.get('Mean', pd.DataFrame())
        filtered_df_mean = filtered_df.get('Sum', pd.DataFrame())
        filtered_df_sd = filtered_df.get('StandardDeviation', pd.DataFrame())
        filtered_df_q1 = filtered_df.get('ApproxQuantiles-0.25', pd.DataFrame())
        filtered_df_q2 = filtered_df.get('ApproxQuantiles-0.5', pd.DataFrame())
        filtered_df_q3 = filtered_df.get('ApproxQuantiles-0.75', pd.DataFrame())

        if level == 'All' or level in ['Category', 'Application'] and sub_level is not None:
            st.subheader('Size')
            st.markdown(':blue[To analyze the total number of rows in the table]')
            fig1, ax1 = plt.subplots(figsize=(10,5))
            sns.lineplot(data=df_sub_selection_size, x='date', y ='value', markersize=6, marker = "o", ax=ax1)
            st.pyplot(fig1)

            st.subheader('Count Distinct')
            st.markdown(':blue[To analyze the total distinct number of values in a specific column]')
            col9, col10 = st.columns(2)
            with col9:
                st.markdown(':red[msisdn]')
                fig2, ax2 = plt.subplots(figsize=(10,5))
                sns.lineplot(data=df_sub_selection_cnt_msisdn, x='date', y ='value', markersize=6, marker = "o", ax=ax2)
                st.pyplot(fig2)
            with col10:   
                st.markdown(':red[session]')
                fig3, ax3 = plt.subplots(figsize=(10,5))
                sns.lineplot(data=df_sub_selection_cnt_session, x='date', y ='value', markersize=6, marker = "o", ax=ax3)
                st.pyplot(fig3)

            st.subheader('Metric')
            st.markdown(':blue[To analyze metrics function on the specific column]')

            df_sub_selection_column_metric = df_sub_selection[df_sub_selection['name'].isin(metrics)]
            metric_selection = st.selectbox('Select a column name below 👇', 
                                             options= sorted(df_sub_selection_column_metric['instance'].unique()),
                                             index=None)

            if metric_selection is not None:
                filtered_df_max = filtered_df_max[filtered_df_max['instance'] == metric_selection]
                filtered_df_min = filtered_df_min[filtered_df_min['instance'] == metric_selection]
                filtered_df_sum = filtered_df_sum[filtered_df_sum['instance'] == metric_selection]
                filtered_df_mean = filtered_df_mean[filtered_df_mean['instance'] == metric_selection]
                filtered_df_sd = filtered_df_sd[filtered_df_sd['instance'] == metric_selection]
                filtered_df_q1 = filtered_df_q1[filtered_df_q1['instance'] == metric_selection]
                filtered_df_q2 = filtered_df_q2[filtered_df_q2['instance'] == metric_selection]
                filtered_df_q3 = filtered_df_q3[filtered_df_q3['instance'] == metric_selection]

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    fig4, ax4 = plt.subplots(figsize=(10,10))
                    #ax4 = sns.lineplot(data=filtered_df_max, x='date', y ='value', markersize=6, marker = "o", ax=ax4)
                    #ax4.set_xticks(filtered_df_max['date'].unique())
                    #fig4.text(s="Maximum",size=40,fontweight="bold",fontname="monospace",y=0.91,x=0.2,alpha=0.8)
                    st.markdown(':red[Maximum]')
                    sns.lineplot(data=filtered_df_max, x='date', y ='value', markersize=6, marker = "o", ax=ax4)
                    st.pyplot(fig4)

                with col2:
                    st.markdown(':red[Minimum]')
                    fig5, ax5 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_min, x='date', y ='value', markersize=6, marker = "o", ax=ax5)
                    st.pyplot(fig5)

                with col3:
                    st.markdown(':red[Sum]')
                    fig6, ax6 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_sum, x='date', y ='value', markersize=6, marker = "o", ax=ax6)
                    st.pyplot(fig6)

                with col4:
                    st.markdown(':red[Mean]')
                    fig7, ax7 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_mean, x='date', y ='value', markersize=6, marker = "o", ax=ax7)
                    st.pyplot(fig7)

                col5, col6, col7, col8 = st.columns(4)
                with col5:
                    st.markdown(':red[Standard Deviation]')
                    fig8, ax8 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_sd, x='date', y ='value', markersize=6, marker = "o", ax=ax8)
                    st.pyplot(fig8)

                with col6:
                    st.markdown(':red[Quantiles1]')
                    fig9, ax9 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_q1, x='date', y ='value', markersize=6, marker = "o", ax=ax9)
                    st.pyplot(fig9)

                with col7:
                    st.markdown(':red[Quantiles2]')
                    fig10, ax10 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_q2, x='date', y ='value', markersize=6, marker = "o", ax=ax10)
                    st.pyplot(fig10)

                with col8:
                    st.markdown(':red[Quantiles3]')
                    fig11, ax11 = plt.subplots(figsize=(10,10))
                    sns.lineplot(data=filtered_df_q3, x='date', y ='value', markersize=6, marker = "o", ax=ax11)
                    st.pyplot(fig11)

            st.subheader('Completeness')
            st.markdown(':blue[To analyze data completeness in a specific column]')

            df_sub_selection_column_complete = df_sub_selection[df_sub_selection['name'] == 'Completeness']
            complete_selection = st.selectbox('Select a column name below 👇', 
                                             options= sorted(df_sub_selection_column_complete['instance'].unique()),
                                             index=None)
            
            if complete_selection is not None:
                filtered_df_complete = df_sub_selection_column_complete[df_sub_selection_column_complete['instance'] == complete_selection]
                st.markdown(':red[Completeness]')
                fig12, ax12 = plt.subplots(figsize=(10,5))
                sns.lineplot(data=filtered_df_complete, x='date', y ='value', markersize=6, marker = "o", ax=ax12)
                st.pyplot(fig12)

        
        