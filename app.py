!pip install plotly

import pandas as pd
import numpy as np
import plotly.express as px 
import streamlit as st


st.set_page_config(page_title="Covid Health Alert Dashboard", page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )


# import xlsx data

def get_messages():
    # import csv data
    df = pd.read_csv('messages.csv', header=0,sep=';')
    df["inserted_at"] = pd.to_datetime(df["inserted_at"])
    return df

df_m = get_messages()


def get_chats():
    # import csv data
    df = pd.read_csv('chats.csv', header=0,sep=';')
    df["inserted_at"] = pd.to_datetime(df["inserted_at"])
    return df

df_c = get_chats()


# ---- MAINPAGE ----
st.title(":bar_chart: Covid Health Stats Dashboard")
st.markdown("##")




# Top KPI's

# count unique users
unique_users = len(np.unique(df_c['id']))
Inbound_mes = df_m[df_m['direction'] == 'inbound']['direction'].count()

left_column, right_column = st.columns(2)


with left_column:
    st.subheader("Total No. Unique Users")
    st.subheader(f"{unique_users:,}")

with right_column:
    st.subheader("Total number of Inbound messages")
    st.subheader(f"{Inbound_mes:,}")
    
st.markdown("---")



# ---- Add Graph ---------#

df_inbound = df_m.loc[df_m['direction'] == 'inbound']
df_outbound = df_m.loc[df_m['direction'] == 'outbound']
df_inbound_tot = df_inbound.set_index('inserted_at').resample('w-mon', label='left').count().reset_index()
df_outbound_tot = df_outbound.set_index('inserted_at').resample('w-mon', label='left').count().reset_index()
message_bound_tot = pd.concat([df_outbound_tot.iloc[:,[0,3]], df_inbound_tot.iloc[:,3]], axis=1)
message_bound_tot.columns = ['Week', 'Outbound', 'Inbound']

fig = px.bar(message_bound_tot, x='Week', y=['Outbound', 'Inbound'], barmode='group', title='Weekly Inbound and Outbound messages')
fig.update_layout(legend_title_text='Message Direction') 
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    hoverformat="%b %d, %Y",
    ticklabelmode="period",
    title_text='Date')



st.plotly_chart(fig)

# ----Return Users Graph  ----

st.markdown("---")

# determine Users that returned, a unique user count greater than 1
df_return = df_m.groupby('chat_id')['message_id'].nunique().reset_index(name='count')
df_return = df_return[df_return['count'] > 1]
# Compare this list of users that returned, to the complete list of users (found that only 3 users never returned)
df_m['returning'] = np.where(df_m['chat_id'].isin(df_return['chat_id']), 'yes', 'no')
df_m_yes = df_m[df_m['returning'] == 'yes']
#Resample to weekly users counts
df_return = df_m_yes.set_index('inserted_at').resample('W-mon', label='left').nunique().reset_index()
df_return = df_return.iloc[:,[0,2]]
# Get total weekly users
df_total = df_m.set_index('inserted_at').resample('W-mon', label='left').nunique().reset_index()
df_total= df_total.iloc[:,[0,2]]
df_total = pd.concat([df_total, df_return.iloc[:,1]], axis=1)
df_total.columns = ['Week', 'Total', 'Returning']
#Plot Graph
fig = px.bar(df_total, x='Week', y=['Total', 'Returning'], barmode='group', title='Weekly Returning and Total Users')
fig.update_layout(legend_title_text='Users') 
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    hoverformat="%b %d, %Y",
    ticklabelmode="period",
    title_text='Date')
    
st.plotly_chart(fig)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
