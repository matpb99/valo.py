import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def init_data():
    players_maps_data_df = pd.read_csv("player_data_by_map.csv")
    last_update = str(players_maps_data_df.sort_values(by="DateStandar", ascending=False  ,ignore_index=True)["DateStandar"][0])
    last_update = last_update.split()[0]

    return players_maps_data_df, last_update

def init_conn(df):
    conn = connect(':memory:')
    df.to_sql(name='test_data', con=conn)
    return conn
        
def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data


def card_function():
    pass

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024] :orange[[Under Developing]]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))

st.title("Placeholder _Countries_")
st.title("Placeholder _Search_")

