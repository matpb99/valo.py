import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def init_data():
    players_maps_data_df = pd.read_csv("player_data_by_map.csv")
    last_update = str(players_maps_data_df.sort_values(by="DateStandar", ascending=False  ,ignore_index=True)["DateStandar"][0])
    last_update = last_update.split()[0]

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

def draw_agent_card_by_metric(agent_name, metric):

    if metric == "FirstKills" or metric == "Kills" or metric == "Assists":
        prefix = ""
    else:
        prefix = "Average "

    sql_query = """SELECT Name, COUNT(Agent) AS MapsPlayed, ROUND(AVG({}),2) AS {}, Team
                    FROM test_data
                    WHERE Agent=="{}" 
                    GROUP BY Name
                    HAVING COUNT(Agent)>=4
                    ORDER BY AVG({}) DESC
                    LIMIT 3;""".format(metric, metric, agent_name, metric)

    df_data = pd.read_sql(sql_query, conn)

    player, value = df_data["Name"][0], df_data[metric][0]
    text = [str(value) + " {}".format(metric), "Best {} by {}{} in All VCTs ".format(agent_name.capitalize(), prefix, metric), "Played at least 4 maps"]
    title = str(player)

    st.header(agent_name.capitalize())

    card(
        title = title,
        text = text,
        image = load_image(agent_name, "agents"),
        styles={
            "card": {
                "width": "100%",
                "height": "600px"
                    }
                }
        )
    
    st.subheader("Top 3 Ranking")
    st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))
st.title("Top Agents")

with st.sidebar:
    st.title("Categories")
    st.markdown("[Top Agents](#top-agents)")
    st.markdown("[Brimstone](#brimstone)")
    st.markdown("[Viper](#viper)")
    st.markdown("[Omen](#omen)")
    st.markdown("[Killjoy](#killjoy)")
    st.markdown("[Cypher](#cypher)")
    st.markdown("[Sova](#sova)")
    st.markdown("[Sage](#sage)")
    st.markdown("[Phoenix](#phoenix)")
    st.markdown("[Jett](#jett)")
    st.markdown("[Raze](#raze)")
    st.markdown("[Breach](#breach)")
    st.markdown("[Skye](#skye)")
    st.markdown("[Yoru](#yoru)")
    st.markdown("[Kayo](#kayo)")
    st.markdown("[Chamber](#chamber)")
    st.markdown("[Fade](#fade)")
    st.markdown("[Harbor](#harbor)")
    st.markdown("[Gekko](#gekko)")
    st.markdown("[Neon](#neon)")


col1, col2, col3, col4 = st.columns(4)

with col1: 
    with st.container(border=True):
        draw_agent_card_by_metric("brimstone","Rating")

with col2:
    with st.container(border=True):
        draw_agent_card_by_metric("viper","Rating")

with col3:
    with st.container(border=True):
        draw_agent_card_by_metric("omen","Rating")

with col4:
    with st.container(border=True):
        draw_agent_card_by_metric("killjoy","Rating")

col5, col6, col7, col8 = st.columns(4)

with col5: 
    with st.container(border=True):
        draw_agent_card_by_metric("cypher","Rating")

with col6:
    with st.container(border=True):
        draw_agent_card_by_metric("sova","Rating")

with col7:
    with st.container(border=True):
        draw_agent_card_by_metric("sage","Rating")

with col8:
    with st.container(border=True):
        draw_agent_card_by_metric("phoenix","Rating")

col9, col10, col11, col12 = st.columns(4)

with col9: 
    with st.container(border=True):
        draw_agent_card_by_metric("jett","Rating")

with col10:
    with st.container(border=True):
        draw_agent_card_by_metric("raze","Rating")

with col11:
    with st.container(border=True):
        draw_agent_card_by_metric("breach","Rating")

with col12:
    with st.container(border=True):
        draw_agent_card_by_metric("skye","Rating")

col13, col14, col15, col16 = st.columns(4)

with col13:
    with st.container(border=True):
        draw_agent_card_by_metric("yoru","Rating")

with col14:
    with st.container(border=True):
        draw_agent_card_by_metric("kayo","Rating")

with col15:
    with st.container(border=True):
        draw_agent_card_by_metric("chamber","Rating")

with col16:
    with st.container(border=True):
        draw_agent_card_by_metric("fade","Rating")

col17, col18, col19, col20 = st.columns(4)

with col17:
    with st.container(border=True):
        draw_agent_card_by_metric("harbor","Rating")

with col18:
    with st.container(border=True):
        draw_agent_card_by_metric("gekko","Rating")

with col19:
    with st.container(border=True):
        draw_agent_card_by_metric("neon","Rating")

with col20:
    with st.container(border=True):
        try:
            draw_agent_card_by_metric("reyna","Rating")
        except: pass

col21, col22, col23, col24 = st.columns(4)

with col21:
    with st.container(border=True):
        try:
            draw_agent_card_by_metric("astra","Rating")
        except: pass

with col22:
    with st.container(border=True):
        try:
            draw_agent_card_by_metric("deadlock","Rating")
        except: pass

with col23:
    with st.container(border=True):
        try:
            draw_agent_card_by_metric("iso","Rating")
        except: pass

with col24:
    with st.container(border=True):
        try:
            draw_agent_card_by_metric("clove","Rating")
        except: pass

### no se han jugado lo suficiente : reyna, astra, deadlock, iso y clove 