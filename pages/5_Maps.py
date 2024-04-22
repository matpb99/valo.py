import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

## General   
def display_card_table(df_data,metric):

    metric_key = translate_dict.get(metric)

    agent, value = df_data["Agent"][0], df_data[metric_key][0]

    text = [str(value) + " {}".format(metric_key), "Most Average {} per Map Played in All VCTs".format(metric_key)]
    title = str(agent).capitalize()

    card_list.append(card(
        title = title,
        text = text,
        image = load_image(agent, "agents"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
                            )
                    )

    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)
  
def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

def return_query(sql_query):
    df = pd.read_sql(sql_query, conn)
    return df

def init_data():
    players_maps_data_df = pd.read_csv("player_data_by_map.csv")
    with open("last_update.txt", "r") as archivo:
        last_update = archivo.read()

    return players_maps_data_df, last_update

def init_conn(df):
    conn = connect(':memory:')
    df.to_sql(name='test_data', con=conn)
    return conn

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

translate_dict = {
    "most_acs" : "ACS",
    "most_adr" : "ADR",
    "most_assists" : "Assists",
    "most_fk" : "FirstKills",
    "most_hs" : "HSRate",
    "most_kast" : "Kast",
    "most_kills" : "Kills",
    "most_rating" : "Rating"
}

card_list = list()

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")

players_maps_data_df, last_update = init_data()

conn = init_conn(players_maps_data_df)

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Compisition By Maps ")

