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
 
def draw_team_card_by_metric(metric):

    if metric == "Rating":
        round_value = 3
    elif metric == "HSRate" or metric == "Kast":
        round_value = 3
    else:
        round_value = 2

    sql_query = """SELECT Team, ROUND(AVG({}),{}) AS {}, COUNT(DISTINCT(TeamMapKey)) AS MapsPlayed
                    FROM test_data
                    GROUP BY Team
                    ORDER BY AVG({}) DESC
                    LIMIT 5;""".format(metric, round_value, metric, metric)
    
    df_data = pd.read_sql(sql_query, conn)


    team, value = df_data["Team"][0], df_data[metric][0]

    text = [str(value) + " {}".format(metric), "Most Average {} per Map Played by Teams in All VCTs".format(metric)]
    title = str(team).upper()

    card(
        title = title,
        text = text,
        image = load_image(team, "teams"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
        )
    
    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

def draw_team_map_card_by_metric(metric):

    if metric == "Rating" or metric == "HSRate":
        round_value = 3
    else:
        round_value = 2

    if metric == "Kills" or metric == "Assists" or metric == "FirstKills":
        prefix = ""
        filter_data = "SUM({})".format(metric)
        group_filter = "SUM({})".format(metric)
    else:
        filter_data = "ROUND(AVG({}),{})".format(metric, round_value)
        group_filter = "AVG({})".format(metric)
        prefix = "Average "

    sql_query = """SELECT Team, {} AS {}, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
                    FROM test_data
                    GROUP BY TeamMapKey
                    ORDER BY {} DESC
                    LIMIT 5;""".format(filter_data, metric, group_filter)

    df_data = pd.read_sql(sql_query, conn)

    
    team, value, matchteams = df_data["Team"][0], df_data[metric][0], df_data["MatchTeams"][0]
    text = [str(value) +" {}".format(metric), "Most {}{} in One Single Map by Teams in All VCTs".format(prefix, metric), matchteams]
    title = str(team).upper()

    card(
        title = title,
        text = text,
        image = load_image(team, "teams"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
        )

    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Teams Overall")

with st.sidebar:
    st.title("Categories")
    st.markdown("[Top Teams Overall](#top-teams-overall)")
    st.markdown("[Top Teams in One Single Map](#top-teams-in-one-single-map)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        draw_team_card_by_metric("Rating")

with col2:
    with st.container(border=True):
        draw_team_card_by_metric("ACS")

with col3:
    with st.container(border=True):
        draw_team_card_by_metric("Kills")

with col4:
    with st.container(border=True):
        draw_team_card_by_metric("Assists")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        draw_team_card_by_metric("Kast")

with col6:
    with st.container(border=True):
        draw_team_card_by_metric("ADR")
    
with col7:
    with st.container(border=True):
        draw_team_card_by_metric("HSRate")

with col8:
    with st.container(border=True):
        draw_team_card_by_metric("FirstKills")
   
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams in One Single Map")

col9, col10, col11, col12 = st.columns(4)

with col9:
    with st.container(border=True):
        draw_team_map_card_by_metric("Rating")

with col10:
    with st.container(border=True):
        draw_team_map_card_by_metric("ACS")

with col11:
    with st.container(border=True):
        draw_team_map_card_by_metric("Kills")

with col12:
    with st.container(border=True):
        draw_team_map_card_by_metric("Assists")

col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        draw_team_map_card_by_metric("Kast")

with col14:
    with st.container(border=True):
        draw_team_map_card_by_metric("ADR")

with col15:
    with st.container(border=True):
        draw_team_map_card_by_metric("HSRate")

with col16:
    with st.container(border=True):
        draw_team_map_card_by_metric("FirstKills")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
