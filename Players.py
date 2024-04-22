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

def draw_player_card_by_metric(metric):

    if metric == "Rating" or "HSRate":
        round_value = 3
    else:
        round_value = 2

    sql_query = """SELECT Name, ROUND(AVG({}),{}) AS {}, Team
                        FROM test_data
                        GROUP BY Name
                        ORDER BY AVG({}) DESC
                        LIMIT 5;""".format(metric, round_value, metric, metric)
    
    df_data = pd.read_sql(sql_query, conn)

    player, value = df_data["Name"][0], df_data[metric][0]

    text = [str(value) + " {}".format(metric), "Most Average {} per Map Played in All VCTs".format(metric)]
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

    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

def draw_player_match_card_by_metric(metric):

    if metric == "Rating" or metric == "HSRate":
        round_value = 3
    else:
        round_value = 2

    if metric == "Kills" or metric == "Assists" or metric == "FirstKills":
        filter_data = "SUM({})".format(metric)
        group_filter = "SUM({})".format(metric)
    else:
        filter_data = "ROUND(AVG({}),{})".format(metric, round_value)
        group_filter = "AVG({})".format(metric)

    sql_query = """SELECT Name, {} AS {}, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
                        FROM test_data
                        GROUP BY PlayerMatchKey
                        ORDER BY {} DESC
                        LIMIT 5;""".format(filter_data, metric, group_filter)
    
    df_data = pd.read_sql(sql_query, conn)

    player, value, matchteams = df_data["Name"][0], df_data[metric][0], df_data["MatchTeams"][0]
    text = [str(value) +" {}".format(metric), "Most {} in One Match in All VCTs".format(metric), matchteams]
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

    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

def draw_player_map_card_by_metric(metric):

    sql_query = """SELECT Name, {}, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
                        FROM test_data
                        ORDER BY {} DESC
                        LIMIT 5;""".format(metric, metric)

    df_data = pd.read_sql(sql_query, conn)

    player, value, map_name, matchteams =  df_data["Name"][0], df_data[metric][0], df_data["Map"][0], df_data["MatchTeams"][0]
    text = [str(value) +" {}".format(metric), "Most {} in One Single Map in All VCTs".format(metric), map_name, matchteams]
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

    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024] :orange[[Under Developing]]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Players Overall")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.header(":blue[MVP Overall]")
        draw_player_card_by_metric("Rating")

with col2:
    with st.container(border=True):
        st.header(":blue[Combat Specialist]")
        draw_player_card_by_metric("ACS")

with col3:
    with st.container(border=True):
        st.header(":blue[Elimination Expert]")
        draw_player_card_by_metric("Kills")

with col4:
    with st.container(border=True):
        st.header(":blue[Support Master]") 
        draw_player_card_by_metric("Assists")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        st.header(":blue[Team Architect]") 
        draw_player_card_by_metric("Kast")

with col6:
    with st.container(border=True):
        st.header(":blue[Consistent Impact]") 
        draw_player_card_by_metric("ADR")
    
with col7:
    with st.container(border=True):
        st.header(":blue[Sharpshooting Champion]") 
        draw_player_card_by_metric("HSRate")

with col8:
    with st.container(border=True):
        st.header(":blue[Aggressive Strategist]") 
        draw_player_card_by_metric("FirstKills")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Match")

col9, col10, col11, col12 = st.columns(4)

with col9:
    with st.container(border=True):
        draw_player_match_card_by_metric("Rating")

with col10:
    with st.container(border=True):
        draw_player_match_card_by_metric("ACS")

with col11:
    with st.container(border=True):
        draw_player_match_card_by_metric("Kills")

with col12:
    with st.container(border=True):
        draw_player_match_card_by_metric("Assists")


col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        draw_player_match_card_by_metric("Kast")

with col14:
    with st.container(border=True):
        draw_player_match_card_by_metric("ADR")

with col15:
    with st.container(border=True):
        draw_player_match_card_by_metric("HSRate")

with col16:
    with st.container(border=True):
        draw_player_match_card_by_metric("FirstKills")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Single Map")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        draw_player_map_card_by_metric("Rating")

with col18:
    with st.container(border=True):
        draw_player_map_card_by_metric("ACS")    

with col19:
    with st.container(border=True):
        draw_player_map_card_by_metric("Kills")

with col20:
    with st.container(border=True):
        draw_player_map_card_by_metric("Assists")

col21, col22, col23, col24 = st.columns(4)

with col21:
    with st.container(border=True):
        draw_player_map_card_by_metric("Kast")

with col22:
    with st.container(border=True):
        draw_player_map_card_by_metric("ADR")

with col23:
    with st.container(border=True):
        draw_player_map_card_by_metric("HSRate")

with col24:
    with st.container(border=True):
        draw_player_map_card_by_metric("FirstKills")
        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
 
st.title("Placeholder _New Statistics_")
st.title("Placeholder _Countries_")
