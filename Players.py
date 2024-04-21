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

    if category1 == "maps":
        player, value, map_name, matchteams =  df_data["Name"][0], df_data[category_key_value][0], df_data["Map"][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key_value), "Most {} in One Single Map in All VCTs".format(category_key_value), map_name, matchteams]
        title = str(player).upper()

    elif category1 == "matches":
        player, value, matchteams = df_data["Name"][0], df_data[category_key_value][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key_value), "Most {} in One Match in All VCTs".format(category_key_value), matchteams]
        title = str(player).upper()

    card_list.append(card(
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
    )

    st.header("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)
## General   
def display_card_table2(df_data,category2):

    category_key_value = translate_dict.get(category2)

    player, value = df_data["Name"][0], df_data[category_key_value][0]

    text = [str(value) + " {}".format(category_key_value), "Most Average {} per Map Played in All VCTs".format(category_key_value)]
    title = str(player).upper()

    card_list.append(card(
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
###############################################################################################################################################################################################################

st.title("Top Players Overall")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""
        player_average_rating_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[MVP Overall]")

        display_card_table2(player_average_rating_overall,"most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ACS),2) AS ACS, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""
        player_average_acs_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Combat Specialist]")

        display_card_table2(player_average_acs_overall,"most_acs")

with col3:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Kills),2) AS Kills, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Kills) DESC
        LIMIT 5;"""
        player_average_kills_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Elimination Expert]")

        display_card_table2(player_average_kills_overall,"most_kills")

with col4:
    with st.container(border=True):

        sql_query = """SELECT Name, ROUND(AVG(Assists),2) AS Assists, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Assists) DESC
        LIMIT 5;"""
        player_average_assists_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Support Master]") 

        display_card_table2(player_average_assists_overall,"most_assists")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Kast),2) AS Kast, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(Kast) DESC
        LIMIT 5;"""
        player_average_kast_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Team Architect]") 

        display_card_table2(player_average_kast_overall,"most_kast")

with col6:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ADR),2) AS ADR, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(ADR) DESC
        LIMIT 5;"""
        player_average_adr_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Consistent Impact]") 

        display_card_table2(player_average_adr_overall,"most_adr")
    
with col7:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(FirstKills),2) AS FirstKills, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(FirstKills) DESC
        LIMIT 5;"""
        player_average_fk_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Aggressive Strategist]") 

        display_card_table2(player_average_fk_overall,"most_fk")

with col8:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(HSRate),2) AS HSRate, Team
        FROM test_data
        GROUP BY Name
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""
        player_average_hs_overall = pd.read_sql(sql_query, conn)

        st.header(":blue[Sharpshooting Champion]") 

        display_card_table2(player_average_hs_overall,"most_hs")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Match")

col9, col10, col11, col12 = st.columns(4)

with col9:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Rating),2) AS Rating, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""

        player_average_rating_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_rating_match,"matches","most_rating")

with col10:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(Kills) AS Kills, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(Kills) DESC
        LIMIT 5;"""

        player_kills_match = pd.read_sql(sql_query, conn)

        display_card_table(player_kills_match,"matches","most_kills")

with col11:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(HSRate),2) AS HSRate, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""

        player_average_hs_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_hs_match,"matches","most_hs")

with col12:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(FirstKills) AS FirstKills, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(FirstKills) DESC
        LIMIT 5;"""

        player_fk_match = pd.read_sql(sql_query, conn)

        display_card_table(player_fk_match,"matches","most_fk")


col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ACS),2) AS ACS, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""

        player_average_acs_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_acs_match,"matches","most_acs")

with col14:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ADR),2) AS ADR, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(ADR) DESC
        LIMIT 5;"""

        player_average_adr_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_adr_match,"matches","most_adr")

with col15:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(Assists) AS Assists, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(Assists) DESC
        LIMIT 5;"""

        player_assists_match = pd.read_sql(sql_query, conn)

        display_card_table(player_assists_match,"matches","most_assists")

with col16:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Kast),2) AS Kast, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(Kast) DESC
        LIMIT 5;"""

        player_average_kast_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_kast_match,"matches","most_kast")


###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Single Map")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(Rating,2) AS Rating, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Rating DESC
        LIMIT 5;"""

        player_rating_map = pd.read_sql(sql_query, conn)

        display_card_table(player_rating_map,"maps","most_rating")

with col18:
    with st.container(border=True):
        sql_query = """SELECT Name, Kills, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Kills DESC
        LIMIT 5;"""

        player_kills_map = pd.read_sql(sql_query, conn)

        display_card_table(player_kills_map,"maps","most_kills")

with col19:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(HSRate,2) AS HSRate, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY HSRate DESC
        LIMIT 5;"""

        player_hs_map = pd.read_sql(sql_query, conn)

        display_card_table(player_hs_map,"maps","most_hs")

with col20:
    with st.container(border=True):
        sql_query = """SELECT Name, FirstKills, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY FirstKills DESC
        LIMIT 5;"""

        player_fk_map = pd.read_sql(sql_query, conn)

        display_card_table(player_fk_map,"maps","most_fk")
        
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
 
st.title("Placeholder _Agents_")
st.title("Placeholder _New Statistics_")
st.title("Placeholder _Countries_")
