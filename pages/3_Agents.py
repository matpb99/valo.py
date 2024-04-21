import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def load_image(filename, folder):
    with open("./{}/{}.png".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

def display_card_table(df_data, agent_name,category):

    category_key_value = translate_dict.get(category)

    if category_key_value == "FirstKills" or category_key_value == "Kills" or category_key_value == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    player, value = df_data["Name"][0], df_data[category_key_value][0]

    text = [str(value) + " {}".format(category_key_value), "Best {} by {}{} in All VCTs ".format(agent_name.capitalize(), prefix, category_key_value), "Played at least 3 maps"]
    title = str(player).capitalize()

    card_list.append(card(
        title = title,
        text = text,
        image = load_image(agent_name, "agents"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
                }
                            )
    )
    st.header("Top 3 Ranking")
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

st.title("Top Agents")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Agent) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Agent=="raze" 
        GROUP BY Name
        HAVING COUNT(Agent)>=3
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        raze_rating = pd.read_sql(sql_query, conn)
        display_card_table(raze_rating,"raze","most_rating")

with col2:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Agent) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Agent=="jett" 
        GROUP BY Name
        HAVING COUNT(Agent)>=3
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        jett_rating = pd.read_sql(sql_query, conn)
        display_card_table(jett_rating,"jett","most_rating")

with col3:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Agent) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Agent=="yoru" 
        GROUP BY Name
        HAVING COUNT(Agent)>=3
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        yoru_rating = pd.read_sql(sql_query, conn)
        display_card_table(yoru_rating,"yoru","most_rating")

with col4:
    with st.container(border=True):
        sql_query = """SELECT Name, COUNT(Agent) AS MapsPlayed, ROUND(AVG(Rating),2) AS Rating, Team
        FROM test_data
        WHERE Agent=="viper" 
        GROUP BY Name
        HAVING COUNT(Agent)>=3
        ORDER BY AVG(Rating) DESC
        LIMIT 3;"""

        viper_rating = pd.read_sql(sql_query, conn)
        display_card_table(viper_rating,"viper","most_rating")