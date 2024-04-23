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

def merge_image(filename1, folder1, filename2, folder2):
    pass

def draw_teams_match_card_by_metric(metric):

    if metric == "FirstKills" or metric == "Kills" or metric == "Assists":
        prefix = ""
    else:
        prefix = "Average "
        
    sql_query = """SELECT LocalTeam, VisitTeam, ROUND(AVG({}),3) AS {}, Date
                    FROM test_data
                    GROUP BY MatchKey
                    ORDER BY AVG({}) DESC
                    LIMIT 5;""".format(metric, metric,metric)
    
    df_data = pd.read_sql(sql_query, conn)

    localteam, visitteam, value = df_data["LocalTeam"][0], df_data["VisitTeam"][0],  df_data[metric][0]

    colx, coly = st.columns(2)

    text = "Most {}{} by Both Teams in All VCTs".format(prefix, metric)

    with colx:
        card(
            title = str(localteam.upper()),
            text = "{} {} {} by Both Teams".format(prefix, value, metric),
            image = load_image(localteam, "Teams"),
            styles={
                "card": {
                    "width": "100%",
                    "height": "300px"
                        }
                    }
             )

    with coly:
        card(
            title = str(visitteam.upper()),
            text = "{} {} {} by Both Teams".format(prefix, value, metric),
            image = load_image(visitteam, "Teams"),
            styles={
                "card": {
                    "width": "100%",
                    "height": "300px"
                        }
                    }
            )

    st.header(text)
    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Matches")

with st.sidebar:
    st.title("Categories")
    st.markdown("[Top Matches](#top-matches)")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        draw_teams_match_card_by_metric("Rating")

with col2:
    with st.container(border=True):
        draw_teams_match_card_by_metric("ACS")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        draw_teams_match_card_by_metric("Kills")

with col4:
    with st.container(border=True):
        draw_teams_match_card_by_metric("HSRate")
