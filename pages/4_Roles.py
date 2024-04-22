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

def display_card_table(df_data, metric):

    metric_key = translate_dict.get(metric)

    if metric_key == "FirstKills" or metric_key == "Kills" or metric_key == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    player, value = df_data["Name"][0], df_data[metric_key][0]

    text = [str(value) + " {}".format(metric_key), "{}{} in All VCTs ".format(prefix, metric_key), "Played at least 4 maps"]
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
    st.subheader("Top 3 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

def display_card_table2(df_data, rol_name):

    agent, value = df_data["Agent"][0], df_data["MapsPlayed"][0]

    text = [str(value) + " Maps Played", " Most {} Played in All VCTs ".format(rol_name)]
    title = str(agent).capitalize()

    card_list.append(card(
        title = title,
        text = text,
        image = load_image(agent, "agents"),
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
st.subheader("_Last Update:_ :green[{}]".format(last_update))

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Roles")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Role) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Role=="duelist" 
        GROUP BY Name
        HAVING COUNT(Role)>=4
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        duelist_rating = pd.read_sql(sql_query, conn)

        st.header(":blue[Best Duelist]")

        display_card_table(duelist_rating,"most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Role) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Role=="sentinel" 
        GROUP BY Name
        HAVING COUNT(Role)>=4
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        sentinel_rating = pd.read_sql(sql_query, conn)

        st.header(":red[Best Sentinel]")

        display_card_table(sentinel_rating,"most_rating")

with col3:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Role) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Role=="controller" 
        GROUP BY Name
        HAVING COUNT(Role)>=4
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        controller_rating = pd.read_sql(sql_query, conn)

        st.header(":white[Best Controller]")

        display_card_table(controller_rating,"most_rating")

with col4:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Role) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Role=="initiator" 
        GROUP BY Name
        HAVING COUNT(Role)>=4
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        initiator_rating = pd.read_sql(sql_query, conn)

        st.header(":orange[Best Initiator]")

        display_card_table(initiator_rating,"most_rating")


st.title("Most Played")

col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(border=True):
        sql_query = """SELECT Agent, COUNT(Agent) AS MapsPlayed
        FROM test_data
        WHERE Role=="duelist" 
        GROUP BY Agent
        ORDER BY COUNT(Agent) DESC
        LIMIT 5;"""

        duelist_played = pd.read_sql(sql_query, conn)

        st.header(":blue[Most Played Duelist]")

        display_card_table2(duelist_played,"duelist")

with col6:
    with st.container(border=True):
        sql_query = """SELECT Agent, COUNT(Agent) AS MapsPlayed
        FROM test_data
        WHERE Role=="sentinel" 
        GROUP BY Agent
        ORDER BY COUNT(Agent) DESC
        LIMIT 5;"""

        sentinel_played = pd.read_sql(sql_query, conn)

        st.header(":red[Most Played Sentinel]")

        display_card_table2(sentinel_played,"sentinel")

with col7:
    with st.container(border=True):
        sql_query = """SELECT Agent, COUNT(Agent) AS MapsPlayed
        FROM test_data
        WHERE Role=="controller" 
        GROUP BY Agent
        ORDER BY COUNT(Agent) DESC
        LIMIT 5;"""

        controller_played = pd.read_sql(sql_query, conn)

        st.header(":white[Most Played Controller]")

        display_card_table2(controller_played,"controller")

with col8:
    with st.container(border=True):
        sql_query = """SELECT Agent, COUNT(Agent) AS MapsPlayed
        FROM test_data
        WHERE Role=="initiator" 
        GROUP BY Agent
        ORDER BY COUNT(Agent) DESC
        LIMIT 5;"""

        initiator_played = pd.read_sql(sql_query, conn)

        st.header(":orange[Most Played Initiator]")

        display_card_table2(initiator_played,"initiator")