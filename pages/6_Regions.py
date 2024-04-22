import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def init_data():
    players_maps_data_df = pd.read_csv("player_data_by_map.csv")
    with open("last_update.txt", "r") as archivo:
        last_update = archivo.read()

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

def draw_region_card_by_metric(metric):

    if metric == "Rating":
        round_value = 4
    else:
        round_value = 2

    sql_query = """SELECT Tournament, ROUND(AVG({}),{}) AS {}
        FROM test_data
        GROUP BY Tournament
        ORDER BY AVG({}) DESC
        LIMIT 3;""".format(metric, round_value, metric, metric)
    
    df_data = pd.read_sql(sql_query, conn)

    region, value = df_data["Tournament"][0], df_data[metric][0]
    text = [str(value) + " {}".format(metric), "Most Average {} per Map Played in All VCTs".format(metric)]
    title = str(region).capitalize()

    card(
        title = title,
        text = text,
        image = load_image(region.replace(":",""), "regions"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
        )
    
    st.subheader("Top 3 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Regions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.header("Best League Overall")
        draw_region_card_by_metric("Rating")

with col2:
    with st.container(border=True):
        st.header("Best Combat Skill League")
        draw_region_card_by_metric("ACS")

with col3:
    with st.container(border=True):
        st.header("Most Intense League")
        draw_region_card_by_metric("Kills")

with col4:
    with st.container(border=True):
        st.header("Most Agressive League")
        draw_region_card_by_metric("FirstKills")