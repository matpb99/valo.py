import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
import base64

def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

translate_dict = {
    "most_rating":"Rating",
    "most_kills":"Kills",
    "most_acs": "ACS",
    "most_assists": "Assists",
    "most_hs": "HS Rate",
    "most_fk": "First Kills",
}

card_list = list()

def display_card_table(category1,category2,category3):

    df_data =  pd.read_csv("./outputs/{}/{}/{}.csv".format(category1,category2,category3))

    category_key_value = translate_dict.get(category3)

    if category2=="players":
        category_key = "Name"
    else:
        category_key = "Team"

    if category1=="maps":
        category, value, map_name, matchteams =  df_data[category_key][0], df_data[category_key_value][0], df_data["Map"][0], df_data["MatchTeams"][0]

    elif category1=="matches":
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
    
def display_card_table2(category1,category2):

    df_data =  pd.read_csv("./outputs/{}/{}.csv".format(category1,category2))
    category_key_value = translate_dict.get(category2)

    if category1=="players":
        category_key = "Name"
    else:
        category_key = "Team"

    category, value = df_data[category_key][0], df_data[category_key_value][0]

    if category1 == "players":
        text = [str(value) + " {}".format(category_key_value), "Most {} in All VCTs".format(category_key_value)]
        title = str(category).capitalize()
    else:
        text = [str(value) + " {}".format(category_key_value), "Most {} by Teams in All VCTs".format(category_key_value)]
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

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

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
        display_card_table2("players","most_rating")

with col2:
    with st.container(border=True):
        display_card_table2("players","most_acs")

with col3:
    with st.container(border=True):
        display_card_table2("players","most_kills")

with col4:
    with st.container(border=True):
        display_card_table2("players","most_assists")

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
