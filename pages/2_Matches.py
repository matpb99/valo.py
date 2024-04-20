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

st.title("Top Matches")