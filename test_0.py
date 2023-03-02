



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

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pd.options.mode.chained_assignment = None

now = datetime.datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

