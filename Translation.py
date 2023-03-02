

#%%
# pipreqs .
# This will create requirements.txt file at the current directory.


from googletrans import Translator
import pandas as pd
import time
import streamlit_ext as ste
import datetime

from deep_translator import GoogleTranslator
import sys


import streamlit as st



pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pd.options.mode.chained_assignment = None

now = datetime.datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")



#### FUNCTIONS #####

def translate_to_english(text_list):
    # translator = Translator(service_urls=['translate.google.com'])
    translator = Translator(service_urls=['translate.google.com'],
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)', proxies=None, timeout=None)
    translated_text = []
    count = 0
    for text in text_list:
        try:
            result = translator.translate(text, dest='en').text
            translated_text.append(result)
            count += 1
            if count % 1000 == 0:
                print('time to sleep 5 sec')
                time.sleep(5)
        except Exception as e:
            translated_text.append("Translation failed")
    return translated_text

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

# IMPORTANT FUNCTIONS:
def data_preprocessing(df):
    # Make all column to lower case.
    df.columns = map(str.lower, df.columns)
    if 'keyword' not in df.columns:
        # print('ERROR: PLEASE CHECK IF YOUR DATA CONTAINS keyword COLUMN')
        st.error('Please ensure that your data includes the column **KEYWORD**', icon="🚨")
        sys.exit(1)

    if 'id' not in df.columns:
        df['id'] = range(len(df))
        print('id is added to the data')

    if 'keyword_eng' not in df.columns:
        with st.spinner('**The keywords are in the process of being translated to ENGLISH. Please hold on ...** '):
            df = df[['id', 'keyword']].copy()
            df.dropna(inplace=True)
            # Adding 'digit-' prefix for the rows that contains digits only as GoogleTranslator can not
            # translate digits only.
            df["keyword"] = df["keyword"].apply(lambda x: 'digit-' + x if x.isdigit() else x)
            # print("The keywords are in the process of being translated to ENGLISH. Please hold on ... ")
            my_list = df["keyword"].to_list()
            df["Keyword_eng"] = translate_to_english(my_list)
            # df["keyword_eng"] = df["keyword"].apply(lambda x: GoogleTranslator(source='auto', target='en').translate(x))
            df = df.mask(df.eq('None')).dropna()  # remove NONE that was produced when trying to translate strange
            # characters like :"????"
            # remove the added prefix from the rows
            df["keyword_eng"] = df["keyword_eng"].apply(lambda x: x.replace("digit-", "") if x.startswith("digit-") else x)
            df["keyword"] = df["keyword"].apply(lambda x: x.replace("digit-", "") if x.startswith("digit-") else x)
        st.success('**The translation process is finished.***')

        # st.balloons()
        # st.dataframe(df)




    return df




html_temp = """
<div style="background-color:green;padding:1.5px">
<h1 style="color:white;text-align:center;"> KEYWORDS TRANSLATION APP</h1>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)


# provide a color for buttons.
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)





st.warning("Please ensure that your data includes the column **KEYWORD** :eye-in-speech-bubble: ")
uploaded_file = st.file_uploader("Upload data", type=['csv'])


if uploaded_file is not None:

    keywords_df = pd.read_csv(uploaded_file,encoding='latin-1')

    processed_data = data_preprocessing(keywords_df)
    data_download = convert_df(processed_data)
    ste.download_button("Press to Download", data_download, "translated_data.csv")
