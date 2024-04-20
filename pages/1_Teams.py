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

def display_card_table(df_data,category1,category2,category3):

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
                "height": "400px"
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
                "height": "400px"
                    }
                }
                            )
    )

    st.header("Top 5 Ranking")
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

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py", page_icon="https://icons8.com/icon/GjCK2f2wpZxt/valorant")
st.header('Valo.py', divider='blue')
st.sidebar.header("Categories")
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Rating),2) AS Rating
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""
        team_average_hs_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_hs_overall,"teams","most_rating")

with col6:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(ACS),2) AS ACS
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""
        team_average_acss_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_acss_overall,"teams","most_acs")

with col7:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Kills),2) AS Kills
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Kills) DESC
        LIMIT 5;"""
        team_average_kills_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_kills_overall,"teams","most_kills")

with col8:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Assists),2) AS Assists
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Assists) DESC
        LIMIT 5;"""
        team_average_assists_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_assists_overall,"teams","most_assists")

col25, col26, col27, col28 = st.columns(4)

with col25:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Kast),2) AS Kast
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Kast) DESC
        LIMIT 5;"""
        team_average_kast_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_kast_overall,"teams","most_kast")

with col26:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(ADR),2) AS ADR
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(ADR) DESC
        LIMIT 5;"""
        team_average_adr_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_adr_overall,"teams","most_adr")
    
with col27:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(FirstKills),2) AS FirstKills
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(FirstKills) DESC
        LIMIT 5;"""
        team_average_fk_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_fk_overall,"teams","most_fk")

with col28:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(HSRate),2) AS HSRate
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""
        team_average_hs_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_hs_overall,"teams","most_hs")
    
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams in One Single Map")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Rating),2) AS Rating, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, DateStandar AS Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""

        team_average_rating_map = pd.read_sql(sql_query, conn)
        display_card_table(team_average_rating_map,"maps","teams","most_rating")

with col18:
    with st.container(border=True):
        sql_query = """SELECT Team, SUM(Kills) AS Kills, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, DateStandar AS Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY SUM(Kills) DESC
        LIMIT 5;"""

        team_kills_map = pd.read_sql(sql_query, conn)
        display_card_table(team_kills_map,"maps","teams","most_kills")

with col19:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(HSRate),2) AS HSRate, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, DateStandar AS Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""

        team_average_hs_map = pd.read_sql(sql_query, conn)
        display_card_table(team_average_hs_map,"maps","teams","most_hs")
      
with col20:
    with st.container(border=True):
        sql_query = """SELECT Team, SUM(FirstKills) AS FirstKills, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, DateStandar AS Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY SUM(FirstKills) DESC
        LIMIT 5;"""

        team_fk_map = pd.read_sql(sql_query, conn)
        display_card_table(team_fk_map,"maps","teams","most_fk")

        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
