import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

def display_card_table(df_data, category):

    category_key_value = translate_dict.get(category)

    if category_key_value == "FirstKills" or category_key_value == "Kills" or category_key_value == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    localteam, visitteam, value = df_data["LocalTeam"][0], df_data["VisitTeam"][0],  df_data[category_key_value][0]

    col1, col2 = st.columns(2)

    text = "Most {}{} by Both Teams in All VCTs".format(prefix, category_key_value)

    with col1:
        card_list.append(card(
            title = str(localteam.upper()),
            text = "",
            image = load_image(localteam, "Teams"),
            styles={
                "card": {
                    "width": "100%",
                    "height": "350px"
                        }
                    }
                                )
        )

    with col2:
        card_list.append(card(
            title = str(visitteam.upper()),
            text = "",
            image = load_image(visitteam, "Teams"),
            styles={
                "card": {
                    "width": "100%",
                    "height": "350px"
                        }
                    }
                                )
                             )

    st.header(text)
    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

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

players_maps_data_df = pd.read_csv("player_data_by_map.csv")
conn = connect(':memory:')
players_maps_data_df.to_sql(name='test_data', con=conn)

with open("last_update.txt", "r") as archivo:
    last_update = archivo.read()

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
st.header('Valo.py', divider='blue')
st.sidebar.header("Categories")
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Matches")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT LocalTeam, VisitTeam, ROUND(AVG(Rating),3) AS Rating, Date
        FROM test_data
        GROUP BY MatchKey
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""
        match_average_rating_overall = pd.read_sql(sql_query, conn)
        display_card_table(match_average_rating_overall,"most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT LocalTeam, VisitTeam, ROUND(AVG(ACS),3) AS ACS, Date
        FROM test_data
        GROUP BY MatchKey
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""
        match_average_acs_overall = pd.read_sql(sql_query, conn)
        display_card_table(match_average_acs_overall,"most_acs")

with col3:
    with st.container(border=True):
        sql_query = """SELECT LocalTeam, VisitTeam, SUM(Kills) AS Kills, Date
        FROM test_data
        GROUP BY MatchKey
        ORDER BY AVG(Kills) DESC
        LIMIT 5;"""
        match_kills_overall = pd.read_sql(sql_query, conn)
        display_card_table(match_kills_overall,"most_kills")

with col4:
    with st.container(border=True):
        sql_query = """SELECT LocalTeam, VisitTeam, ROUND(AVG(HSRate),3) AS HSRate, Date
        FROM test_data
        GROUP BY MatchKey
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""
        match_average_hs_overall = pd.read_sql(sql_query, conn)
        display_card_table(match_average_hs_overall,"most_hs")