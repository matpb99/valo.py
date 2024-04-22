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
#Detalle
def display_card_table(df_data,category1,category3):

    category_key_value = translate_dict.get(category3)

    if category_key_value == "FirstKills" or category_key_value == "Kills" or category_key_value == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    if category1 == "maps":
        team, value, map_name, matchteams =  df_data["Team"][0], df_data[category_key_value][0], df_data["Map"][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key_value), "Most {}{} in One Single Map by Teams in All VCTs".format(prefix, category_key_value), map_name, matchteams]
        title = str(team).upper()

    elif category1 == "matches":
        team, value, matchteams = df_data["Team"][0], df_data[category_key_value][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key_value), "Most {}{} in One Match by Teams in All VCTs".format(prefix, category_key_value), matchteams]
        title = str(team).upper()

    card_list.append(card(
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
    )

    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)
## General   
def display_card_table2(df_data,category2):

    category_key_value = translate_dict.get(category2)

    team, value = df_data["Team"][0], df_data[category_key_value][0]

    text = [str(value) + " {}".format(category_key_value), "Most Average {} per Map Played by Teams in All VCTs".format(category_key_value)]
    title = str(team).upper()

    card_list.append(card(
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

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
st.header('Valo.py', divider='blue')
st.sidebar.header("Categories")
st.subheader("_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024]")
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Rating),4) AS Rating
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""
        team_average_hs_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_hs_overall,"most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(ACS),2) AS ACS
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""
        team_average_acss_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_acss_overall,"most_acs")

with col3:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Kills),2) AS Kills
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Kills) DESC
        LIMIT 5;"""
        team_average_kills_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_kills_overall,"most_kills")

with col4:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Assists),2) AS Assists
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Assists) DESC
        LIMIT 5;"""
        team_average_assists_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_assists_overall,"most_assists")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Kast),2) AS Kast
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(Kast) DESC
        LIMIT 5;"""
        team_average_kast_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_kast_overall,"most_kast")

with col6:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(ADR),2) AS ADR
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(ADR) DESC
        LIMIT 5;"""
        team_average_adr_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_adr_overall,"most_adr")
    
with col7:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(FirstKills),2) AS FirstKills
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(FirstKills) DESC
        LIMIT 5;"""
        team_average_fk_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_fk_overall,"most_fk")

with col8:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(HSRate),2) AS HSRate
        FROM test_data
        GROUP BY Team
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""
        team_average_hs_overall = pd.read_sql(sql_query, conn)

        display_card_table2(team_average_hs_overall,"most_hs")
    
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams in One Single Map")

col9, col10, col11, col12 = st.columns(4)

with col9:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(Rating),2) AS Rating, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""

        team_average_rating_map = pd.read_sql(sql_query, conn)
        display_card_table(team_average_rating_map,"maps","most_rating")

with col10:
    with st.container(border=True):
        sql_query = """SELECT Team, SUM(Kills) AS Kills, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY SUM(Kills) DESC
        LIMIT 5;"""

        team_kills_map = pd.read_sql(sql_query, conn)
        display_card_table(team_kills_map,"maps","most_kills")

with col11:
    with st.container(border=True):
        sql_query = """SELECT Team, ROUND(AVG(HSRate),2) AS HSRate, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""

        team_average_hs_map = pd.read_sql(sql_query, conn)
        display_card_table(team_average_hs_map,"maps","most_hs")
      
with col12:
    with st.container(border=True):
        sql_query = """SELECT Team, SUM(FirstKills) AS FirstKills, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY TeamMapKey
        ORDER BY SUM(FirstKills) DESC
        LIMIT 5;"""

        team_fk_map = pd.read_sql(sql_query, conn)
        display_card_table(team_fk_map,"maps","most_fk")

        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
