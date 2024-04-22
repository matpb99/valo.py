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

def display_card_table(df_data, category, metric):

    category_key = translate_dict.get(metric)

    if category == "maps":
        player, value, map_name, matchteams =  df_data["Name"][0], df_data[category_key][0], df_data["Map"][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key), "Most {} in One Single Map in All VCTs".format(category_key), map_name, matchteams]
        title = str(player).capitalize()

    elif category == "matches":
        player, value, matchteams = df_data["Name"][0], df_data[category_key][0], df_data["MatchTeams"][0]
        text = [str(value) +" {}".format(category_key), "Most {} in One Match in All VCTs".format(category_key), matchteams]
        title = str(player).capitalize()

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

    st.subheader("Top 5 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)
   
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
        sql_query = """SELECT Name, ROUND(AVG(Rating),2) AS Rating, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(Rating) DESC
        LIMIT 5;"""

        player_average_rating_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_rating_match,"matches","most_rating")

with col10:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(ACS),2) AS ACS, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(ACS) DESC
        LIMIT 5;"""

        player_average_acs_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_acs_match,"matches","most_acs")

with col11:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(Kills) AS Kills, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(Kills) DESC
        LIMIT 5;"""

        player_kills_match = pd.read_sql(sql_query, conn)

        display_card_table(player_kills_match,"matches","most_kills")

with col12:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(Assists) AS Assists, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(Assists) DESC
        LIMIT 5;"""

        player_assists_match = pd.read_sql(sql_query, conn)

        display_card_table(player_assists_match,"matches","most_assists")


col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        sql_query = """SELECT Name, ROUND(AVG(Kast),2) AS Kast, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(Kast) DESC
        LIMIT 5;"""

        player_average_kast_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_kast_match,"matches","most_kast")

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
        sql_query = """SELECT Name, ROUND(AVG(HSRate),2) AS HSRate, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY AVG(HSRate) DESC
        LIMIT 5;"""

        player_average_hs_match = pd.read_sql(sql_query, conn)

        display_card_table(player_average_hs_match,"matches","most_hs")

with col16:
    with st.container(border=True):
        sql_query = """SELECT Name, SUM(FirstKills) AS FirstKills, Team, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        GROUP BY PlayerMatchKey
        ORDER BY SUM(FirstKills) DESC
        LIMIT 5;"""

        player_fk_match = pd.read_sql(sql_query, conn)

        display_card_table(player_fk_match,"matches","most_fk")

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Single Map")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        sql_query = """SELECT Name, Rating, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Rating DESC
        LIMIT 5;"""

        player_rating_map = pd.read_sql(sql_query, conn)

        display_card_table(player_rating_map,"maps","most_rating")

with col18:
    with st.container(border=True):
        sql_query = """SELECT Name, ACS, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY ACS DESC
        LIMIT 5;"""

        player_acs_map = pd.read_sql(sql_query, conn)

        display_card_table(player_acs_map,"maps","most_acs")       

with col19:
    with st.container(border=True):
        sql_query = """SELECT Name, Kills, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Kills DESC
        LIMIT 5;"""

        player_kills_map = pd.read_sql(sql_query, conn)

        display_card_table(player_kills_map,"maps","most_kills")

with col20:
    with st.container(border=True):
        sql_query = """SELECT Name, Assists, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Assists DESC
        LIMIT 5;"""

        player_assists_map = pd.read_sql(sql_query, conn)

        display_card_table(player_assists_map,"maps","most_assists")

col21, col22, col23, col24 = st.columns(4)

with col21:
    with st.container(border=True):
        sql_query = """SELECT Name, Kast, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY Kast DESC
        LIMIT 5;"""

        player_kast_map = pd.read_sql(sql_query, conn)

        display_card_table(player_kast_map,"maps","most_kast")

with col22:
    with st.container(border=True):
        sql_query = """SELECT Name, ADR, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY ADR DESC
        LIMIT 5;"""

        player_adr_map = pd.read_sql(sql_query, conn)

        display_card_table(player_adr_map,"maps","most_adr")

with col23:
    with st.container(border=True):
        sql_query = """SELECT Name, HSRate, Team, Map, LocalTeam || " VS " || VisitTeam AS MatchTeams, Date
        FROM test_data
        ORDER BY HSRate DESC
        LIMIT 5;"""

        player_hs_map = pd.read_sql(sql_query, conn)

        display_card_table(player_hs_map,"maps","most_hs")

with col24:
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
