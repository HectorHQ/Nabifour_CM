
import pandas as pd
import streamlit as st
import json
import requests

st.set_page_config('Credit Memos Automation Service Nabifour',
                    page_icon= ':file_folder:',
                    layout= 'wide'
                    )

st.title(':orange[Credit Memos] Automation Service Nabifour:file_folder:')


@st.cache_data
def load_dataframe(file):
    """
    Loads the uploaded file into a Pandas DataFrame.
    """

    file_extension = file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(file)

    elif file_extension == "xlsx":
        df = pd.read_excel(file)

    return df


file_uploaded = st.file_uploader('Please upload the file with the items you want to process.',type=["csv", "xlsx"])

if file_uploaded:
    df = load_dataframe(file_uploaded)
    df['Date'] = df['Date'].astype(str)

    data = df.to_json(orient='records')
    data_json = {'data':data}
    info_json = json.dumps(data_json)
    
    df
    st.write(f'{df.shape[0]} Credit Memos to create')

    submit_applications = st.button('Send Applications')
    if submit_applications:

        cm_webhook = 'https://hook.us1.make.com/5v0d49mwuhyvc20kxh5q78thhhdt2d7r'
        response = requests.post(cm_webhook,data=info_json,headers={'Content-Type': 'application/json'})

        st.text('Review Applications on google sheet below')
        st.text('Review Column "Status" for Failed items and fix them in QBO')
        st.text('Once reviewed and fixed cut and paste the data into tab "Data Processed"')
        cms_logs = 'https://docs.google.com/spreadsheets/d/1ikssSgXY7nBuGtkD9gogeXxB2Vrxn0VfEKg6lpL8Gzw/edit?gid=0#gid=0'
        st.markdown(cms_logs)
