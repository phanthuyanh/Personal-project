from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data, Style

st.title('Welcome to the new :green[Project Tracker]:heavy_dollar_sign:')
st.markdown('''The tracker wil be now more customized to your project! More interactive options are now  
available per your demand. Find out the following **ways** to check on your project's progress!''')

st.header("PM's space in :bar_chart:**Projects**")


st.subheader("1. Filter your project and adjust the wanted time period")
st.markdown('''Search for your project in "Select your project", then adust the Time period slider to your liking. Seeing only the previous fiscal month is also possible''')

 
st.subheader("2. Some familiar checkings on your projects")
st.markdown('''**a. Total SUM checkbox**:  Check the box to see the total sum of spendings. Remember to uncheck to get the amount spread out per fiscal month  

**b. Viewing by on the sidebar**''')  

st.markdown(''':star2:***Spends over time***: Uncheck the Total SUM check box before select this to see the spendings per month''')
   
st.markdown(''':star2:***Spends per supplier***: Select to see total spendings per suppliers''')
   
st.markdown(''':star2:***PO numbers by suppliers***: Select to see if all POs of your supplier(s) are already in yet''')
   
st.markdown(':star2:***PO numbers by month***: Good to check which period arrive in the last period')


st.subheader("3. Adjust expenditure type and your project status")
st.markdown('''Filtering for CAPEX or OPEX spends for cleaner checking per each spending category compared to project's budget. In case your project is componentized, ensure to adjust the status for Open only''')



st.header("Feel free to visit	:nerd_face:**Controlling**")
st.markdown('''This page is specifically for potential checking for reclass. Feel free to visit if you also have to work with the Chart of accounts too!''')