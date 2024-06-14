from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart
st.title("For Controlling Intern")

data_frame = pd.read_csv("first3.csv", dtype={"Month": str, "Invoice":str, "Account Number":str, "Line of Business":str})

data = Data()
data.add_df(data_frame)

chart = VizzuChart(key="vizzu", width = "100%", height=700)
chart.animate(data)
chart.feature("tooltip", True)
chart.scroll_into_view = True

#SIDE BAR OPTIONS
with st.sidebar:
    col1, col2 = st.columns(2)

    action = st.radio("Checking type", ["General checking", "PO inspection"])
    general = col1.radio("Project info", ["Budget", "Legal Entity", "LOB"], disabled = action == "PO inspection")
    expenditure = col2.radio("Expenditure Type", ["Capex", "Opex", "Total spending"])
    st.write('<p class="small-font">Additional options</p>', unsafe_allow_html=True)

#FILTER FOR PROJECT ID 
defaultFormats = ["NL02-08"]
allFormats = defaultFormats + ["NL01-13", "NL01-15"]
items: List[str] = st.multiselect(
    "Select your project", allFormats, defaultFormats, key="multiselect"
)

if items:
    filter_format = " || ".join([f"record['Project ID'] == '{item}'" for item in items])
else:
    filter_format = None


#FILTER FOR TIME
month1, month2 = st.select_slider(
    "Time period", options=map(str, np.arange(1, 13)), value=("1", "12")
)
filter_time = f"record['Month'] >= {month1} && record['Month'] <= {month2}"

#FILTER FOR EXPENDITURE
if expenditure != "Total spending":
    filter_expenditure = f"record['Account Category'] == '{expenditure}'"
else:
    filter_expenditure = ""

#CONCAT FILTER
filters = [filter_time]
if filter_format:
    filters.append(filter_format)
if filter_expenditure:
    filters.append(filter_expenditure)
combined_filter = " && ".join(filters)

#DIMENSIONS FOR GENERAL CHECKING 
if action == "General checking" and general ==  "Legal Entity":
    x =  "Legal Entity"
    y = ["PO Number", "Amount"]
    color = "PO Number"
elif action == "General checking" and general ==  "LOB":
    x =  "Line of Business"
    y = ["PO Number", "Amount"]
    color = "PO Number"
elif action == "General checking" and general == "Budget": 
    x = "Account Category" 
    y = "Amount" 
    color = "Account Category"
else: 
    x = ["Account Number", "Amount"]
    y = "PO Number"
    color = "Account Number"

if month1 != month2:
    if action == "General checking":
        title = f"General checking by project's {general} from month {month1} to {month2}"
    if action == "PO inspection":
        title = f"Accounts where {expenditure} is booked from month {month1} to {month2}"        
elif month1 == month2:
    if action == "General checking":
        title = f"General checking by project's {general} in month {month1}"
    if action == "PO inspection":
        title = f"Accounts where {expenditure} is booked in month {month1}" 
    
else:
    title = f"Accounts where {expenditure} is booked"

config = {"title": title, "y": y, "x": x, "color": color}
chart.animate(data.filter(combined_filter), Config(config), delay=0, duration=0.7)
chart.animate(Style({"title": {"fontSize": 20}}))
chart.show()
