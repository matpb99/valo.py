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

def draw_player_rol_card_by_metric(role_name, metric):

    if metric == "FirstKills" or metric == "Kills" or metric == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    if role_name == "duelist":
        color = "blue"
    elif role_name == "sentinel":
        color = "red"
    elif role_name == "controller":
        color = "white"
    else:
        color = "orange"

    st.header(":{}[Best {}]".format(color, role_name.capitalize()))

    if metric == "FirstKills" or metric == "Kills" or metric == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    sql_query = """SELECT Name, COUNT(Role) AS MapsPlayed, ROUND(AVG({}),2) AS {}, Team
                    FROM test_data
                    WHERE Role=="{}" 
                    GROUP BY Name
                    HAVING COUNT(Role)>=8
                    ORDER BY AVG({}) DESC
                    LIMIT 3;""".format(metric, metric, role_name, metric)

    df_data = pd.read_sql(sql_query, conn)

    player, value = df_data["Name"][0], df_data[metric][0]

    text = [str(value) + " {}".format(metric), "{}{} in All VCTs ".format(prefix, metric), "Played at least 8 maps"]
    title = str(player).capitalize()

    card(
        title = title,
        text = text,
        image = load_image(player, "players"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
                            )
    st.subheader("Top 3 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

def draw_agent_rol_card_by_times_played(role_name):
    
    sql_query = """SELECT Agent, COUNT(Agent) AS MapsPlayed
                    FROM test_data
                    WHERE Role=="{}" 
                    GROUP BY Agent
                    ORDER BY COUNT(Agent) DESC
                    ;""".format(role_name)

    df_data = pd.read_sql(sql_query, conn)

    agent, value = df_data["Agent"][0], df_data["MapsPlayed"][0]

    text = [str(value) + " Maps Played", " Most {} Played in All VCTs ".format(role_name.capitalize())]
    title = str(agent).capitalize()

    card(
        title = title,
        text = text,
        image = load_image(agent, "agents"),
        styles={
            "card": {
                "width": "100%",
                "height": "600px"
                    }
                }
        )
    
    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Roles")

with st.sidebar:
    st.title("Categories")
    st.markdown("[Top Roles](#top-roles)")
    st.markdown("[Most Played](#most-played)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        draw_player_rol_card_by_metric("duelist","Rating")

with col2:
    with st.container(border=True):
        draw_player_rol_card_by_metric("sentinel","Rating")

with col3:
    with st.container(border=True):
        draw_player_rol_card_by_metric("controller","Rating")

with col4:
    with st.container(border=True):
        draw_player_rol_card_by_metric("initiator","Rating")

st.title("Most Played")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        draw_agent_rol_card_by_times_played("duelist")

with col6:
    with st.container(border=True):
        draw_agent_rol_card_by_times_played("sentinel")

with col7:
    with st.container(border=True):
        draw_agent_rol_card_by_times_played("controller")

with col8:
    with st.container(border=True):
        draw_agent_rol_card_by_times_played("initiator")