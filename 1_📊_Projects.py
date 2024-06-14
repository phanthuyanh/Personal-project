from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

from streamlit_vizzu import VizzuChart
st.title("For Project Managers")

data_frame = pd.read_csv("first3.csv", dtype={"Month": str, "Invoice":str})

data = Data()
data.add_df(data_frame)

chart = VizzuChart(key="vizzu", width = "100%", height=700)
chart.animate(data)
chart.feature("tooltip", True)
chart.scroll_into_view = True

#SIDE BAR OPTIONS
with st.sidebar:
    col1, col2 = st.columns(2)

    expenditure = col1.radio("Expenditure Type", ["Capex", "Opex", "Total"])
    status = col2.radio("Status", ["Open", "Closed", "All"])
    po = st.radio("Viewing by", ["Spends over time", "PO numbers by month","Spends per supplier", "PO numbers by supplier"])
    inspection = st.checkbox("PO and invoice inspection", disabled = po!="PO numbers by month")
    st.write('<p class="small-font">Additional options</p>', unsafe_allow_html=True)

#SIDEBAR FILTERS 
if expenditure != "Total":
    filter_expenditure = f"record['Account Category'] == '{expenditure}'"
else:
    filter_expenditure = ""

if status != "All":
    filter_status = f"record['Status'] == '{status}'"
else:
    filter_status = ""

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

#GENERAL BUDGET CHECKING
total = st.checkbox("Total SUM", disabled = po!="Spends over time", value = True)

##Dynamic title
if month1 == month2:
    title = f"Project's {expenditure} spending for month {month1}"
else:
    title = f"Project's {expenditure} spending from month {month1} to {month2}"

#CONCAT FILTER
filters = [filter_time]
if filter_format:
    filters.append(filter_format)
if filter_expenditure:
    filters.append(filter_expenditure)
if filter_status:
    filters.append(filter_status)

combined_filter = " && ".join(filters)
#if filter_format == None:
    #filter = filter_time
#else:
    #filter = " && ".join([filter_time, filter_format])

if po !=  "Spends over time" and inspection:
    x =  ["Invoice", "Amount"]
    y = "PO Number"
    color = "Invoice"
elif po == "PO numbers by month" and inspection == False:
    x = "Month"
    y = ["PO Number", "Amount"]
    color = "PO Number"
elif po == "PO numbers by supplier": 
    x = ["PO Number", "Amount"]
    y = "Supplier"
    color = "PO Number"
elif po == "Spends per supplier":
    x = "Amount"
    y = "Supplier"
    color = None
else: 
    x = "Month"
    y = "Amount"
    color = None

if total:
    config = {"title": title, "y": "Amount", "x": "Project ID"}
    chart.feature("tooltip", True)
else: 
    config = {"title": title, "y": y, "x": x, "color": color}

#config = {"title": title, "y": "Amount", "x": "Month"}

chart.feature("tooltip", True)
if combined_filter:
    chart.animate(data.filter(combined_filter), Config(config), delay=0, duration=0.7)
    chart.animate(Style({"title": {"fontSize": 30}})) 
else:
    chart.animate(data, Config(config), delay=0, duration=0.7)
    chart.animate(Style({"title": {"fontSize": 30}}))

#chart.animate(data.filter(filter), Config(config), delay=0, duration=0.7)
chart.show()




