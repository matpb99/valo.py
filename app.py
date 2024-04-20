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

def display_card_table(category1,category2,category3):

    df_data =  pd.read_csv("./outputs/{}/{}/{}.csv".format(category1,category2,category3))

    category_key_value = translate_dict.get(category3)

    if category2 == "players":
        category_key = "Name"
    else:
        category_key = "Team"

    if category1 == "maps":
        category, value, map_name, matchteams =  df_data[category_key][0], df_data[category_key_value][0], df_data["Map"][0], df_data["MatchTeams"][0]

    elif category1 == "matches":
        category, value, matchteams = df_data[category_key][0], df_data[category_key_value][0], df_data["MatchTeams"][0]

    if category1 == "maps":
        if category2 == "players":
            text = [str(value) +" {}".format(category_key_value), "Most {} in One Single Map in All VCTs".format(category_key_value), map_name, matchteams]
            title = str(category).capitalize()
        else:
            text = [str(value) +" {}".format(category_key_value), "Most {} in One Single Map by Teams in All VCTs".format(category_key_value), map_name, matchteams]
            title = str(category).upper()
    else:
        if category2 == "players":
            text = [str(value) +" {}".format(category_key_value), "Most {} in One Match in All VCTs".format(category_key_value), matchteams]
            title = str(category).capitalize()
        else:
            text = [str(value) +" {}".format(category_key_value), "Most {} in One Match by Teams in All VCTs".format(category_key_value), matchteams]
            title = str(category).upper()

    card_list.append(card(
        title = title,
        text = text,
        image = load_image(category, category2),
        styles={
            "card": {
                "width": "100%",
                "height": "500px"
                    }
                }
                            )
    )

    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)
    
def display_card_table2(df_data,category1,category2):

    category_key_value = translate_dict.get(category2)

    if category1=="players":
        category_key = "Name"
    else:
        category_key = "Team"

    category, value = df_data[category_key][0], df_data[category_key_value][0]

    if category1 == "players":
        text = [str(value) + " {}".format(category_key_value), "Most Average {} per Map Played in All VCTs".format(category_key_value)]
        title = str(category).capitalize()
    else:
        text = [str(value) + " {}".format(category_key_value), "Most Average {} per Map Played by Teams in All VCTs".format(category_key_value)]
        title = str(category).upper()

    card_list.append(card(
        title = title,
        text = text,
        image = load_image(category, category1),
        styles={
            "card": {
                "width": "100%",
                "height": "500px"
                    }
                }
                            )
    )

    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

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

players_maps_data_df = pd.read_csv("player_data_by_map2.csv")
conn = connect(':memory:')
players_maps_data_df.to_sql(name='test_data', con=conn)

with open("last_update.txt", "r") as archivo:
    last_update = archivo.read()

st.header('Valo.py', divider='blue')
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""
        player_average_rating_overall = pd.read_sql(sql_query, conn)

        display_card_table2(player_average_rating_overall,"players","most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ACS),2) AS ACS, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""
        player_average_acs_overall = pd.read_sql(sql_query, conn)

        display_card_table2(player_average_acs_overall,"players","most_acs")

with col3:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Kills),2) AS Kills, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Kills) DESC
        LIMIT 5;"""
        player_average_kills_overall = pd.read_sql(sql_query, conn)

        display_card_table2(player_average_kills_overall,"players","most_kills")


with col4:
    with st.container(border=True):

        sql_query = """SELECT Name, ROUND(AVG(Assists),2) AS Assists, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Assists) DESC
        LIMIT 5;"""
        player_average_assists_overall = pd.read_sql(sql_query, conn)

        display_card_table2(player_average_assists_overall,"players","most_assists")

col21, col22, col23, col24 = st.columns(4)

with col21:
    with st.container(border=True):
        display_card_table2("players","most_kast")

with col22:
    with st.container(border=True):
        display_card_table2("players","most_adr")
    
with col23:
    with st.container(border=True):
        display_card_table2("players","most_fk")

with col24:
    with st.container(border=True):
        display_card_table2("players","most_hs")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        display_card_table2("teams","most_rating")

with col6:
    with st.container(border=True):
        display_card_table2("teams","most_acs")

with col7:
    with st.container(border=True):
        display_card_table2("teams","most_kills")

with col8:
    with st.container(border=True):
        display_card_table2("teams","most_assists")

col25, col26, col27, col28 = st.columns(4)

with col25:
    with st.container(border=True):
        display_card_table2("teams","most_kast")

with col26:
    with st.container(border=True):
        display_card_table2("teams","most_adr")
    
with col27:
    with st.container(border=True):
        display_card_table2("teams","most_fk")

with col28:
    with st.container(border=True):
        display_card_table2("teams","most_hs")
        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Match")

col9, col10, col11, col12 = st.columns(4)

with col9:
    with st.container(border=True):
        display_card_table("matches","players","most_rating")

with col10:
    with st.container(border=True):
        display_card_table("matches","players","most_kills")

with col11:
    with st.container(border=True):
        display_card_table("matches","players","most_hs")

with col12:
    with st.container(border=True):
        display_card_table("matches","players","most_fk")

col29, col30, col31, col32 = st.columns(4)

with col29:
    with st.container(border=True):
        display_card_table("matches","players","most_acs")

with col30:
    with st.container(border=True):
        display_card_table("matches","players","most_adr")

with col31:
    with st.container(border=True):
        display_card_table("matches","players","most_assists")

with col32:
    with st.container(border=True):
        display_card_table("matches","players","most_kast")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Single Map")

col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        display_card_table("maps","players","most_rating")

with col14:
    with st.container(border=True):
        display_card_table("maps","players","most_kills")

with col15:
    with st.container(border=True):
        display_card_table("maps","players","most_hs")

with col16:
    with st.container(border=True):
        display_card_table("maps","players","most_fk")
        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams in One Single Map")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        display_card_table("maps","teams","most_rating")

with col18:
    with st.container(border=True):
        display_card_table("maps","teams","most_kills")

with col19:
    with st.container(border=True):
        display_card_table("maps","teams","most_hs")
        
with col20:
    with st.container(border=True):
        display_card_table("maps","teams","most_fk")
        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Placeholder _Agents_")
st.title("Placeholder _New Statistics_")
st.title("Placeholder _Countries_")
